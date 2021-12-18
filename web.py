import streamlit as st
import os
import zipfile
import time
import pandas as pd
from config import *


def make_zip(source_dir, output_filename):
    zipf = zipfile.ZipFile(output_filename, 'w')
    pre_len = len(os.path.dirname(source_dir))
    for parent, dirnames, filenames in os.walk(source_dir):
        for filename in filenames:
            pathfile = os.path.join(parent, filename)
            arcname = pathfile[pre_len:].strip(os.path.sep)   #相对路径
            zipf.write(pathfile, arcname)
    zipf.close()

def dict2args(dic_s, dic_u):
    arg = ''
    for s, v in dic_s.items():
        if v == 1:
            arg = arg + s
            arg = arg + ','
    for u, v in dic_u.items():
        if v == 1:
            arg = arg + u
            arg = arg + ','
    return arg[:-1]   


SURFACE = client['SURFACE'].list_collection_names()
UPPER_AIR = client['UPPER_AIR'].list_collection_names()

st.title('MICAPS4数据下载助手')
with open(r'{}\docs\MICAPS4.pdf'.format(os.getcwd()), 'rb') as file:
    st.download_button(label='下载MICAPS4数据说明', data=file, file_name='MICAPS4.pdf')
user = st.text_input('用户名', '')
mode = st.selectbox('模式(mode)', options=['id', 'area', 'inc'])
ids = st.text_input('站点的编号', '')
area = st.text_input('经度和纬度的限制(请按照顺序：纬度下界，经度下界，纬度上界，经度上界, 中间使用逗号分离)', '')
coly, colm = st.columns(2)
with coly:
    year = st.text_input('年', '')
with colm:
    month = st.text_input('月', '')
cold, colh = st.columns(2)
with cold:
    day = st.text_input('日', '')
with colh:
    hour = st.text_input('时辰', '')

###############################################################
variable_s = {s:0 for s in SURFACE}
variable_u = {u:0 for u in UPPER_AIR}
st.write('SURFACE')
col1, col2 = st.columns(2)
for s in SURFACE[:len(SURFACE) // 2]:
    with col1:
    # variable = st.text_area('变量', '')
        variable_s[s] = st.checkbox(s)
for s in SURFACE[len(SURFACE) // 2:]:
    with col2:
    # variable = st.text_area('变量', '')
        variable_s[s] = st.checkbox(s)
st.write('UPPER_AIR')
for u in UPPER_AIR:
    # variable = st.text_area('变量', '')
    variable_u[u] = st.checkbox(u)
#################################################################
configure = st.button('确认你的配置')
st.write('你的配置是:')

if configure:
    st.write('user:{}'.format(user))
    st.write('mode:{}'.format(mode))
    st.write('year:{}'.format(year))
    st.write('month:{}'.format(month))
    st.write('day:{}'.format(day))
    st.write('hour:{}'.format(hour))
    st.write('variable:{}'.format(dict2args(variable_s, variable_u)))


if st.button('确认'):
    variable = dict2args(variable_s, variable_u)
    if user:
        if mode == 'inc':
            os.system('python find_arg.py --mode inc')
        if mode == 'id':
            if ids:
                t = str(time.time())
                if not os.path.exists('{}\data\{}'.format(os.getcwd(), user + t)):
                    os.mkdir('{}\data\{}'.format(os.getcwd(), user + t))
                year = year.replace('，', ',')
                month = month.replace('，', ',')    
                day = day.replace('，', ',')
                hour = hour.replace('，', ',')
                ids = ids.replace('，', ',')
                variable = variable.replace('，', ',')
                with st.spinner('请稍等'):
                    os.system(
                        r'python find_arg.py --mode id --id {} --year {} --month {} --day {} --hour {} --variable {} --output {}\data\{}'. \
                        format(ids, year, month, day, hour, variable, os.getcwd(), user + t)
                    )
                    make_zip('{}\data\{}'.format(os.getcwd(), user + t), '{}\data\{}'.format(os.getcwd(), user + t + '.zip'))
                    st.success('已下载完毕！')
                    with open(r'{}\data\{}'.format(os.getcwd(), user + t + '.zip'), 'rb') as file:
                        st.download_button(label='下载数据(打包为zip格式)', data=file, file_name=user + t + '.zip')
            else:
                st.error('使用该下载模式的时候，站点编号必须被提供')
        if mode == 'area':
            if area:
                t = str(time.time())
                if not os.path.exists('{}\data\{}'.format(os.getcwd(), user + t)):
                    os.mkdir('{}\data\{}'.format(os.getcwd(), user + t))
                year = year.replace('，', ',')
                month = month.replace('，', ',')
                day = day.replace('，', ',')
                hour = hour.replace('，', ',')
                area = area.replace('，', ',')
                variable = variable.replace('，', ',')
                with st.spinner('请稍等'):
                    os.system(
                        r'python find_arg.py --mode area --area {} --year {} --month {} --day {} --hour {} --variable {} --output {}\data\{}'. \
                        format(area, year, month, day, hour, variable, os.getcwd(), user + t)
                    )
                    make_zip('{}\data\{}'.format(os.getcwd(), user + t), '{}\data\{}'.format(os.getcwd(), user + t + '.zip'))
                    st.success('已下载完毕！')
                    with open(r'{}\data\{}'.format(os.getcwd(), user + t + '.zip'), 'rb') as file:
                        st.download_button(label='下载数据(打包为zip格式)', data=file, file_name=user + t + '.zip')

            else:
                st.error('使用该下载模式的时候，区域范围必须被提供')
    else:
        st.warning('用户名必须被提供')