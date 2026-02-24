import pygame
from vectors import *
from color_class import *
from spatial import *
from inputsys import *
from objects import *
from components import *

# SCREEN 
class Screen:
    def __init__(self, size: Vector2, title: str="Engine Test Model 1.0"):
        pygame.init()
        self.size = size
        self.surface = pygame.display.set_mode((size.x, size.y))
        self.screen_title = pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.delta_time = 0
        self.running = True
        self.background_color = RGBa.WHITE
        self.scene = Scene()

    def set_background_color(self, new_color: RGBa):
        self.background_color = new_color

    def clear(self):
        self.surface.fill(self.background_color.rgb)

    def update(self):
        self.delta_time = self.clock.tick(60) / 1000
        Input._delta_time = self.delta_time
        pygame.display.flip()   
        self.scene._process_destroy_queue()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        Input.update()
        
    @property
    def centre(self):
        return Vector2(self.size.x/2, self.size.y/2)
    

class Scene:
    def __init__(self):
        self.scene_objects = []
        self._destroy_queue = []

    def add_objects(self, *objects):
        if isinstance(objects, (list, tuple, set)):
            for inner in objects:
                self._add_single(inner)

        else:
            self._add_single(objects) 

    def _add_single(self, obj):
        obj.scene = self
        self.scene_objects.append(obj)

    def start(self):
        for obj in self.scene_objects:
            obj.start()

    def update(self, dt):
        for obj in self.scene_objects:
            obj.update(dt)

    def physics_update(self, dt):
        for obj in self.scene_objects:
            obj.physics_update(dt)

    def render(self, screen):
        for obj in self.scene_objects:
            obj.draw(screen)

    def _queue_destroy(self, obj):
        self._destroy_queue.append(obj)

    def _process_destroy_queue(self):
        for obj in self._destroy_queue:
            if obj in self.scene_objects:
                self.scene_objects.remove(obj)

            for c in obj.components:
                c.owner = None

            obj.scene = None
            
        self._destroy_queue.clear()
    
    def find_object_by_id(self, obj_id):
        for obj in self.scene_objects:
            if obj.id == obj_id:
                return obj
        return None
    
    def find_objects_by_name(self, name):
        return [obj for obj in self.scene_objects if obj.name == name]
    
    def find_objects_by_type(self, obj_type):
        return [obj for obj in self.scene_objects if isinstance(obj, obj_type)]
    
    def get_overview(self):
        overview = []

        for i, obj in enumerate(self.scene_objects, start=1):
            text_r = obj.get_component(TextRenderer)

            if text_r:
                name = f'"{text_r.text}"' 

            else:
                name = obj.name

            overview.append((i, name))

        return overview
    
    def debug_view(self):
        print("\n --------- SCENE OBJECTS ---------")

        for i, name in self.get_overview():
            print(f"{i} -> {name}")
        
    
    



