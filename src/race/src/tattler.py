#!/usr/bin/env python

import rospy
import math
from sensor_msgs.msg import LaserScan
from race.msg import pid_input


def callback(data):
   print data.ranges[1080/4]#a
   return


if __name__ == '__main__':
    print("Tattler node started")
    rospy.init_node('tattler',anonymous = True)
    rospy.Subscriber("scan",LaserScan,callback)
    rospy.spin()
