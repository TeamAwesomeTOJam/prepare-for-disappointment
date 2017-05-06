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
        for c in self.cams:
            c.render()


class EditorMode(awesomeengine.mode.Mode):
    def enter(self):
        e = awesomeengine.get()

        p = Entity('platform')
        ce = Entity('editor_camera')
        m = Entity('editor_mouse')
        c = Entity('editor_entity_chooser')
        b1 = Entity('editor_place_button')
        b2 = Entity('editor_select_button')
        b3 = Entity('editor_delete_button')
        b4 = Entity('editor_move_button')

        e.entity_manager.add(p, ce, m, b1, b2, b3, b4, c)

        l = awesomeengine.layer.SimpleCroppedLayer('draw')
        l2 = awesomeengine.layer.SolidBackgroundLayer((0, 0, 0, 255))

        cam = Camera(awesomeengine.get().renderer, ce, [l2, l], [b1, b2, b3, b4, c])

        self.entities = [p, ce, m, b1, b2, b3, b4, c]
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
        for c in self.cams:
            c.render()