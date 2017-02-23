#!/usr/bin/env python

import rospy
from std_msgs.msg import Bool
from race.msg import drive_param
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Int32
'''Need rospy and message types for eStop (bool), drive_parameters (drive_param), scan (LaserScan)'''

from math import radians, degrees, pi #for conversions
from numpy import isnan 


#Global parameters
'''Drive parameters'''
velocity = 0
angle = 0

'''Publisher'''
#em_pub = rospy.Publisher('eStop', Bool, queue_size=10)
v_pub  = rospy.Publisher('drive_velocity', Int32, queue_size=1)
activated = False


'''Update saved drive parameters'''
def save_drive(drive_data):
    global velocity,angle
    velocity = drive_data.velocity
    angle = drive_data.angle

'''
Check for immediate obstacles that we are not avoiding
If the data points around our headed trajectory seem close,
pull emergency stop, which can be reset in kill switch
'''
def safety_checker(laser_data):
    global em_pub, activated
    v_msg = Int32(-70)
    if not activated and detect_collision(laser_data):
        v_pub.publish(v_msg) 
        activated = True

        
        
        for x in range(10):
            v_msg.data -= 10
            v_pub.publish(v_msg)
        
        #em_pub.publish(True)
        print("Emergency STOP!!!!!")

'''
Input:  data: Lidar scan data
        theta_start: Min angle data to give (RADIANS)
        theta_end: Max angle data to give (RADIANS)
OUTPUT: distance of scan at angle theta
'''
def getSomeScans(data,theta_start,theta_end):
    if (theta_start > theta_end):
        return None
    theta_0 = data.angle_min
    theta_delta = data.angle_increment
    
    start = int((theta_start-theta_0)/theta_delta)
    end = int((theta_end-theta_0)/theta_delta)

    subset = data.ranges[start:end]
    MIN = data.range_min
    return [x for x in subset if (~isnan(x) and x>MIN)] #discards garbage


# 12 --> 1
# 30 --> 2
# 45 --> 5.5
### 5.5 is good enough but 6 for extra safety

FRONT_BUMPER_THRESHOLD = 3.0 

'''Check points around headed angle, and also right in front'''
def detect_collision(laser_data):
    global velocity,angle,FRONT_BUMPER_THRESHOLD
    theta_d = radians(angle/2) #approximately??

    left_theta = -pi/64
    right_theta = pi/64

    #Check scans in immediate front
    distances = getSomeScans(laser_data,left_theta,right_theta)
    if min(distances)<FRONT_BUMPER_THRESHOLD:
        if (abs(theta_d) < pi/4): # going to hit in front and not turned away from wall 
                    return True
    '''
    #Check scans in trajectory
    distances = getSomeScans(laser_data,theta_d+left_theta,theta_d+right_theta)
    if min(distances)<FRONT_BUMPER_THRESHOLD:
        return True '''

    return False

def set_threshold(data):
    global FRONT_BUMPER_THRESHOLD
    FRONT_BUMPER_THRESHOLD = (.5 if data.data else 1.5)

if __name__=='__main__':
    rospy.init_node('wall_detector', anonymous=True)

    #drive_sub = rospy.Subscriber('drive_parameters', drive_param, save_drive)
    laser_sub = rospy.Subscriber('scan', LaserScan, safety_checker)
    #turn_sub = rospy.Subscriber('is_turning', Bool, set_threshold)
    rospy.spin()

