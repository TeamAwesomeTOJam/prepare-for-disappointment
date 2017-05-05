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
        c = Entity('editor_camera')
        m = Entity('editor_mouse')
        b1 = Entity('editor_place_button')
        b2 = Entity('editor_select_button')
        b3 = Entity('editor_delete_button')

        e.entity_manager.add(p, c, m, b1, b2, b3)

        l = awesomeengine.layer.SimpleCroppedLayer('draw')
        l2 = awesomeengine.layer.SolidBackgroundLayer((0, 0, 0, 255))

        cam = Camera(awesomeengine.get().renderer, c, [l2, l], [b1, b2, b3])

        self.entities = [p, c, m, b1, b2, b3]
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