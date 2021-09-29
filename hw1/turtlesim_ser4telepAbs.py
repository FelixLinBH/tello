#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from std_srvs.srv import Empty as EmptySrv
from turtlesim.srv import SetPen as SetPenSrv 
from turtlesim.srv import TeleportAbsolute as taSrv 
  
def turtle_callSer():
  rospy.wait_for_service('/turtle1/teleport_absolute')
  try:
    call1 = rospy.ServiceProxy('/turtle1/teleport_absolute', taSrv)
    resp1 = call1(x = 15, y = 50, theta = 30)
    return resp1
  except rospy.ServiceException, e:
    print "Service call failed: %s" % e
  
  rospy.spin()
  
if __name__ == '__main__':
  rospy.init_node('turtlesim_ser4ta', anonymous = True)
  turtle_callSer()





