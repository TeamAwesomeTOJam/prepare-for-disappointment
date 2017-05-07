import os, sys

import awesomeengine
import behaviors
import editor_behaviors
import modes


def go():
    if getattr(sys, 'frozen', False):
        root = sys._MEIPASS
    else:
        root = os.path.dirname(os.path.abspath(__file__))

    e = awesomeengine.Engine(os.path.join(root, 'res'))
    e.behavior_manager.register_module(behaviors)
    e.behavior_manager.register_module(editor_behaviors)

    e.create_window(title='Prepare For Disappointment', size=(1280, 720))

    e.add_mode('welcome', modes.AttractMode())
    e.add_mode('edit', modes.EditorMode())
    e.add_mode('play', modes.PlayMode())
    e.add_mode('splash', modes.SpalshScreen())
    e.add_mode('dead', modes.DeadMode())

    e.change_mode('welcome')
    e.run()


if __name__ == '__main__':
    go()
