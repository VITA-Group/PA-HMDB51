#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
print(sys.executable)


# In[2]:


#from __future__ import print_function

import os
user_paths = os.environ['PYTHONPATH'].split(os.pathsep)
print user_paths
import sys
#print(sys.path)
sys.path.extend(['/usr/local/lib/python2.7/dist-packages', '/usr/lib/python2.7/dist-packages'])
import numpy
import cv2
print os.path.dirname(cv2.__file__)
print sys.path


# In[3]:


from __future__ import division
import rosbag, rospy, numpy as np
import sys, os, cv2, glob
from itertools import izip, repeat
import argparse
print(os.path.dirname(cv2.__file__))


# In[4]:


# try to find cv_bridge:
try:
    from cv_bridge import CvBridge
except ImportError:
    # assume we are on an older ROS version, and try loading the dummy manifest
    # to see if that fixes the import error
    try:
        import roslib; roslib.load_manifest("bag2video")
        from cv_bridge import CvBridge
    except:
        print "Could not find ROS package: cv_bridge"
        print "If ROS version is pre-Groovy, try putting this package in ROS_PACKAGE_PATH"
        sys.exit(1)


# In[5]:


def get_info(bag, topic=None, start_time=rospy.Time(0), stop_time=rospy.Time(sys.maxint)):
    size = (0,0)
    times = []

    # read the first message to get the image size
    msg = bag.read_messages(topics=topic).next()[1]
    #size = (msg.width, msg.height)
    size = (640, 480)
    # now read the rest of the messages for the rates
    iterator = bag.read_messages(topics=topic, start_time=start_time, end_time=stop_time)#, raw=True)
    for _, msg, _ in iterator:
        time = msg.header.stamp
        times.append(time.to_sec())
        #size = (msg.width, msg.height)
    diffs = 1/np.diff(times)
    return np.median(diffs), min(diffs), max(diffs), size, times

def calc_n_frames(times, precision=10):
    # the smallest interval should be one frame, larger intervals more
    intervals = np.diff(times)
    return np.int64(np.round(precision*intervals/min(intervals)))

def write_frames(bag, writer, total, topic=None, nframes=repeat(1), start_time=rospy.Time(0), stop_time=rospy.Time(sys.maxint), encoding='bgr8'):
    bridge = CvBridge()
    count = 1
    iterator = bag.read_messages(topics=topic, start_time=start_time, end_time=stop_time)
    for (topic, msg, time), reps in izip(iterator, nframes):
        print '\rWriting frame %s of %s at time %s' % (count, total, time),
        #img = np.asarray(bridge.imgmsg_to_cv2(msg, 'bgr8'))
        np_arr = np.fromstring(msg.data, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        print img.shape
        for rep in range(reps):
            writer.write(img)
        count += 1


# In[10]:


if __name__ == '__main__':
#     parser = argparse.ArgumentParser(description='Extract and encode video from bag files.')
#     parser.add_argument('--outfile', '-o', action='store', default=None,
#                         help='Destination of the video file. Defaults to the location of the input file.')
#     parser.add_argument('--precision', '-p', action='store', default=10, type=int,
#                         help='Precision of variable framerate interpolation. Higher numbers\
#                         match the actual framerater better, but result in larger files and slower conversion times.')
#     parser.add_argument('--start', '-s', action='store', default=rospy.Time(0), type=rospy.Time,
#                         help='Rostime representing where to start in the bag.')
#     parser.add_argument('--end', '-e', action='store', default=rospy.Time(sys.maxint), type=rospy.Time,
#                         help='Rostime representing where to stop in the bag.')
#     parser.add_argument('--encoding', choices=('rgb8', 'bgr8', 'mono8'), default='bgr8',
#                         help='Encoding of the deserialized image.')

#     parser.add_argument('--topic', '--t', action='store', default='camera/rgb/image_color/compressed', 
#                         type=str, help='the topic for reading message')
#     parser.add_argument('--bagfile', '--b', action='store', default='/home/wuzhenyu_sjtu/IAS-Lab_Action_Dataset/01-Alessandro/1/*.bag', 
#                         type=str, help='the directory of bag files')

#     args = parser.parse_args()
    import easydict
    args = easydict.EasyDict({
        "outfile": None,
        "precision": 10,
        "start": rospy.Time(0),
        "end": rospy.Time(sys.maxint),
        "encoding": 'bgr8',
        "topic": 'camera/rgb/image_color/compressed',
        "bagfile": '/home/wuzhenyu_sjtu/IAS-Lab_Action_Dataset/*/*/*.bag'
    })
    
    for bagfile in glob.glob(args.bagfile):
        print bagfile
        outfile = args.outfile
        if not outfile:
            outfile = os.path.join(*os.path.split(bagfile)[-1].split('.')[:-1]) + '.avi'
            folder = os.path.join('/home/wuzhenyu_sjtu', '/'.join(bagfile.split('/')[-3:-1]))
            print outfile
            if not os.path.exists(folder):
                os.makedirs(folder)
            outfile = os.path.join(folder, outfile)
        bag = rosbag.Bag(bagfile, 'r')
        print 'Calculating video properties'
        rate, minrate, maxrate, size, times = get_info(bag, args.topic, start_time=args.start, stop_time=args.end)
        nframes = calc_n_frames(times, args.precision)
        # writer = cv2.VideoWriter(outfile, cv2.cv.CV_FOURCC(*'DIVX'), rate, size)
        writer = cv2.VideoWriter(outfile, cv2.VideoWriter_fourcc(*'DIVX'), np.ceil(maxrate*args.precision), size)
        print 'Writing video'
        write_frames(bag, writer, len(times), topic=args.topic, nframes=nframes, start_time=args.start, stop_time=args.end, encoding=args.encoding)
        writer.release()
        print '\n'

