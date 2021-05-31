import numpy as np 
from skimage.io import imsave
from skvideo.io import vread
import os

root_dir = 'HMDB51'
video_name = 'Perfect_Pull_Up_-_How_To_Do_Pull_Ups_pullup_u_cm_np1_fr_goo_2.avi'
path = os.path.join(root_dir, 'pullup', video_name)
video = vread(path)
print('video:', video.shape)

image = video[-1,:,:,:]
print('image:', image.shape)
imsave('frame.bmp', image)