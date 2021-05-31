import numpy as np 
import json, os

root_dir = '../HMDB51_labels'
save_dir = '../train_test_split'
if not os.path.isdir(save_dir):
    os.mkdir(save_dir)

# get all 51 filenames:
for i, (_, _, f) in enumerate(os.walk(root_dir)):
    # print(i, f, len(f))
    pass
filenames = f
assert len(filenames) is 51

def valid_label(s,e):
    '''
    Judge whether the labeling is valid.
    Args:
        s: list of ints. list of starting frame idx.
        e: list of ints. list of ending frame idx.
    Return:
        valid: bool. If truth, the labeling is valid.
    Valid labeling should satisfy two conditions:
    1. e_i > s_i
    2. [e_i, s_i] \intersection [e_j, s_j] = \empty_set
    '''
    assert len(s) == len(e)
    n = len(s)
    for i in range(n):
        if not e[i] >= s[i]: # check first condition
            return False
        for j in range(n):
            if j == i:
                continue
            if s[i] >= s[j] and s[i] <= e[j]: # check second condition
                return False
    return True

# loop through each of the 51 json files:
total_vdo_num = 0
for filename in filenames:  # each filename corresponds to an action
    json_file = open(os.path.join(root_dir, filename))
    data = json.load(json_file) # dictionary, each element coresponds to a video.
    print('data:', type(data), len(data))
    # loop through each video of a certain action:
    for vdo_name in data: # each vdo_name corresponds to a video
        vdo_label_dict = data[vdo_name] # get an element from the dictionary. All labels for a video.
        # loop through each attribute:
        for attribute in ['skin_color', 'relationship', 'face', 'nudity', 'gender']:
            label_list = vdo_label_dict[attribute]
            n = len(label_list)
            if n == 1:
                continue
            s, e = [None]*n, [None]*n
            for i in range(len(label_list)):
                s[i], e[i], _ = label_list[i] # s: start frame idx, e: end frame idx, v: value
            if not valid_label(s,e):
                print("bad label in action %s, video %s, attribute %s\n" %
                     (filename, vdo_name, attribute))
                print(vdo_label_dict)
        
    total_vdo_num += len(data)

print('total num:', total_vdo_num)