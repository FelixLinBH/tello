#!/usr/bin/env python
import rospy
import roslib
import tello_drone
import sys
from geometry_msgs.msg import Twist
from std_msgs.msg import Empty, UInt8
from behave import *
from time import sleep

rospy.init_node('bt_mission', anonymous=True)
sleep(2)
print("takeoff")
takeoff_pub = rospy.Publisher('/tello/takeoff', Empty, queue_size =1)
sleep(3)
msg = Empty()
takeoff_pub.publish(msg)
print("TakeOff done")
sleep(3)

class bt_mission:

    # common member
    drone = tello_drone.Drone()
    isContinue = True
    center = (480, 270)
    color = "red"
    cmd_pub = rospy.Publisher('/tello/cmd_vel', Twist, queue_size = 10)
    land_pub = rospy.Publisher('/tello/land', Empty, queue_size = 1)
    change_pub = rospy.Publisher('/selfChanged', UInt8, queue_size = 10)
    rate = rospy.Rate(10)
    distance = 7000

    def __init__(self):
        self.tree = (
            self.RedNotFinish  >> ((self.isNotCenter >> self.FixedPose) >> (self.isCenter >> self.isNotFitDistance >> self.FixedDistance)) >> self.isFitDistance >> (self.rec_over1 | self.hover)
            # self.RedNotFinish  >> ((self.isNotFitDistance >> self.FixedDistance) >> (self.isFitDistance >> self.isNotCenter >> self.FixedPose)) >> self.isCenter  >> (self.rec_over1 | self.hover)

            # self.RedNotFinish >> self.NotReady2Pass >> ( (self.isNotCenter >> self.FixedPose) | (self.isCenter >> self.FixedDistance) ) >> (self.rec_over1 | self.hover)
            # |self.BlueNotFinish >> (self.NotReady2Pass | self.PassAndLand) >> ( (self.isNotCenter >> self.FixedPose) | (self.isCenter >> self.Forward) ) >> (self.rec_over1 | self.hover)
        )

    # @condition
    # def BlueNotFinish(self):
    #     print("condition: BlueNotFinish")
    #     return bt_mission.color == "blue"

    @condition
    def isNotFitDistance(self):
        # print("condition: isNotFitDistance")
        return bt_mission.drone.suber.target[2] > 20000 or bt_mission.drone.suber.target[2] < 7000

    @condition
    def isFitDistance(self):
        # print("condition: isFitDistance")
        return bt_mission.drone.suber.target[2] <= 20000 and bt_mission.drone.suber.target[2] >= 7000


    @condition
    def RedNotFinish(self):
        # print("condition: RedNotFinish")
        return bt_mission.color == "red"

    @condition
    def NotReady2Pass(self):
        # print("condition: NotReady2Pass")
        return bt_mission.drone.suber.target[3] != -1

    @condition
    def isNotCenter(self):
        # print("condition: isNotCenter")
        return abs(bt_mission.drone.suber.target[0] - bt_mission.center[0]) > 60 or abs(bt_mission.drone.suber.target[1] - bt_mission.center[1]) > 60

    @condition
    def isCenter(self):
        # print("condition: isCenter")
        return abs(bt_mission.drone.suber.target[0] - bt_mission.center[0]) <= 60 and abs(bt_mission.drone.suber.target[1] - bt_mission.center[1]) <= 60

    @condition
    def rec_over1(self):
        print("condition: rec_over1")
        return rospy.get_time() - bt_mission.drone.suber.rec_time <= 1.0

    # @action
    # def PassAndSwitch(self):
    #     print("action: PassAndSwitch")
    #     msg = Twist()
    #     msg.linear.x = 1
    #     #msg.linear.y = -0.1
    #     bt_mission.cmd_pub.publish(msg)
    #     bt_mission.rate.sleep()
    #     sleep(2)
    #     msg = Twist()
    #     msg.angular.x = 0.7
    #     msg.angular.z = 0.05
    #     bt_mission.cmd_pub.publish(msg)
    #     bt_mission.rate.sleep()
    #     sleep(2)
    #     msg = Twist()
    #     msg.angular.x = 0.3
    #     msg.angular.z = 0.03
    #     bt_mission.cmd_pub.publish(msg)
    #     bt_mission.rate.sleep()
    #     sleep(2)
    #     msg = Twist()
    #     msg.angular.z = 1
    #     bt_mission.cmd_pub.publish(msg)
    #     bt_mission.rate.sleep()
    #     sleep(2)
    #     bt_mission.change_pub.publish(Empty())
    #     bt_mission.rate.sleep()
    #     msg = Twist()
    #     bt_mission.cmd_pub.publish(msg)
    #     bt_mission.rate.sleep()
    #     bt_mission.color = "blue"


    @action
    def PassAndLand(self):
        # print("action: PassAndLand")
        msg = Twist()
        msg.linear.x = 0.3
        #msg.linear.z = 0.2
        bt_mission.cmd_pub.publish(msg)
        bt_mission.rate.sleep()
        sleep(2)
        msg = Twist()
        msg.linear.x = 0.4 
        #msg.linear.z = 0.2
        bt_mission.cmd_pub.publish(msg)
        bt_mission.rate.sleep()
        sleep(2)
        msg = Twist()
        bt_mission.cmd_pub.publish(msg)
        bt_mission.rate.sleep()

        while bt_mission.drone.suber.canLand is not True:
          msg = Empty()
          bt_mission.land_pub.publish(msg)
          bt_mission.rate.sleep()

    @action
    def FixedPose(self):
      print(bt_mission.drone.suber.target[0],bt_mission.drone.suber.target[1],bt_mission.drone.suber.target[2])
      if bt_mission.drone.suber.target[0] == -1 or bt_mission.drone.suber.target[1] == -1 or bt_mission.drone.suber.target[2] == -1:
        print("skip")
        # msg = Twist()
        # bt_mission.cmd_pub.publish(msg)
        # bt_mission.rate.sleep()
      else:
        msg = Twist()
        if abs(bt_mission.drone.suber.target[0] - bt_mission.center[0]) >= 60:
          msg.angular.z = (bt_mission.drone.suber.target[0] - bt_mission.center[0]) / abs((bt_mission.drone.suber.target[0] - bt_mission.center[0])) * 0.2
          # msg.linear.x = (bt_mission.drone.suber.target[0] - bt_mission.center[0]) / abs((bt_mission.drone.suber.target[0] - bt_mission.center[0])) * 0.1
          print("action: FixedPose linear x",msg.angular.z)
          bt_mission.cmd_pub.publish(msg)
          bt_mission.rate.sleep()
          # bt_mission.change_pub.publish(0)
          # bt_mission.rate.sleep()
        else:
          if abs(bt_mission.drone.suber.target[1] - bt_mission.center[1]) >= 60:
            msg.linear.z = -(bt_mission.drone.suber.target[1] - bt_mission.center[1]) / abs((bt_mission.drone.suber.target[1] - bt_mission.center[1])) * 0.2
            print("action: FixedPose linear z",msg.linear.z)
            bt_mission.cmd_pub.publish(msg)
            bt_mission.rate.sleep()
            # bt_mission.change_pub.publish(0)
            # bt_mission.rate.sleep()
        

    @action
    def FixedDistance(self):
      print(bt_mission.drone.suber.target[0],bt_mission.drone.suber.target[1],bt_mission.drone.suber.target[2])
      if bt_mission.drone.suber.target[0] == -1 or bt_mission.drone.suber.target[1] == -1 or bt_mission.drone.suber.target[2] == -1:
        print("action: FixedDistance ")
        # msg = Twist()
        # bt_mission.cmd_pub.publish(msg)
        # bt_mission.rate.sleep()
      else:
        msg = Twist()
        if bt_mission.drone.suber.target[2] < 7000:
          msg.linear.y = 0.2
          print("action: FixedDistance linear y",msg.linear.x)
          bt_mission.cmd_pub.publish(msg)
          bt_mission.rate.sleep()
        else:
          if bt_mission.drone.suber.target[2] > 20000:
            msg.linear.y = -0.2
            print("action: FixedDistance linear y",msg.linear.x)
            bt_mission.cmd_pub.publish(msg)
            bt_mission.rate.sleep()
        # if abs(bt_mission.distance - bt_mission.drone.suber.target[2]) >= 3000:
        #   if bt_mission.distance > bt_mission.drone.suber.target[2]:
        #     msg.linear.y = 0.2
        #   else:
        #     msg.linear.y = -0.2
          # print("action: FixedDistance linear y",msg.linear.x)
          # bt_mission.cmd_pub.publish(msg)
          # bt_mission.rate.sleep()
          # bt_mission.change_pub.publish(0)
          # bt_mission.rate.sleep()

    @action
    def hover(self):
      print("action: hover")
      msg = Twist()
      bt_mission.cmd_pub.publish(msg)
      bt_mission.rate.sleep()
      # bt_mission.change_pub.publish(1)
      # bt_mission.rate.sleep()

    def run(self):
        while True:
            if bt_mission.isContinue == False:
                break
            bb = self.tree.blackboard(1)
            state = bb.tick()
            # print "state = %s\n" % state
            #if bt_mission.drone.isStop == True:
            #  exec("f = open(\"123.txt\",\'rb\')")           
            while state == RUNNING:
                state = bb.tick()
                # print "state = %s\n" % state
                #if bt_mission.drone.isStop == True:
                #  exec("f = open(\"123.txt\",\'rb\')")
            assert state == SUCCESS or state == FAILURE

def main():
    print("start...") 
    btCm_n = bt_mission()
    sleep(2)

    try:
        btCm_n.run()
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down ROS module")

if __name__ == "__main__":
    main()
