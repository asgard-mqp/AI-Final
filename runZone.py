#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 17:31:11 2017

@author: gtabor
"""

import gym
import time
from random import *
import time
import numpy as np
import math


def getxy(index):
    x = index % 6
    y = int(index / 6)
    return (x,y)
def getDistance(index1,index2):
    start = getxy(index1)
    stop = getxy(index2)
    xDist = start[0] - stop[0]
    yDist = start[1] - stop[1]
    return math.sqrt(xDist**2 + yDist **2)
def find_next_goal_location(goals,tiles):
    for tile in tiles:
        if(goals[0][0] == tile or
           goals[1][0] == tile or
           goals[2][0] == tile or
           goals[3][0] == tile):#
            continue
        return tile
def AI(my_data, their_data,tiles_data,my_goals,their_goals,important_tiles):
    if my_data[1] > 0 : #have a goal
        if my_data[0] in important_tiles[:-1]: #if im at scoring location
            return 36
        if my_goals[my_data[1] - 1][1] >=8: #if my goal has 8 cones
            return find_next_goal_location(my_goals,important_tiles[:-1])
        else: #get cones
            if tiles_data[my_data[0]]>0: #if cones where I am
                return 37 
            elif my_data[3] > 0 and important_tiles[4] == my_data[0]: #can get loads
                return 37 
            else:
                distance = []
                locations = []
                for i in range(len(tiles_data)):
                    if tiles_data[i] > 0: 
                        distance.append(getDistance(my_data[0],i))
                        locations.append(i)
                if len(distance) == 0:
                    if(my_data[3]>0):
                        return important_tiles[4]
#                    print('going to next goal location')
                    return find_next_goal_location(my_goals,important_tiles[:-1])
                bestLocation = locations[np.argmin(distance)]
#                print(bestLocation)
                return(bestLocation)
    else:#dont have goal
        r = [0,1,2,3]
        shuffle(r)
        goto = 0
        for i in r: #find 1st not scored
            if(my_goals[i][0] in important_tiles[:-1]):
#                print('already done '+str(important_tiles[4]))
                continue
            else:
                if(my_data[0] == my_goals[i][0]):#if im there
#                    print('im there')
                    return 36
                else:
                    goto= my_goals[i][0] #go there
#        print('kill time ' +str(important_tiles[4]))
#        print(my_goals)
#        print(important_tiles)
        return goto #nothing else to do but need to kill time
        
    
env = gym.make("GridWorld-v0")
start_time= time.time()
red_wins=0
blue_wins = 0
ties = 0
red = []
blue = []
bigdic = {}
total = 0

num = 100000
for i in range(num):
    env.reset()
    state_list = []
    state, reward, done, info = env.step(200) # fake action with no time penalty to get field state
    for i in range(1000):
    #    print('red time ' + str(state.red_data[2]))
    #    print('blue time ' + str(state.blue_data[2]))
        if done ==True:
            break
        if state.blue_data[2] > state.red_data[2]:
            #print('reds turn')
            choice = AI(state.red_data,state.blue_data,state.tile_data,\
               [state.goal_data[i] for i in range(4)],[state.goal_data[4 + i] for i in range(4)],\
               [30,31,24,25,12])
            action = random()            
            if action < 0.01:
                choice = randint(0,37)
            pair_string = state.get_Key_Red(choice)
            #print(pair_string)
            state_list.append(pair_string)
            state, reward, done, info = env.step(choice)
            total +=1
        else:
           # print('blues turn')
    
            choice = AI(state.blue_data,state.red_data,state.tile_data,\
               [state.goal_data[4 + i] for i in range(4)],[state.goal_data[i] for i in range(4)],\
               [5,4,11,10,2])
            action = random()
            if action < 0.01:
                choice = randint(0,37)
            state, reward, done, info = env.step(100 + choice)
#        if(True or i%5 ==0):
#            env.render(close=True)
#            
#            env.render()
#            time.sleep(0.3)
#env.render() 
    won = 0
    lost = 0
    if reward[0] > reward[1]:
        red_wins += 1
        won = 1
    elif reward[0] < reward[1]: 
        blue_wins += 1
        lost = 1
    else:
        ties += 1
    red.append(reward[0])
    blue.append(reward[1])
    for state_pair in state_list:
        if won or lost:
            if state_pair in bigdic:
                old = bigdic[state_pair]
                bigdic[state_pair] = [old[0] + won,old[1] + lost]
            else:
                bigdic[state_pair] = [won,lost]
elapsed_time = time.time() - start_time
print(elapsed_time/num)
#print(elapsed_time)
#print(np.amax(red))
#print(np.amax(blue))
#print(np.average(red))
#print(np.average(blue))
print(len(bigdic))
print(total)
print(len(bigdic)/total)
from datetime import datetime
now = datetime.now()
#print (now)
np.save('new/'+str(now)+'.npy',bigdic)
#env.render(close=True)
#
#env.render()
#time.sleep(0.5)

