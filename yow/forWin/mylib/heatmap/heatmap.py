import datetime as dt

from ..svg4py.svg import SVG, RGB
from .config import settings # パス出力用

FILE_NAME = 'heatmap.svg'
WEEK_NUM = 53

def get_commit_num(date: dt.date):
    return None

def get_color(num: int): # commit数に対応する色(RGB)を返す
    if num != 0:
        return RGB(0, 70 + min(20 * (num // 3), 155), 0)
    else:
        return RGB(25, 25, 25)

def create_heatpmap(daily_commits: dict, file_path: str = None):
    if file_path is None:
        file_path = FILE_NAME
    today = dt.datetime.today().date()
    # print(today) # debug

    # svgの生成と背景や文字の太さの設定
    svg = SVG(file_path, -40, -40, 1100, 180, unit='px')
    svg.rect(-40, -40, 1100, 180, RGB(10, 14, 18), stroke_width=0)
    svg.set_width(1)

    # debug daili_commits: dict の内容を表示
    # for daily_commit in daily_commits.items():
    #     print(daily_commit)

    # print(this_saturday) # debug

    # ヒートマップを出力
    first_x_list = [0] * 12 # 各月1日のx座標
    this_saturday = today + dt.timedelta(6 - today.isoweekday() % 7) # 今日以降直近の土曜日(今週の土曜日)
    date = this_saturday
    for i in range(WEEK_NUM):
        for j in range(7):
            svg.rect(1041 - 20 * i, 121 - 20 * j, 20, 20, get_color(daily_commits.get(date, 0)), RGB(10, 14, 18))
            if date.day == 1: # 1日の場合、そのx座標をfirst_x_listに記録する。
                first_x_list[date.month - 1] = 1041 - 20 * i
            # print(daily_commits.get(date, 0), end=' ') # debug
            date += dt.timedelta(-1)
        # print() # debug

    # 曜日の出力
    rgb_text = RGB(180, 180, 180)
    size_text = 18
    svg.text(-35, 40, 'Mon', font_size=size_text, fill=rgb_text, stroke_width=0)
    svg.text(-35, 80, 'Wed', font_size=size_text, fill=rgb_text, stroke_width=0)
    svg.text(-35, 120, 'Fri', font_size=size_text, fill=rgb_text, stroke_width=0)

    # 月の出力
    for i, x in enumerate(first_x_list):
        svg.text(x, -2, dt.date(2000, i + 1, 1).strftime('%b'), font_size=size_text, fill=rgb_text, stroke_width=0)

    # リポジトリ名の出力
    svg.text(-40, -20, 'Contributions on ' + settings['paths'][0], font_size=size_text, fill=rgb_text, stroke_width=0)
