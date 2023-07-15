from .svg import SVG
from .color import RGB

file_name = 'test.svg'

svg = SVG(file_name, 0, 0, 1920, 1080, unit='px')
svg.set_stroke_color(RGB(255, 0, 255))
svg.set_fill_color(RGB(255, 255, 0))
svg.rect(10, 10, 1910, 1070, RGB(3, 10, 0))
svg.circle(50, 50, 40)
svg.line(0, 500, 1000, 500, RGB(120, 30, 250))
svg.text(500, 500, 'hogehogeTestText', font_size=30)
