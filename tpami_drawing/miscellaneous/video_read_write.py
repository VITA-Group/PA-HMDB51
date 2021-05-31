#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import cv2
framearray = []
filename = "TwoPushUp.mp4"
cap = cv2.VideoCapture(filename)
nframe = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print(nframe)
for i in range(nframe):
    cap.set(cv2.CAP_PROP_POS_FRAMES, i)
    ret, frame = cap.read()
    if frame is None:
        continue
    h, w, c = frame.shape
    print(h, w, c)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    framearray.append(frame)
cap.release()


# In[ ]:


import os
save_dir = 'TwoPushUp'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
for i in range(len(framearray)):
    cv2.imwrite(os.path.join(save_dir, '{}.jpg'.format(i)), cv2.cvtColor(framearray[i], cv2.COLOR_RGB2BGR))
    


# In[ ]:


import re
def sorted_nicely( l ):
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key = alphanum_key)


# In[ ]:


w, h = 1280, 720
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Be sure to use lower case
output = "{}.avi".format('TwoPushUp')
out = cv2.VideoWriter(output, fourcc, 20.0, (w, h), True)
read_dir = 'TwoPushUp'
imgs = sorted_nicely(os.listdir(read_dir))
print(imgs)


# In[ ]:


for img in imgs:
    frame= cv2.imread(os.path.join(read_dir, img))
    print(frame.shape)
    out.write(frame)
out.release()
cv2.destroyAllWindows()

