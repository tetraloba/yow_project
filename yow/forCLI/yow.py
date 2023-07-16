from datetime import datetime as dt
from os import name, system

from yow.forCLI.mylib.calendar.calendar import Calendar
from yow.forCLI.mylib.heatmap.heatmap import create_heatpmap
from yow.forCLI.mylib.heatmap.git import get_commits_per_date
from yow.forCLI.mylib.heatmap.config import settings
from yow.forCLI.mylib.linguist.linguist import print_linguist
from yow.forCLI.mylib.abstinence.abstinence import create_abstinence

def clear():
    if name == 'nt': # for windows
        _ = system('cls')
    else: # for mac and linux(here, os.name is 'posix')
        _ = system('clear')

clear()

strings = get_commits_per_date()
print('Contributions on /home/tetraloba/KagawaU') # todo ハリボテ修正
create_heatpmap(strings)
print()

print('Languages on /home/tetraloba/projects/competitiveProgramming') # todo ハリボテ修正
print_linguist()

print('\n\n\n\n\n')
create_abstinence()

calendar = Calendar(row=14, column=60)
calendar.draw_calendar(dt.now()) # 現在日時を渡す
