from vectors import *

class Transform:
    def __init__(
        self,
        owner,
        position: Vector2 | None=None,
        rotation: float=0.0,
        scale: Vector2 | None=None,
    ):
        self.owner = owner
        self.position = position or Vector2.ZERO
        self.rotation = rotation 
        self.scale  = scale or Vector2.UNIT


    def locally_rotate(self, angle: float):
        self.rotation += angle

    def absolute_rotation(self, angle: float):
        self.rotation = angle % 360


    def set_scale(self, new_scale):
        self.scale = new_scale

    def scale_by(self, scale):
        self.scale += scale


    @property
    def world_position(self):
        if self.owner.parent:
            rotated = rotate(self.position, self.owner.parent.transform.world_rotation)
            return self.owner.parent.transform.world_position + rotated
        return self.position

    @property
    def world_rotation(self):
        if self.owner.parent:
            return self.owner.parent.transform.world_rotation + self.rotation
        return self.rotation
    
    @property
    def forward(self):
        rad = math.radians(self.rotation - 90)
        return Vector2(math.cos(rad), math.sin(rad))
    
    @property
    def right(self):
        return Vector2(-self.forward.y, self.forward.x)
    
    def apply_to_point(self, point: Vector2):
        scaled = Vector2(self.scale.x * point.x, self.scale.y * point.y)
        rotated = rotate(scaled, self.world_rotation)
        world = rotated + self.world_position

        return world 
    
        
