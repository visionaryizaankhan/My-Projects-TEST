import math

class Vector2():

    def __init__(self, x=0.0, y=0.0):
        self.x = float(x)
        self.y = float(y)


    def __repr__(self):
        return f"({self.x}, {self.y})"
    
    def __sub__(self, other):
        if isinstance(other, Vector2):
            ox, oy = other.x, other.y
        elif isinstance(other, (float, int)):
            ox = oy = other
        else:
            return NotImplemented
        
        return Vector2(self.x - ox, self.y - oy)
    
    def __neg__(self):
        return Vector2(-self.x, -self.y)
    
    def __add__(self, other):
        if isinstance(other, Vector2):
            ox, oy = other.x, other.y
        elif isinstance(other, (float, int)):
            ox = oy = other
        else:
            return NotImplemented
        
        return Vector2(self.x + ox, self.y + oy)
    
    def __radd__(self, other):
        return self.__add__(other)
    
    def __mul__(self, other):
        if isinstance(other, Vector2):
            ox, oy = other.x, other.y
        elif isinstance(other, (float, int)):
            ox = oy = other
        else:
            return NotImplemented
        
        return Vector2(self.x * ox, self.y * oy)
    
    def __rmul__(self, other):
        return self.__mul__(other)


    @property
    def magnitude(self)  -> float:
        return math.hypot(self.x, self.y)
    
    @property
    def sqr_magnitude(self)  -> float:
        return (self.x ** 2) + (self.y ** 2)
    
    @property
    def normalized(self) -> float:
        mag = self.magnitude
        if mag == 0:
            return Vector2.ZERO
        return Vector2(self.x / mag, self.y / mag)
    
    @property
    def direction(self):
        def sign(x):
            if x > 0:
                return 1
            elif x < 0:
                return -1
            return 0
        
        return Vector2(sign(self.x), sign(self.y))
    
    @property
    def to_tuple(self):
        return (self.x, self.y)
    
    @property
    def to_int_tuple(self):
        return (int(self.x), int(self.y))
    
    @property
    def prime(self):
        ix, iy = int(self.x), int(self.y)
        gcd = math.gcd(ix, iy)

        if gcd == 0:
            return Vector2(0, 0)
        
        return Vector2(self.x / gcd, self.y / gcd)
    
    @property
    def angle(self):
        _ang = math.atan2(self.y, self.x) * (180/math.pi)
        return _ang
    
    def set_x(self, new_val):
        return Vector2(new_val, self.y)
    
    def set_y(self, new_val):
        return Vector2(self.x, new_val)
    
    def add_to_x(self, val):
        return Vector2(self.x + val, self.y)
    
    def add_to_y(self, val):
        return Vector2(self.x, self.y + val)
    
    @staticmethod
    def dot(v1, v2):
        return (v1.x * v2.x) + (v1.y * v2.y)

# VEC FUNCS
    
def distance_between(v: Vector2, _v: Vector2) -> float:
    return math.hypot((_v.x-v.x), (_v.y-v.y)) 

def mid_point(v: Vector2, _v: Vector2) -> float:
    return Vector2((v.x + _v.x) / 2, (v.y + _v.y) / 2) 

def int_distance(v: Vector2, _v: Vector2) -> int:
    return round(distance_between(v, _v))     

def section(a: Vector2, b: Vector2, m: int, n: int) -> Vector2:
    px: float = ((b.x * m) + (a.x * n) / (m+n))
    py: float = ((b.y * m) + (a.y * n) / (m+n))
    return Vector2(px, py)

def cross_scalar(a: Vector2, b: Vector2) -> float:
    return (a.x * b.y) - (b.x * a.y)

def rotate(source: Vector2, angle: float) -> Vector2: 
    sin_t = math.sin(math.radians(angle))
    cos_t = math.cos(math.radians(angle))
    return Vector2(source.x * cos_t - source.y * sin_t, source.x * sin_t + source.y * cos_t)

def rotate_around(point: Vector2, centre: Vector2, angle_rad: float) -> Vector2:
    translated = point - centre
    rotated = rotate(translated, angle_rad)
    return rotated + centre


    
Vector2.ZERO = Vector2(0, 0)
Vector2.UNIT = Vector2(1, 1)
Vector2.RIGHT = Vector2(1, 0)
Vector2.LEFT = Vector2(-1, 0)
Vector2.UP = Vector2(0, -1)
Vector2.DOWN = Vector2(0, 1)