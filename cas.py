import os

def id():
    os.system('pack\python.exe find.py station --id {}'.format(id.get()))


def area():
    os.system('pack\python.exe find.py area --llat {} --llon {} --ulat {} --ulon {} --dype txt'.format(llat.get(), llon.get(), ulat.get(), ulon.get()))