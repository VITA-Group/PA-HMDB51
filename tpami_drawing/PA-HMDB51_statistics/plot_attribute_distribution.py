'''
All labeled videos in PA-HMDB51 are used as testing set.
The rest videos in HMDB51 are used as training set.
This script gets the file names of PA_HMDB51 dataset.
'''

import numpy as np
import matplotlib.pyplot as plt
plt.style.use([ '/Users/wuzhenyu/.matplotlib/stylelib/science.mplstyle' ,
               '/Users/wuzhenyu/.matplotlib/stylelib/ieee.mplstyle'])

import json, os, csv


from calculate_statistics import attribute_list, attribute_value_dict

attribute_N = len(attribute_list)


f = open(os.path.join("attribute_value_num.json"))
attribute_value_num = json.load(f)
# construct attribute_value_num_mat:
attribute_value_num_mat = np.zeros((5,4)) # all initialized as 0.
for i in range(5):
    each_attribute_value_num = attribute_value_num[attribute_list[i]]
    print(each_attribute_value_num, np.sum(each_attribute_value_num))
    attribute_value_num_mat[i,0:len(each_attribute_value_num)] = each_attribute_value_num
print('attribute_value_num_mat:\n', attribute_value_num_mat)


category_names = ['0', '1', '2', '3']

results = {
    'skin color': list(attribute_value_num_mat[0]),
    'relationship': list(attribute_value_num_mat[1]),
    'face': list(attribute_value_num_mat[2]),
    'nudity': list(attribute_value_num_mat[3]),
    'gender': list(attribute_value_num_mat[4])
}

labels = list(results.keys())
data = np.array(list(results.values()))
data_cum = data.cumsum(axis=1)

category_colors = ['r', 'g', 'b', 'k']
fig, ax = plt.subplots(figsize=(10, 5))
ax.invert_yaxis()
ax.xaxis.set_visible(False)
ax.set_xlim(0, np.sum(data, axis=1).max())

for i, (colname, color) in enumerate(zip(category_names, category_colors)):
    widths = data[:, i]
    starts = data_cum[:, i] - widths
    ax.barh(labels, widths, left=starts, height=0.5,
            label=colname, color=color, edgecolor='k')
    xcenters = starts + widths / 2

    for y, (x, c) in enumerate(zip(xcenters, widths)):
        ax.text(x, y, str(int(c)), ha='center', va='center',
                color=color)
ax.legend(ncol=len(category_names), bbox_to_anchor=(0.5, 1),
          loc='lower center', fontsize='xx-large')
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.show()
# plt.ylabel('Privacy Attribute', fontdict=font)
# plt.xlabel('Number of Frames', fontdict=font)
# plt.legend(prop={'size': fontsize_legend}, ncol=4, loc='upper center', framealpha=0.9)
#plt.gcf().subplots_adjust(left=0.12, right=0.96, top=0.98, bottom=0.08)
plt.savefig('attributes_distribution.pdf')
