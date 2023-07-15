from ..svg4py.svg import SVG, RGB
from .config import svg_files

def create_integrated(file_name: str = None):
    if file_name is None:
        file_name = 'integrated.svg'
    svg = SVG(file_name, 0, 0, 1920, 1080, unit='px') # SVGファイルの生成
    svg.rect(0, 0, '100%', '100%', RGB(0, 0, 0), stroke_width=0) # 背景色を設定

    for file_path, option in svg_files.items(): # config.pyに従ってSVGをインポート
        svg.import_svg(file_path, option['x'], option['y'], option['width'], option['height'])
