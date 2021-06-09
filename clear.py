import w
import os

for file in os.listdir(w.path):
    os.remove(w.path + file)