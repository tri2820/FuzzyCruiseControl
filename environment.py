#!/usr/bin/python39

from math import cos,pi
import numpy as np
import matplotlib.pyplot as plt
from random import random
from dataclasses import dataclass

"""
Simulate an adaptive cruising system over a bumpy road
controller(v) -> action (hit gas/brake) -> change car state -> new v -> controller(v) -> ...

Basic usage: 
    see example.py, example2.py

Consts
    Contains constants of the simulator
    goal    : to check whether car successfully goes over bumpy road and reaches goal
    gravity : to update car's velocity (v = v + gravity * terrain + ...)
    xmin to xmax : length of road
    vmin to vmax : car's bounded velocity

terrain_gen
    Generate terrain factor of the road. 
    Terrain factor is sum of many factors like slope, rolling resistance, air resistance,...
    Result is function `terrain` mapping (-inf,inf) which is the position to [-1,1] which is the terrain factor
    smoothness is in range [1,inf)
        1 will make the road look like cos-wave 
        inf will make the road totally flat
    npeaks is the number of peaks

Car 
    x       : current position
    v       : current velocity
    force   : how much velocity is increased per controller's action (v = v + action * force + ...)

step
    Input
    car             : car's state
    terrain         : generated from terrain_gen
    action          : controller action, <0 means brake, >0 means gas 

    Output
    next car's state

loop
    Simulate 1000 steps given terrain and controller

error
    Calculate variance of a list of velocity over time
    If error equals zero means constant speed (Good controller) 

evaluate
    Evaluate a controller
    Use this function to evaluate different controllers
"""


@dataclass 
class Consts:
    goal    : float = 0.6
    gravity : float = 0.0025
    xmax    : float = 0.6
    xmin    : float = -1.2
    vmax    : float = 0.07
    vmin    : float = -0.07


def terrain_gen(npeaks=1, smoothness=1.7):
    def terrain(x):
        return cos(npeaks*pi*x) / smoothness 
    return terrain


def debug_draw_terrain(f,color=None):
    x = np.linspace(Consts.xmin,Consts.xmax,1000)
    y = np.vectorize(f)(x)
    plt.axis((Consts.xmin, Consts.xmax, -1, 1))
    plt.plot(x,y,color=color)
    return plt
    

def debug_draw_errors(errors,color=None):
    x = range(len(errors))
    y = errors
    plt.plot(x,y,color=color)
    x1,x2,_,_ = plt.axis()
    plt.axis((x1, x2, 0, 0.00025))
    return plt


@dataclass
class Car:
    v : float = 0.01
    x : float = -0.5
    force : float = 0.001
    

def step(car, terrain, action) -> Car:
    car_ = Car()
    car_.v = car.v + action * car.force + terrain(car.x) * (-Consts.gravity)
    car_.v = np.clip(car_.v, Consts.vmin, Consts.vmax)
    car_.x = car.x + car_.v 
    return car_


def __dumb_controller(v,terrain):
    # Always hit gas
    return 1


def loop(terrain, controller,limit=10000):
    result = {'x': [], 'v': [], 'c': [], 'nstep':0, 'failed': False}
    car = Car()

    while car.x<Consts.goal:
        
        if result['nstep']>limit:
            result['failed'] = True
            return result
        
        next_input = (car.v, terrain(car.x))
        action = controller(*next_input)
        car = step(car, terrain, action)

        result['x'].append(car.x)
        result['v'].append(car.v)
        result['c'].append(terrain(car.x))
        result['nstep']+=1
    return result


def error(vs):
    return np.var(vs)


def evaluate(controller, silent=True):
    nfailed = 0
    errors = []
    t = 0

    for npeaks in range(1,11):
        for smoothness in np.linspace(1,3,20):
            t+=1
            if not silent:
                print(f'Test {t}.')
            terrain = terrain_gen(npeaks=npeaks, smoothness=smoothness)
            result = loop(terrain, controller)
            if result['failed']:  
                if not silent:
                    print(f' Failed!')
                nfailed+=1
                continue
            errors.append(error(result['v']))
            if not silent:
                    print(f' Success!')
    
    return nfailed, errors


if __name__=='__main__':
    nfailed, errors = evaluate(__dumb_controller)
    print(f'Failed {nfailed} times')
    debug_draw_errors(errors)
    plt.show()



    


