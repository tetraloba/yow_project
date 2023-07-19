import datetime

from .config import addictions
from ..svg4py.svg import SVG, RGB

def create_abstinence(file_path: str = None):
    if file_path is None:
        file_path = 'abstinence'
    char_size = 10
    svg = SVG(file_path, 0, 0, char_size * 50, char_size * addictions.__len__(), unit='px')
    today_date = datetime.date.today()
    for i, (addiction, ban_date) in enumerate(addictions.items()):
        num_of_days = (today_date - datetime.datetime.strptime(ban_date, "%Y/%m/%d").date()).days
        # print(f'{addiction} has been banned for {num_of_days} days.')
        svg.text(0, char_size * (i + 1), f'{addiction} has been banned for {num_of_days} days.', font_size=char_size, fill=RGB(0, 200, 0), stroke_width=0)
