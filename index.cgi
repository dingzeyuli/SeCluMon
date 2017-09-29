#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cgi
import cgitb 
import os
import time
#cgitb.enable()  # for troubleshooting
from glob import glob
import random

def rgb_to_hex(rgb):
  rgb = (rgb[0], rgb[1], rgb[2])
  return '#%02x%02x%02x' % rgb
def sine_mapping(input_x):
  if input_x <= 0.5:
    output_y = input_x*input_x*input_x*input_x/0.125
  elif input_x > 0.5:
    input_x = 1 - input_x
    output_y = ( -input_x*input_x*input_x*input_x+0.125)/0.125
  return output_y

def value_to_color(value, min_value, max_value):
  value = float(value)
  min_value = float(min_value)
  max_value = float(max_value)
  white = [128, 255, 128]
  red   = [255, 128, 128]
  ratio = float(value-min_value)/float(max_value - min_value)

  if ratio<0:
    ratio = 0
  elif ratio > 1:
    ratio = 1
  mcolor = [ratio * r + (1-ratio) * w for r,w in zip(red,white) ]
  machinecolor1 = rgb_to_hex(mcolor)
  return machinecolor1



print "Content-type: text/html"
print

print """
<html>

<head>
  <title>Server Cluster Monitor (SeCluMon)</title>
  <meta http-equiv="refresh" content="120">
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
background_colors=["#222222", "#111111", "#222222"]

print """<table border='0'>
  <tr bgcolor='#66ccee'>
    <td><pre>Machine</pre></td>
    <td><pre>CPU Hypercores<br>(Active/Total)</pre></td>
    <td><pre>Memory<br>(Free/Used/Total)</pre></td>
    <td><pre>Response time (s)</pre></td>
    <td><pre>Temperature<br>current / maximum</pre></td>
    <td><pre>Most Active Processes</pre></td>
  </tr>
"""

total_cores = 0
total_active_cores = 0

random.seed()

for group in groups:
  print """
  <tr>
     <td><pre><emph></emph></pre></td>
  </tr>
  <tr>
  <td><pre><emph>%s:</emph></pre></td>
  </tr>
  """ % (group)

  bg_color = "#%i%i%i%i%i%i" % (random.randint(1,2),random.randint(1,2),random.randint(1,2),random.randint(1,2),random.randint(1,2),random.randint(1,2))

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
    temperature = lines[4].split()
    curr_temp = temperature[0]
    max_temp = temperature[1]
    top_cmds_string = lines[5].rstrip()

    #print response_time
    #print top_cmds_string

    total_cores += int(nproc)
    total_active_cores += float(cpu_realtime)
  
    cpu_color = value_to_color(cpu_realtime, 0,  nproc)
    ram_color = value_to_color(used_ram, 0,  total_ram)
    temp_color = value_to_color(curr_temp, 30,  max_temp)
  
    bg_color = "#EFEFEF"
    cmds = ""
    a = int(top_cmds_string)
    better_cpu = 0
    for i in range(a):
      line = lines[6+i].rstrip()
      entries = line.split()
      if float(entries[1]) < 110:
          break
      cmds = cmds +  "%s %i-cores <span style='color:%s'>%s</span><br>" % (entries[0], int(int(entries[1])/100),bg_color, entries[2])
      better_cpu = better_cpu + int(entries[1])/100.0
    if (better_cpu > float(cpu_realtime)):
        cpu_realtime = better_cpu


 
    print """
    <tr bgcolor='%s'>
       <td><pre>%s</pre></td>
       <td bgcolor='%s'><pre>%s/%s</pre></td>
       <td bgcolor='%s'><pre>%s/%s/%s</pre></td>
       <td><pre>%s</pre></td>
       <td bgcolor='%s'><pre>%.1f / %.1f &deg;C<br>%.1f / %.1f &deg;F</pre></td>
       <td><pre>%s</pre></td>
    </tr>
    """ % (bg_color, 
           hostname, 
           cpu_color, cpu_realtime, nproc,
           ram_color, free_ram, used_ram, total_ram,
           response_time,
           temp_color, float(curr_temp), float(max_temp), float(curr_temp)*1.8+32, float(max_temp)*1.8+32,
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
<br>

<pre>
Code is on <a href="https://github.com/dingzeyuli/SeCluMon">github</a>. Group members, feel free to modify/improve it and send in pull requests.
<br><br>
"""


print "<h3>changelog:</h3>"
import requests
import json
url = "https://api.github.com/repos/dingzeyuli/SeCluMon/commits"
myResponse = requests.get(url)

if(myResponse.ok):
  #print myResponse.encoding
  #myResponse.encoding = 'ISO-8859-1'
  jData = json.loads(myResponse.content)
  #  print("The response contains {0} properties".format(len(jData)))
  #  print("\n")
  for key in jData:
    #for item in key:
      # print item
    commit_info = key.get(u'commit')
    commit_msg = commit_info.get(u'message')
    if "README" in commit_msg or "eadme" in commit_msg:
      continue
    if "Merge" in commit_msg and "branch" in commit_msg:
      continue
    if len(commit_msg) < 4:
      continue
    c_date = commit_info.get(u'committer').get(u'date')
    c_date = c_date[0:10]
    #c_date = c_date.replace('T', ' ' )
    #c_date = c_date.replace('Z', ' ' )
    #commit_url = commit_info.get(u'tree').get(u'url')
    #print commit_url

    print "%s %s -%s"%(c_date, commit_msg, commit_info.get(u'committer').get(u'name'))
else:
  # If response code is not ok (200), print the resulting http error code with description
  myResponse.raise_for_status()


print
"""
</pre>
</body>
</html>
""" 
