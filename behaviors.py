from awesomeengine.behavior import Behavior
from awesomeengine import engine
from awesomeengine.entity import Entity
from awesomeengine.rectangle import from_entity, Rect

class PlayerInput(Behavior):

    def __init__(self):
        self.required_attrs = [('dir', 'none')]
        self.event_handlers = {'input': self.handle_input}

    def handle_input(self, entity, action, value):
        if action == 'left':
            if value == 1:
                entity.dir = 'left'
            else:
                entity.dir = 'none'
        elif action == 'right':
            if value == 1:
                entity.dir = 'right'
            else:
                entity.dir = 'none'


class PlayerMovement(Behavior):

    def __init__(self):
        self.required_attrs = ['x', 'y',
                               'width', 'height',
                               ('vel_x', 0),
                               ('vel_y', 0),
                               ('grounded', True),
                               ('dir', 'none'),
                               'max_ground_speed',
                               'ground_acceleration']
        self.event_handlers = {'update' : self.handle_update}

    def handle_update(self, entity, dt):
        e = engine.get()
        if entity.grounded:
            if entity.dir == 'none':
                entity.vel_x = toward_zero(entity.vel_x, entity.ground_acceleration, dt)
            elif entity.dir == 'right':
                entity.vel_x = min(entity.max_ground_speed, entity.vel_x + entity.ground_acceleration * dt)
            elif entity.dir == 'left':
                entity.vel_x = max(-entity.max_ground_speed, entity.vel_x - entity.ground_acceleration * dt)
            entity.vel_y = 0

            #will we run into something
            r = from_entity(entity)
            r.x += entity.vel_x * dt

            blocking = e.entity_manager.get_in_area('platform', r)
            if blocking:
                # we hit something
                # lets move into it
                o = blocking.pop()
                if entity.vel_x > 0:
                    side = from_entity(o).left
                    entity.x = side - entity.width/2
                else:
                    side = from_entity(o).right
                    entity.x = side + entity.width/2


                entity.vel_x = 0
            else:
                entity.x += entity.vel_x * dt

            #are we still grounded
            test = Rect(entity.x, entity.y - entity.height/2 - 0.1, entity.width,0)
            ground = e.entity_manager.get_in_area('platform', test)
            if not ground:
                #we are floating
                entity.grounded = False
        else:
            #temp freefall
            entity.vel_y -= 9.8 * dt

            #test for ground
            test = Rect(entity.x, entity.y - entity.height / 2 - 0.1, entity.width, 0)
            ground = e.entity_manager.get_in_area('platform', test)
            if ground:
                entity.grounded = True
                entity.vel_y = 0
                floor = ground.pop()
                r = from_entity(floor)
                entity.y = r.top + entity.height/2 + 0.01

            entity.x += entity.vel_x * dt
            entity.y += entity.vel_y * dt




def toward_zero(v, a, dt):
    if v > 0:
        return max(0, v - a * dt)
    else:
        return  min(0, v + a * dt)