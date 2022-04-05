import os
import sys
import subprocess
import numpy as np
import random
import pickle
import json
import time
timestr = time.strftime("%Y%m%d-%H%M%S")


#CONSTANTS FOR SAMPLING 
t_max_min = 30
t_max_max =150
clips_min_min = 0.3
clips_min_max =0.6
clips_diff_min = 0.3
clips_diff_max =0.5
room_scale_min_min=0
room_scale_min_max=30
room_scale_diff_min=30
room_scale_diff_max= 100
pitch_shift_min = 150
pitch_shift_max = 450
rejection_min = 3
def prob_func():
    return random.random()

def create_params_sample(outdir, outname="possible_dict"):
    params_dict = {}
    effects_probs={}
    
    effects_names =["bandreject", "pitch", "reverb", "time_drop", "clip"] 
    sum_test =True
    while sum_test : 
        for name in effects_names:
            effects_probs[name]=prob_func()
        considered_sum  = sum([effects_probs[x] for x in  effects_names])
        sum_test = considered_sum < rejection_min
        if sum_test :
            print("rejecting this sampling")
        else : 
            print("sampling considered")
            print(effects_probs)
    
    params_dict["effects_probs"]=effects_probs
    params_dict["band_scaler"]= np.random.uniform
    params_dict["pitch_shift_max"]=np.random.uniform(pitch_shift_min,
                                                     pitch_shift_max)
    params_dict["pitch_quick_prob"] = random.random()
    params_dict["clip_min"] = np.random.uniform(clips_min_min, clips_min_max)
    params_dict["clip_max"]= min(params_dict["clip_min"] +
                                 np.random.uniform(clips_diff_min,
                                                   clips_diff_max),1)
    params_dict["t_ms"] = np.random.uniform(t_max_min, t_max_max)
    params_dict["room_scale_min"]= np.random.uniform(room_scale_min_min,
                                                room_scale_min_max)
    params_dict["band_scaler"]= random.random()
    params_dict["room_scale_max"] = min(params_dict["room_scale_min"] +
                                   np.random.uniform(room_scale_diff_min,
                                                     room_scale_diff_max),100)
    params_dict["reverberance_min"]=50
    params_dict["reverberance_max"]=50
    params_dict["damping_min"]=50
    params_dict["damping_max"]=50
    if outname != "possible_dict" : 
        nameout = os.path.join(outdir, outname)
        with open(os.path.join(outdir, outname), 'w') as json_file:
            json.dump(params_dict, json_file)
    else : 
        randomint = "_"+str(np.random.randint(1500))
        nameout=os.path.join(outdir, outname+"_"+timestr+randomint+".json")
        with open(nameout, 'w') as json_file:
            json.dump(params_dict, json_file)
    return nameout

outdir = sys.argv[1]

number_of_params=10
number_of_runs_per_param= 10
params_dirs= []
params_files = []
for i in range(number_of_params):
    param_name = "exp_param"+str(i)
    if not os.path.exists(os.path.join(outdir, param_name)):
        os.makedirs(os.path.join(outdir,param_name))
    param_out = os.path.join(outdir,param_name)
    params_dirs.append(param_out)
    param_file = create_params_sample(param_out)
    params_files.append(param_file)
names = [str(x) for x in range(number_of_runs_per_param)]
#create params_files 


for ind in range(number_of_params):
    aug_file=params_files[ind]
    params_out= params_dirs[ind]
    for name in names : 
        bashCmd=["bash","file_pipeline_voxforge.sh",os.path.join(params_out,name), aug_file ]
        process = subprocess.Popen(bashCmd, stdout=subprocess.PIPE)
        output, error = process.communicate()
        print(output)
