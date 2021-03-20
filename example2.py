#!/usr/bin/python39
from environment import evaluate, debug_draw_errors

# Static side effects
const_velocity = None
def my_controller(velocity, terrain):
    global const_velocity
    
    if const_velocity is None:
        # Assume the first input as the speed we want to keep
        const_velocity = velocity

    if velocity>const_velocity:
        action = 0.1
    else:
        action = 1

    return action

nfailed, errors = evaluate(my_controller,silent=False)
print(f'Car stuck inside valley {nfailed} times')
debug_draw_errors(errors).show()


