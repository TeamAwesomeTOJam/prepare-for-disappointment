import sdl2hl
import awesomeengine


def print_map(path):    
    e = awesomeengine.get()
    entities = e.entity_manager.get_by_tag('editable')
    
    min_x = 0
    min_y = 0
    max_x = 0
    max_y = 0
    
    for entity in entities:
        for attr in ('x', 'y', 'width', 'height', 'colour'):
            if not hasattr(entity, attr):
                continue
        
        min_x = min(min_x, entity.x - entity.width / 2.0)
        min_y = min(min_y, entity.y - entity.width / 2.0)
        max_x = max(max_x, entity.x + entity.width / 2.0)
        max_y = max(max_y, entity.y + entity.height / 2.0)
        
    x_offset = -min_x
    y_offset = -min_y
    
    surface = sdl2hl.Surface(int(max_x + x_offset), int(max_y + y_offset), 32, sdl2hl.PixelFormat.rgba8888)
    renderer = sdl2hl.Renderer.create_software_renderer(surface)
    renderer.draw_color = (0, 0, 0, 255)
    renderer.clear()
    
    for entity in entities:
        for attr in ('x', 'y', 'width', 'height', 'colour'):
            if not hasattr(entity, attr):
                continue
        
        renderer.draw_color = entity.colour
        
        screen_x = int((entity.x - entity.width / 2.0) + x_offset)
        screen_y = int(max_y - (entity.y + entity.height / 2.0))
        
        renderer.fill_rect(sdl2hl.Rect(screen_x, screen_y, int(entity.width), int(entity.height)))
    
    renderer.present()
    surface.save_bmp(path)
