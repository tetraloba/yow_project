from os import path
import subprocess
from collections import defaultdict
from glob import glob

from .config import settings

def get_sizes_per_lang(dir_path: str) -> dict:

    ext2lang = {ext:lang for lang, prop in settings['langs'].items() for ext in prop[1]}

    # 各言語の容量を計測 (find -name "*.EXT" | xargs du -c | tail -n 1 | cut -f1 に相当)
    res = subprocess.run(['wsl', '--', 'git', '-C', dir_path, 'ls-files', '-z'], capture_output=True).stdout
    lang2size = defaultdict(int)
    for file_path_b in res.split(b'\0')[:-1]:
        file_path = file_path_b.decode('utf-8')
        ext = path.splitext(file_path)[1]
        if len(ext):
            ext = ext[1:] # 拡張子の'.'を取り除く
        if ext not in ext2lang:
            continue # 対象外の拡張子をスキップ
        lang2size[ext2lang[ext]] += path.getsize(path.join(dir_path, file_path))
    return lang2size

if __name__ == '__main__':
    get_sizes_per_lang()
