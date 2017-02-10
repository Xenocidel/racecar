#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Imu 

pub = rospy.Publisher('imu/data', Imu, queue_size=1)
avg = 0
N = 0

def fix(data):
    global avg, N
    data.linear_acceleration.x -= 1.33
    data.linear_acceleration.y += 0.128
    data.linear_acceleration.z += 1.054
    pub.publish(data)
    '''
    if avg == 0: 
         avg = data.linear_acceleration.y 
         N = 1
    approxRollingAverage(data.linear_acceleration.y)
    '''

def approxRollingAverage(new_sample):
       global avg, N
       avg = avg - avg/N
       avg = avg + new_sample/N
       N = N + 1
       print(avg)


if __name__ == '__main__':
    print("Doing stuff to Imu")
    rospy.init_node('imu_fixer', anonymous=True)
    rospy.Subscriber("imu", Imu, fix)
    rospy.spin()
