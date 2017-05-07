from awesomeengine.behavior import Behavior
from awesomeengine import engine
from awesomeengine.entity import Entity
from awesomeengine.rectangle import from_entity, Rect
from math import sin, cos, radians, atan, sqrt, degrees, pi
from awesomeengine.vec2d import Vec2d

class PlayerInput(Behavior):

    def __init__(self):
        self.required_attrs = [('dir', 'none'),
                               ('grounded', False),
                               ('jump_count', 0),
                               'jump_time',
                               'air_jumps',
                               ('air_jumps_remaining', 0),
                               ('air_jump', False)]
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
        elif action == 'up':
            if value == 1:
                if entity.grounded:
                    entity.jump = True
                    entity.jump_count = entity.jump_time

                elif entity.air_jumps_remaining > 0:
                    entity.air_jumps_remaining -= 1
                    entity.jump = True
                    entity.air_jump = True
                    entity.jump_count = entity.jump_time
            elif value == 0:
                entity.jump = False


class PlayerMovement(Behavior):

    def __init__(self):
        self.required_attrs = ['x', 'y',
                               'width', 'height',
                               ('vel_x', 0),
                               ('vel_y', 0),
                               ('grounded', True),
                               ('dir', 'none'),
                               ('jump', False),
                               'max_ground_speed',
                               'ground_acceleration',
                               'max_ground_speed',
                               'ground_acceleration',
                               'gravity',
                               ('jump_count', 0),
                               'jump_time',
                               'jump_force']
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
                    entity.x = side - entity.width/2 - 0.1
                else:
                    side = from_entity(o).right
                    entity.x = side + entity.width/2 + 0.1


                entity.vel_x = 0
            else:
                entity.x += entity.vel_x * dt

            if entity.jump:
                entity.grounded = False
                entity.vel_y = entity.jump_vel
                entity.y += entity.vel_y * dt


            #are we still grounded
            test = Rect(entity.x, entity.y - entity.height/2 - 0.1, entity.width,0)
            ground = e.entity_manager.get_in_area('platform', test)
            if not ground:
                #we are floating
                entity.grounded = False
        else:
            entity.vel_y -= entity.gravity * dt
            if entity.air_jump:
                entity.vel_y = entity.jump_vel
                entity.air_jump = False
            if entity.jump:
                entity.vel_y += entity.jump_force * dt * entity.jump_count
                entity.jump_count -= dt
                if entity.jump_count <= 0:
                    entity.jump = False

            #if falling test for ground
            if entity.vel_y < 0:
                test = Rect(entity.x, entity.y - entity.height / 2 - 0.1, entity.width, 0)
                ground = e.entity_manager.get_in_area('platform', test)
                if ground:
                    entity.grounded = True
                    entity.air_jumps_remaining = entity.air_jumps
                    entity.vel_y = 0
                    floor = ground.pop()
                    r = from_entity(floor)
                    entity.y = r.top + entity.height/2 + 0.01
            else:
                #test for ceiling
                test = Rect(entity.x, entity.y + entity.height / 2 + 0.1, entity.width, 0)
                ceiling = e.entity_manager.get_in_area('platform', test)
                if ceiling:
                    entity.vel_y = 0
                    c = ceiling.pop()
                    r = from_entity(c)
                    entity.y = r.bottom - entity.height/2 - 0.01

            if entity.dir == 'none':
                entity.vel_x = toward_zero(entity.vel_x, entity.air_acceleration, dt)
            elif entity.dir == 'right':
                entity.vel_x = min(entity.max_air_speed, entity.vel_x + entity.air_acceleration * dt)
            elif entity.dir == 'left':
                entity.vel_x = max(-entity.max_air_speed, entity.vel_x - entity.air_acceleration * dt)

            # will we run into something
            r = from_entity(entity)
            r.x += entity.vel_x * dt

            blocking = e.entity_manager.get_in_area('platform', r)
            if blocking:
                # we hit something
                # lets move into it
                o = blocking.pop()
                if entity.vel_x > 0:
                    side = from_entity(o).left
                    entity.x = side - entity.width / 2 - 0.1
                else:
                    side = from_entity(o).right
                    entity.x = side + entity.width / 2 + 0.1

                entity.vel_x = 0

            entity.x += entity.vel_x * dt
            entity.y += entity.vel_y * dt


class PlayerCameraFollower(Behavior):

    def __init__(self):
        self.required_attrs = ['x', 'y',
                               'dead_zone_width',
                               'dead_zone_height',
                               'follow_enabled']
        self.event_handlers = {'update': self.handle_update}

    def handle_update(self, entity, dt):
        if entity.follow_enabled:
            p = engine.get().entity_manager.get_by_name('player')
            if p.x > entity.x + entity.dead_zone_width/2:
                entity.x = p.x - entity.dead_zone_width/2
            elif p.x < entity.x - entity.dead_zone_width/2:
                entity.x = p.x + entity.dead_zone_width/2
            if p.y > entity.y + entity.dead_zone_height/2:
                entity.y = p.y - entity.dead_zone_height/2
            elif p.y < entity.y - entity.dead_zone_height/2:
                entity.y = p.y + entity.dead_zone_height/2

class PlayerDeathZone(Behavior):
    def __init__(self):
        self.required_attrs = ['x', 'y',
                               'width', 'height']
        self.event_handlers = {'update': self.handle_update}

    def handle_update(self, entity, dt):
        if engine.get().entity_manager.get_in_area('death_zone',from_entity(entity)):
            print 'ow'

class GoombaWalk(Behavior):

    def __init__(self):
        self.required_attrs = ['x', 'y',
                               ('vel_x', 0),
                               ('vel_y', 0),
                               'width', 'height',
                               ('grounded', False),
                               'ground_speed',
                               ('dir', 'left'),
                               'gravity']
        self.event_handlers = {'update': self.handle_update}

    def handle_update(self, entity, dt):

        e = engine.get()
        if entity.grounded:
            if entity.dir == 'right':
                entity.vel_x = entity.ground_speed
            elif entity.dir == 'left':
                entity.vel_x = -entity.ground_speed

            # will we run into something
            r = from_entity(entity)
            r.x += entity.vel_x * dt

            blocking = e.entity_manager.get_in_area('platform', r)
            if blocking:
                # we hit something
                # lets move into it
                o = blocking.pop()
                if entity.vel_x > 0:
                    side = from_entity(o).left
                    entity.x = side - entity.width / 2 - 0.1
                    entity.dir = 'left'
                else:
                    side = from_entity(o).right
                    entity.x = side + entity.width / 2 + 0.1
                    entity.dir = 'right'
                entity.vel_x = 0
            else:
                #check if we will run off the edge
                if entity.dir == 'left':
                    px, py = r.bottom_left
                else:
                    px,py = r.bottom_right
                py -= 0.1
                if not e.entity_manager.get_in_area('platform',Rect(px,py,0,0)):
                    if entity.dir == 'left':
                        entity.dir = 'right'
                    else:
                        entity.dir = 'left'

            entity.x += entity.vel_x * dt
        else:
            entity.vel_y -= entity.gravity * dt
            if entity.vel_y < 0:
                test = Rect(entity.x, entity.y - entity.height / 2 - 0.1, entity.width, 0)
                ground = e.entity_manager.get_in_area('platform', test)
                if ground:
                    entity.grounded = True
                    entity.vel_y = 0
                    floor = ground.pop()
                    r = from_entity(floor)
                    entity.y = r.top + entity.height/2 + 0.01
            entity.y += entity.vel_y * dt


class Projectile(Behavior):

    def __init__(self):
        self.required_attrs = ['x', 'y',
                               ('vel_x', 0),
                               ('vel_y', 0),
                               'width', 'height',
                               'gravity']
        self.event_handlers = {'update': self.handle_update}

    def handle_update(self, entity, dt):
        entity.vel_y -= entity.gravity * dt
        entity.x += entity.vel_x * dt
        entity.y += entity.vel_y * dt

        r = from_entity(entity)
        if engine.get().entity_manager.get_in_area('platform', r):
            engine.get().entity_manager.remove(entity)

class FacingTracker(Behavior):

    def __init__(self):
        self.required_attrs = [('vel_x', 0),
                               ('facing', 'right')]
        self.event_handlers = {'update': self.handle_update}

    def handle_update(self, entity, dt):
        if entity.vel_x > 0:
            entity.facing = 'right'
        elif entity.vel_x < 0:
            entity.facing = 'left'

class PlayerProjectileShooter(Behavior):

    def __init__(self):
        self.required_attrs = ['shoot_time', ('shoot_counter', 0)]
        self.event_handlers = {'input' : self.handle_input,
                               'update' : self.handle_update}

    def handle_update(self, entity, dt):
        if entity.shoot_counter > 0:
            entity.shoot_counter -= dt

    def handle_input(self, entity, action, value):
        if action == 'fire' and value == 1 and entity.shoot_counter <= 0:
            entity.shoot_counter = entity.shoot_time

            m = engine.get().entity_manager.get_by_name('mouse')

            angle = radians((Vec2d(m.x, m.y) - Vec2d(entity.x, entity.y)).angle)

            p = Entity('projectile')

            p.x = entity.x
            p.y = entity.y
            p.vel_x = cos(angle) * entity.launch_speed# + entity.vel_x
            p.vel_y = sin(angle) * entity.launch_speed# + entity.vel_y

            engine.get().entity_manager.add(p)


class PlayerAnimationChooser(Behavior):

    def __init__(self):
        self.required_attrs = [('facing', "none"), ('dir', "none"), ('grounded', True)]
        self.event_handlers = {'update': self.handle_update}
        
    def handle_update(self, entity, dt):
        if entity.facing == 'left':
            entity.flip = 1
        elif entity.facing == 'right':
            entity.flip = 0
    
        if entity.grounded:
            if entity.animation_name == 'character-in-air':
                entity.handle('play_animation', 'character-land')                
            if entity.dir == "none":
                entity.handle('play_animation', 'character-idle')
            elif entity.dir != "none":
                entity.handle('play_animation', 'character-walk')
        else:
            if entity.jump:
                entity.handle('play_animation', 'character-jump')
            else:
                entity.handle('play_animation', 'character-in-air') 

class HurtBadGuy(Behavior):

    def __init__(self):
        self.required_attrs = ['x', 'y', 'width', 'height']
        self.event_handlers = {'update' : self.handle_update}

    def handle_update(self, entity, dt):
        hit = engine.get().entity_manager.get_in_area('bad_guy', from_entity(entity))
        for h in hit:
            h.health -= 1
        if hit:
            engine.get().entity_manager.remove(entity)

class DieOnZeroHealth(Behavior):

    def __init__(self):
        self.required_attrs = ['health']
        self.event_handlers = {'update' : self.handle_update}

    def handle_update(self, entity, dt):
        if entity.health == 0:
            engine.get().entity_manager.remove(entity)


class PlayerHurt(Behavior):

    def __init__(self):
        self.required_attrs = ['health',
                               'i_time',
                               ('i_count', 0)]
        self.event_handlers = {'update' : self.handle_update,
                               'damage' : self.handle_damage}

    def handle_update(self, entity, dt):
        if entity.i_count > 0:
            entity.i_count -= dt
        if engine.get().entity_manager.get_in_area('death_zone', from_entity(entity)):
            entity.handle('damage', 1)

    def handle_damage(self, entity, damage):
        if entity.i_count <= 0:
            entity.i_count = entity.i_time
            entity.health -= damage
            print 'ow', entity.health
            if entity.health <= 0:
                print 'i am dead'


class HurtPlayer(Behavior):
    def __init__(self):
        self.required_attrs = ['x', 'y', 'width', 'height']
        self.event_handlers = {'update': self.handle_update}


    def handle_update(self, entity, dt):
        hit = engine.get().entity_manager.get_in_area('player', from_entity(entity))
        for h in hit:
            h.handle('damage', 1)
        if hit:
            engine.get().entity_manager.remove(entity)


class BadGuyShoot(Behavior):

    def __init__(self):
        self.required_attrs = ['shoot_rate', ('shoot_counter', 0)]
        self.event_handlers = {'update' : self.handle_update}

    def handle_update(self, entity, dt):
        if entity.shoot_counter > 0:
            entity.shoot_counter -= dt

        if entity.shoot_counter <= 0:
            entity.shoot_counter = entity.shoot_rate

            p = Entity('bad_guy_projectile')

            target = engine.get().entity_manager.get_by_name('player')

            x = target.x - entity.x
            y = target.y - entity.y

            v = entity.launch_speed
            g = p.gravity


            test = v*v*v*v - g * (g * x * x + 2 * y * v * v )

            if x < 0:
                add = pi
            else:
                add = 0

            if test >= 0:
                angle = atan((v*v + sqrt(test))/(g*x)) + add

                p.x = entity.x
                p.y = entity.y
                p.vel_x = cos(angle) * entity.launch_speed
                p.vel_y = sin(angle) * entity.launch_speed

                engine.get().entity_manager.add(p)

def toward_zero(v, a, dt):
    if v > 0:
        return max(0, v - a * dt)
    else:
        return  min(0, v + a * dt)
