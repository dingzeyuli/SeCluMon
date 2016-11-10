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
  response = 0
  #trials = 2
  #while ( trials > 0):
  response = os.system("ping -c 1 " + hostname)
  #  trials = trials - 1
  #  print trials
  #if (response == 0):
  #  break
  folder_name = 'data/' + check_group(hostname) + '/' +  hostname
  log_txt_name = 'data/history/' + check_group(hostname) + '/' +  hostname + '.txt'
  if response == 0:
    print hostname, 'is up!'
    if not os.path.exists(folder_name):
      os.makedirs(folder_name)
    #return
  else:
    with open(log_txt_name, "a") as myfile:
      myfile.write("%s 0 0 \n" % time.strftime("%Y-%m-%d-%H:%M").rstrip())
    print hostname, 'is down!'
    if not os.path.exists(folder_name):
      return
    os.remove(folder_name + "/info.txt")
    os.rmdir(folder_name)
    return
  
  # gather cpu, memory, and related info
  nproc, response_time = check_nproc(hostname)
  total_ram, used_ram, free_ram = check_memory(hostname)
  active_processes, cpu_realtime = check_running_processes(hostname)

  with open(log_txt_name, "a") as myfile:
    myfile.write("%s %s %s \n" % (time.strftime("%Y-%m-%d-%H:%M").rstrip(), cpu_realtime, nproc ) )

  # write them to the folder
  text_file = open(folder_name + "/info.txt", "w")
  text_file.write("%s \n" % (hostname))
  text_file.write("%s %s\n" % (nproc, cpu_realtime))
  text_file.write("%s %s %s\n" % (total_ram, used_ram, free_ram))
  text_file.write("%s \n" % (response_time))
  if not active_processes:
    text_file.write("0\n" )
  else:
    text_file.write("%i \n" % (len(active_processes)))
    for line in active_processes:
      text_file.write("%s \n" % (line))

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
  
  cmd = " \' top -b -n 1  | grep \"^[0-9]\" | head -n 10 \' "
  output = subprocess.check_output("ssh " + server_name +  cmd, shell=True)
  process_info = subprocess.check_output("echo \"" + output + "\"| awk '{ printf(\"%s %-8s %-8s\\n\", $2, $9, $12); }'", shell=True)

  process_info = process_info.rstrip().split('\n')
  active_processes = []
  for line in process_info:
    tokens = line.split()
    if (len(tokens) < 2):
      break
    if (float(tokens[1]) < 50):
      break

    for i in tokens:
      active_processes.append(line)



  #for i in range(0,10):
  #  output2 = output1[i].split()
  #  # output2 looks like this ['dli', '4345', '1-01:44:42']

  #  # ignore process using less than 0.8 CPU
  #  if (float(output2[1])< 80 and i>=1):
  #    break
  #  output2[1] = output2[1][:-2]
  #  output2.append(output1_cmd[i])
  #  process_info.append(output2)
  return active_processes, cpu_realtime.rstrip()

def check_memory(server_name):
  cmd = " \'free -g | head -n2 | tail -n1  \' "
  output = subprocess.check_output("ssh " + server_name +  cmd, shell=True)
  output1 = output.split() 
  return output1[1], output1[2], output1[3]
 
if __name__ == "__main__":
  process_node("beijing")

