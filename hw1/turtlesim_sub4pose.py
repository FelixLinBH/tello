#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose


def callback(data):
  print(data.x)
  print("--------------")
  print(data.y)
  print("--------------")
  print(data.theta)
  print("--------------")
  print(data.linear_velocity)
  print(data.angular_velocity)
  print("--------------")  
  
def turtle_sub():
  sub = rospy.Subscriber('/turtle1/pose', Pose, callback)
  rospy.spin()
  
if __name__ == '__main__':
  rospy.init_node('turtlesim_sub4pose', anonymous = True)
  turtle_sub()
