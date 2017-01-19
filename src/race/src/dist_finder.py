#!/usr/bin/env python

import rospy
import math
from sensor_msgs.msg import LaserScan
from race.msg import pid_input
from math import *

# same as desired trajectory
AC = 1
#vel = 30
#vel = 12
CENTER= None

pub = rospy.Publisher('error', pid_input, queue_size=10)

##  Input:  data: Lidar scan data
##          theta: The angle at which the distance is requried
##  OUTPUT: distance of scan at angle theta
def getRange(data,theta):
# Find the index of the arary that corresponds to angle theta.
# Return the lidar scan value at that index
# Do some error checking for NaN and ubsurd values
## Your code goes here

    theta_0 = data.angle_min
    theta_delta = data.angle_increment

    idx = int((theta-theta_0)/theta_delta)

    i = 1

    for j in range(len(data.ranges)):
            # discard any values that are outside valid range
            if math.isnan(data.ranges[idx]) or data.ranges[idx] > data.range_max or data.ranges[idx] < data.range_min:
                    if (i % 2 == 0):
                            idx = idx + -i
                    else: 
                            idx = idx + i

                    i = i + 1
            else: 
                    return data.ranges[idx]

    return None

def callback(data):
    global AC, CENTER

    theta = 50;
    swing = math.radians(theta)
    a = getRange(data,-pi/2+swing)
    b = getRange(data,-pi/2)

    alpha = atan((a*cos(swing)-b)/(a*sin(swing))) 

    if (CENTER == None):
            CENTER = b*cos(alpha)

    
    ## Your code goes here
    AB = b*cos(alpha)
    CD = AB + AC*sin(alpha)
    
    error = CENTER-CD






    ## END

    msg = pid_input()
    msg.pid_error = error
    print(CENTER,AB) 
    #msg.pid_vel = vel
    pub.publish(msg)
    

if __name__ == '__main__':
    print("Laser node started")
    rospy.init_node('dist_finder',anonymous = True)
    rospy.Subscriber("scan",LaserScan,callback)
    rospy.spin()
