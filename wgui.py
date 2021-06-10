from tkinter import Checkbutton, ttk
import tkinter
from typing import DefaultDict
from init import *
import init
from click.decorators import command
import os
import asyncio
import w
import tkinter.messagebox
import tkinter.filedialog
import webbrowser


root = tkinter.Tk()
root.title('CAS DESKTOP')
root.geometry('400x800')
root.iconbitmap(".\\nuist.ico")

MonStr = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec')
"""
两种格式的命令
python select id --id xx"
python select area --llat xx --llon xx --ulat xx --ulon xx
"""
n = ttk.Notebook(root)

f_area = ttk.Frame(n, width=390, height=750)
f_id = ttk.Frame(n, width=390, height=400)
f_setting = ttk.Frame(n, width=390, height=200)
f_about = ttk.Frame(n, width=390, height=200)

n.add(f_area, text='Select by Area')
n.add(f_id, text='Select by station id')
n.add(f_setting, text='Settings')
n.add(f_about, text='About')


var1 = tkinter.IntVar()
var_1 = tkinter.IntVar()
var_2 = tkinter.IntVar()
var_3 = tkinter.IntVar()
vari1 = tkinter.IntVar()

m = []
for mon_ in range(12):
    m.append(tkinter.IntVar())
m_id = []
for mon_ in range(12):
    m_id.append(tkinter.IntVar())

def update_variables():
    if var1.get() == 1:
        var.append('TMP_ALL_STATION')
        domain.append('SURFACe')
    else:
        var.remove('TMP_ALL_STATION')
        domain.append('SURFACe')

def update_month():
    """这个函数是月份的响应函数
    """
    for i in range(12):
        if m[i].get() == 1:
            if str(i + 1) not in monthseq:
                monthseq.append(str(i + 1).zfill(2))
        #else:
        #    if str(i + 1) in monthseq:
        #        monthseq = [m_ for m_ in monthseq if m_ != str(i + 1).zfill(2)]
    update_month_year()    
    

def update_time():
    """V1版本的年月集合模式，V2版本我仿照ECMWF，将他们区分开来
    if var_1.get() == 1:
        time['202004'] = []
    else:
        if '202004' in time.keys():
            time.pop('202004')
    if var_2.get() == 1:
        time['202006'] = []
    else:
        if '202006' in time.keys():
            time.pop('202006')
    if var_3.get() == 1:
        time['202007'] = []
    else:
        if '202007' in time.keys():
            time.pop('202007')
    """ 
    if var_1.get() == 1:
        init.yearseq.append('2020')
    else:
        if '2020' in init.yearseq:
            init.yearseq = [y_ for y_ in init.yearseq if y_ != '2020']
    update_month_year()


def update_month_year():
    if len(monthseq) != 0 and len(yearseq) != 0:
        for y_ in yearseq:
            for m_ in monthseq:
                if (y_ + m_) not in time.keys():
                    time[y_ + m_] = []
    else:
        """不满足更新年份月份的条件，啥都不干
        """
        pass
            

######################### Select by area ####################################
def cas_area():
    async def gui2cli():
        os.system('pack\python.exe find.py area --llat {} --llon {} --ulat {} --ulon {} --filetype txt'.format(llat.get(), llon.get(), ulat.get(), ulon.get()))
    asyncio.run(gui2cli())
    for file in os.listdir(w.path):
        with open(w.path + file) as f:
            f.seek(0, os.SEEK_END)
            size = f.tell()
            if size == 0:
                tkinter.messagebox.showinfo(title='Attention', message='Some of the data you requested is not in our database, you\'ll get an empty file')
                break
    tkinter.messagebox.showinfo(title='Attention', message='Done')
               

p = ttk.PanedWindow(f_area, width=340)
"""Select Variables"""
f1 = ttk.Labelframe(f_area, text='Product')
demo = ttk.Checkbutton(f1, text='TMP_ALL_STATION', variable=var1, command=update_variables)
demo.pack(side='left')


"""Select domain"""
f3 = ttk.Labelframe(f_area, text='Product Type')
surface = ttk.Checkbutton(f3, text='SURFACe', width=25, variable=vari1)
#upper_air = ttk.Checkbutton(f3, text='UPPER AIR', width=25)
surface.pack(side='left')
#upper_air.pack(side='right')

"""Select Year & Month"""
"""这个地方需要维护一个巨大的日历系统..."""
"""为了增加稳定性, 我这个地方写死它"""
f2 = ttk.Labelframe(f_area, text='Year')

year_month_1 = ttk.Checkbutton(f2, text='2020', width=25, variable=var_1, command=update_time)
#year_month_2 = ttk.Checkbutton(f2, text='202006', width=25, variable=var_2, command=update_time)
#year_month_3 = ttk.Checkbutton(f2, text='202007', width=25, variable=var_3, command=update_time)

year_month_1.grid(row=0, column=1)
#year_month_2.grid(row=0, column=2)
#year_month_3.grid(row=1, column=1)

"""Select Time"""
"""设计逻辑上实在是有很多问题..."""
"""如果允许用户指定时间，那么用户将不得不在GUI界面上点击几十乃至几百次
   从GUI设计思想看，这种想法几乎是无法避免的
   即使是GUI只负责生成代码给用户，也将会面临这个问题。
   这个问题我还没有想到一个比较合理的解决方案，但是为了应付项目交差我决定先撂担子。
   毕竟这个难题在cli命令行程序中完全不是事。
   我认为这种需要超多参数指定的任务真的很难在GUI中为之设计一个合理的逻辑...
   V2 版本：我仿照了ERA5的映射模式
"""

f9 = ttk.Labelframe(f_area, text='Month')
month = []
for mon_ in range(12):
    month.append(ttk.Checkbutton(f9, text=MonStr[mon_], width=25, variable=m[mon_], command=update_month))


mon_ = 0
for ro in range(6):
    for col in range(1, 2 + 1):
        month[mon_].grid(row=ro, column=col)
        mon_ += 1
del mon_


"""Set Geo Limit"""
f4 = ttk.LabelFrame(f_area, text='Geographical area')
ulat = ttk.Entry(f4, show=None, width=4, text='upper lat')
llon = ttk.Entry(f4, show=None, width=4, text='lower lon')
ulon = ttk.Entry(f4, show=None, width=4, text='upper lon')
llat = ttk.Entry(f4, show=None, width=4, text='lower lat')

"""
ulat.pack(padx=10, pady=10)
llon.pack(side='left')
ulon.pack(side='right')
llat.pack(padx=10, pady=10)
"""
ttk.Label(f4, text='upper lat').grid(row=0, column=1)
ulat.grid(row=0, column=2, sticky='N',padx=30, pady=10)
ttk.Label(f4, text='lower lon').grid(row=1, column=0)
llon.grid(row=1, column=1, sticky='W', padx=16, pady=10)
ttk.Label(f4, text='upper lon').grid(row=1, column=4)
ulon.grid(row=1, column=3, sticky='E', padx=20, pady=20)
llat.grid(row=2, column=2, sticky='S')
ttk.Label(f4, text='lower lat').grid(row=2, column=1)


def submitForm():
    with open('config.py', 'w') as file:
        file.write(templatea + templateb.format(domain, var, time) + templatec)


f6 = ttk.LabelFrame(f_area)
sc = ttk.Button(f6, text='Configure', command=submitForm)
"""If configured. The Input will be written to config.py"""
sc.grid(row=0, column=1)
configure = ttk.Button(f6, text='Download Data', command=cas_area)
configure.grid(row=0, column=2)



p.add(f3)
p.add(f1)
p.add(f2)
p.add(f9)
p.add(f4)
p.add(f6)
p.pack()
#############################################################################
#############################################################################
#############################################################################
def update_variables_id():
    if var1_id.get() == 1:
        var.append('TMP_ALL_STATION')
        domain.append('SURFACe')
    else:
        var.remove('TMP_ALL_STATION')
        domain.append('SURFACe')

"""
def update_time_id():
    if var_1_id.get() == 1:
        time['202004'] = []
    else:
        if '202004' in time.keys():
            time.pop('202004')
    if var_2_id.get() == 1:
        time['202006'] = []
    else:
        if '202006' in time.keys():
            time.pop('202006')
    if var_3_id.get() == 1:
        time['202007'] = []
    else:
        if '202007' in time.keys():
            time.pop('202007')
"""

def update_month_id():
    """这个函数是月份的响应函数
    """
    for i in range(12):
        if m_id[i].get() == 1:
            if str(i + 1) not in monthseq:
                monthseq.append(str(i + 1).zfill(2))
        #else:
        #    if str(i + 1) in monthseq:
        #        monthseq = [m_ for m_ in monthseq if m_ != str(i + 1).zfill(2)]
    update_month_year()    
    

def update_time_id():
    """V1版本的年月集合模式，V2版本我仿照ECMWF，将他们区分开来
    if var_1.get() == 1:
        time['202004'] = []
    else:
        if '202004' in time.keys():
            time.pop('202004')
    if var_2.get() == 1:
        time['202006'] = []
    else:
        if '202006' in time.keys():
            time.pop('202006')
    if var_3.get() == 1:
        time['202007'] = []
    else:
        if '202007' in time.keys():
            time.pop('202007')
    """ 
    if var_1_id.get() == 1:
        init.yearseq.append('2020')
    else:
        if '2020' in init.yearseq:
            init.yearseq = [y_ for y_ in init.yearseq if y_ != '2020']
    update_month_year()


def update_month_year_id():
    if len(monthseq) != 0 and len(yearseq) != 0:
        for y_ in yearseq:
            for m_ in monthseq:
                if (y_ + m_) not in time.keys():
                    time[y_ + m_] = []
    else:
        """不满足更新年份月份的条件，啥都不干
        """
        pass

var1_id = tkinter.IntVar()
var_1_id = tkinter.IntVar()
var_2_id = tkinter.IntVar()
var_3_id = tkinter.IntVar()
vari1_id = tkinter.IntVar()
pid = ttk.PanedWindow(f_id, width=340)

"""Select Variables"""
f1_id = ttk.Labelframe(f_id, text='Product')
demo_id = ttk.Checkbutton(f1_id, text='TMP_ALL_STATION', variable=var1_id, command=update_variables_id)
demo_id.pack(side='left')


"""Select domain"""
f3_id = ttk.Labelframe(f_id, text='Product Type')
surface_id = ttk.Checkbutton(f3_id, text='SURFACe', width=25, variable=vari1_id)
#upper_air = ttk.Checkbutton(f3, text='UPPER AIR', width=25)
surface_id.pack(side='left')
#upper_air.pack(side='right')

"""Select Year & Month"""
"""这个地方需要维护一个巨大的日历系统..."""
"""同上，为了增加稳定性, 这个地方写死它"""
f2_id = ttk.Labelframe(f_id, text='Year')

year_month_1_id = ttk.Checkbutton(f2_id, text='2020', width=25, variable=var_1_id, command=update_time_id)
#year_month_2_id = ttk.Checkbutton(f2_id, text='202006', width=25, variable=var_2_id, command=update_time_id)
#year_month_3_id = ttk.Checkbutton(f2_id, text='202007', width=25, variable=var_3_id, command=update_time_id)

year_month_1_id.grid(row=0, column=1)
#year_month_2_id.grid(row=0, column=2)
#year_month_3_id.grid(row=1, column=1)


f9_id = ttk.Labelframe(f_id, text='Month')
month_id = []
for mon_ in range(12):
    month_id.append(ttk.Checkbutton(f9_id, text=MonStr[mon_], width=25, variable=m_id[mon_], command=update_month_id))


mon_ = 0
for ro in range(6):
    for col in range(1, 2 + 1):
        month_id[mon_].grid(row=ro, column=col)
        mon_ += 1
del mon_


f4_id = ttk.Labelframe(f_id, text='station id')
id = ttk.Entry(f4_id, show=None, width=16, text='id')
id.pack()

def submitid():
    with open('config.py', 'w') as file:
        file.write(templatea + templateb.format(domain, var, time) + templatec)

def cas_id():
    os.system('pack\python.exe find.py station --id {} --filetype txt'.format(id.get()))
    tkinter.messagebox.showinfo(title='Attention', message='Done!')

f6_id = ttk.LabelFrame(f_id)
sc_id = ttk.Button(f6_id, text='Configure', command=submitid)
"""If configured. The Input will be written to config.py"""
sc_id.grid(row=0, column=1)
configure_id = ttk.Button(f6_id, text='Download Data', command=cas_id)
configure_id.grid(row=0, column=2)


def cas_all_id():
    async def gui2cli():
        os.system('pack\python.exe find.py area --llat -90 --llon -180 --ulat 90 --ulon 180 --filetype txt')
    asyncio.run(gui2cli())
    for file in os.listdir(w.path):
        with open(w.path + file) as f:
            f.seek(0, os.SEEK_END)
            size = f.tell()
            if size == 0:
                tkinter.messagebox.showinfo(title='Attention', message='Some of the data you requested is not in our database, you\'ll get an empty file')
                break

download_all_id = ttk.Button(f6_id, text='Download All Data', command=cas_all_id)
download_all_id.grid(row=0, column=3)


pid.add(f3_id)
pid.add(f1_id)
pid.add(f2_id)
pid.add(f9_id)
pid.add(f4_id)
pid.add(f6_id)
pid.pack()

########################################################################################
"""Settings of all tabs
"""
def get_path():
    with open('w.py', 'r') as w:
        path = w.read()
    path = path[(path.index('\'') + 1):(-1)]
    return path

StrPath = tkinter.StringVar(value='{}'.format(get_path()))

psettings = ttk.PanedWindow(f_setting, width=340)
def set_data_download_path():
    pass

def pathCallBack():
    filePath = tkinter.filedialog.askdirectory(title='Set data path')
    if filePath != '':
        StrPath.set(filePath)
        with open('w.py', 'w') as w:
            w.write('path = \'{}\''.format(StrPath.get() + '/'))

ttk.Label(psettings, text="Data Path:").grid(row=0, column=0)
txtResult = tkinter.Entry(psettings, width=40, textvariable=StrPath)
txtResult.grid(row=1, column=0)

btnPath = ttk.Button(psettings, text='Change', width=10, command=pathCallBack)
btnPath.grid(row=1, column=1)

psettings.pack()
#######################################################################################
pabout = ttk.PanedWindow(f_about, width=340)

def open_readme():
    url = '{}\docs\MICAPS4.pdf'.format(os.getcwd())
    webbrowser.open(url, new=2)

btnr = ttk.Button(pabout, text='Open data format introduction', width=30, command=open_readme)
btnr.grid(row=1, column=1)
pabout.pack()

n.pack()
root.mainloop()