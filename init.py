var = []
domain = []
time = {}
monthseq = []
yearseq = []

templatea = """
from pymongo import MongoClient\n
client = MongoClient('127.0.0.1', 27017)\n
monthDays = {\n
    1:31,\n
    2:29,\n
    3:31,\n
    4:30,\n
    5:31,\n
    6:30,\n
    7:31,\n
    8:31,\n
    9:30,\n
    10:31,\n
    11:30,\n
    12:31\n
}\n
"""
templateb = """
domain = {}\n
variable = {}\n
time = {}\n
"""

templatec = """
for ti in time.keys():\n
    mon = int(ti[4:])\n
    for day in range(1, monthDays[mon]+1):\n
        day = str(day).zfill(2)\n
        for clock in range(0, 24):\n
            time[ti].append('{}-{}-{}-00-00'.format(ti[4:], day, clock))\n
"""