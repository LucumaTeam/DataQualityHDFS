#!/usr/bin/env python
import subprocess
from os import listdir
from os.path import isfile, join
import time

def run_cmd(args_list):
    """
    run linux commands
    """
    # import subprocess
    print('Running system command: {0}'.format(' '.join(args_list)))
    proc = subprocess.Popen(args_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    s_output, s_err = proc.communicate()
    s_return =  proc.returncode
    return s_return, s_output, s_err 

path_input = '/input/tv-audience/'
path_ouput_hdfs = '/tfm/tv-audience/landing/tv_audience/'

onlyfiles = [f for f in listdir(path_input) if isfile(join(path_input, f))]

path_input_final = path_input + '/' + onlyfiles[0]
path_ouput_hdfs_final = path_ouput_hdfs + '/time='+ str(time.time()).split('.')[0]+'/'

(ret, out, err)= run_cmd(['hdfs', 'dfs', '-mkdir', path_ouput_hdfs_final])
(ret, out, err)= run_cmd(['hdfs', 'dfs', '-put', path_input_final, path_ouput_hdfs_final])

