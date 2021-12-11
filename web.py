import streamlit as st
from PIL import Image
import os

st.title('MICAPS4数据下载助手')
user = st.text_input('用户名', '')
mode = st.selectbox('模式(mode)', options=['id', 'area', 'inc'])
ids = st.text_input('站点的编号', '')
area = st.text_input('经度和纬度的限制', '')
year = st.text_input('年', '')
month = st.text_input('月', '')
day = st.text_input('日', '')
hour = st.text_input('时辰', '')
variable = st.text_area('变量', '')

configure = st.button('确认你的配置')
st.write('你的配置是:')

if configure:
    st.write('user:{}'.format(user))
    st.write('mode:{}'.format(mode))
    st.write('year:{}'.format(year))
    st.write('month:{}'.format(year))
    st.write('day:{}'.format(day))
    st.write('hour:{}'.format(hour))
    st.write('variable:{}'.format(variable))

if st.button('确认'):
    try:
        if not os.path.exists('./data/{}'.format(user)):
            os.mkdir('./data/{}'.format(user))
    except:
        st.warning('用户名必须被提供！')
    if mode == 'inc':
        os.system('python find_arg.py --mode inc')
    if mode == 'id':
        try:
            year = year.replace('，', ',')
            month = month.replace('，', ',')    
            day = day.replace('，', ',')
            hour = hour.replace('，', ',')
            ids = ids.replace('，', ',')
        except:
            pass
        with st.spinner('请稍等'):
            os.system(
                'python find_arg.py --mode id --id {} --year {} --month {} --day {} --hour {} --variable {} --output ./data/{}'.format(ids, year, month, day, hour, variable, user)
            )
            st.success('已下载完毕！')
    if mode == 'area':
        try:
            year = year.replace('，', ',')
            month = month.replace('，', ',')
            day = day.replace('，', ',')
            hour = hour.replace('，', ',')
            area = area.replace('，', ',')
        except:
            pass
        with st.spinner('请稍等'):
            os.system(
                'python find_arg.py --mode area --area {} --year {} --month {} --day {} --hour {} --variable {} --output ./data/{}'.format(area, year, month, day, hour, variable, user)
            )
            st.success('已下载完毕！')