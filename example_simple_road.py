#!/usr/bin/python39

from environment import terrain_gen, error, loop
from environment import __dumb_controller, debug_draw_terrain
import numpy as np
import matplotlib.pyplot as plt

print('Draw road')
terrain = terrain_gen()
plt = debug_draw_terrain(terrain)
plt.xlabel('Example road segment')
plt.legend()
plt.show()

result = loop(terrain,__dumb_controller)
if result['failed']:
    print('Car stuck, retry with better controller or smoother road')
    exit(0)

print(f'Error : {error(result["v"])}')

print('Testing dumb controller')
print('Draw velocity and terrain over time')
plt.plot(range(result['nstep']),result['v'],'r',label='velocity')
plt.plot(range(result['nstep']),result['c'],'b',label='terrain factor')
    
plt.ylabel('Value (Corresponding unit)')
plt.xlabel('Time')

plt.legend()
plt.show()