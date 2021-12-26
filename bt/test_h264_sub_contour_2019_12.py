#!/usr/bin/env python2

import rospy
from sensor_msgs.msg import CompressedImage
from std_msgs.msg import Empty, UInt8
from tello_driver.msg import test
import av
import cv2
import numpy as np
import threading
import traceback
import time
import math


class StandaloneVideoStream(object):
    def __init__(self):
        self.cond = threading.Condition()
        self.queue = []
        self.closed = False

    def read(self, size):
        self.cond.acquire()
        try:
            if len(self.queue) == 0 and not self.closed:
                self.cond.wait(2.0)
            data = bytes()
            while 0 < len(self.queue) and len(data) + len(self.queue[0]) < size:
                data = data + self.queue[0]
                del self.queue[0]
        finally:
            self.cond.release()
        return data

    def seek(self, offset, whence):
        return -1

    def close(self):
        self.cond.acquire()
        self.queue = []
        self.closed = True
        self.cond.notifyAll()
        self.cond.release()

    def add_frame(self, buf):
        self.cond.acquire()
        self.queue.append(buf)
        self.cond.notifyAll()
        self.cond.release()


stream = StandaloneVideoStream()

global tag
tag = 0

# initialize the known distance from the camera to the object, which
# in this case is 24 inches
global KNOWN_DISTANCE
KNOWN_DISTANCE = 10.0
# initialize the known object width, which in this case, the piece of
# paper is 12 inches wide
global KNOWN_WIDTH
KNOWN_WIDTH = 10.0

def callback(msg):
  #rospy.loginfo('frame: %d bytes' % len(msg.data))
  #if len(msg.data) > 1000:  
    stream.add_frame(msg.data)


def changeCB(msg):
  print("changeCB",msg.data)
  global tag
  if msg:
    tag = msg.data


def findMask(img):
  # 0,114,27~0,255,255

  lr0 = np.array([19,107,89])
  ur0 = np.array([35,255,255])
  # lr1 = np.array([170,100,0])
  # ur1 = np.array([180,255,255])
  rm0 = cv2.inRange(img, lr0, ur0)
  # rm1 = cv2.inRange(img, lr1, ur1)
  # rm = cv2.bitwise_or(rm0, rm1)
  return rm0

def findMask1(img):
  lr0 = np.array([110,40,0])
  ur0 = np.array([125,255,255])
  #lr1 = np.array([175,150,0])
  #ur1 = np.array([180,255,255])
  rm0 = cv2.inRange(img, lr0, ur0)
  #rm1 = cv2.inRange(img, lr1, ur1)
  #rm = cv2.bitwise_or(rm0, rm1)
  return rm0

def distance_to_camera(knownWidth, focalLength, perWidth):
  # compute and return the distance from the maker to the camera
  return (knownWidth * focalLength) / perWidth


def main():
    global tag
    old_center = [0,0,0]
    fourcc = cv2.VideoWriter_fourcc('X','V','I','D')
    out = cv2.VideoWriter('test_contour.avi', fourcc, 10.0, (1920, 720))
    rospy.init_node('h264_listener')
    rospy.Subscriber("/tello/image_raw/h264", CompressedImage, callback)
    pub = rospy.Publisher('/selfDefined', test, queue_size = 1)
    rospy.Subscriber('/selfChanged', UInt8, changeCB)
    container = av.open(stream)
    rospy.loginfo('main: opened')
    frame_skip = 300

    for frame in container.decode(video=0):
        if 0 < frame_skip:
          frame_skip -= 1
          continue
        start_time = time.time()

        image = cv2.cvtColor(np.array(frame.to_image()), cv2.COLOR_RGB2BGR)
        blurred_img = cv2.GaussianBlur(image, (13, 13), 0)
        hsv = cv2.cvtColor(blurred_img.copy(), cv2.COLOR_BGR2HSV)
        # blurred = cv2.GaussianBlur(frame, (11, 11), 0)

        # construct a mask for the color "green", then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        greenLower = (19, 107, 89)
        greenUpper = (35, 255, 255)
        mask = cv2.inRange(hsv, greenLower, greenUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        # cv2.circle(hsv,(480,270),40,(255,0,0),5)

        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
        for cnt in cnts:
          area = cv2.contourArea(cnt)
          areaMin = 1000
          if area > areaMin:
            x,y,w,h = cv2.boundingRect(cnt)
            
            if area >= 7000 and area <= 20000:
              cv2.rectangle(hsv,(x,y),(x+w,y+h),(0,0,255),2)
            else:
              cv2.rectangle(hsv,(x,y),(x+w,y+h),(0,255,255),2)
            # if tag == 0:
            #   cv2.rectangle(hsv,(x,y),(x+w,y+h),(0,255,255),2)
            # elif tag == 1:
            #   cv2.rectangle(hsv,(x,y),(x+w,y+h),(0,0,255),2)
            ce_x = x + w/2
            ce_y = y + h/2
            cv2.circle(hsv,(ce_x,ce_y),5,(0,255,0),5)
            old_center = [int(ce_x),int(ce_y),int(area)]
            pub.publish(test([int(old_center[0]),int(old_center[1]),int(area),1]))
            # if old_center[0] == 0 and old_center[1] == 0 and old_center[2] == 0:
            #   old_center = [int(ce_x),int(ce_y),int(area)]
            #   pub.publish(test([int(old_center[0]),int(old_center[1]),int(area),1]))
            # else:
            #   #print(math.sqrt( (int(mean_y) - old_center[0])**2 + (int(mean_x) - old_center[1])**2 ))
            #   # cv2.putText(show_image, str(rect_width*rect_height/(960*720.0)), (10,40),5 ,2, 255)
            #   if w*h >= 960*720*0.25:
            #     pub.publish(test([old_center[0],old_center[1],old_center[2],-1]))
            #     print(">= 100")
            #     t = rospy.get_time()
            #     while rospy.get_time() - t < 1:
            #       pass
            #     #rospy.signal_shutdown('Quit')
            #   else:
            #     old_center = [int(ce_x),int(ce_y),int(area)]
            #     pub.publish(test([int(old_center[0]),int(old_center[1]),int(old_center[2]),1]))
        # 
        # image = cv2.cvtColor(np.array(frame.to_image()), cv2.COLOR_RGB2BGR)
        # blurred_img = cv2.GaussianBlur(image, (13, 13), 0)
        # hsv_img = cv2.cvtColor(blurred_img.copy(), cv2.COLOR_BGR2HSV)
        # if tag == 0:
        #   red_mask = findMask(hsv_img)
        # elif tag == 1:
        #   red_mask = findMask1(hsv_img)        
        # (c_i, c_c, c_h) = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        # show_image = cv2.cvtColor(c_i, cv2.COLOR_GRAY2BGR)


        # if len(c_c) != 0:
        #   cv2.drawContours(show_image, c_c, 0, (0,0,255), -1)
        #   out_max_contours = max(c_c, key = cv2.contourArea)
        #   rect = cv2.minAreaRect(out_max_contours)
        #   rect_width, rect_height = rect[1]
        #   print(rect_width,rect_height)
        #   focalLength = (rect_width * KNOWN_DISTANCE) / KNOWN_WIDTH
        #   #avg_x = []
        #   #avg_y = []
        #   #for c in out_max_contours:
        #   #    avg_x.append(c[0][0])
        #   #    avg_y.append(c[0][1])
        #   ce_x = rect[0][0] + 1/2*rect_width
        #   ce_y = rect[0][1] + 1/2*rect_height
        #   if old_center[0] == 0 and old_center[1] == 0 and old_center[2] == 0:
        #     old_center = [int(ce_x),int(ce_y),int(focalLength)]
        #     pub.publish(test([int(old_center[0]),int(old_center[1]),int(focalLength),1]))
        #   else:
        #     #print(math.sqrt( (int(mean_y) - old_center[0])**2 + (int(mean_x) - old_center[1])**2 ))
        #     cv2.putText(show_image, str(rect_width*rect_height/(960*720.0)), (10,40),5 ,2, 255)
        #     if rect_width*rect_height >= 960*720*0.25:
        #       pub.publish(test([old_center[0],old_center[1],old_center[2],-1]))
        #       print(">= 100")
        #       t = rospy.get_time()
        #       while rospy.get_time() - t < 1:
        #         pass
        #       #rospy.signal_shutdown('Quit')
        #     else:
        #       old_center = [int(ce_x),int(ce_y),int(focalLength)]
        #       pub.publish(test([int(old_center[0]),int(old_center[1]),int(old_center[2]),1]))
        
        out.write(np.concatenate((blurred_img, hsv), axis=1))
        cv2.imshow('result', np.concatenate((blurred_img, hsv), axis=1))
        cv2.waitKey(1)
        if frame.time_base < 1.0/60:
          time_base = 1.0/60
        else:
          time_base = frame.time_base
        frame_skip = int((time.time() - start_time)/time_base)

if __name__ == '__main__':
    try:
        main()
    except BaseException:
        traceback.print_exc()
    finally:
        stream.close()
        cv2.destroyAllWindows()
