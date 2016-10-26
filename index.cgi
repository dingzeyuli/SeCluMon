#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import seclumon as scm
import cgi
import cgitb 
#cgitb.enable()  # for troubleshooting

print "Content-type: text/html"
print

print """
<html>

<head>
  <title>Server Cluster Monitor (SeCluMon)</title>
  <meta http-equiv="refresh" content="300">
</head>

<body>
"""
# "noether","#FEDBD9", 
machines = ["stokes", "noether", "navier00", "navier01", "navier02", "navier03", "ampere00", "ampere01", "ampere02", "compute01", "compute02", "compute03", "compute04", "compute05", "compute06", "compute07", "compute08"] 
machinecolors = ["#FEDBD9", "#FEDBD9", "#CCF1FD", "#CCF1FD", "#CCF1FD", "#CCF1FD", "#E0EDD5", "#E0EDD5", "#E0EDD5", "#F0CBFD", "#F0CBFD", "#F0CBFD", "#F0CBFD", "#F0CBFD", "#F0CBFD", "#F0CBFD", "#F0CBFD"]

print """<table border='0'>
  <tr bgcolor='#66ccee'>
    <td><pre>Machine</pre></td>
    <td><pre>CPU Cores<br>(Active/Total)</pre></td>
    <td><pre>Memory<br>(Free/Used/Total)</pre></td>
    <td><pre>Response time (s)</pre></td>
    <td><pre>Most Active Processes</pre></td>
  </tr>
"""

for i in range(0, len(machines)):
  server_name = machines[i] + '.cs.columbia.edu'
  nproc, response_time = scm.check_nproc(server_name) #subprocess.check_output("ssh " + server_name +  " \'nproc\'", shell=True)
  total_ram, used_ram, free_ram = scm.check_memory(server_name)
  cpu_info, cpu_realtime = scm.check_running_processes(server_name)
  
  top_cmds = []
  for j in range(0, len(cpu_info)):
    top_cmds.append(cpu_info[j][3])
  top_cmds_string = ''.join(top_cmds)

  print """
  <tr bgcolor='%s'>
     <td><pre>%s</pre></td>
     <td bgcolor='%s'><pre>%s/%s</pre></td>
     <td><pre>%s/%s/%s</pre></td>
     <td><pre>%f</pre></td>
     <td><pre>%s</pre></td>
  </tr>
  """ % (machinecolors[i], 
         machines[i], 
         machinecolors[i], cpu_realtime, nproc,
         free_ram, used_ram, total_ram,
         response_time,
         top_cmds_string)

print "</table>"

print """
</body>
</html>
""" 
