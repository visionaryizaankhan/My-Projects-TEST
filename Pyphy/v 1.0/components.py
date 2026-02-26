from vectors import *
from enum import Enum 
from color_class import RGBa
import pygame
from inputsys import Input
from geom import *
from objects import StageObject
from pyphy_errors import *

class ForceType(Enum):
    FORCE = 1
    IMPULSE = 2

class Component:
    def __init__(self):
        self.owner = None 
        self.enabled = True

    def c_start(self):
        pass

    def c_update(self, dt):
        pass

    def c_physics_update(self, dt):
        pass

    def c_render(self, screen):
        pass

    def draw_on_screen(self, screen):
        pass

    def c_destroy(self):
        self.enabled = False

class RigidBody(Component):
    def __init__(self):
        super().__init__()
        self.velocity = Vector2.ZERO
        self.mass = 1
        self._force_accum = Vector2.ZERO
        self.drag = 0

    def c_physics_update(self, dt):

        if not self.owner.enabled or not self.enabled: 
            return
    
        drag_force = -self.velocity * self.drag
        self._force_accum += drag_force
        acc = Vector2(self._force_accum.x / self.mass, self._force_accum.y / self.mass)
        self.velocity += acc * dt
        self.owner.transform.position += self.velocity * dt

        self._force_accum = Vector2.ZERO

    def apply_force(self, direction, magnitude, force_type):
        if not self.owner.enabled or not self.enabled: 
            return

        f = direction.normalized * magnitude
        if force_type == ForceType.FORCE:
            self._force_accum += f
        elif force_type == ForceType.IMPULSE:
            self.velocity += Vector2(f.x / self.mass, f.y / self.mass)
 
class PlayerController(Component):
    def __init__(self,
                 move_accel: float = 2000,
                 max_speed: float = 300,
                 jump_impulse: float = 600,
                 air_control: float = 0.4
                 ):
        super().__init__()
        self.move_accel = move_accel
        self.max_speed = max_speed
        self.jump_impulse = jump_impulse
        self.air_control = air_control

        self.rb = None
        self.is_grounded = False

    def c_start(self):
        self.rb = self.owner.get_component(RigidBody)
        if self.rb is None:
            raise MissionComponentError(f"PlayerController requires a > Rigidbody < component, but the StageObject > {self.owner.name} < does not have any")
    

    def c_update(self, dt):
        if not self.owner.enabled or not self.enabled:
            return

        move_input = 0

        if Input.get_key(pygame.K_a) or Input.get_key(pygame.K_LEFT):
            
            move_input -= 1

        if Input.get_key(pygame.K_d) or Input.get_key(pygame.K_RIGHT):
            move_input += 1
        
        if move_input != 0:
            control = 1 if self.is_grounded else self.air_control

            direction = Vector2.RIGHT if move_input > 0 else Vector2.LEFT
            self.rb.apply_force(direction, self.move_accel * control, ForceType.FORCE)

        if abs(self.rb.velocity.x) > self.max_speed:
            self.rb.velocity.x = (
                        self.max_speed if self.rb.velocity.x > 0 else -self.max_speed
                    )
        
        if self.owner.transform.position.y >= 300:
            self.is_grounded = True


        if Input.get_key_down(pygame.K_SPACE) and self.is_grounded:
            self.rb.velocity.y = 0
            self.rb.apply_force(Vector2.UP, self.jump_impulse, ForceType.IMPULSE)
        
        else:
            self.is_grounded = False   

#region Renderers
class ShapeRenderer(Component):
    def __init__(self, shape, color: RGBa | None=None, fill_color: RGBa | None=None):
        super().__init__()
        self.shape = shape
        self.color = color
        self.fill_color = fill_color

    def c_render(self, screen):
        if not self.owner.enabled or not self.enabled:
            return
        
        color = self.color or RGBa.BLACK

        if self.fill_color:
            self.shape.draw_filled(screen, self.owner.transform, self.fill_color)
            self.shape.draw(screen, self.owner.transform, color)
        
class TextRenderer(Component):
    def __init__(self, text: None | str="Lorem Ipsum", font_style="font_styles/arial/arial.ttf", font_size=24, color: RGBa= RGBa.BLACK):
        super().__init__()
        self.text = text
        self._fsz = font_size
        self.font_style = font_style
        self.color = color
        # self.font = pygame.font.Font(self.font_style, self._fsz)

        self._surface = None
        self._dirty = True

    def set_font_size(self, new_size):
        if self._fsz != new_size:
            self._fsz = new_size
            self._dirty = True

    def set_text(self, new_text):
        if self.text != new_text:
            self.text = new_text
            self._dirty = True 

    def c_render(self, screen):
        if not self.enabled or not self.owner.enabled:
            return
        
        position = self.owner.transform.position.to_int_tuple

        if self._dirty:
            self.font = pygame.font.Font(self.font_style, self._fsz)
            self._surface = self.font.render(self.text, True, self.color.rgb)
            self._dirty = False

        screen.surface.blit(self._surface, position)

class ImageRenderer(Component):


    
    def __init__(self, image_path: str, width: int =None, heigth: int = None):
        super().__init__()
        self.image_path = image_path

        self.original_image = pygame.image.load(self.image_path).convert_alpha()

        if width and heigth:
            self.image = pygame.transform.scale(self.original_image, (width, heigth))
        else:
            self.image = self.original_image

    def set_img_size(self, wid, hei):
        self.image = pygame.transform.scale(self.original_image, (wid, hei))

    def c_render(self, screen):
        if not self.enabled or not self.owner.enabled:
            return

        pos = self.owner.transform.position.to_tuple

        angle = getattr(self.owner.transform, 'rotation', 0)
        if angle != 0:
            rotated_img = pygame.transform.rotate(self.image, angle)
            rect = rotated_img.get_rect(center=pos)
            screen.surface.blit(rotated_img, rect.topleft)

        else:
            rect = self.image.get_rect(center=pos)
            screen.surface.blit(self.image, rect.topleft)  
#endregion

class CollisonInfo:
    def __init__(self, normal, depth):
        self.normal = normal
        self.depth = depth

    def __repr__(self):
        return f"COLLISON DATA: [NORMAL] -> {self.normal}, [DEPTH] -> {self.depth}"

class PolygonCollider(Component):
    def __init__(self, shape):
        super().__init__()
        self.shape = shape
        self.verticles = self.shape.get_points()

    @property
    def get_world_points(self):
        return [
            self.owner.transform.apply_to_point(p) for p in self.shape.get_points()
        ]
    
    
    def _get_axes_from(self, vertices):
        axes = []

        for i in range(len(vertices)):
            p1 = vertices[i]
            p2 = vertices[(i+1) % len(vertices)]

            edge = p2 - p1
            
            normal = Vector2(-edge.y, edge.x).normalized

            axes.append(normal)

        return axes
    
    @staticmethod
    def _project(verts, axis):        
        min_pro =  float("inf")
        max_pro =  float("-inf")

        for v in verts:
            proj = Vector2.dot(v, axis)
            min_pro = min(min_pro, proj)
            max_pro = max(max_pro, proj)

        return min_pro, max_pro
    
    def _sat(self, other, return_info=False):
        vert_a = self.get_world_points
        vert_b = other.get_world_points

        axes = self._get_axes_from(vert_a) + self._get_axes_from(vert_b)

        min_overlap = float("inf")
        sm_axis = None

        for axis in axes:
            min_a, max_a = self._project(vert_a, axis)
            min_b, max_b = self._project(vert_b, axis)

            if max_a < min_b or max_b < min_a:
                return False if not return_info else None
            
            overlap = min(max_a, max_b) - max(min_a, min_b)

            if overlap < min_overlap:
                min_overlap = overlap
                sm_axis = axis

        if not return_info:
            return True
        
        direc = other.owner.transform.position - self.owner.transform.position

        if Vector2.dot(direc, sm_axis) < 0:
            sm_axis = -sm_axis

        return CollisonInfo(sm_axis, min_overlap)
    

    def intersects(self, other):
        if isinstance(other, StageObject):
            for c in other.components:
                collider = other.get_component(PolygonCollider)
                return self._sat(collider, return_info=False)
            
        if isinstance(other, PolygonCollider):
            return self._sat(other, return_info=False)

        raise NotExpectedArgumentType(f"The argument in intersects() must be a StageObject or a Collider, not {type(other).__name__} ")
    
    def intersection(self, other):
        if isinstance(other, StageObject):
            for c in other.components:
                collider = other.get_component(PolygonCollider)
                return self._sat(collider, return_info=True)
            
        if isinstance(other, PolygonCollider):
            return self._sat(other, return_info=True)

        raise NotExpectedArgumentType(f"The argument in intersects() must be a StageObject or a Collider, not {type(other).__name__} ")

            









