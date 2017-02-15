#!/usr/bin/env python
import rospy
import math
from sensor_msgs.msg import Imu

from std_msgs.msg import Float64

em_pub = rospy.Publisher('velocity', Float64, queue_size=1)

# imu update rate in hertz
DELTA_T = 20
THRESH_X = 0.1
THRESH_Y = 0.1
VELOCITY = Float64(0)


def callback(data):
        global VELOCITY

        # calculate velocity according to delta time and vf = a*t
        # this is basically integration of acceleration and may not be accurate but worth a try
        if not (data.linear_acceleration.x <= THRESH_X and data.linear_acceleration >= 0):

            VELOCITY.data += data.linear_acceleration.x*(1.0/(20*math.pow(10,6)))


        em_pub.publish(VELOCITY)
            


        
if __name__ == '__main__':
        print("Velocity detector started")
        rospy.init_node('velocity_detector',anonymous=True)
        rospy.Subscriber('imu/data',Imu, callback)
        rospy.spin()

