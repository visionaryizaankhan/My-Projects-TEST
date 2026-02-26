import pygame
from vectors import *

class Input:
    _current_keys = ()
    _previous_keys = ()

    _axes = {}

    _delta_time = 0.0

    mouse_position = Vector2.ZERO

    @classmethod
    def update(cls):
        pygame.event.pump()
        cls._previous_keys = cls._current_keys
        cls._current_keys = pygame.key.get_pressed()

        mx, my = pygame.mouse.get_pos()
        cls.mouse_position = Vector2(mx, my)

        for axis in cls._axes.values():
            target = 0 

            if cls._current_keys[axis["negetive"]]:
                target -= 1
            if cls._current_keys[axis["positive"]]:
                target += 1

            
            axis["value"] = target
            
            axis["smooth"] += (target - axis["smooth"]) * axis["speed"] * cls._delta_time
            
            if abs(axis["smooth"] - target < 0.001):
                axis["smooth"] = target
            
            axis["smooth"] = max(-1.0, min(1.0, axis["smooth"]))



    @classmethod
    def get_key(cls, key):
        if not cls._current_keys:
            return False
        return cls._current_keys[key]
    
    @classmethod
    def get_key_down(cls, key):
        if not cls._current_keys or not cls._previous_keys:
            return False
        return cls._current_keys[key] and not cls._previous_keys[key]
    
    @classmethod
    def get_key_up(cls, key):
        if not cls._current_keys or not cls._previous_keys:
            return False
        return not cls._current_keys[key] and cls._previous_keys[key]
    
    @classmethod
    def add_axes(cls, *args):
        if all(isinstance(arg, (list, tuple)) and len(arg) == 3 for arg in args):
            for name, neg, pos in args:
                cls._register_axis(name, neg, pos)
            return

        if len(args) == 3:
            names, negetives, positives = args
            if not isinstance(names, (list, tuple)):
                cls._register_axis(names, negetives, positives)
                return
            for name, neg, pos in zip(names, negetives, positives):
                cls._register_axis(name, neg, pos)

            return
        
        raise ValueError("Invalid add_axes format. It should be list, tuple or separate, values")

    
    @classmethod
    def _register_axis(cls, name, neg, pos):
        if name in cls._axes:
            raise ValueError(f"Axis '{name}' already exists")
        
        cls._axes[name] = {
            "negetive": neg,
            "positive": pos,
            "value": 0,
            "smooth": 0.0,
            "speed": 8.0
        }
    
    @classmethod
    def get_axis(cls, name):
        return cls._axes[name]["smooth"]
    
    @classmethod
    def get_axis_exact(cls, name):
        return cls._axes[name]["value"]
    



    

