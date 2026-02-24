from vectors import *
import math
import pygame
from visual import Screen
from color_class import RGBa
from spatial import Transform

class Shape:
    def draw(self, screen, transfrom, color):
        raise NotImplementedError
    
    def draw_filled(self, screen, transform, fill_color):
        raise NotImplementedError


class Circle(Shape):
    def __init__(self, centre: Vector2, point: Vector2):
        self.centre = centre
        self.point = point
        self.radius = (point - centre).magnitude

    @property
    def radial_circumference(self):
        return 2 * math.pi * self.radius
    
    @property
    def radial_semi_circumference(self):
        return (2 * self.radius) + (math.pi * self.radius)
    
    @property
    def radial_area(self):
        return math.pi * (self.point - self.centre).sqr_magnitude

    @classmethod
    def from_diametre(cls, a: Vector2, b: Vector2): 
        cent = mid_point(a, b)
        return cls(cent, a)
    
    def sector_area(self, theta_in_rad: float) -> float:
        r2 = (self.point - self.centre).sqr_magnitude
        return 0.5 * r2 * theta_in_rad@staticmethod
    def draw(screen: Screen, circle_data: "Circle", color: RGBa | None = None, width=2):
        if color is None: 
            color = RGBa.BLACK
        pygame.draw.circle(
            screen.surface,
            color.rgb,
            (int(circle_data.centre.x), int(circle_data.centre.y)),
            int(circle_data.radius),
            width
        )

    def draw(self, screen: Screen, color: RGBa | None = None, width=2):
        if color is None: 
            color = RGBa.BLACK
        pygame.draw.circle(
            screen.surface,
            color.rgb,
            (int(self.centre.x), int(self.centre.y)),
            int(self.radius),
            width
        )


  ######################  
    

    def __init__(self, size: Vector2 =Vector2.UNIT):
        self.size = size
    
    def get_points(self):
        hw = 0.5
        hh = 0.5
        local = [
            Vector2(-hw, -hh),
            Vector2(hw, -hh),
            Vector2(hw, hh),
            Vector2(-hw, hh)
        ]

        points = [Vector2(p.x * self.size.x, p.y * self.size.y) for p in local]

        return points
    
    @property
    def centroid(self):
        return Vector2.ZERO
    
    def draw(self, screen, transform, color):
        points = [transform.apply_to_point(p).to_tuple for p in self.get_points()] 
        pygame.draw.polygon(screen.surface, color.rgb, points, width=1)

    def draw_filled(self, screen, transform, fill_color):
        points = [transform.apply_to_point(p).to_tuple for p in self.get_points()] 
        pygame.draw.polygon(screen.surface, fill_color.rgb, points)

    
class Triangle(Shape):
    def __init__(self, size: Vector2 = Vector2.UNIT):
        self.size = size

    def get_points(self):
        h = 1
        w = 1
        local_points = [
            Vector2(0, -h/3),
            Vector2(-w/2, 2*h/3),
            Vector2(w/2, 2*h/3)
        ]

        points = [Vector2(p.x * self.size.x, p.y * self.size.y) for p in local_points]
        return points
    
    @property
    def centroid(self):
        return Vector2.ZERO
    
    def draw(self, screen, transform, color):
        points = [transform.apply_to_point(p).to_tuple for p in self.get_points()] 
        pygame.draw.polygon(screen.surface, color.rgb, points, width=2)

    def draw_filled(self, screen, transform, fill_color):
        points = [transform.apply_to_point(p).to_tuple for p in self.get_points()] 
        pygame.draw.polygon(screen.surface, fill_color.rgb, points)

class Rectangle(Shape):
    def __init__(self, size: Vector2 = Vector2.UNIT):
        self.size = size

    def get_points(self):
        hw = 0.5
        hh = 0.5
        local = [
            Vector2(-hw, -hh),
            Vector2(hw, -hh),
            Vector2(hw, hh),
            Vector2(-hw, hh)
        ]

        points = [Vector2(p.x * self.size.x, p.y * self.size.y) for p in local]

        return points
    
    @property
    def centroid(self):
        return Vector2.ZERO
    
    def draw(self, screen, transform, color):
        points = [transform.apply_to_point(p).to_tuple for p in self.get_points()]
        pygame.draw.polygon(screen.surface, color.rgb, points)

    def draw_filled(self, screen, transform, fill_color):
        points = [transform.apply_to_point(p).to_tuple for p in self.get_points()] 
        pygame.draw.polygon(screen.surface, fill_color.rgb, points)

# CIRCLE FUNC
def spatial_circle(a: Vector2, b: Vector2):
    return Circle.from_diametre(a, b)