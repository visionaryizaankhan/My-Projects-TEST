from pyphy import *
import math

source = Screen(Vector2(800, 600), "Pyphy Test") # IMPORTANT


class Game(Scene):

    def start(self):
        self.tobj = StageObject() 
        self.t = self.tobj.add_component(ShapeRenderer(Triangle(Vector2(100, 100)), RGBa.RED, RGBa.RED))
        self.add_objects(self.tobj)
        self.tobj.transform.position = self.screen.centre

    def update(self, dt):
        print("Hello world")
        
        
source.set_scene(Game())
source.run()



