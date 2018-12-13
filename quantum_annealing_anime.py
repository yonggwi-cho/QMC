'''
Created on 2018/11/30

@author: 0145215059
'''
#coding:utf-8
import time
import math
import os
import sys
import matplotlib.pyplot as plt
import argparse
import numpy as np
import qmc
from concorde.tsp import TSPSolver

#QMC simulation
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--file",required=True,help="specify a file which contains cities's information.")
    parser.add_argument("--trotter_dim",type=int,default=10)
    parser.add_argument("--ann_para",type=float,default=1.0,help="initial annealing parameter")
    parser.add_argument("--ann_step",type=int,default=330)
    parser.add_argument("--mc_step",type=int,default=13320)
    parser.add_argument("--beta",type=float,default=float(37))
    parser.add_argument("--reduc_para",type=float,default=0.99)
    args = parser.parse_args()

    # prepare annealer
    anneal = qmc.QMC(args.trotter_dim,args.ann_para,args.ann_step,args.mc_step,args.beta,args.reduc_para)
    anneal.read(args.file)
    
    anneal.max_distance = 0
    for i in range(anneal.NCITY):
        for j in range(anneal.NCITY):
            if anneal.max_distance <= qmc.distance(anneal.POINT[i], anneal.POINT[j]):
                anneal.max_distance = qmc.distance(anneal.POINT[i], anneal.POINT[j])

    config_at_init_time = list(-np.ones(anneal.NCITY,dtype=np.int))
    config_at_init_time[0] = 1

    print "start..."
    t0 = time.clock()

    # solve by concorde
    list_x = list()
    list_y = list()
    for i in range(len(anneal.POINT)):
        list_x.append(anneal.POINT[i][0])
        list_y.append(anneal.POINT[i][1])
    solver = TSPSolver.from_data(list_x,list_y,norm="EUC_2D")
    optimal_tour = solver.solve()

    # extract positions of optimal tour
    optimal_pos_x =  list()
    optimal_pos_y =  list()
    for i in range(len(anneal.POINT)) :
        optimal_pos_x.append(anneal.POINT[optimal_tour.tour[i]][0])
        optimal_pos_y.append(anneal.POINT[optimal_tour.tour[i]][1])

    # prepare for figure
    fig,ax = plt.subplots(1,1)
    lines, = ax.plot(optimal_pos_x,optimal_pos_y)

    np.random.seed(100)
    spin = anneal.getSpinConfig(config_at_init_time)
    LengthList = list()
    for t in range(anneal.ANN_STEP):
        for i in range(anneal.MC_STEP):
            con = anneal.move(spin)
            rou = anneal.getBestRoute(con)
            length = anneal.getRealTotaldistance(rou)
            # make plot data
            x = list()
            y = list()
            for l in range(len(rou)):
                x.append((anneal.POINT[rou[l]])[0])
                y.append((anneal.POINT[rou[l]])[1])
            plt.plot(optimal_pos_x,optimal_pos_y,"ro-")
            lines.set_data(x,y)
            ax.set_xlim(min(x),max(x))
            ax.set_ylim(min(y),max(y))
            plt.pause(0.01)
        LengthList.append(length)
        print "Step:{}, Annealing Parameter:{}, length:{}".format(t+1,anneal.ANN_PARA, length)
        anneal.ANN_PARA *= anneal.reduc_para

    Route = anneal.getBestRoute(spin)
    Total_Length = anneal.getRealTotaldistance(Route)
    elapsed_time = time.clock()-t0

    print "shortest path is {}".format(Route)
    print "shortest lenght is {}".format(Total_Length)
    print "processing time is {}s".format(elapsed_time)

    plt.plot(LengthList)
    plt.show()
