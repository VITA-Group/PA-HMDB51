#!/usr/bin/env python
# coding: utf-8

# In[9]:


'''
All labeled videos in PA-HMDB51 are used as testing set.
The rest videos in HMDB51 are used as training set.
This script gets the file names of PA_HMDB51 dataset.
'''

import numpy as np 
import matplotlib.pyplot as plt
import json, os, csv

attribute_list = ['skin_color', 'relationship', 'face', 'nudity', 'gender']
attribute_value_dict = {
    'skin_color': ['Unidentifiable', 'White', 'Brown/Yellow', 'Black', 'Coexisting'],
    'relationship': ['Unidentifiable', 'Identifiable'],
    'face': ['Invisible', 'Partial', 'Complete'], 
    'nudity': ['No-nudity', 'Partial-nudity' ,'Semi-nudity'],
    'gender': ['Unidentifiable', 'Male', 'Female', 'Coexisting']
    }


def calculate_statistics():
    root_dir = './HMDB_labels_multilabel'

    # get all 51 filenames:

    filenames = os.listdir(root_dir)
    assert len(filenames) is 51
    print(filenames)
    
    action_list = []
    action_number = []
    for fname in filenames:
        data =  json.load(open(os.path.join(root_dir, fname)))
        action_list.append(fname.split('.')[0].replace('_', ' '))
        action_number.append(len(data))
    indexes = list(range(len(action_number)))
    indexes.sort(key=action_number.__getitem__)
    sorted_action_list = list(map(action_list.__getitem__, indexes))
    sorted_action_number = list(map(action_number.__getitem__, indexes))
    sorted_filenames = list(map(filenames.__getitem__, indexes))
    assert len(action_list) is 51
    #  write csv files:
    w = csv.writer(open("act_vid_dist.csv", "w", newline=''))
    w.writerow(sorted_action_list)
    w.writerow(sorted_action_number)
    
    
    # loop through each of the 51 json files:
    total_vid_num = 0
    attr_value_num = {
        'skin_color': [0] * 7, 'relationship': [0] * 2, 'face': [0] * 3, 'nudity': [0] * 3, 'gender': [0] * 4}
    attr_act_corl_mat = {
        'skin_color': np.zeros((7,51)).tolist(), 'relationship': np.zeros((2,51)).tolist(), 
        'face': np.zeros((3,51)).tolist(), 'nudity': np.zeros((3,51)).tolist(), 'gender': np.zeros((4,51)).tolist()
        }
    for action_id, fname in enumerate(sorted_filenames):  # each filename corresponds to an action
        f = open(os.path.join(root_dir, fname))
        data = json.load(f) # dictionary, each element coresponds to a video.
        print('data:', type(data), len(data))
        # loop through each video of a certain action:
        for vid_name in data: # each vid_name corresponds to a video
            vid_label_dict = data[vid_name] # get an element from the dictionary. All labels for a video.
            # loop through each attribute:
            for attribute in attribute_list:
                label_list = vid_label_dict[attribute]
                for label in label_list:
                    s, e, v = label # s: start frame idx, e: end frame idx, v: value
                    if isinstance(v, list): # multiple labels in the same frame, e.g., both male and female
                        if attribute == 'gender':
                            _v = np.sum(v)
                        elif attribute == 'skin_color':
                            _v = np.sum(v) + 1
                        else:
                            raise Exception('%s cannot be %s' % (attribute, v))
                        print(attribute, v, _v)
                        attr_value_num[attribute][_v] += e-s+1
                        attr_act_corl_mat[attribute][_v][action_id] += e-s+1
                    else:
                        attr_value_num[attribute][v] += e-s+1
                        attr_act_corl_mat[attribute][v][action_id] += e-s+1
        print("%s data:" % fname, len(data), type(data))
        total_vid_num += len(data)

    # write stat to json:
    f = open("attr_value_num.json","w")
    f.write(json.dumps(attr_value_num, sort_keys=True))
    f.close()

    # write stat to json:
    f = open("attr_act_corl_mat.json","w")
    f.write(json.dumps(attr_act_corl_mat, sort_keys=True))
    f.close()

    print('total num:', total_vid_num)

if __name__ == '__main__':
    calculate_statistics()

