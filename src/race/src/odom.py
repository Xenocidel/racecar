#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Imu
from nav_msgs.msg import Odometry

location = [0,0,0]
prev = None
odom_pub = rospy.Publisher('odom_est', Odometry, queue_size=10)

def predictor(data):
    vel = data.angular_velocity
    dx = vel[0]
    dy = vel[1]
    dz = vel[2]
    
    dt = data.header.stamp - prev
    prev = data.header.stamp

    location[0] = dx/dt
    location[1] = dy/dt
    location[2] = dz/dt

    msg = Odometry()
    msg.pose = PoseWithCovariance()
    msg.pose.pose = Pose()
    msg.pose.pose.position = Point()


if __name__=='__main__':
    rospy.init_node('odom', anonymous=True)
    rospy.Subscriber('/imu', Imu, predictor)
    rospy.spin()
