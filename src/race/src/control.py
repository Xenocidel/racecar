#!/usr/bin/env python
import Tkinter as tk
import rospy
from race.msg import drive_param
from race.msg import pid_input
from std_msgs.msg import Int32

SIDE = -1
kp = 14.0
kd = 0.09
servo_offset = 18.5
prev_error = 0.0 
vel_input = 12.0
C = 10
pub = rospy.Publisher('drive_parameters', drive_param, queue_size=1)
#publish = rospy.Publisher('side', Int32, queue_size=1)
def control(data):
    global prev_error
    global vel_input
    global kp
    global kd
    global SIDE

    ## Your code goes here
    # 1. Scale the error
    # 2. Apply the PID equation on error
    # 3. Make sure the error is within bounds
    

    ## END
    curr_error = data.pid_error
    vel = data.pid_vel
    diff_error = (curr_error - prev_error) 
    prev_error = curr_error

    

    angle = SIDE * C * (kp*curr_error + kd*diff_error) 


    if angle > 90: 
            angle = 90
    elif angle < -90: 
            angle = -90

    msg = drive_param();
    msg.velocity = vel_input    
    msg.angle = -angle
    pub.publish(msg)

def updateSide(data):
        global SIDE
        SIDE = data.data


if __name__ == '__main__':
    global kp
    global kd
    global vel_input
    print("Listening to error for PID")
    kp = 14
    kd = 0.9
    vel_input = 12.0
    
    #kp = input("Enter Kp Value: ")
    #kd = input("Enter Kd Value: ")
    #vel_input = input("Enter Velocity: ")
    rospy.init_node('pid_controller', anonymous=True)
    #msg = Int32()
    #msg.data = SIDE
    #publish.publish(msg)
    rospy.Subscriber('side',Int32, updateSide)
    rospy.Subscriber("error", pid_input, control)
    rospy.spin()
