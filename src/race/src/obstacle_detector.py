#!/usr/bin/env python

import rospy
from std_msgs.msg import Bool
from race.msg import drive_param
from sensor_msgs.msg import LaserScan
'''Need rospy and message types for eStop (bool), drive_parameters (drive_param), scan (LaserScan)'''

from math import radians, degrees, pi #for conversions
from np import isnan 


#Global parameters
'''Drive parameters'''
velocity = 0
angle = 0

'''Publisher'''
em_pub = rospy.Publisher('eStop', Bool, queue_size=10)


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
def sanity_checker(laser_data):
	global em_pub
	if detect_collision(laser_data):
		em_pub.publish(True)
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
	return [x for x in subset if (~isnan(x) && x>MIN)] #discards garbage

FRONT_BUMPER_THRESHOLD = .25

'''Check points around headed angle, and also right in front'''
def detect_collision(laser_data):
	global velocity,angle,FRONT_BUMPER_THRESHOLD
	theta_d = radians(angle/2) #approximately??

	left_theta = -pi/3
	right_theta = pi/3

	#Check scans in immediate front
	distances = getSomeScans(left_theta,right_theta)
	if min(distances)<FRONT_BUMPER_THRESHOLD:
		return True

	#Check scans in trajectory
	distances = getSomeScans(theta_d+left_theta,theta_d+right_theta)
	if min(distances)<FRONT_BUMPER_THRESHOLD:
		return True

	return False

if __name__=='__main__':
	rospy.init_node('wall_detector', anonymous=True)
	drive_sub = rospy.Publisher('drive_parameters', drive_param, save_drive)
	laser_sub = rospy.Publisher('scan', LaserScan, sanity_checker)
