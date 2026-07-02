import subprocess
from datetime import datetime

def get_commits_per_date(path):
    # path = "~/projects/competitiveProgramming" # debug

    # git log コマンドの実行
    res = subprocess.run(["wsl", "--", "git", "-C", path, "log", "--pretty=format:'%ai'"], shell=True, capture_output=True, text=True).stdout

    # 年/月/日 の列を抽出して各日の出現数をカウント(awk + uniq的な)
    dates = dict()
    for line in res.split('\n'):
        date = datetime.strptime(line.split()[0], '%Y-%m-%d').date()
        dates[date] = dates.get(date, 0) + 1
    # for date, cnt in dates.items():
    #     print(date, cnt) # debug

    # シェルスクリプトでカウントしてしまう手もある
    # cmd_str = f"git -C '{path}' log --pretty=format:'%ai' | cut -d ' ' -f 1 | uniq -c | sed 's/^[[:space:]]*//'"
    # res = subprocess.run(["wsl", "--", "bash", "-c", cmd_str], shell=True, capture_output=True, text=True).stdout
    # dates = {datetime.strptime(line.split()[1], '%Y-%m-%d').date():int(line.split()[0]) for line in res.split('\n')[:-1]}
    # ワンライナー（笑）
    # return {datetime.strptime(line.split()[1], '%Y-%m-%d').date():int(line.split()[0]) for line in subprocess.run(["wsl", "--", "bash", "-c", f"git -C '{path}' log --pretty=format:'%ai' | cut -d ' ' -f 1 | uniq -c | sed 's/^[[:space:]]*//'"], shell=True, capture_output=True, text=True).stdout.split('\n')[:-1]}

    return dates
