import os,sys,subprocess 
import time

def check_group(hostname):
  if "compute" in hostname:
    return "department"
  if "navier" in hostname:
    return "graphics"
  if "ampere" in hostname:
    return "graphics"
  if "stokes" in hostname:
    return "graphics"
  if "noether" in hostname:
    return "graphics"
  if "green" in hostname:
    return "graphics"
  if "perelman" in hostname:
    return "graphics"

  return "clic"

def process_node(hostname):
  # check if the host is online
  # this old script only checks if a host is online
  response = os.system("ping -c 1 " + hostname)
  if (response == 0):
    # this new script checks if SSH port 22 is responding, much more robust than ping
    # it's slower than ping when the host is actually down
    # so I am only checking it when the host is up 
    # This will confirm is port 22 is responding.
    response = os.system(" nc -zv " + hostname + " 22")

  folder_name = 'data/' + check_group(hostname) + '/' +  hostname
  log_txt_name = 'data/history/' + check_group(hostname) + '/' +  hostname + '.txt'
  if response == 0:
    print hostname, 'is up!'
    if not os.path.exists(folder_name):
      os.makedirs(folder_name)
    #return
  else:
    #with open(log_txt_name, "a") as myfile:
    #  myfile.write("%s 0 0 \n" % time.strftime("%Y-%m-%d-%H:%M").rstrip())
    print hostname, 'is down!'
    if not os.path.exists(folder_name):
      return
    os.remove(folder_name + "/info.txt")
    os.rmdir(folder_name)
    return
  
  # gather cpu, memory, and related info
  nproc, response_time = check_nproc(hostname)
  total_ram, used_ram, free_ram = check_memory(hostname)
  cpu_realtime = check_running_processes(hostname)
  active_processes = check_busy_user(hostname)
  curr_temp, max_temp = check_temperature(hostname)
  disk = check_disk(hostname)

  #with open(log_txt_name, "a") as myfile:
  #  myfile.write("%s %s %s \n" % (time.strftime("%Y-%m-%d-%H:%M").rstrip(), cpu_realtime, nproc ) )

  # write them to the folder
  text_file = open(folder_name + "/info.txt", "w")
  text_file.write("%s \n" % (hostname))
  text_file.write("%s %s\n" % (nproc, cpu_realtime))
  text_file.write("%s %s %s\n" % (total_ram, used_ram, free_ram))
  text_file.write("%s \n" % (response_time))
  text_file.write("%s %s\n" % (curr_temp, max_temp))
  text_file.write("%s\n" % (disk))
  if not active_processes:
    text_file.write("0\n" )
  else:
    text_file.write("%i \n" % (len(active_processes)))
    for line in active_processes:
      for entry in line:
        text_file.write("%s " % entry)
      text_file.write("\n")


  text_file.close()
  return

def check_nproc(server_name):
  t0 = time.time()
  nproc = subprocess.check_output("ssh " + server_name +  " \'nproc\'", shell=True)
  t1 = time.time()
  response_time = t1-t0

  return nproc.rstrip(), response_time


def check_running_processes(server_name):
  #cmd = " \' ps -e -o uname,pcpu,etime --sort=-pcpu,-etime | head -n 11 | tail -n 10  \' "
  #output = subprocess.check_output("ssh " + server_name +  cmd, shell=True)
  #output1 = output.split('\n')
  #
  #cmd = " \' ps -e -o cmd --sort=-pcpu,-etime | head -n 11 | tail -n 10  \' "
  #output_cmd = subprocess.check_output("ssh " + server_name +  cmd, shell=True)
  #output1_cmd = output_cmd.split('\n')

  cmd = " \' cat <(grep \"cpu \" /proc/stat) <(sleep 1 && grep \"cpu \" /proc/stat) \' "
  output = subprocess.check_output("ssh " + server_name +  cmd, shell=True)
  cpu_realtime = subprocess.check_output("echo \"" + output + "\"| awk -v RS='' '{print ($13-$2+$15-$4)/100 }'", shell=True)
  
  # cmd = " \' top -b -n 1  | grep \"^[0-9]\" | head -n 10 \' "
  # output = subprocess.check_output("ssh " + server_name +  cmd, shell=True)
  # process_info = subprocess.check_output("echo \"" + output + "\"| awk '{ printf(\"%s %-8s %-8s\\n\", $2, $9, $12); }'", shell=True)

  #process_info = process_info.rstrip().split('\n')
  #active_processes = []
  #for line in process_info:
  #  tokens = line.split()
  #  if (len(tokens) < 2):
  #    break
  #  if (float(tokens[1]) < 50):
  #    break

  #  for i in tokens:
  #    active_processes.append(line)



  #for i in range(0,10):
  #  output2 = output1[i].split()
  #  # output2 looks like this ['dli', '4345', '1-01:44:42']

  #  # ignore process using less than 0.8 CPU
  #  if (float(output2[1])< 80 and i>=1):
  #    break
  #  output2[1] = output2[1][:-2]
  #  output2.append(output1_cmd[i])
  #  process_info.append(output2)
  return cpu_realtime.rstrip()

def check_memory(server_name):
  cmd = " \'free -g | head -n2 | tail -n1  \' "
  output = subprocess.check_output("ssh " + server_name +  cmd, shell=True)
  output1 = output.split() 
  return output1[1], output1[2], output1[3]

def check_busy_user(server_name):
  cmd = " \'ps aux | sort -nrk 3,3 | head -n 5 \' "
  output = subprocess.check_output("ssh " + server_name +  cmd, shell=True)
  output1 = output.split('\n') 

  index = 0
  w, h = 3, 5;
  output = [[' ' for x in range(w)] for y in range(h)] 

  for line in output1:
    entries = line.split()
    if len(entries) < 4:
      continue
    output[index][0] = entries[0]
    output[index][1] = entries[2]
    output[index][2] = entries[10]
    index += 1

  return output

def check_disk(server_name):
  cmd = " df | grep local | awk \'{print $5}\' "
  output = subprocess.check_output("ssh " + server_name +  cmd, shell=True)
  output1 = output.split('\n') 
  
  return output1[0]

def check_temperature(server_name):
  cmd = " cat /sys/devices/platform/coretemp.\?/hwmon\*/hwmon\*/temp\*_input | awk \'{ total += $1 } END { print total/NR/1000 }\' "
  output = subprocess.check_output("ssh " + server_name +  cmd, shell=True)
  output1 = output.split('\n') 
  
  cmd = " cat /sys/devices/platform/coretemp.\?/hwmon\*/hwmon\*/temp\*_max | awk \'{ total += $1 } END { print total/NR/1000 }\' "
  output = subprocess.check_output("ssh " + server_name +  cmd, shell=True)
  output2 = output.split('\n') 

  return output1[0], output2[0]


def test_github_api():
  import requests
  import json
  url = "https://api.github.com/repos/dingzeyuli/SeCluMon/commits"
  myResponse = requests.get(url)
  
  if(myResponse.ok):
    print myResponse.encoding
    #myResponse.encoding = 'ISO-8859-1'
    jData = json.loads(myResponse.content)
    print("The response contains {0} properties".format(len(jData)))
    print("\n")
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
      print commit_info.get(u'committer').get(u'date')
      print commit_info.get(u'message')
      print commit_info.get(u'committer').get(u'name')
  else:
    # If response code is not ok (200), print the resulting http error code with description
    myResponse.raise_for_status()


if __name__ == "__main__":
  #process_node("beijing")
  hostname = "stokes"
  #output = check_busy_user(hostname)
  # output, o2 = check_temperature(hostname)
  # print output, o2
  output = check_disk(hostname)
  print output

  #response = os.system(" nc -zv " + hostname + " 22")
  #print "response: ", response
  #hostname = "ampere00"
  #response = os.system(" nc -zv " + hostname + " 22")
  #print "response: ", response

  #test_github_api()
