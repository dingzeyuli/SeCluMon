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
<!-- Start of StatCounter Code for Default Guide -->
<script type="text/javascript">
var sc_project=11155756; 
var sc_invisible=1; 
var sc_security="de515cde"; 
var scJsHost = (("https:" == document.location.protocol) ?
    "https://secure." : "http://www.");
document.write("<sc"+"ript type='text/javascript' src='" +
    scJsHost+
    "statcounter.com/counter/counter.js'></"+"script>");
</script>
<noscript><div class="statcounter"><a title="shopify visitor
statistics" href="http://statcounter.com/shopify/"
            target="_blank"><img class="statcounter"
                                 src="//c.statcounter.com/11155756/0/de515cde/1/"
                                 alt="shopify visitor statistics"></a></div></noscript>
<!-- End of StatCounter Code for Default Guide -->


"""
# os.environ["REMOTE_ADDR"]
# <meta http-equiv="refresh" content="80">

groups = ["graphics", "department", "clic"]

print """<table border='0'>
  <tr bgcolor='#66ccee'>
    <td><pre>Machine</pre></td>
    <td><pre>CPU Hypercores<br>(Active/Total)</pre></td>
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

    cmds = ""
    a = int(top_cmds_string)
    for i in range(a):
      line = lines[5+i].rstrip()
      entries = line.split()
      if float(entries[1]) < 110:
          break
      cmds = cmds +  "%s %i-cores %s<br>" % (entries[0], int(int(entries[1])/100), entries[2])


    #print response_time
    #print top_cmds_string

    total_cores += int(nproc)
    total_active_cores += float(cpu_realtime)
  
    def rgb_to_hex(rgb):
      rgb = (rgb[0], rgb[1], rgb[2])
      return '#%02x%02x%02x' % rgb
  
    white = [128,255,128]
    red  = [255, 128, 128]
    ratio = float(cpu_realtime)/float(nproc)
    if ratio<0:
      ratio = 0
    elif ratio > 1:
      ratio = 1
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
           cmds
           )

print "</table>"

lines = []
with open("cron.log") as f:
  for line in f:
    lines.append(line)
print "<pre>summary - CPU cores: %.2f / %i</pre>" % (total_active_cores, total_cores)
print "<br><pre>last updated on " + lines[0] + "(Eastern Time) </pre>"
print """
<br><br>
<pre>
Code is on <a href="https://github.com/dingzeyuli/SeCluMon">github</a>. Group members, feel free to modify/improve it.
</pre>
</body>
</html>
""" 
