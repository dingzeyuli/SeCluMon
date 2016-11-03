#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cgi
import cgitb 
import os
import time
#cgitb.enable()  # for troubleshooting
from glob import glob

print "Content-type: text/html"
print

print """
<html>

<head>
  <title>Server Cluster Monitor (SeCluMon)</title>
</head>

<body>
"""
# os.environ["REMOTE_ADDR"]
# <meta http-equiv="refresh" content="80">

groups = ["graphics", "department", "clic"]

print """<table border='0'>
  <tr bgcolor='#66ccee'>
    <td><pre>Machine</pre></td>
    <td><pre>CPU Cores<br>(Active/Total)</pre></td>
    <td><pre>Memory<br>(Free/Used/Total)</pre></td>
    <td><pre>Response time (s)</pre></td>
    <td><pre>Most Active Processes</pre></td>
  </tr>
"""

total_cores = 0
total_active_cores = 0

for group in groups:
  print """
  <tr>
     <td><pre><emph></emph></pre></td>
  </tr>
  <tr>
  <td><pre><emph>%s:</emph></pre></td>
  </tr>
  """ % (group)

  folders = sorted(glob("data/" + group + "/*/"))
  
  
  for folder in folders:
    file = glob(folder + "*.txt")
  
    lines = []
    with open(file[0]) as f:
      for line in f:
        lines.append(line)
    #print lines
    
    hostname = lines[0].rstrip()
    token = lines[1].split()
    nproc = token[0]
    cpu_realtime = token[1]
    #print nproc
    #print cpu_realtime
    token = lines[2].split()
    total_ram = token[0]
    used_ram = token[1]
    free_ram = token[2]
    #print total_ram, used_ram, free_ram
    response_time = lines[3].rstrip()
    top_cmds_string = lines[4].rstrip()
  
    #print response_time
    #print top_cmds_string
  
    total_cores += int(nproc)
    total_active_cores += float(cpu_realtime)
  
    def rgb_to_hex(rgb):
      rgb = (rgb[0], rgb[1], rgb[2])
      return '#%02x%02x%02x' % rgb
  
    white = [255,255,255]
    red  = [255, 128, 128]
    ratio = float(cpu_realtime)/float(nproc)
    machinecolor = [ratio * r + (1-ratio) * w for r,w in zip(red,white) ]
    machinecolor = rgb_to_hex(machinecolor)
  
    print """
    <tr bgcolor='%s'>
       <td><pre>%s</pre></td>
       <td bgcolor='%s'><pre>%s/%s</pre></td>
       <td><pre>%s/%s/%s</pre></td>
       <td><pre>%s</pre></td>
       <td><pre>%s</pre></td>
    </tr>
    """ % (machinecolor, 
           hostname, 
           machinecolor, cpu_realtime, nproc,
           free_ram, used_ram, total_ram,
           response_time,
           top_cmds_string)

print "</table>"

lines = []
with open("cron.log") as f:
  for line in f:
    lines.append(line)
print "<pre>summary - CPU cores: %.2f / %i</pre>" % (total_active_cores, total_cores)
print "<br><pre>last updated on " + lines[0] + "</pre>"
print """
</body>
</html>
""" 

