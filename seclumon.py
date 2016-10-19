import os,sys,subprocess 
import time

def check_nproc(server_name):
  t0 = time.time()
  nproc = subprocess.check_output("ssh " + server_name +  " \'nproc\'", shell=True)
  t1 = time.time()
  response_time = t1-t0

  return nproc.rstrip(), response_time


def check_running_processes(server_name):
  cmd = " \' ps -e -o uname,pcpu,etime --sort=-pcpu,-etime | head -n 11 | tail -n 10  \' "
  output = subprocess.check_output("ssh " + server_name +  cmd, shell=True)
  output1 = output.split('\n')
  
  cmd = " \' ps -e -o cmd --sort=-pcpu,-etime | head -n 11 | tail -n 10  \' "
  output_cmd = subprocess.check_output("ssh " + server_name +  cmd, shell=True)
  output1_cmd = output_cmd.split('\n')
  
  process_info = []
  for i in range(0,10):
    output2 = output1[i].split()
    # output2 looks like this ['dli', '4345', '1-01:44:42']

    # ignore process using less than 0.8 CPU
    if (float(output2[1])< 80):
      break
    output2[1] = output2[1][:-2]
    output2.append(output1_cmd[i])
    process_info.append(output2)
  return process_info



def check_memory(server_name):
  cmd = " \'free -g | head -n2 | tail -n1  \' "
  output = subprocess.check_output("ssh " + server_name +  cmd, shell=True)
  output1 = output.split() 
  return output1[1], output1[2], output1[3]
 
if __name__ == "__main__":
  server_name = "noether.cs.columbia.edu"
  cmd = " \' ps -e -o uname,pcpu,etime --sort=-pcpu,-etime | head -n 11 | tail -n 10  \' "
  output = subprocess.check_output("ssh " + server_name +  cmd, shell=True)
  output1 = output.split('\n')
