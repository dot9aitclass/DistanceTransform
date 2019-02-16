#!/usr/bin/env python
"""Sweeps throught the depth image showing 100 range at a time"""
import freenect
import cv2
import numpy as np
import time
from scipy import ndimage

cv2.namedWindow('Depth')


def disp_thresh(lower, upper):
    depth, timestamp = freenect.sync_get_depth()
    depth = 255 * np.logical_and(depth > lower, depth < upper)
    depth = depth.astype(np.uint8)
    bw = depth#cv2.cvtColor(depth, cv2.COLOR_BGR2GRAY)
    _, bw = cv2.threshold(bw, 40, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    edt, dist = ndimage.distance_transform_edt(bw, return_indices=True)
    cv2.normalize(edt, edt, 0, 1.0, cv2.NORM_MINMAX)
    cv2.imshow('Distance Transform Image', edt)
    #cv2.imshow('Depth', depth)
contours1=[]
lower = 0
upper = 300
max_upper = 2048
while upper < max_upper:
    print('%d < depth < %d' % (lower, upper))
    depth, timestamp = freenect.sync_get_depth()
    depth = 255 * np.logical_and(depth > lower, depth < upper)
    depth = depth.astype(np.uint8)
    ftry=len(contours1)
    im3, contours1, hierarchy = cv2.findContours(depth, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if ftry>len(contours1):
        print ftry,len(contours1)
        cv2.destroyAllWindows()
        break
    cv2.imshow('Depth', depth)
    cv2.waitKey(5)
    time.sleep(.1)
    lower += 20
    upper += 20
while True:
    #print('%d < depth < %d' % (lower, upper))
    if lower-100>0 and upper+100<max_upper:
        disp_thresh(lower-100,upper+250)
        if cv2.waitKey(1)==27:
            cv2.destroyAllWindows()
            break
    else:
        disp_thresh(lower,upper+250)
        if cv2.waitKey(1)==27:
            cv2.destroyAllWindows()
            break
    # else:
    #     disp_thresh(lower,upper+250)
    #     if cv2.waitKey(1)==27:
    #         cv2.destroyAllWindows()
    #         break