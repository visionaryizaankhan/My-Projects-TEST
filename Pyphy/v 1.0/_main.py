from pyphy import *
import math

source = Screen(Vector2(800, 600), "Pyphy Test") # IMPORTANT

source.scene.start()

while source.running:
            source.clear()
            source.handle_events() 

            source.scene.update(source.delta_time)
            source.scene.physics_update(source.delta_time)
            source.scene.render(source)   

            # CODE

            source.update()




