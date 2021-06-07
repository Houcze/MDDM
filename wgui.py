from tkinter import Checkbutton, ttk
import tkinter
from init import *
from click.decorators import command
import os

root = tkinter.Tk()
root.title('CAS DESKTOP')
root.geometry('400x800')
root.iconbitmap(".\\nuist.ico")
"""
两种格式的命令
python select id --id xx"
python select area --llat xx --llon xx --ulat xx --ulon xx
"""
n = ttk.Notebook(root)

f_area = ttk.Frame(n, width=390, height=750)
f_id = ttk.Frame(n, width=390, height=400)
n.add(f_area, text='Select by Area')
n.add(f_id, text='Select by station id')


var1 = tkinter.IntVar()
var_1 = tkinter.IntVar()
var_2 = tkinter.IntVar()
var_3 = tkinter.IntVar()
vari1 = tkinter.IntVar()
def update_variables():
    if var1.get() == 1:
        var.append('TMP_ALL_STATION')
        domain.append('SURFACe')
    else:
        var.remove('TMP_ALL_STATION')
        domain.append('SURFACe')

def update_time():
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

######################### Select by area ####################################
def cas_area():
    os.system('pack\python.exe find.py area --llat {} --llon {} --ulat {} --ulon {} --dype txt'.format(llat.get(), llon.get(), ulat.get(), ulon.get()))

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
f2 = ttk.Labelframe(f_area, text='Year & Month')

year_month_1 = ttk.Checkbutton(f2, text='202004', width=25, variable=var_1, command=update_time)
year_month_2 = ttk.Checkbutton(f2, text='202006', width=25, variable=var_2, command=update_time)
year_month_3 = ttk.Checkbutton(f2, text='202007', width=25, variable=var_3, command=update_time)

year_month_1.grid(row=0, column=1)
year_month_2.grid(row=0, column=2)
year_month_3.grid(row=1, column=1)

"""Select Time"""
"""设计逻辑上实在是有很多问题..."""
"""如果允许用户指定时间，那么用户将不得不在GUI界面上点击几十乃至几百次
   从GUI设计思想看，这种想法几乎是无法避免的
   即使是GUI只负责生成代码给用户，也将会面临这个问题。
   这个问题我还没有想到一个比较合理的解决方案，但是为了应付项目交差我决定先撂担子。
   毕竟这个难题在cli命令行程序中完全不是事。
   我认为这种需要超多参数指定的任务真的很难在GUI中为之设计一个合理的逻辑...
"""

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
surface_id = ttk.Checkbutton(f3_id, text='SURFACe', width=25, variable=vari1)
#upper_air = ttk.Checkbutton(f3, text='UPPER AIR', width=25)
surface_id.pack(side='left')
#upper_air.pack(side='right')

"""Select Year & Month"""
"""这个地方需要维护一个巨大的日历系统..."""
"""同上，为了增加稳定性, 这个地方写死它"""
f2_id = ttk.Labelframe(f_id, text='Year & Month')

year_month_1_id = ttk.Checkbutton(f2_id, text='202004', width=25, variable=var_1_id, command=update_time_id)
year_month_2_id = ttk.Checkbutton(f2_id, text='202006', width=25, variable=var_2_id, command=update_time_id)
year_month_3_id = ttk.Checkbutton(f2_id, text='202007', width=25, variable=var_3_id, command=update_time_id)

year_month_1_id.grid(row=0, column=1)
year_month_2_id.grid(row=0, column=2)
year_month_3_id.grid(row=1, column=1)

f4_id = ttk.Labelframe(f_id, text='station id')
id = ttk.Entry(f4_id, show=None, width=16, text='id')
id.pack()

def submitid():
    with open('config.py', 'w') as file:
        file.write(templatea + templateb.format(domain, var, time) + templatec)

def cas_id():
    os.system('pack\python.exe find.py station --id {}'.format(id.get()))

f6_id = ttk.LabelFrame(f_id)
sc_id = ttk.Button(f6_id, text='Configure', command=submitid)
"""If configured. The Input will be written to config.py"""
sc_id.grid(row=0, column=1)
configure_id = ttk.Button(f6_id, text='Download Data', command=cas_id)
configure_id.grid(row=0, column=2)

pid.add(f3_id)
pid.add(f1_id)
pid.add(f2_id)
pid.add(f4_id)
pid.add(f6_id)
pid.pack()


n.pack()
root.mainloop()