#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist



def callback(data):
  print(data.linear)
  print("--------------")
  print(data.angular)
  print("--------------")
  
def turtle_sub():
  sub = rospy.Subscriber('/turtle1/cmd_vel', Twist, callback)
  rospy.spin()
  
if __name__ == '__main__':
  rospy.init_node('turtlesim_sub', anonymous = True)
  turtle_sub()
