class RGBa:    
    def __init__(self, r: int, g: int, b: int, a: int = 255):
        self.r = self._clamp_color_(r)
        self.g = self._clamp_color_(g)
        self.b = self._clamp_color_(b)
        self.a = self._clamp_color_(a)

    def _clamp_color_(self, value: int) -> int:
        return max(0, min(255, int(value)))
    
    def scale(self, factor: float):
        self.r = self._clamp_color_(self.r * factor)
        self.g = self._clamp_color_(self.g * factor)
        self.b = self._clamp_color_(self.a * factor)

    @property
    def rgb(self) -> tuple[int, int, int]:
        return (self.r, self.g, self.b)

    @property
    def rgba(self) -> tuple[int, int, int, int]:
        return (self.r, self.g, self.b, self.a)

    def __repr__(self):
        return f"RGBa COLOR : ({self.r}, {self.g}, {self.b}, {self.a})"
    
RGBa.BLACK = RGBa(0, 0, 0)
RGBa.WHITE = RGBa(255, 255, 255)
RGBa.RED = RGBa(255, 0, 0)
RGBa.GREEN = RGBa(0, 255, 0)
RGBa.BLUE = RGBa(0, 0, 255)
RGBa.SKY_BLUE = RGBa(135, 206, 235)
