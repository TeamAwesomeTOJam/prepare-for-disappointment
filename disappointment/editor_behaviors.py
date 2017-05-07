from awesomeengine.behavior import Behavior
from awesomeengine import engine
from awesomeengine.entity import Entity
from awesomeengine.rectangle import from_entity, Rect


class EntityPlacer(Behavior):

    def __init__(self):
        self.required_attrs = ['x', 'y',
                               ('world_x', 0),
                               ('world_y', 0),
                               ("mode" , "place")]
        self.event_handlers = {'input': self.handle_input}

    def handle_input(self, entity, action, value):
        if action == 'button' and value == 1:
            e = engine.get()
            place_button = e.entity_manager.get_by_name('place_button')
            if place_button.selected:
                chooser = e.entity_manager.get_by_name('entity_chooser')
                name = chooser.entity_list[chooser.entity_list_selected_index]
                new_entity = Entity(name,x=entity.world_x, y=entity.world_y)
                if not e.entity_manager.has_by_name(new_entity.name):
                    e.entity_manager.add(new_entity)
            select_button = e.entity_manager.get_by_name('select_button')
            if select_button.selected:
                try:
                    selector = e.entity_manager.get_by_name('selector')
                    e.entity_manager.remove(selector)
                except:
                    pass
                to_select = e.entity_manager.get_in_area("editable", Rect(entity.world_x, entity.world_y, 0, 0))
                if to_select:
                    f = to_select.pop()
                    selector = Entity('editor_selector', follow=f, x=f.x, y = f.y)
                    e.entity_manager.add(selector)
            move_button = e.entity_manager.get_by_name('move_button')
            if move_button.selected:
                try:
                    selector = e.entity_manager.get_by_name('selector')
                    selector.follow.x = entity.world_x
                    selector.follow.y = entity.world_y
                    selector.x = entity.world_x
                    selector.y = entity.world_y
                except:
                    pass

class Selector(Behavior):

    def __init__(self):
        self.required_attrs = ['x', 'y',
                               'width', 'height',
                               'follow']
        self.event_handlers = {'draw': self.handle_draw,
                               'update' : self.handle_update,
                               'input' : self.handle_input}

    def handle_draw(self, entity, camera):
        r = from_entity(entity)
        camera.draw_rect((255,0,0,0), r)

    def handle_update(self, entity, dt):
        entity.x = entity.follow.x
        entity.y = entity.follow.y

    def handle_input(self, entity, action, value):
        e = engine.get()
        try:
            selector = e.entity_manager.get_by_name('selector')
            p = selector.follow
            if value == 1:
                if action == 'right':
                    p.x += 10
                elif action == 'left':
                    p.x -= 10
                elif action == 'up':
                    p.y += 10
                elif action == 'down':
                    p.y -= 10
                elif action == 'grow_x':
                    p.width += 10
                elif action == 'shrink_x':
                    p.width = max(p.width - 10, 0)
                elif action == 'grow_y':
                    p.height += 10
                elif action == 'shrink_y':
                    p.height = max(p.height - 10, 0)
        except:
            pass

class DeleteSelected(Behavior):

    def __init__(self):
        self.required_attrs = []
        self.event_handlers = {"clicked": self.handle_clicked}

    def handle_clicked(self, entity):
        e = engine.get()
        try:
            selector = e.entity_manager.get_by_name('selector')
            e.entity_manager.remove(selector.follow)
            e.entity_manager.remove(selector)
        except:
            pass

class EntityChooser(Behavior):

    def __init__(self):
        self.required_attrs = ["entity_list", "entity_list_selected_index", "text"]
        self.event_handlers = {"input": self.handle_input}

    def handle_input(self, entity, action, value):
        if value == 1:
            if action == 'next':
                entity.entity_list_selected_index = (entity.entity_list_selected_index + 1) % len(entity.entity_list)
                entity.text = entity.entity_list[entity.entity_list_selected_index]
            elif action == 'prev':
                entity.entity_list_selected_index = (entity.entity_list_selected_index - 1) % len(entity.entity_list)
                entity.text = entity.entity_list[entity.entity_list_selected_index]
