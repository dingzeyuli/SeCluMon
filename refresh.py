#!/usr/bin/env python

import time
import os
os.chdir("html/db/SeCluMon/")
import seclumon as scm

import multiprocessing as mp



if __name__ == "__main__":
  hostnames=[]
  hostnames = ["stokes", "noether", "ampere00", "ampere01", "ampere02", "compute01", "compute02", "compute03", "compute04", "compute05", "compute06", "compute07", "compute08", "navier00", "navier01", "navier02", "navier03", "green",]# "perelman"] 

  hostnames.append("beijing")
  hostnames.append("paris")
  hostnames.append("santiago")
  hostnames.append("brussels")
  hostnames.append("damascus")
  hostnames.append("tokyo")
  hostnames.append("hanoi")
  hostnames.append("kathmandu")
  hostnames.append("moscow")
  hostnames.append("rabat")
  hostnames.append("wellington")
  hostnames.append("nassau")
  hostnames.append("yerevan")
  hostnames.append("dhaka")
  hostnames.append("jakarta")
  hostnames.append("lisbon")
  hostnames.append("budapest")
  hostnames.append("pretoria")
  hostnames.append("tripoli")
  hostnames.append("ankara")
  hostnames.append("jerusalem")
  hostnames.append("cairo")
  hostnames.append("havana")
  #hostnames.append("islamabad")
  hostnames.append("nairobi")
  hostnames.append("lima")
  hostnames.append("copenhagen")
  hostnames.append("helsinki")
  hostnames.append("brasilia")
  hostnames.append("canberra")
  hostnames.append("tehran")
  hostnames.append("sofia")
  
  t2 = time.time()
  #for hostname in hostnames:
  #  print hostname
  #  scm.process_node( hostname)
  pool = mp.Pool(10)
  pool.map(scm.process_node, hostnames)
  t3 = time.time()
  print t3-t2
  pool.terminate()

  text_file = open("./cron.log", "w")
  text_file.write("%s\n" % time.strftime("%Y-%m-%d %H:%M"))
  text_file.write("%s\n" % os.getcwd())
  text_file.write("%f\n" % (t3-t2))
  text_file.close()
  
