#!/usr/bin/python39

from environment import terrain_gen, error, loop
from environment import __dumb_controller, debug_draw_terrain
import numpy as np
import matplotlib.pyplot as plt

print('Draw road')
terrain = terrain_gen()
debug_draw_terrain(terrain)
plt.show()

result = loop(terrain,__dumb_controller)
if result['failed']:
    print('Car stuck, retry with better controller or smoother road')
    exit(0)

print(f'Error : {error(result["v"])}')

print('Draw velocity and terrain over time')
plt.plot(range(result['nstep']),result['v'],'r')
plt.plot(range(result['nstep']),result['c'],'b')
plt.show()