from xml.dom import minidom as md
import re

from .color import RGB

class SVG:
    units = {'mm', 'px'}
    linecaps = {'butt', 'square', 'round'}


    def __init__(self, file_name, viewBox_min_x = 0, viewBox_min_y = 0, viewBox_width = 600, viewBox_height = 400, width=None, height=None, unit:str='mm'):
        if width is None:
            width = viewBox_width
        if height is None:
            height = viewBox_height
        try:
            self.fp = open(file_name, mode='w')
        except FileNotFoundError: # 権限などのエラーは含まれない？
            print('ファイル', file_name, 'を開けませんでした。')
        self.encoding:str = 'utf-8' # 'Shift-JIS'?
        self.unit:str
        self._set_unit(unit)
        self.stroke_width = 3
        self.stroke_color:RGB = RGB(255, 255, 255) # 'white'
        self.fill_color:RGB = RGB(255, 255, 255) # 'white'
        self.font_family = 'monospace'
        self.sequence_counter = 0 # _add_sequencial_drawing_animation 用

        self._start(viewBox_min_x, viewBox_min_y, viewBox_width, viewBox_height, width, height)

    def __del__(self):
        self._finish()
        self.fp.close()


    def _start(self, viewBox_min_x = 0, viewBox_min_y = 0, viewBox_width = 600, viewBox_height = 400, width = 600, height = 400):
        self.fp.write(f"<?xml version=\"{1.0}\" encoding=\"{self.encoding}\"?>\n")
        self.fp.write("<!DOCTYPE svg PUBLIC \"-//W3C//DTD SVG 1.1//EN\"\n"
                      "  \"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd\">\n")
        self.fp.write(f"<svg version=\"1.1\" "
                      f"width=\"{width}{self.unit}\" "
                      f"height=\"{height}{self.unit}\" "
                      f"viewBox=\"{viewBox_min_x} {viewBox_min_y} {viewBox_width} {viewBox_height}\" "
                      f"preserveAspectRatio=\"xMidYMid\" "
                      f"fill-rule=\"evenodd\" "
                      f"xmlns=\"http://www.w3.org/2000/svg\" "
                      f"xmlns:xlink=\"http://www.w3.org/1999/xlink\">\n")

    def _finish(self):
        self.fp.write('</svg>\n')

    def _set_unit(self, unit: str):
        if unit in self.units:
            self.unit = unit
        else:
            raise ValueError('the unit unavailable!')


    def set_width(self, stroke_width):
        self.stroke_width = stroke_width

    def set_fill_color(self, color: RGB):
        self.fill_color = color

    def set_stroke_color(self, color: RGB):
        self.stroke_color = color

    def _make_attributes(self, dictionary: dict): # 引数の辞書からSVGの属性辞書を生成して返す

        del dictionary['self'] # self は 要らない

        # _ を - に置き換える
        keys_with_hyphen = [key for key in dictionary if '_' in key]
        for key_with_hyphen in keys_with_hyphen:
            dictionary[key_with_hyphen.replace('_', '-')] = dictionary[key_with_hyphen]
            del dictionary[key_with_hyphen]

        return dictionary

    # line(), rect(), circle()を一般化したもの。
    def _add(self, element: str, attributes: dict, time: float = 0.1):
        # 描画アニメーションのために不透明度を強制的に0にする。
        if 'stroke-opacity' in attributes:
            attributes['stroke-opacity'] = 0
        if 'fill-opacity' in attributes:
            attributes['fill-opacity'] = 0

        self.fp.write(f'<{element} ')
        for attribute, value in attributes.items():
            self.fp.write(f'{attribute}="{value}" ')
        self.fp.write('>\n')

        self._add_sequencial_drawing_animation([attribute for attribute in attributes if attribute in ['stroke-opacity', 'fill-opacity']], time)

        self.fp.write(f'</{element}>\n')
    
    def _add_sequencial_drawing_animation(self, attributes: list, time: float):
        for attribute in attributes:
            self.fp.write('<animate attributeType="XML"\n'
                        f'attributeName="{attribute}"\n'
                        'to="1"\n'
                        f'begin="{self.sequence_counter}"\n'
                        f'dur="{time}s"\n'
                        'fill="freeze" />\n')
            self.sequence_counter += time

    def line(self, x1: float, y1: float, x2: float, y2: float, stroke: RGB = None, stroke_width = None, stroke_opacity = None, stroke_linecap='batt'):
        if stroke is None:
            stroke = self.stroke_color
        if stroke_width is None:
            stroke_width = self.stroke_width
        if stroke_opacity is None:
            stroke_opacity = 1
        self._add('line', self._make_attributes(locals()))

    def rect(self, x: float = 0, y: float = 0, width = 'auto', height = 'auto', fill = None, stroke = None, stroke_width: float = None, fill_opacity: float = 1.0, stroke_opacity: float = 1.0):
        if fill is None:
            fill = self.fill_color
        if stroke is None:
            stroke = self.stroke_color
        self._add('rect', self._make_attributes(locals()), 0.01)

    def circle(self, cx: float = 0, cy: float = 0, r: float = 0, fill: RGB = None, stroke: RGB = None, stroke_width: float = None, fill_opacity: float = 1.0, stroke_opacity: float = 1.0):
        if fill is None:
            fill = self.fill_color
        if stroke is None:
            stroke = self.stroke_color
        if stroke_width is None:
            stroke_width = self.stroke_width
        self._add('circle', self._make_attributes(locals()))

    def text(self, x: float = 0, y: float = 0, text: str = '', font_family: str = None, font_size: float = None, fill: RGB = None, stroke: RGB = None, stroke_width: float = None, fill_opacity:float = 1.0, stroke_opacity: float = 1.0):
        if font_family is None:
            font_family = self.font_family
        if font_size is None:
            font_size = self.font_size
        if fill is None:
            fill = self.fill_color
        if stroke is None:
            stroke = self.stroke_color
        if stroke_width is None:
            stroke_width = self.stroke_width
        attributes = self._make_attributes(locals())
        del attributes['text']

        self.fp.write(f'<text x="{x}" y="{y}" '
                      f'font-family="{font_family}" font-size="{font_size}" '
                      f'fill="{fill}" stroke="{stroke}" '
                      f'stroke-width="{stroke_width}" fill-opacity="{0}" '
                      f'stroke-opacity="{0}" >\n' + text + '\n')

        self._add_sequencial_drawing_animation([attribute for attribute in attributes if attribute in ['stroke-opacity', 'fill-opacity']], 0.03)
        self.sequence_counter += 0.1

        self.fp.write('</text>\n')

    def image(self, path: str, width, height, x, y):
        self.fp.write(f'<image xlink:href="{path}" width="{width}" height="{height}" x="{x}" y="{y}" />\n')
    
    def import_svg(self, path: str, x = 0, y = 0, width = None, height = None):
        document = md.parse(path)
        element_svg = document.getElementsByTagName('svg')[0]
        original_width = float(re.sub('[^\d.]', '', element_svg.getAttribute("width"))) # 数字とドット(小数点)以外を削除
        original_height = float(re.sub('[^\d.]', '', element_svg.getAttribute("height")))
        if width is None:
            width = original_width
        if height is None:
            height = original_height
        translate = (x, y)
        scale = (width / original_width, height / original_height)
        self.fp.write(f'<g transform="translate({translate[0]} {translate[1]}) scale({scale[0]} {scale[1]})" >\n')
        for child_node in element_svg.childNodes:
            child_node.writexml(self.fp)
        self.fp.write("</g>\n")
