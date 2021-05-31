'''
All labeled videos in PA-HMDB51 are used as testing set.
The rest videos in HMDB51 are used as training set.
This script gets the file names of PA_HMDB51 dataset.
'''

import numpy as np 
import json, os

root_dir = '../HMDB51_labels'
save_dir = 'train_test_split'
if not os.path.isdir(save_dir):
    os.mkdir(save_dir)

# get all 51 filenames:
for i, (_, _, f) in enumerate(os.walk(root_dir)):
    # print(i, f, len(f))
    pass
filenames = f
assert len(filenames) is 51

# loop through each of the 51 json files:
total_num = 0
for i, filename in enumerate(filenames):  # each filename corresponds to an action
    json_file = open(os.path.join(root_dir, filename))
    data = json.load(json_file)
    # loop through each video:
    output_file = open(os.path.join(save_dir, filename.split(".")[0]+".txt"), 'a+')
    for j, video_name in enumerate(data): # each video_name corresponds to a video
        # print(video_name)
        # print(data[video_name])
        output_file.write(video_name)
        output_file.write('\n')
    print("data:", len(data), type(data))
    total_num += len(data)

print('total num:', total_num)