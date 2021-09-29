#!/usr/bin/env python
import rospy
import simple_turtle
from geometry_msgs.msg import Twist

def main():
  t1 = simple_turtle.Turtle("turtle1")
  t2 = simple_turtle.Turtle("turtle2")

  t1.state.show()
  t1.crtl.ser_reset()
  
  t2.state.show()
  t2.crtl.ser_reset()

  msg = Twist()
  msg.linear.x = 2.0
  msg.angular.z = 2.4
  t1.crtl.move(msg, 1.0)
  t1.state.show()  

  msg = Twist()
  msg.linear.x = 2.0
  msg.angular.z = -2.4
  t2.crtl.move(msg, 1.0)
  t2.state.show()  
  
  t1.crtl.ser_setpen(255, 0, 0, 5, 0)
  t2.crtl.ser_setpen(0, 128, 128, 5, 0)


  # msg = Twist()
  # msg.linear.x = 2.0
  # msg.angular.z = 2.4
  # t1.crtl.move(msg, 1.0)
  
  # t1.state.show()
  
  # t1.crtl.ser_clear()
  # t1.crtl.ser_setpen(0, 255, 0, 5, 0)
  
  # msg = Twist()
  # msg.linear.x = 2.0
  # msg.angular.z = -2.4
  # t1.crtl.move(msg, 1.0)
  
  # t1.state.show()
 
  # t1.crtl.ser_setabs(6, 4, -30)
  # t1.state.show() 

  # t1.crtl.ser_setrel(-2, -6)
  # t1.state.show() 
  
  # t1.crtl.ser_reset()
  # t1.state.show()
  
  # t1.crtl.ser_spawn(6, 4, -30, "turtle2")

  
  # msg = Twist()
  # msg.linear.x = 2.0
  # msg.angular.z = -1.8
  # t2.crtl.move(msg, 1.0)
  
  # t2.state.show()  
  
  # t2.crtl.ser_setpen(0, 128, 128, 5, 0)

  # msg = Twist()
  # msg.linear.x = 2.0
  # msg.angular.z = 2.4
  # t2.crtl.move(msg, 1.0)
  
  # t2.state.show()
  
  # t2.crtl.ser_clear()
  # t2.crtl.ser_setpen(128, 128, 0, 5, 0)
  
  # msg = Twist()
  # msg.linear.x = 2.0
  # msg.angular.z = -2.4
  # t2.crtl.move(msg, 1.0)
  
  # t2.state.show()
  
if __name__ == "__main__":
  rospy.init_node("run_turtle", anonymous=True)
  main()
