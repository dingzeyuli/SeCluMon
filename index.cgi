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

  #ratio = sine_mapping(ratio)
  mcolor = [ratio * r + (1-ratio) * w for r,w in zip(red,white) ]
  machinecolor1 = rgb_to_hex(mcolor)
  return machinecolor1, ratio



print "Content-type: text/html"
print

print """
<html>

<head>
  <title>Server Cluster Monitor (SeCluMon)</title>
  <meta http-equiv="refresh" content="120">
  <link rel="apple-touch-icon" sizes="57x57" href="./assets/apple-icon-57x57.png">
  <link rel="apple-touch-icon" sizes="60x60" href="./assets/apple-icon-60x60.png">
  <link rel="apple-touch-icon" sizes="72x72" href="./assets/apple-icon-72x72.png">
  <link rel="apple-touch-icon" sizes="76x76" href="./assets/apple-icon-76x76.png">
  <link rel="apple-touch-icon" sizes="114x114" href="./assets/apple-icon-114x114.png">
  <link rel="apple-touch-icon" sizes="120x120" href="./assets/apple-icon-120x120.png">
  <link rel="apple-touch-icon" sizes="144x144" href="./assets/apple-icon-144x144.png">
  <link rel="apple-touch-icon" sizes="152x152" href="./assets/apple-icon-152x152.png">
  <link rel="apple-touch-icon" sizes="180x180" href="./assets/apple-icon-180x180.png">
  <link rel="icon" type="image/png" sizes="192x192"  href="./assets/android-icon-192x192.png">
  <link rel="icon" type="image/png" sizes="32x32" href="./assets/favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="96x96" href="./assets/favicon-96x96.png">
  <link rel="icon" type="image/png" sizes="16x16" href="./assets/favicon-16x16.png">
  <link rel="manifest" href="./assets/manifest.json">
  <meta name="msapplication-TileColor" content="#ffffff">
  <meta name="msapplication-TileImage" content="./assets/ms-icon-144x144.png">
  <meta name="theme-color" content="#ffffff">
</head>

<body>

<!-- Start of StatCounter Code for Default Guide -->
<script type="text/javascript">
var sc_project=11459683; 
var sc_invisible=1; 
var sc_security="7a468f14"; 
var scJsHost = (("https:" == document.location.protocol) ?
"https://secure." : "http://www.");
document.write("<sc"+"ript type='text/javascript' src='" +
scJsHost+
"statcounter.com/counter/counter.js'></"+"script>");
</script>
<noscript><div class="statcounter"><a title="Web Analytics
Made Easy - StatCounter" href="http://statcounter.com/"
target="_blank"><img class="statcounter"
src="//c.statcounter.com/11459683/0/7a468f14/0/" alt="Web
Analytics Made Easy - StatCounter"></a></div></noscript>
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
    <td><pre>Memory (GB)<br>(Used/Total)</pre></td>
    <td><pre>Response time (s)</pre></td>
    <td><pre>Disk </pre></td>
    <td><pre>Temperature<br>current/maximum</pre></td>
    <td><pre>Top 5 Active CLIC users</pre></td>
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
    disk = lines[5].split()
    top_cmds_string = lines[6].rstrip()

    #print response_time
    #print top_cmds_string
    bg_color = "#EFEFEF"

    total_cores += int(nproc)
    total_active_cores += float(cpu_realtime)
  
 
    cmds = ""
    a = int(top_cmds_string)
    better_cpu = 0
    for i in range(a):
      line = lines[7+i].rstrip()
      entries = line.split()
      if float(entries[1]) < 90:
          break
      cmds = cmds +  "%s %i-cores <span style='color:%s'>%s</span><br>" % (entries[0], int(round(float(entries[1])/100.0)),bg_color, entries[2].encode('utf-8'))
    #  better_cpu = better_cpu + int(entries[1])/100.0
    #if (better_cpu > float(cpu_realtime)):
    #    cpu_realtime = better_cpu

    cpu_color, cpu_ratio = value_to_color(cpu_realtime, 0,  nproc)
    ram_color, ram_ratio = value_to_color(used_ram, 0,  total_ram)
    temp_color,temp_ratio= value_to_color(curr_temp, 30,  max_temp)
   
    def p2f(x):
      return float(x.strip('%'))/100
    if not disk:
      disk = "N/A"
      disk_color = bg_color
      disk_ratio = 0
    else:
      disk = disk[0]
      disk_color, disk_ratio = value_to_color(p2f(disk), 0, 1)
    
    all_ratios = [cpu_ratio, ram_ratio, temp_ratio, disk_ratio]
    max_index =  all_ratios.index(max(all_ratios))
    all_colors = [cpu_color, ram_color, temp_color, disk_color]
    max_color = all_colors[max_index]
 
 
    print """
    <tr bgcolor='%s'>
       <td bgcolor='%s'><pre>%s</pre></td>
       <td bgcolor='%s'><pre>%s/%s</pre></td>
       <td bgcolor='%s'><pre>%s/%s</pre></td>
       <td><pre>%s</pre></td>
       <td bgcolor='%s'><pre>%s</pre></td>
       <td bgcolor='%s'><pre>%.1f / %.1f &deg;C<br>%.1f / %.1f &deg;F</pre></td>
       <td><pre>%s</pre></td>
    </tr>
    """ % (bg_color, 
           max_color, hostname, 
           cpu_color, cpu_realtime, nproc,
           ram_color, used_ram, total_ram,
           response_time,
           disk_color, disk,
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
