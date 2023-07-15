from abc import ABCMeta, abstractmethod
from colorsys import rgb_to_hls, hls_to_rgb

class Color(metaclass = ABCMeta):

    @abstractmethod
    def to_rgb(self) -> 'RGB':
        raise NotImplementedError()

    @abstractmethod
    def to_hsl(self) -> 'HLS':
        raise NotImplementedError()

class RGB(Color):

    def __init__(self, r:int, g:int, b:int):
        self.r:int = r
        self.g:int = g
        self.b:int = b

    def __str__(self):
        return "#{rr:02x}{gg:02x}{bb:02x}".format(rr=self.r, gg=self.g, bb=self.b)

    def to_rgb(self) -> 'RGB':
        return self

    def to_hsl(self) -> 'HLS':
        h, l, s = rgb_to_hls(self.r / 255, self.g / 255, self.b / 255)
        return HLS(h * 255, l * 255, s * 255)

class HLS(Color):

    def __init__(self, h:int, l:int, s:int):
        self.h:int = h
        self.l:int = l
        self.s:int = s

    def __str__(self):
        return "#{hh:02x}{ll:02x}{ss:02x}".format(hh=self.h, ll=self.l, ss=self.s)

    def to_rgb(self) -> 'RGB':
        r, g, b = hls_to_rgb(self.h / 255, self.l / 255, self.s / 255)
        return RGB(r * 255, g * 255, b * 255)

    def to_hsl(self) -> 'HLS':
        return self
