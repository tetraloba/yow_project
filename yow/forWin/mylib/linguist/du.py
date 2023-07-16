from os import path
from glob import glob

from .config import settings

def get_sizes_per_lang(dir_path: str) -> dict:

    # 各言語の容量を計測 (find -name "*.EXT" | xargs du -c | tail -n 1 | cut -f1 に相当)
    sizes = dict() # 言語:容量
    for lang, prop in settings['langs'].items():
        for ext in prop[1]:
            # print(path.join(dir_path, '**', f'*.{ext}')) # debug
            file_list = glob(path.join(dir_path, '**', f'*.{ext}'), recursive=True)
            if file_list.__len__() == 0:
                break
            # print(file_list) # debug
            size = sum(path.getsize(file) for file in file_list)
            sizes[lang] = size + sizes.get(lang, 0)

    # for key, value in sizes.items():
    #     print(key, value) # debug
    return sizes

if __name__ == '__main__':
    get_sizes_per_lang()
