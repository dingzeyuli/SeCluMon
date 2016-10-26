#!/usr/bin/env python

import time
import os

import multiprocessing as mp


if __name__ == "__main__":
  os.chdir("html/db/SeCluMon/")
  import seclumon as scm

  hostnames = ["noether", "stokes", "ampere01"]
  hostnames = ["stokes", "noether", "navier00", "navier01", "navier02", "navier03", "ampere00", "ampere01", "ampere02", "compute01", "compute02", "compute03", "compute04", "compute05", "compute06", "compute07", "compute08"] 
  t0 = time.time()
  #for hostname in hostnames:
  #  scm.process_node(hostname)
  t1 = time.time()

  
  t2 = time.time()
  pool = mp.Pool()
  pool.map(scm.process_node, hostnames)
  t3 = time.time()


  
  
  text_file = open("./cron.log", "w")
  text_file.write("%s\n" % time.strftime("%Y-%m-%d %H:%M"))
  text_file.write("%s\n" % os.getcwd())
  text_file.write("%f\n" % (t1-t0))
  text_file.write("%f\n" % (t3-t2))
  text_file.close()
  
