import awesomeengine
from awesomeengine.camera import Camera
from awesomeengine.entity import Entity


class AttractMode(awesomeengine.mode.Mode):
    def enter(self):
        e = awesomeengine.get()

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
        if awesomeengine.get().entity_manager.has_by_name(event.target):
            awesomeengine.get().entity_manager.get_by_name(event.target).handle('input', event.action, event.value)

    def update(self, dt):
        for e in awesomeengine.get().entity_manager.get_by_tag('update'):
            e.handle('update', dt)

    def draw(self):
        for c in awesomeengine.get().entity_manager.get_by_tag('camera'):
            c.camera.render()


class EditorMode(awesomeengine.mode.Mode):
    def enter(self):
        e = awesomeengine.get()

        ce = Entity('camera')
        m = Entity('editor_mouse')
        c = Entity('editor_entity_chooser')
        b1 = Entity('editor_place_button')
        b2 = Entity('editor_select_button')
        b3 = Entity('editor_delete_button')
        b4 = Entity('editor_move_button')

        e.entity_manager.add(ce, m, b1, b2, b3, b4, c)

        l = awesomeengine.layer.SimpleCroppedLayer('draw')
        l2 = awesomeengine.layer.SolidBackgroundLayer((0, 0, 0, 255))

        cam = Camera(awesomeengine.get().renderer, ce, [l2, l], [b1, b2, b3, b4, c])

        self.entities = [ce, m, b1, b2, b3, b4, c]

        self.cams = [cam]
        self._load_map("1")

    def leave(self):
        e = awesomeengine.get()
        for c in self.cams:
            c.hud_entities = []
        for ent in e.entity_manager.get_by_tag('editor'):
            e.entity_manager.remove(ent)

    def handle_event(self, event):
        e = awesomeengine.get()
    
        if event.target == 'EDITOR':
            if event.action == 'SAVE':
                e.entity_manager.save_to_map(self.current_map, lambda x : 'editable' in x.tags)
            if event.target == 'EDITOR':
                e.change_mode('play')
            if event.action.startswith('LOAD_'):
                _, map_name = event.action.split('_')
                self._load_map(map_name)
        elif e.entity_manager.has_by_name(event.target):
            e.entity_manager.get_by_name(event.target).handle('input', event.action, event.value)

    def update(self, dt):
        for e in awesomeengine.get().entity_manager.get_by_tag('update'):
            e.handle('update', dt)
        awesomeengine.get().entity_manager.update_all_positions()

    def draw(self):
        for c in awesomeengine.get().entity_manager.get_by_tag('camera'):
            c.camera.render()

    def _load_map(self, map_name):
        e = awesomeengine.get()
        
        if e.entity_manager.has_by_name('selector'):
            selector = e.entity_manager.get_by_name('selector')
            e.entity_manager.remove(selector)

        for entity in e.entity_manager.get_by_tag('editable'):
            e.entity_manager.remove(entity)
        e.entity_manager.commit_changes()
        
        e.entity_manager.add_from_map(map_name)
        self.current_map = map_name

class PlayMode(awesomeengine.mode.Mode):

    def enter(self):
        awesomeengine.get().input_manager.set_input_map('play')

    def leave(self):
        pass

    def handle_event(self, event):
        if awesomeengine.get().entity_manager.has_by_name(event.target):
            awesomeengine.get().entity_manager.get_by_name(event.target).handle('input', event.action, event.value)

    def update(self, dt):
        for e in awesomeengine.get().entity_manager.get_by_tag('update'):
            e.handle('update', dt)
        awesomeengine.get().entity_manager.update_all_positions()

    def draw(self):
        for c in awesomeengine.get().entity_manager.get_by_tag('camera'):
            c.camera.render()
