import subprocess
from os import chdir, getcwd
from datetime import datetime

from .config import settings

def get_commits_per_date(path):
    # path = "~/projects/competitiveProgramming"

    # git log コマンドの実行 と 解析用コマンドの実行
    # cp = subprocess.run(["wsl", "--", "git", "-C", path, "log"], capture_output=True, text=True, shell=True, encoding='utf-8')
    cp = subprocess.run(["wsl", "--", "git", "-C", path, "log"], shell=True, capture_output=True)
    # print('stdout is ', cp.stdout) # debug
    # print(cp) # debug
    line_date = [line.decode() for line in cp.stdout.split(b'\n') if b'Date: ' in line] # 'Date: 'の含まれる行を抽出(grep的な)
    # 年/月/日 の列を抽出して各日の出現数をカウント(awk + uniq的な)
    dates = dict()
    for line in line_date:
        l = line.split()
        date = datetime.strptime(f'{l[5]}/{l[2]}/{l[3]}', '%Y/%b/%d').date()
        dates[date] = dates.get(date, 0) + 1
    # for date, cnt in dates.items():
    #     print(date, cnt)

    # return [s.strip() for s in cp.stdout.split('\n')]
    return dates
