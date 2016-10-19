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

machines = ["stokes", "noether", "navier00", "navier01", "navier02", "navier03", "ampere00", "ampere02"]
machinecolors = ["#FEDBD9", "#FFECD6", "#CCF1FD", "#CCF1FD", "#CCF1FD", "#CCF1FD", "#E0EDD5", "#E0EDD5"]

print """<table border='0'>
  <tr bgcolor='#66ccee'>
    <td><pre>Machine</pre></td>
    <td><pre>CPU Threads <br>(Active/Total)</pre></td>
    <td><pre>Memory <br>(Free/Used/Total)</pre></td>
    <td><pre>Response time (s)</pre></td>
    <td><pre>Most Active Processes</pre></td>
  </tr>
"""

for i in range(0, len(machines)):
  server_name = machines[i] + '.cs.columbia.edu'
  nproc, response_time = scm.check_nproc(server_name) #subprocess.check_output("ssh " + server_name +  " \'nproc\'", shell=True)
  total_ram, used_ram, free_ram = scm.check_memory(server_name)
  cpu_info = scm.check_running_processes(server_name)
  
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
         machinecolors[i], cpu_info[0][1] , nproc,
         free_ram, used_ram, total_ram,
         response_time,
         top_cmds_string)

print "</table>"

print """
</body>
</html>
""" 
