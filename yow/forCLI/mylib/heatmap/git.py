import subprocess
from os import chdir, getcwd

from .config import settings

def get_commits_per_date():

    path = settings['path']

    # カレントディレクトリの操作と表示
    # print('now directory is ' + getcwd()) # debug
    # chdir(path)
    # print('now directory is ' + getcwd()) # debug

    # git log コマンドの実行 と 解析用コマンドの実行
    cp = subprocess.run(["git", "-C", path, "log"], capture_output=True, text=True)
    # print(cp.stdout) # debug
    cp = subprocess.run(["grep", "^Date:"], input=cp.stdout, capture_output=True, text=True) # '"^Date:"' や "\"^Date:\"" だと上手く行かない。なぜか。
    # print(cp.stdout) # debug
    cp = subprocess.run(["awk", "{print $6, $3, $4}"], input=cp.stdout, capture_output=True, text=True) # '"{print $6, $3, $4}"' だとだめ…
    # print(cp.stdout) # debug
    cp = subprocess.run(["uniq", "-c"], input=cp.stdout, capture_output=True, text=True)
    # print(cp.stdout) # debug

    return [s.strip() for s in cp.stdout.split('\n')]
