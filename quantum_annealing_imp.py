#coding:utf-8
import time
import math
import os
import matplotlib.pyplot as plt
import argparse
import numpy as np
import qmc

#QMC simulation
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--file",type=str,default="./data/wi29.tsp",help="specify a file which contains cities's information.")
    parser.add_argument("--trotter_dim",type=int,default=10)
    parser.add_argument("--ann_para",type=float,default=1.0,help="initial annealing parameter")
    parser.add_argument("--ann_step",type=int,default=1000)
    parser.add_argument("--mc_step",type=int,default=5000)
    parser.add_argument("--beta",type=float,default=float(36))
    parser.add_argument("--reduc_para",type=float,default=0.999)
    args = parser.parse_args()

    # prepare annealer
    anneal = qmc.QMC(args.trotter_dim,args.ann_para,args.ann_step,args.mc_step,args.beta,args.reduc_para)
    anneal.read(args.file)

    anneal.calc_max_distance()

    config_at_init_time = list(-np.ones(anneal.NCITY,dtype=np.int))
    config_at_init_time[0] = 1

    print("start...")
    t0 = time.clock()

    np.random.seed(100)
    spin = anneal.getSpinConf(config_at_init_time)
    LengthList = list()
    for t in range(anneal.ANN_STEP):
        for i in range(anneal.MC_STEP):
            con = anneal.move_imp(spin)
            path = anneal.getBestPath(con)
            length = anneal.getRealTotaldistance(path)
        LengthList.append(length)
        print("Step:{},Annealing Parameter:{},length:{}".format(t+1,anneal.ANN_PARA, length))
        anneal.ANN_PARA *= anneal.reduc_para

    Route = anneal.getBestPath(spin)
    Total_Length = anneal.getRealTotaldistance(Route)
    elapsed_time = time.clock()-t0

    print("shortest path is {}".format(Route))
    print("shortest lenght is {}".format(Total_Length))
    print("processing time is {}s".format(elapsed_time))

    plt.plot(LengthList)
    plt.show()
