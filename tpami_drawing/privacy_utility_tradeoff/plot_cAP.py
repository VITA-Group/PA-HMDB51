import numpy as np 
import matplotlib.pyplot as plt

def plot_cAP():
    pa_list = ['gender', 'face', 'nudity', 'skin color', 'relationship']

    ind = np.arange(1, 1+len(pa_list))  # the x locations for the groups
    width = 0.1  # the width of the bars

    original = [97.51, 86.96, 65.83, 97.93, 27.26]
    naive_downsampling_4 = [97.64, 86.60, 58.21, 98.06, 25.73]

    ours_r_M1 = [97.84, 80.34, 53.77, 97.48, 22.62]
    ours_r_M4 = [97.77, 81.96, 52.41, 97.80, 28.07]

    ours_M1 = [98.47, 81.09, 52.72, 97.05, 21.31]
    ours_M4 = [97.87, 81.65, 54.36, 97.47, 23.17]


    ax = plt.subplot(1,1,1)
    # plt.bar(ind - 2.5*width, original, width*0.8, color='r', label='Original')
    # plt.bar(ind - 1.5*width, naive_downsampling_4, width*0.8, color='tomato', label=r'Naive Downsample $4\times$')
    # plt.bar(ind - 0.5*width, ours_M1, width*0.8, color='g', label='Ours-Entropy(no restarting, M=1)')
    # plt.bar(ind + 0.5*width, ours_M4, width*0.8, color='lightgreen', label='Ours-Entropy(no restarting, M=4)')
    # plt.bar(ind + 1.5*width, ours_r_M1, width*0.8, color='b', label='Ours-Entropy(restarting, M=1)')
    # plt.bar(ind + 2.5*width, ours_r_M4, width*0.8, color='lightblue', label='Ours-Entropy(restarting, M=4)')
    width = 0.3
    plt.bar(ind - 0.5*width, original, width*0.8, color='r', label='Original')
    plt.bar(ind + 0.5*width, ours_M1, width*0.8, color='g', label='Ours-Entropy(no restarting, M=1)')

    text_size = 52
    # legend:
    ax.legend(prop={'size': text_size})

    # set xticks:
    ax.set_xticklabels(['temp'] + pa_list)
    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=0, ha="center", rotation_mode="anchor")

    # plt.tick_params(labelsize=fontsize)
    plt.xticks(fontsize=text_size, weight='medium')
    plt.yticks(fontsize=text_size, weight='medium')
    plt.xlabel('Privacy Attributes', fontsize=text_size, weight='semibold')
    plt.ylabel('cMAP', fontsize=text_size, weight='semibold')
    # plt.tight_layout()
    plt.gcf().subplots_adjust(bottom=0.08, top=0.98, left=0.08, right=0.98)
    plt.show()

if __name__ == '__main__':
    plot_cAP()