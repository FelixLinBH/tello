#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from std_srvs.srv import Empty as EmptySrv
from turtlesim.srv import SetPen as SetPenSrv 
  
def turtle_callSer():
  rospy.wait_for_service('/turtle1/set_pen')
  try:
    call1 = rospy.ServiceProxy('/turtle1/set_pen', SetPenSrv)
    resp1 = call1(r = 255, width = 10, off = 0)
    return resp1
  except rospy.ServiceException, e:
    print "Service call failed: %s" % e
  
  rospy.spin()
  
if __name__ == '__main__':
  rospy.init_node('turtlesim_ser4setpen', anonymous = True)
  turtle_callSer()





