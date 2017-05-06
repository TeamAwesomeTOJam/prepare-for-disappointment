import awesomeengine
import mapprinter
from awesomeengine.camera import Camera
from awesomeengine.entity import Entity


class AttractMode(awesomeengine.mode.Mode):
    def enter(self):
        e = awesomeengine.get()
        e.input_manager.set_input_map('default')

        h = Entity('hello')
        c = Entity('welcome_camera')

        e.entity_manager.add(h, c)

        l2 = awesomeengine.layer.SolidBackgroundLayer((0, 0, 0, 255))

        cam = Camera(awesomeengine.get().renderer, c, [l2], [h])

        self.entities = [h, c]
        self.cams = [cam]

    def leave(self):
        e = awesomeengine.get()
        for ent in self.entities:
            e.entity_manager.remove(ent)

    def handle_event(self, event):
        if event.target == 'MODE':
            if event.action == 'play':
                awesomeengine.get().change_mode('play')
    
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
                e.entity_manager.save_to_map(self.current_map, lambda x : 'editable' in x.tags)
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

        cam = Camera(awesomeengine.get().renderer, ce, [l2, l], [])
        self.cams = [cam]
        
        if not hasattr(e, 'current_map'):
            load_map("1")

    def leave(self):
        c = awesomeengine.get().entity_manager.get_by_name('play_camera')
        awesomeengine.get().entity_manager.remove(c)       

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

    def draw(self):
        for c in awesomeengine.get().entity_manager.get_by_tag('camera'):
            c.camera.render()
            
            
def load_map(map_name):
    e = awesomeengine.get()
    
    if e.entity_manager.has_by_name('selector'):
        selector = e.entity_manager.get_by_name('selector')
        e.entity_manager.remove(selector)

    for entity in e.entity_manager.get_by_tag('editable'):
        e.entity_manager.remove(entity)
    e.entity_manager.commit_changes()
    
    e.entity_manager.add_from_map(map_name)
    e.current_map = map_name
