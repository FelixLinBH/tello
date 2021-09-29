#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist

# def draw_star(size, color):
#     angle = 120
#     turtle.fillcolor(color)
#     turtle.begin_fill()

#     for side in range(5):
#         turtle.forward(size)
#         turtle.right(angle)
#         turtle.forward(size)
#         turtle.right(72 - angle)
#     turtle.end_fill()
#     return

# # draw_star(100, "purple")

def turtle_pub():
  rate = rospy.Rate(10)
  pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size = 10)
  while not rospy.is_shutdown():
    for side in range(6):
      msg = Twist()
      msg.linear.x = 10
      rospy.loginfo(msg)
      pub.publish(msg)
      rate.sleep(3)

      msg = Twist()
      msg.angular.z = 60
      rospy.loginfo(msg)
      pub.publish(msg)
      rate.sleep(3)

    # msg = Twist()
    # msg.linear.x = 10
    # rospy.loginfo(msg)
    # pub.publish(msg)
    # rate.sleep()

    # msg = Twist()
    # msg.angular.z = 60
    # rospy.loginfo(msg)
    # pub.publish(msg)
    # rate.sleep()
  
if __name__ == '__main__':
  rospy.init_node('turtlesim_pub', anonymous = True)
  try:
    turtle_pub()
  except rospy.ROSInterruptException:
    pass