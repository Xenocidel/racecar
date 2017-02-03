#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Imu 

pub = rospy.Publisher('imu/data', Imu, queue_size=1)

def fix(data):
    data.linear_acceleration.x -= 1.3
    data.linear_acceleration.z -= 8.6
    pub.publish(data)

if __name__ == '__main__':
    print("Doing stuff to Imu")
    rospy.init_node('imu_fixer', anonymous=True)
    rospy.Subscriber("imu", Imu, fix)
    rospy.spin()
