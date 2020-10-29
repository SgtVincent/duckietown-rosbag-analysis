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

ROSBAG_READ = "/home/amod20-rh3-ex-record-JuntingChen.bag"
ROSBAG_WRITE = "/home/amod20-rh3-ex-record-processed.bag"
# ROSBAG_READ = "/home/chenjunting/Documents/duckie_data/amod20-rh3-ex-record-JuntingChen.bag"
# ROSBAG_WRITE = "./amod20-rh3-ex-record-processed.bag"
IMG_TOPIC = "/duckiechan/camera_node/image/compressed"

if 'ROSBAG_NAME' in os.environ:
    ROSBAG_READ = os.environ['ROSBAG_READ']
if 'ROSBAG_WRITE' in os.environ:
    ROSBAG_WRITE = os.environ['ROSBAG_WRITE']
if 'IMG_TOPIC' in os.environ:
    IMG_TOPIC = os.environ['IMG_TOPIC']


bridge = CvBridge()

bag_read = rosbag.Bag(ROSBAG_READ)
bag_write = rosbag.Bag(ROSBAG_WRITE, 'w')

for topic, msg, t in bag_read.read_messages():

    if topic == IMG_TOPIC:
        
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