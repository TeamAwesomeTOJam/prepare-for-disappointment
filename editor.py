import awesomeengine
import behaviors
import editor_behaviors
import modes


def go():
    e = awesomeengine.Engine('res')
    e.behavior_manager.register_module(behaviors)
    e.behavior_manager.register_module(editor_behaviors)

    e.create_window(title='Prepare For Disappointment', size=(1280, 720))

    e.add_mode('edit', modes.EditorMode())

    e.change_mode('edit')
    e.run()


if __name__ == '__main__':
    go()
