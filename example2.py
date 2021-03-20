#!/usr/bin/python39
from environment import evaluate, debug_draw_errors

memory = [0]
def my_controller(velocity):
    action = None
    if velocity>memory[-1]: 
        action = 0.5
    else:
        action = 1

    memory.append(velocity)
    return action

nfailed, errors = evaluate(my_controller,silent=False)
print(f'Car stuck inside valley {nfailed} times')
debug_draw_errors(errors)

