from datetime import datetime as dt

from yow.forCLI.mylib.calendar.calendar import Calendar
from yow.forCLI.mylib.heatmap.heatmap import create_heatpmap
from yow.forCLI.mylib.heatmap.git import get_commits_per_date
from yow.forCLI.mylib.heatmap.config import settings
from yow.forCLI.mylib.linguist.linguist import print_linguist

strings = get_commits_per_date()
create_heatpmap(strings)
print()

print_linguist()

calendar = Calendar(row=10, column=80)
calendar.draw_calendar(dt.now()) # 現在日時を渡す
