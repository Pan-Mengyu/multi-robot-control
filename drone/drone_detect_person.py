#!/usr/bin/env python

import math
from numpy.core.numeric import NaN
import cv_bridge
import numpy as np
import cv2
import rospy
from sensor_msgs.msg import Image
from geometry_msgs.msg import Point
from nav_msgs.msg import Odometry


rospy.init_node('detect_person')

def euler_from_quaternion(x, y, z, w):
    """
    Convert a quaternion into euler angles (roll, pitch, yaw)
    roll is rotation around x in radians (counterclockwise)
    pitch is rotation around y in radians (counterclockwise)
    yaw is rotation around z in radians (counterclockwise)
    """
    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + y * y)
    roll_x = math.atan2(t0, t1)
    
    t2 = +2.0 * (w * y - z * x)
    pitch_y = math.asin(t2)
    
    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    yaw_z = math.atan2(t3, t4)
    
    return roll_x, pitch_y, yaw_z # in radians


class Detection:
    def __init__(self,drone_N):
        self.bridge = cv_bridge.CvBridge()
        # Define subscribers
        self.rgb_sub = rospy.Subscriber("/drone{}/camera/rgb/image_raw".format(drone_N), Image, self.rgb_callback)
        self.depth_sub = rospy.Subscriber('/drone{}/camera/depth/image_raw'.format(drone_N), Image, self.depth_callback)
        self.odom_sub=rospy.Subscriber("drone{}/ground_truth/state".format(drone_N), Odometry,self.odom_callback)
        # Define publishers
        self.pos_pub= rospy.Publisher("/person/position", Point, queue_size=1)
        self.angle=NaN
        self.depth=NaN
        self.cent_x=None
        self.cent_y=None

        

    def rgb_callback(self,image_msg):
        image = self.bridge.imgmsg_to_cv2(image_msg, "rgb8")
        human_mask_down=(0,102,0)
        human_mask_up=(3,105,3)
        mask = cv2.inRange(image, human_mask_down, human_mask_up)
        # result = cv2.bitwise_and(image, image, mask=mask)
        # cv2.imshow("detect_result", result)
        # cv2.waitKey(0)
        if sum(sum(mask))>1000:
            print("detect people")
            mass_x, mass_y = np.where(mask >0)
            self.cent_y = int(np.average(mass_x))
            self.cent_x = int(np.average(mass_y))
            image_center_x=320.5
            f=554.254691191187
            distance_x=self.cent_x-image_center_x
            self.angle=math.atan2(distance_x,f)
            self.calculate_position()

    def depth_callback(self,depth_msg):
        image = self.bridge.imgmsg_to_cv2(depth_msg,desired_encoding="passthrough")
        if self.cent_x is not None and self.cent_y is not None:
            self.depth=image[self.cent_y,self.cent_x]

    def odom_callback(self,odom_msg):
        self.x=odom_msg.pose.pose.position.x
        self.y=odom_msg.pose.pose.position.y
        ox=odom_msg.pose.pose.orientation.x
        oy=odom_msg.pose.pose.orientation.y
        oz=odom_msg.pose.pose.orientation.z
        ow=odom_msg.pose.pose.orientation.w

        _,_,self.yaw=euler_from_quaternion(ox,oy,oz,ow)
        
    
    def calculate_position(self):
        if self.angle is not NaN and self.depth is not NaN:
            people_angle=self.yaw-self.angle
            people_x=math.cos(people_angle)*self.depth+self.x
            people_y=math.sin(people_angle)*self.depth+self.y
            print("x={},y={},angle={}".format(people_x,people_y,people_angle))

if __name__=="__main__":
    drone_N=1
    d=Detection(drone_N)
    rospy.spin()

