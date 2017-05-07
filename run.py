#!/bin/env python

try:
    from disappointment import main

    main.go()
except:
    import os
    import traceback

    with open(os.path.expanduser('~/disappointment-crash.log'), 'w') as error_log:
        traceback.print_exc(file=error_log)
