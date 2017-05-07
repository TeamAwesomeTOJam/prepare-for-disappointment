import awesomeengine
import mapprinter
from awesomeengine.camera import Camera
from awesomeengine.entity import Entity


class AttractMode(awesomeengine.mode.Mode):
    def enter(self):
        e = awesomeengine.get()
        e.input_manager.set_input_map('default')

        h = Entity('title')
        c = Entity('welcome_camera')

        e.entity_manager.add(h, c)

        l = awesomeengine.layer.SimpleCroppedLayer('draw')

        cam = Camera(awesomeengine.get().renderer, c, [l], [])

        self.entities = [h, c]
        self.cams = [cam]

    def leave(self):
        e = awesomeengine.get()
        for ent in self.entities:
            e.entity_manager.remove(ent)

    def handle_event(self, event):
        if event.target == 'MODE':
            if event.action == 'play':
                awesomeengine.get().change_mode('splash')
    
        if awesomeengine.get().entity_manager.has_by_name(event.target):
            awesomeengine.get().entity_manager.get_by_name(event.target).handle('input', event.action, event.value)

    def update(self, dt):
        for e in awesomeengine.get().entity_manager.get_by_tag('update'):
            e.handle('update', dt)

    def draw(self):
        for c in awesomeengine.get().entity_manager.get_by_tag('camera'):
            c.camera.render()


class EditorMode(awesomeengine.mode.Mode):

    def __init__(self):
        self.cams = []

    def enter(self):
        awesomeengine.get()
        e = awesomeengine.get()
        e.input_manager.set_input_map('edit')

        m = Entity('editor_mouse')
        c = Entity('editor_entity_chooser')
        b1 = Entity('editor_place_button')
        b2 = Entity('editor_select_button')
        b3 = Entity('editor_delete_button')
        b4 = Entity('editor_move_button')

        e.entity_manager.add( m, b1, b2, b3, b4, c)

        ce = Entity('editor_camera')

        if hasattr(e, 'save_xy'):
            ce.x = e.save_xy[0]
            ce.y = e.save_xy[1]

        e.entity_manager.add(ce)
        l = awesomeengine.layer.SimpleCroppedLayer('draw')
        l2 = awesomeengine.layer.SolidBackgroundLayer((0, 0, 0, 255))
        l3 = awesomeengine.layer.GridLayer((75,75,0,0),200)

        cam = Camera(awesomeengine.get().renderer, ce, [l2,l3, l], [b1, b2, b3, b4, c])
        self.cams = [cam]
        
        if not hasattr(e, 'current_map'):
            load_map("1")

    def leave(self):
        e = awesomeengine.get()
        for ent in e.entity_manager.get_by_tag('editor'):
            e.entity_manager.remove(ent)

    def handle_event(self, event):
        e = awesomeengine.get()
    
        if event.target == 'MODE':
            if event.action == 'SAVE':
                e.entity_manager.save_to_map(e.current_map, lambda x : 'editable' in x.tags)
            if event.action == 'play':
                e.change_mode('play')
            if event.action.startswith('LOAD_'):
                _, map_name = event.action.split('_')
                load_map(map_name)
            if event.action == 'PRINT':
                mapprinter.print_map('/tmp/map.bmp')
        elif e.entity_manager.has_by_name(event.target):
            e.entity_manager.get_by_name(event.target).handle('input', event.action, event.value)

    def update(self, dt):
        for e in awesomeengine.get().entity_manager.get_by_tag('update'):
            e.handle('update', dt)
        awesomeengine.get().entity_manager.update_all_positions()

    def draw(self):
        for c in awesomeengine.get().entity_manager.get_by_tag('camera'):
            c.camera.render()


class PlayMode(awesomeengine.mode.Mode):

    def enter(self):
        e = awesomeengine.get()
        e.input_manager.set_input_map('play')
        
        ce = Entity('play_camera')
        e.entity_manager.add(ce)
        l = awesomeengine.layer.SimpleCroppedLayer('draw')
        l2 = awesomeengine.layer.SolidBackgroundLayer((0, 0, 0, 255))

        h = Entity('hearts')


        cam = Camera(awesomeengine.get().renderer, ce, [l2, l], [h])
        self.cams = [cam]

        m = Entity('mouse')
        e.entity_manager.add(m, h)

        if not hasattr(e, 'current_map'):
            load_map("1")

    def leave(self):
        c = awesomeengine.get().entity_manager.get_by_name('play_camera')
        awesomeengine.get().save_xy = (c.x,c.y)
        awesomeengine.get().entity_manager.remove(c)
        m = awesomeengine.get().entity_manager.get_by_name('mouse')
        awesomeengine.get().entity_manager.remove(m)

    def handle_event(self, event):
        if event.target == 'MODE':
            if event.action == 'edit':
                awesomeengine.get().change_mode('edit')
        elif awesomeengine.get().entity_manager.has_by_name(event.target):
            awesomeengine.get().entity_manager.get_by_name(event.target).handle('input', event.action, event.value)

    def update(self, dt):
        for e in awesomeengine.get().entity_manager.get_by_tag('update'):
            e.handle('update', dt)
        awesomeengine.get().entity_manager.update_all_positions()
        
        if awesomeengine.get().entity_manager.has_by_name('map_finish'):
            map_end = awesomeengine.get().entity_manager.get_by_name('map_finish')
            player = awesomeengine.get().entity_manager.get_by_name('player')
            if (abs(map_end.x - player.x) < 10) and (abs(map_end.y - player.y) < 10):
                awesomeengine.get().change_mode('splash')
                #load_map(str(int(awesomeengine.get().current_map) + 1))

    def draw(self):
        for c in awesomeengine.get().entity_manager.get_by_tag('camera'):
            c.camera.render()

class SpalshScreen(awesomeengine.mode.Mode):

    def enter(self):
        un_load_map()

        e = awesomeengine.get()
        e.input_manager.set_input_map('default')

        s = Entity('splash_screens')

        if not hasattr(e, 'current_map'):
            s.image = s.screens[0]
        else:
            s.image = s.screens[int(e.current_map)]

        c = Entity('splash_camera')

        e.entity_manager.add(s, c)

        l = awesomeengine.layer.SimpleCroppedLayer('draw')

        cam = Camera(awesomeengine.get().renderer, c, [l], [])

        self.entities = [s, c]
        self.cams = [cam]

    def leave(self):

        e = awesomeengine.get()
        for ent in self.entities:
            e.entity_manager.remove(ent)


        if not hasattr(e, 'current_map'):
            load_map("1")
        else:
            load_map(str(int(awesomeengine.get().current_map) + 1))

    def update(self, dt):
        pass

    def draw(self):
        for c in awesomeengine.get().entity_manager.get_by_tag('camera'):
            c.camera.render()

    def handle_event(self, event):
        e = awesomeengine.get()
        if event.target == 'MODE' and event.value == 1:
            if event.action == 'play':
                e.change_mode('play')


def un_load_map():
    e = awesomeengine.get()

    if e.entity_manager.has_by_name('player'):
        player = e.entity_manager.get_by_name('player')
        e.entity_manager.remove(player)

    if e.entity_manager.has_by_name('selector'):
        selector = e.entity_manager.get_by_name('selector')
        e.entity_manager.remove(selector)

    for entity in e.entity_manager.get_by_tag('editable'):
        e.entity_manager.remove(entity)

    for entity in e.entity_manager.get_by_tag('kill_me'):
        e.entity_manager.remove(entity)

    e.entity_manager.commit_changes()


def load_map(map_name):
    e = awesomeengine.get()

    un_load_map()

    e.entity_manager.add_from_map(map_name)
    e.entity_manager.commit_changes()
    
    if not e.entity_manager.has_by_name('player'):
        p = Entity('player')

        l = int(map_name) - 1

        p.max_health = p.max_health_level[l]
        p.health = p.max_health

        p.air_jumps = p.air_jumps_level[l]

        p.num_projectiles = p.num_projectiles_level[l]

        e.entity_manager.add(p)
        e.entity_manager.commit_changes()
    
    if e.entity_manager.has_by_name('map_start'):
        map_start = e.entity_manager.get_by_name('map_start')
        player = e.entity_manager.get_by_name('player')
        player.x = map_start.x
        player.y = map_start.y

    e.current_map = map_name
