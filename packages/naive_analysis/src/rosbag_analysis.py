#!/usr/bin/env python3

import rosbag
import os 
import numpy as np

if 'ROSBAG_NAME' in os.environ:
    ROSBAG_NAME = os.environ['ROSBAG_NAME']
else:
    # ROSBAG_NAME = "example_rosbag_H3.bag"
    ROSBAG_NAME = "/home/example_rosbag_H3.bag"

bag = rosbag.Bag(ROSBAG_NAME)
topics = []
t_arr = []
for topic, _, t in bag.read_messages():
    topics.append(topic)
    t_arr.append(t.to_sec())

topics = np.array(topics)
t_arr = np.array(t_arr)
u_topics = np.unique(topics)

for topic in u_topics:
    
    topic_t = np.sort(t_arr[topics == topic])
    msg_num = topic_t.shape[0]
    t_diff = np.diff(topic_t)
    
    diff_min = t_diff.min()
    diff_max = t_diff.max()
    diff_average = t_diff.mean()
    diff_median = np.median(t_diff)
    
    print('''
        {}:
        \tnum_messages: {:3d}
        \tperiod:
        \t\tmin: {:.2f}
        \t\tmax: {:.2f}
        \t\taverage: {:.2f}
        \t\tmedian: {:.2f}\n
        '''.format(
            topic,msg_num,diff_min,diff_max,diff_average,diff_median
            )
    )
bag.close()