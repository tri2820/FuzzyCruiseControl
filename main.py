import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

from environment import evaluate, debug_draw_errors

def controller_gen():
    velocity = ctrl.Antecedent(np.arange(-0.07,0.07,0.01), 'velocity')
    terrain = ctrl.Antecedent(np.arange(-1, 1, 0.01), 'terrain')
    acceleration = ctrl.Consequent(np.arange(-1,1,0.01), 'acceleration')

    velocity.automf(3)
    terrain.automf(3)
    acceleration.automf(7)

    rules = [
        ctrl.Rule(velocity['poor'] | terrain['poor'], acceleration['dismal']),
        ctrl.Rule(velocity['poor'] | terrain['average'], acceleration['poor']),
        ctrl.Rule(velocity['poor'] | terrain['good'], acceleration['mediocre']),
        ctrl.Rule(velocity['average'] | terrain['poor'], acceleration['poor']),
        ctrl.Rule(velocity['average'] | terrain['average'], acceleration['average']),
        ctrl.Rule(velocity['average'] | terrain['good'], acceleration['good']),
        ctrl.Rule(velocity['good'] | terrain['poor'], acceleration['decent']),
        ctrl.Rule(velocity['good'] | terrain['average'], acceleration['good']),
        ctrl.Rule(velocity['good'] | terrain['good'], acceleration['excellent'])
    ]

    cs = ctrl.ControlSystem(rules)
    csS = ctrl.ControlSystemSimulation(cs)
    
    def controller(velocity, terrain):
        csS.input['terrain'] = terrain
        csS.input['velocity'] = velocity
        csS.compute()
        action = csS.output['acceleration']
        return action   
    return controller


if __name__ == '__main__':
    # Compare 2 controllers
    
    # Draw errors of our group's controller as red line
    print('Evaluating our fuzzy controller')
    controller = controller_gen()
    nfailed, errors = evaluate(controller,silent=False)
    print(f'Car stuck inside valley {nfailed} times')
    plt.plot(errors, color='r', label='Our fuzzy controller')

    # Draw errors of the simple controller as blue line
    print('Evaluating simple controller')
    from simple_controller import simple_controller
    nfailed, errors = evaluate(simple_controller,silent=False)
    print(f'Car stuck inside valley {nfailed} times')
    plt.plot(errors, color='b', label='Simple controller')


    plt.ylabel('Error')
    plt.xlabel('Iteration (Road becomes more bumpy)')

    plt.legend()
    plt.show()
    