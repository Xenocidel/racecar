#!/usr/bin/env python

import rospy
import math
from sensor_msgs.msg import LaserScan
from race.msg import pid_input


def callback(data):
   theta = 15
   print [(i,data.ranges[i*4]) for i in range(10,20)]
   # print data.ranges[15*4 - 8 : 15*4 + 8]
   return


if __name__ == '__main__':
    print("Tattler node started")
    rospy.init_node('tattler',anonymous = True)
    rospy.Subscriber("scan",LaserScan,callback)
    rospy.spin()
