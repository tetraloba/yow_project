import datetime as dt

WEEK_NUM = 53

def get_commit_num(date: dt.date):
    return None

def get_color(num: int): # commit数に対応する色(RGB)を返す
    if num != 0:
        return (0, 70 + min(20 * (num // 3), 155), 0)
    else:
        return (25, 25, 25)

def create_heatpmap(strings: list):
    today = dt.datetime.today().date()
    # print(today) # debug

    # strings から {date:commit数}のdictを作成
    daily_commits = dict() # {date:commit数}
    for s in strings:
        if s == '': # 空文字列の場合
            continue
        commit_num, year, month, day = s.split()
        date_string = year + ' ' + month + ' ' + day
        # print(commit_num, ': ', year, '/', month, '/', day) # debug
        daily_commits[dt.datetime.strptime(date_string, '%Y %b %d').date()] = int(commit_num)

    # debug daily_commits: dict の内容を表示
    # for daily_commit in daily_commits.items():
    #     print(daily_commit)


    # print(this_saturday) # debug

    # ヒートマップを出力
    wdays = ['   ', 'Mon', '   ', 'Wed', '   ', 'Fri', '   ']
    first_x_list = [0] * 12 # 各月1日のx座標
    this_saturday = today + dt.timedelta(6 - today.isoweekday() % 7) # 今日以降直近の土曜日(今週の土曜日)
    first_sunday = this_saturday - dt.timedelta(6 + 7 * (WEEK_NUM - 1))
    # print(first_sunday) # debug
    date = first_sunday
    print('         Aug     Sep     Oct       Nov     Dec       Jan     Feb     Mar     Apr       May     Jub     Jul   ')
    for i in range(7):
        print(f'\033[48;2;{10};{14};{18}m', end='') # 背景色を設定
        print(f'\033[37m{wdays[i]}\033[30m', end='')
        for j in range(WEEK_NUM):
            r, g, b = get_color(daily_commits.get(date, 0))
            print(f'\033[38;2;{r};{g};{b}m■ \033[30m', end='')
            date += dt.timedelta(7)
        print('\033[0m', end='') # 背景色の設定を解除
        print()
        date += dt.timedelta(-7 * WEEK_NUM + 1) # 7足しすぎているから(WEEK_NUM - 1)ではなくWEEK_NUM
    # print('\033[38;2;0;0;0mtest000\033[38;2;255;255;255mtest111\033[30m') # debug test


    # for i in range(WEEK_NUM):
    #     for j in range(7):
    #         svg.rect(1041 - 20 * i, 121 - 20 * j, 20, 20, get_color(daily_commits.get(date, 0)), RGB(10, 14, 18))
    #         if date.day == 1: # 1日の場合、そのx座標をfirst_x_listに記録する。
    #             first_x_list[date.month - 1] = 1041 - 20 * i
    #         # print(daily_commits.get(date, 0), end=' ') # debug
    #         date += dt.timedelta(-1)
    #     # print() # debug


    # # 月の出力
    # for i, x in enumerate(first_x_list):
    #     svg.text(x, -2, dt.date(2000, i + 1, 1).strftime('%b'), font_size=size_text, fill_color=rgb_text, stroke_width=0)
