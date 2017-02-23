#!/usr/bin/env python
import Tkinter as tk
import rospy
from race.msg import drive_param
from race.msg import pid_input
from std_msgs.msg import Int32
from std_msgs.msg import Bool

##IGNORE
# (kp,kd,C,SCALE_FACTOR)

# constants = {'30': (5.75,5,25,1.5), '12': (14,.09,10,1)}
##ENDIGNORE 

# (kd,SCALE_FACTOR)
constants = {'30': (12.5,1.5), '12': (.09,1), '45': (15,1.5)}

dead = False
SIDE = 1 #-1
kp = 14.0 #14.0
kd = 0.09 #15 #12.5 #0.09
servo_offset = 18.5
prev_error = 0.0 
vel_input = 12.0
C = 10 
pub = rospy.Publisher('drive_parameters', drive_param, queue_size=1)

def kill(data):
    global dead
    dead = data.data

def updateVelocity(data):
    global vel_input
    vel_input = data.data
    print "updated velocity"

def control(data):
    global prev_error
    global vel_input
    global kp
    global kd
    global SIDE
    global dead

    '''if (dead):
        msg = drive_param() 
        msg.velocity = 0
        msg.angle = 0
        pub.publish(msg)
        return''' 

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
    if (not dead):
        msg.velocity = vel_input    
        msg.angle = -angle
        pub.publish(msg)
    else:
        msg.velocity = -70
        pub.publish(msg)


        '''
        for x in range(10):
            if vel_input > -180:
                vel_input -= 10
                msg.velocity = vel_input
                pub.publish(msg)
        '''

        




def updateSide(data):
    global SIDE
    SIDE = data.data


if __name__ == '__main__':
    print("Listening to error for PID")
    rospy.init_node('pid_controller', anonymous=True)
    rospy.Subscriber('side',Int32, updateSide)
    rospy.Subscriber("error", pid_input, control)
    #rospy.Subscriber("eStop", Bool,kill) 
    rospy.Subscriber("drive_velocity", Int32, updateVelocity) 
    rospy.spin()
