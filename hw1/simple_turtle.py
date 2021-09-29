#!/usr/bin/env python
import rospy
import time

from geometry_msgs.msg import Twist
from turtlesim.msg import Pose, Color
from std_srvs.srv import Empty as EmptySrv
from turtlesim.srv import SetPen as SetPenSrv, TeleportAbsolute as taSrv, Kill as KillSrv, Spawn as SpawnSrv, TeleportRelative as trSrv

class TurtleState:

    def __init__(self, name):
    
        self.name = name
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        self.linear_v = 0.0
        self.angular_v = 0.0
        self.color = [0.0, 0.0, 0.0]
        
    def show(self):
      print("name: ", self.name)
      print("x: ", self.x)
      print("y: ", self.y)
      print("theta: ", self.theta)
      print("linear_velocity: ", self.linear_v)      
      print("angular_velocity: ", self.angular_v)
      print("color (R, G, B): ", self.color)
      print("====================")

class TurtleController:
    
    def __init__(self, ns):
      self.name = ns
    
    def move(self, twist, limitTime):
      limitTime = limitTime * 1000
      startTime = int(round(time.time()*1000))
      rate = rospy.Rate(10)
      # print "MOVE~~~~"
      pub_move = rospy.Publisher("/" + self.name + "/cmd_vel", Twist, queue_size = 10)

      while not rospy.is_shutdown():
        connections = pub_move.get_num_connections()
        if connections > 0:
          endTime = int(round(time.time()*1000))
          if endTime - startTime < limitTime:
            pub_move.publish(twist)

          else:
            pub_move.publish(Twist())
            break
          rate.sleep()

    def ser_clear(self):
      rospy.wait_for_service('/clear')
      try:
        call1 = rospy.ServiceProxy('/clear', EmptySrv)
        resp1 = call1()
        return resp1
      except rospy.ServiceException, e:
        print "Service call failed: %s" % e
    
    def ser_reset(self):
      rospy.wait_for_service('/reset')
      try:
        call1 = rospy.ServiceProxy('/reset', EmptySrv)
        resp1 = call1()
        return resp1
      except rospy.ServiceException, e:
        print "Service call failed: %s" % e
         
    def ser_kill(self, n):
      rospy.wait_for_service('/kill')
      try:
        call1 = rospy.ServiceProxy('/kill', KillSrv)
        resp1 = call1(name = n)
        return resp1
      except rospy.ServiceException, e:
        print "Service call failed: %s" % e
    
    def ser_spawn(self, x, y, theta, name):
      rospy.wait_for_service('/spawn')
      try:
        call1 = rospy.ServiceProxy('/spawn', SpawnSrv)
        resp1 = call1(x = x, y = y, theta = theta, name = name)
        return resp1
      except rospy.ServiceException, e:
        print "Service call failed: %s" % e

    def ser_setpen(self, r, g, b, w, o):
      rospy.wait_for_service('/' + self.name + '/set_pen')
      try:
        call1 = rospy.ServiceProxy('/' + self.name + '/set_pen', SetPenSrv)
        resp1 = call1(r = r, g = g, b = b, width = w, off = o)
        return resp1
      except rospy.ServiceException, e:
        print "Service call failed: %s" % e
     
    def ser_setabs(self, x, y, theta):
      rospy.wait_for_service('/' + self.name + '/teleport_absolute')
      try:
        call1 = rospy.ServiceProxy('/' + self.name + '/teleport_absolute', taSrv)
        resp1 = call1(x = x, y = y, theta = theta)
        return resp1
      except rospy.ServiceException, e:
        print "Service call failed: %s" % e

    def ser_setrel(self, l, a):
      rospy.wait_for_service('/' + self.name + '/teleport_relative')
      try:
        call1 = rospy.ServiceProxy('/' + self.name + '/teleport_relative', trSrv)
        resp1 = call1(linear = l, angular = a)
        return resp1
      except rospy.ServiceException, e:
        print "Service call failed: %s" % e
    

class Turtle():
    def __init__(self, name):

        self.name = name
        self.state = TurtleState(self.name)
        self.crtl = TurtleController(self.name)
        self._sensor()

    def _sensor(self):
        _pose_sub = rospy.Subscriber("/" + self.name + "/pose", Pose, self._pose_cb, queue_size = 10)
        _color_sub = rospy.Subscriber("/" + self.name + "/color_sensor", Color, self._color_cb, queue_size = 10)

    def _pose_cb(self, msg):
      self.state.x = msg.x
      self.state.y = msg.y
      self.state.theta = msg.theta
      self.state.linear_v = msg.linear_velocity
      self.state.angular_v = msg.angular_velocity
    
    def _color_cb(self, msg):
      self.state.color = [msg.r, msg.g, msg.b]

