#!/usr/bin/env python

import time
import os
os.chdir("html/db/SeCluMon/")
import seclumon as scm

import multiprocessing as mp


if __name__ == "__main__":

  hostnames = ["stokes",  "navier00", "navier01", "navier02", "navier03", "ampere00", "ampere01", "ampere02", "compute01", "compute02", "compute03", "compute05", "compute06", "compute07", "compute08"] 

  #hostnames.append("beijing")
  #hostnames.append("paris")
  #hostnames.append("santiago")
  #hostnames.append("brussels")
  #hostnames.append("damascus")
  #hostnames.append("tokyo")
  #hostnames.append("hanoi")
  #hostnames.append("kathmandu")
  
  t2 = time.time()
  #for hostname in hostnames:
    #print hostname
    #scm.process_node( hostname)
  pool = mp.Pool()
  pool.map(scm.process_node, hostnames)
  t3 = time.time()

  text_file = open("./cron.log", "w")
  text_file.write("%s\n" % time.strftime("%Y-%m-%d %H:%M"))
  text_file.write("%s\n" % os.getcwd())
  text_file.write("%f\n" % (t3-t2))
  text_file.close()
  
