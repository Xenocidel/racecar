#!/usr/bin/env python

import rospy
from std_msgs.msg import Bool
from std_msgs.msg import Int32
import curses

stdscr = curses.initscr()
curses.cbreak()
stdscr.keypad(1)
rospy.init_node('wall_switcher', anonymous=True)
em_pub = rospy.Publisher('side', Int32, queue_size=1)
k_pub = rospy.Publisher('eStop',Bool,queue_size=10)
stdscr.refresh()

msg = Int32()
msg.data = 1
em_pub.publish(msg)
k_pub.publish(False)

key = ''
while key != ord('q'):
    key = stdscr.getch()
    stdscr.refresh()
    if key == curses.KEY_LEFT:
        msg = Int32()
        msg.data = -1
        em_pub.publish(msg)
        stdscr.addstr(5, 20, "LEFT ")
    elif key == curses.KEY_RIGHT:
        msg = Int32()
        msg.data = 1
        em_pub.publish(msg)
        stdscr.addstr(5, 20, "RIGHT")

k_pub.publish(True)

curses.endwin()
