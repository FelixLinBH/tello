#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from std_srvs.srv import Empty as EmptySrv

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
  
def turtle_callSer():
  rospy.wait_for_service('/reset')
  try:
    call1 = rospy.ServiceProxy('/reset', EmptySrv)
    resp1 = call1()
    return resp1
  except rospy.ServiceException, e:
    print "Service call failed: %s" % e
  
  rospy.spin()
  
if __name__ == '__main__':
  rospy.init_node('turtlesim_ser4reset', anonymous = True)
  turtle_callSer()





