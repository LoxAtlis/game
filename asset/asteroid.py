from if3_game.engine import Sprite, Layer
from pyglet.window.key import symbol_string
from math import cos, sin, radians
from random import randint

RESOLUTION = (800, 600)

class GameLayer(Layer):
    def __init__(self):

        super().__init__()
        self.reset()
        
    def reset(self):
        self.remove_all_items()

        asteroid = Asteroid((100, 200))
        self.add(asteroid)

        spaceship = Spaceship((400,300))
        self.add(spaceship)

    def on_key_press(self, key, modifiers):
        if symbol_string(key) == "ENTER":
            self.reset()

        super().on_key_press(key, modifiers)

class SpaceObject(Sprite):
    def __init__(self, image, position=(0,0), anchor=(0,0), rotation_speed=0):
        super().__init__(image, position, anchor=anchor, collision_shape="cirlce")
        self.rotation_speed = rotation_speed
        self.speed = (0, 0)
        
    def update(self, dt):
        self.rotation += self.rotation_speed * dt

        new_x = self.position[0] + self.speed[0] * dt
        new_y = self.position[1] + self.speed[1] * dt
        
        
        if new_y > RESOLUTION[1]:
            new_y = 0
        elif new_y < 0:
            new_y = RESOLUTION[1]

        if new_x > RESOLUTION[0]:
            new_x = 0
        elif new_x < 0:
            new_x = RESOLUTION[0]
            
        self.position = (new_x, new_y)
        super().update(dt)

class Asteroid(SpaceObject):

    def __init__(self, position=(0,0), size=3):
        if size == 3:
            super().__init__("asteroid128.png", position,(64, 64),90)
        elif size == 2 :
            super().__init__("asteroid64.png", position,(32, 32),120)
        elif size == 1:
            super().__init__("asteroid32.png", position,(16, 16),160)
        self.size = size
        self.speed = (-50,-70)

    def on_collision(self, other):
        if isinstance(other, Spaceship):
            other.destroy()

    def destroy(self):
        if self.size > 1:
            for i in range(2):
                baby_asteroid = Asteroid(self.position,self.size-1)
                baby_asteroid.speed = (randint(-150,150), randint(-150,150))
                self.layer.add(baby_asteroid)

        super().destroy() 

class Bullet(SpaceObject):
    def __init__(self, position=(0, 0)):
        super().__init__("bullet.png", position,(8, 8))
        self.lifetime = 2
    def update(self, dt):
        super().update(dt)

        self.lifetime -= dt
        if self.lifetime <= 0:
            self.destroy()
    def on_collision(self, other):
        if isinstance(other, Asteroid):
            self.destroy()
            other.destroy()

class Spaceship(SpaceObject):
    def __init__(self, position=(0,0)):
        super().__init__("spaceship.png", position, anchor=(32, 32))
        self.power_on = False
        self.turn_speed = 180
        self.velocity = 0

    def on_key_press(self, key, modifiers):
        if symbol_string(key) == "RIGHT":
            self.rotation_speed += 100
        elif symbol_string(key) == "LEFT":
            self.rotation_speed -= 100
        elif symbol_string(key) == "UP":
            self.power_on = True
        elif symbol_string(key) == "SPACE":
            self.shoot()
            
    def on_key_release(self, key,modifiers):
        if symbol_string(key) == "RIGHT":
            self.rotation_speed -= 100
        elif symbol_string(key) == "LEFT":
            self.rotation_speed += 100
        elif symbol_string(key) == "UP":
            self.power_on = False

    def update(self, dt):

        if self.power_on:
            angle = -radians(self.rotation)
            self.velocity += 200 * dt
            if self.velocity > 100:
                self.velocity = 100

            #self.velocity = min(self.velocity, 1000)
            new_speed_x = self.speed[0] + cos(angle) * self.velocity * dt
            new_speed_y = self.speed[1] + sin(angle) * self.velocity * dt

            self.speed = (new_speed_x, new_speed_y)
        else:
            new_speed_x = self.speed[0] * 0.99
            new_speed_y = self.speed[1] * 0.99
            self.speed = (new_speed_x, new_speed_y)
            self.velocity = 0
        
        super().update(dt)

    def shoot(self):
        

        bullet = Bullet(self.position)

        angle = -radians(self.rotation)
        bullet.speed = (cos(angle) * 500, sin(angle) * 500)

        self.layer.add(bullet)

    
  