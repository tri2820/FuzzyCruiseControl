#!/usr/bin/python39
from environment import evaluate, debug_draw_errors
import matlab
import matlab.engine
eng = matlab.engine.start_matlab()

def load_controller(filename):
    matlab_controller = eng.readfis(filename)
    def controller(velocity, terrain):
        inp = matlab.double([velocity, terrain])
        action = eng.evalfis(matlab_controller, inp)
        return action
    return controller

SIT215_controller = load_controller('PBL_Task_1.fis')
nfailed, errors = evaluate(SIT215_controller,silent=False)
print(f'Car stuck inside valley {nfailed} times')
debug_draw_errors(errors).show()


