from decimal import Decimal, ROUND_HALF_UP
from os import getcwd, chdir

from .du import get_sizes_per_lang
from .config import settings
from ..svg4py.svg import SVG, RGB

def round(f: float, precision: str):
    return float(Decimal(str(f)).quantize(Decimal(precision), rounding=ROUND_HALF_UP))

def create_linguist(repository_path: str, file_path: str = None):
    if file_path is None:
        file_path = 'linguist.svg'
    path_origin = getcwd() # 元のカレントディレクトリ(復元用)
    chdir(repository_path)

    sizes_dict = get_sizes_per_lang(repository_path)
    size_sum = sum(size for size in sizes_dict.values()) # 容量の合計
    # print(sizes_list) # debug
    for lang, size in sizes_dict.items(): # 割合(四捨五入したもの)に変換
        sizes_dict[lang] = size / size_sum

    sizes_list = sorted(sizes_dict.items(), key=lambda x:x[1], reverse=True) # 降順ソートしてリスト化

    # SVGファイルの生成
    width = 1100
    char_size = 20
    bar_height = char_size
    background_color = RGB(0, 0, 0)
    svg = SVG(file_path, 0, -char_size, width, bar_height + char_size * (sizes_list.__len__() + 1), unit='px')
    svg.rect(0, 0, '100%', '100%', background_color, stroke_width=0)
    # グラフを表示
    pen_x = 0
    for lang, size in sizes_list:
        r, g, b = settings['langs'][lang][0] # todo 例外処理すべき
        svg.line(pen_x, char_size / 2, pen_x + size * width, char_size / 2, RGB(r, g, b), stroke_width=char_size)
        pen_x += size * width
    # 言語とその割合を表示
    for i, (lang, size) in enumerate(sizes_list):
        if size != 0:
            r, g, b = settings['langs'][lang][0] # todo 例外処理すべき
            svg.circle(char_size / 2, bar_height + char_size * i + char_size / 1.5, char_size / 3, RGB(r, g, b), stroke_width=0)
            svg.text(char_size, bar_height + char_size * i + char_size, f"{lang} {round(size * 100, '0.1')}%", font_size=char_size, fill=RGB(255, 255, 255), stroke_width=0)
    # リポジトリ名を表示
    svg.text(0, -char_size * 0.5, 'Languages on ' + settings['paths'][0], font_size=18, fill=RGB(150, 150, 150), stroke_width=0)

    chdir(path_origin) # カレントディレクトリを復元
