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