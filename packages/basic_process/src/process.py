#!/usr/bin/env python3

# 1.Extract the timestamp from the message
# 2.Extract the image data from the message
# 3.Draw the timestamp on top of the image
# 4.Write the new image to the new bag file, with the same topic name, 
# same timestamp, and the same message type as the original message

from cv_bridge import CvBridge
import os 
import numpy as np
import cv2
import rosbag 
import datetime
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--bag_read', type=str, default="/home/amod20-rh3-ex-record-JuntingChen.bag")
    parser.add_argument('--bag_write', type=str, default="/home/amod20-rh3-ex-process-JuntingChen.bag")
    parser.add_argument('--img_topic', type=str, default="/duckiechan/camera_node/image/compressed")
    args = parser.parse_args()
    return args

args = parse_args()

bridge = CvBridge()


bag_read = rosbag.Bag(args.bag_read)
bag_write = rosbag.Bag(args.bag_write, 'w')

for topic, msg, t in bag_read.read_messages():

    if topic == args.img_topic:
        
        img_msg = msg
        cv2_img = bridge.compressed_imgmsg_to_cv2(img_msg, desired_encoding='passthrough')

        height, width, channels = cv2_img.shape
        date_time = datetime.datetime.fromtimestamp(t.to_sec()).strftime("%m/%d/%Y, %H:%M:%S")
        cv2.putText(cv2_img, date_time, (100, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)

        img_msg = bridge.cv2_to_compressed_imgmsg(cv2_img)

        bag_write.write(topic, img_msg, t)
    else: # write original data to bag_write

        bag_write.write(topic, msg, t)

bag_read.close()
bag_write.close()