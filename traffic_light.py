from __future__ import absolute_import
from __future__ import print_function

import os, sys
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:   
    sys.exit("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary
import subprocess
import traci 
import random
import numpy as np
import h5py
import DQNA 
import SUMOinter 



if __name__ == '__main__':
    sumoInt = SUMOinter.SumoIntersection()
    # this script has been called from the command line. It will start sumo as a
    # server, then connect and run
    options = sumoInt.get_options()

    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')
    sumoInt.generate_routefile()

    # Main logic
    # parameters
    episodes = 2000
    batch_size = 32

    tg = 10
    ty = 6
    agent = DQNA.DQNAgent()
    try:
        agent.load('Models/reinf_traf_control.h5')
    except:
        print('No models found')

    for e in range(episodes):
        # DNN Agent
        # Initialize DNN with random weights
        # Initialize target network with same weights as DNN Network
        #log = open('log.txt', 'a')
        step = 0
        waiting_time = 0
        reward1 = 0
        reward2 = 0
        total_reward = reward1 - reward2
        stepz = 0
        action = 0

        traci.start([sumoBinary, "-c", "cross3ltl.sumocfg", '--start'])
        traci.trafficlight.setPhase("0", 0)
        traci.trafficlight.setPhaseDuration("0", 200)
        while traci.simulation.getMinExpectedNumber() > 0 and stepz < 7000:
            traci.simulationStep()
            state = sumoInt.getState()
            action = agent.act(state)
            light = state[2]

            if(action == 0 and light[0][0][0] == 0):
                # Transition Phase
                for i in range(6):
                    stepz += 1
                    traci.trafficlight.setPhase('0', 1)
                    waiting_time += (traci.edge.getLastStepHaltingNumber('1si') + traci.edge.getLastStepHaltingNumber(
                        '2si') + traci.edge.getLastStepHaltingNumber('3si') + traci.edge.getLastStepHaltingNumber('4si'))
                    traci.simulationStep()
                for i in range(10):
                    stepz += 1
                    traci.trafficlight.setPhase('0', 2)
                    waiting_time += (traci.edge.getLastStepHaltingNumber('1si') + traci.edge.getLastStepHaltingNumber(
                        '2si') + traci.edge.getLastStepHaltingNumber('3si') + traci.edge.getLastStepHaltingNumber('4si'))
                    traci.simulationStep()
                for i in range(6):
                    stepz += 1
                    traci.trafficlight.setPhase('0', 3)
                    waiting_time += (traci.edge.getLastStepHaltingNumber('1si') + traci.edge.getLastStepHaltingNumber(
                        '2si') + traci.edge.getLastStepHaltingNumber('3si') + traci.edge.getLastStepHaltingNumber('4si'))
                    traci.simulationStep()

                # Action Execution
                reward1 = traci.edge.getLastStepVehicleNumber(
                    '1si') + traci.edge.getLastStepVehicleNumber('2si')
                reward2 = traci.edge.getLastStepHaltingNumber(
                    '3si') + traci.edge.getLastStepHaltingNumber('4si')
                for i in range(10):
                    stepz += 1
                    traci.trafficlight.setPhase('0', 4)
                    reward1 += traci.edge.getLastStepVehicleNumber(
                        '1si') + traci.edge.getLastStepVehicleNumber('2si')
                    reward2 += traci.edge.getLastStepHaltingNumber(
                        '3si') + traci.edge.getLastStepHaltingNumber('4si')
                    waiting_time += (traci.edge.getLastStepHaltingNumber('1si') + traci.edge.getLastStepHaltingNumber(
                        '2si') + traci.edge.getLastStepHaltingNumber('3si') + traci.edge.getLastStepHaltingNumber('4si'))
                    traci.simulationStep()

            if(action == 0 and light[0][0][0] == 1):
                # Action Execution, no state change
                reward1 = traci.edge.getLastStepVehicleNumber(
                    '1si') + traci.edge.getLastStepVehicleNumber('2si')
                reward2 = traci.edge.getLastStepHaltingNumber(
                    '3si') + traci.edge.getLastStepHaltingNumber('4si')
                for i in range(10):
                    stepz += 1
                    traci.trafficlight.setPhase('0', 4)
                    reward1 += traci.edge.getLastStepVehicleNumber(
                        '1si') + traci.edge.getLastStepVehicleNumber('2si')
                    reward2 += traci.edge.getLastStepHaltingNumber(
                        '3si') + traci.edge.getLastStepHaltingNumber('4si')
                    waiting_time += (traci.edge.getLastStepHaltingNumber('1si') + traci.edge.getLastStepHaltingNumber(
                        '2si') + traci.edge.getLastStepHaltingNumber('3si') + traci.edge.getLastStepHaltingNumber('4si'))
                    traci.simulationStep()

            if(action == 1 and light[0][0][0] == 0):
                # Action Execution, no state change
                reward1 = traci.edge.getLastStepVehicleNumber(
                    '4si') + traci.edge.getLastStepVehicleNumber('3si')
                reward2 = traci.edge.getLastStepHaltingNumber(
                    '2si') + traci.edge.getLastStepHaltingNumber('1si')
                for i in range(10):
                    stepz += 1
                    reward1 += traci.edge.getLastStepVehicleNumber(
                        '4si') + traci.edge.getLastStepVehicleNumber('3si')
                    reward2 += traci.edge.getLastStepHaltingNumber(
                        '2si') + traci.edge.getLastStepHaltingNumber('1si')
                    traci.trafficlight.setPhase('0', 0)
                    waiting_time += (traci.edge.getLastStepHaltingNumber('1si') + traci.edge.getLastStepHaltingNumber(
                        '2si') + traci.edge.getLastStepHaltingNumber('3si') + traci.edge.getLastStepHaltingNumber('4si'))
                    traci.simulationStep()

            if(action == 1 and light[0][0][0] == 1):
                for i in range(6):
                    stepz += 1
                    traci.trafficlight.setPhase('0', 5)
                    waiting_time += (traci.edge.getLastStepHaltingNumber('1si') + traci.edge.getLastStepHaltingNumber(
                        '2si') + traci.edge.getLastStepHaltingNumber('3si') + traci.edge.getLastStepHaltingNumber('4si'))
                    traci.simulationStep()
                for i in range(10):
                    stepz += 1
                    traci.trafficlight.setPhase('0', 6)
                    waiting_time += (traci.edge.getLastStepHaltingNumber('1si') + traci.edge.getLastStepHaltingNumber(
                        '2si') + traci.edge.getLastStepHaltingNumber('3si') + traci.edge.getLastStepHaltingNumber('4si'))
                    traci.simulationStep()
                for i in range(6):
                    stepz += 1
                    traci.trafficlight.setPhase('0', 7)
                    waiting_time += (traci.edge.getLastStepHaltingNumber('1si') + traci.edge.getLastStepHaltingNumber(
                        '2si') + traci.edge.getLastStepHaltingNumber('3si') + traci.edge.getLastStepHaltingNumber('4si'))
                    traci.simulationStep()

                reward1 = traci.edge.getLastStepVehicleNumber(
                    '4si') + traci.edge.getLastStepVehicleNumber('3si')
                reward2 = traci.edge.getLastStepHaltingNumber(
                    '2si') + traci.edge.getLastStepHaltingNumber('1si')
                for i in range(10):
                    stepz += 1
                    traci.trafficlight.setPhase('0', 0)
                    reward1 += traci.edge.getLastStepVehicleNumber(
                        '4si') + traci.edge.getLastStepVehicleNumber('3si')
                    reward2 += traci.edge.getLastStepHaltingNumber(
                        '2si') + traci.edge.getLastStepHaltingNumber('1si')
                    waiting_time += (traci.edge.getLastStepHaltingNumber('1si') + traci.edge.getLastStepHaltingNumber(
                        '2si') + traci.edge.getLastStepHaltingNumber('3si') + traci.edge.getLastStepHaltingNumber('4si'))
                    traci.simulationStep()

            new_state = sumoInt.getState()
            reward = reward1 - reward2
            agent.remember(state, action, reward, new_state, False)
            # Randomly Draw 32 samples and train the neural network by RMS Prop algorithm
            if(len(agent.memory) > batch_size):
                agent.replay(batch_size)

        mem = agent.memory[-1]
        del agent.memory[-1]
        agent.memory.append((mem[0], mem[1], reward, mem[3], True))
        #log.write('episode - ' + str(e) + ', total waiting time - ' +
        #          str(waiting_time) + ', static waiting time - 338798 \n')
        #log.close()
        print('episode - ' + str(e) + ' total waiting time - ' + str(waiting_time))
        #agent.save('reinf_traf_control_' + str(e) + '.h5')
        traci.close(wait=False)

sys.stdout.flush()
