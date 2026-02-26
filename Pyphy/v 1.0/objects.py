
from spatial import *
from color_class import RGBa
from pyphy_errors import *

class StageObject:
    _counter = 0
    _id_counter = 0

    def __init__(self, name=None):
        cls = type(self)
        cls._counter += 1
        
        StageObject._id_counter += 1
        self.id = StageObject._id_counter
        if name is None:
            self.name = f"{cls.__name__} {cls._counter:02d}"
        else: 
            self.name = name

        self.transform = Transform(self)
        self.scene = None
        self.children = []
        self.parent = None
        self.components = []
        self.enabled = True

        self._destroyed = False

    def set_parent(self, parent):
        if not isinstance(parent, StageObject):
            raise StageObjectError(f"Parent given > {parent} < is not a StageObject pygame/objects/class.StageObject")
        
        if self.parent:
            self.parent.children.remove(self)

        self.parent = parent
        parent.children.append(self)

    def get_component(self, component_class):
        for c in self.components:
            if isinstance(c, component_class):
                return c
        return None
        
    def add_component(self, component):
        if isinstance(component, type):
            raise ComponentError("add_component() expects an instance, not a class")
        for c in self.components:
            if isinstance(c, type(component)):
                raise DupeComponentError(f"You are adding a already there component -> '{type(component).__name__}' ")
            
        component.owner = self
        self.components.append(component)
        
        
        return component
    
    def draw(self, screen):
        if not self.enabled:
            return
        
        for c in self.components:
            if hasattr(c, "c_render"):
                c.c_render(screen)

        for child in self.children:
            child.draw(screen)
        
    def start(self):
        if not self.enabled:
            return
        
        for c in self.components:
            c.c_start()
        
        for child in self.children:
            child.start()

    def update(self, dt):
        if not self.enabled:
            return
    
        for c in self.components:
            c.c_update(dt)

        for child in self.children:
            child.update(dt)

    def physics_update(self, dt):
        if not self.enabled:
            return
    
        for c in self.components:
            c.c_physics_update(dt)

        for child in self.children:
            child.physics_update(dt)

    def late_update(self, dt):
        pass

    def destroy(self):
        if self._destroyed == True:
            return 
        
        self.enabled = False
        self._destroyed = True

        for c in self.components:
            c.c_destroy()
    
        if self.scene:
            self.scene._queue_destroy(self)
    
    def get_component_overview(self):
        overview = []

        for i, c in enumerate(self.components, start=1):
            overview.append((i, c.__class__.__name__))

        return overview
    
    def component_debug_view(self, to_print: bool | None =False):
        if to_print == True:
            print(f"\n --------- {self.name} Components ---------")
            for i, name in self.get_component_overview():
                print(f"{i} -> {name}")

        return f"{i} -> {name}"
                
    


