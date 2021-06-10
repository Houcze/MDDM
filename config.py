
from pymongo import MongoClient

client = MongoClient('172.16.52.24', 80)

monthDays = {

    1:31,

    2:29,

    3:31,

    4:30,

    5:31,

    6:30,

    7:31,

    8:31,

    9:30,

    10:31,

    11:30,

    12:31

}


domain = ['SURFACe']

variable = ['TMP_ALL_STATION']

time = {'202004': []}


for ti in time.keys():

    mon = int(ti[4:])

    for day in range(1, monthDays[mon]+1):

        day = str(day).zfill(2)

        for clock in range(0, 24):

            time[ti].append('{}-{}-{}-00-00'.format(ti[4:], day, clock))

