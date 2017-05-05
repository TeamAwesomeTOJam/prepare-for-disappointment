import awesomeengine
import behaviors
import modes


def go():
    e = awesomeengine.Engine('res')
    e.behavior_manager.register_module(behaviors)

    e.create_window(title='Prepare For Disappointment', size=(1280, 720))

    e.add_mode('welcome', modes.AttractMode())

    e.change_mode('welcome')
    e.run()


if __name__ == '__main__':
    go()
