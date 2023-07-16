import datetime

from .config import addictions

def create_abstinence():
    today_date = datetime.date.today()
    for addiction, ban_date in addictions.items():
        num_of_days = (today_date - datetime.datetime.strptime(ban_date, "%Y/%m/%d").date()).days
        print(f'\033[32m{addiction} has been banned for {num_of_days} days.\033[0m')
