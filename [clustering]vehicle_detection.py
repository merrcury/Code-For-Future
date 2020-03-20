import cv2 as cv
import numpy as np
import scipy.cluster.hierarchy as hcluster
import  matplotlib.pyplot as plt

#Reading the video
cap = cv.VideoCapture('road.mp4')

#Writing the video
out = cv.VideoWriter('Tracking.avi',cv.VideoWriter_fourcc('M','J','P','G'), 30, (1280,480))


#bg subtractor
fgbg = cv.createBackgroundSubtractorMOG2()

#Feature detector

fast = cv.FastFeatureDetector_create(50)

cv.namedWindow('image', cv.WINDOW_NORMAL)

n_cluster = 5

frame_count = 0

while (1):
    ret, frame = cap.read()
    frame_count+=1
    if ret == False:
        break
    frame = cv.resize(frame, (640, 480))
    #print(frame_count)

    #bg subtraction -> feature detection
    fgmask = fgbg.apply(frame)
    blurred_image = cv.GaussianBlur(fgmask, (5,5), 0)
    kp = fast.detect(blurred_image, None)
    frame_with_features = cv.drawKeypoints(blurred_image, kp, None, color=(255, 255, 0))
    #out.write(frame)

    #print("test")
    kp_coordinates = []
    tmp = []
    if len(kp) < n_cluster:
        continue
    for i in range(len(kp)):
        tmp.append(kp[i])
    #print(len(kp))
    for i in range(len(tmp)):
        kp_coordinates.append(np.asarray(tmp[i].pt))
    #print(len(kp_coordinates))
    kp_coordinates = np.asarray(kp_coordinates)
    #print(kp_coordinates.shape, kp_coordinates.size)
    kp_coordinates = np.float32(kp_coordinates)

    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    ret, label, center = cv.kmeans(kp_coordinates, n_cluster, None, criteria, 10, cv.KMEANS_RANDOM_CENTERS)
    
    lst = []
    for i in range(n_cluster):
        lst.append([np.amin(kp_coordinates[label.ravel() == i][:,0]), np.amin(kp_coordinates[label.ravel() == i][:,1])])
        lst.append([np.amax(kp_coordinates[label.ravel() == i][:, 0]), np.amax(kp_coordinates[label.ravel() == i][:, 1])])

    lst = np.array(lst)
    for i in range(0,len(lst),2):
        if (lst[i+1,0] - lst[i,0] > 10 and lst[i+1,1] - lst[i,1] > 10 and lst[i+1,0] - lst[i,0] <1000 and lst[i+1,1] - lst[i,1] < 1000):
            cv.rectangle(frame, (lst[i,0], lst[i,1]), (lst[i+1,0], lst[i+1,1]), (0, 255, 0))
    cv.imshow('frame', blurred_image)
    
    k = cv.waitKey(30) & 0xFF

    if k == 27:
        break

cap.release()
out.release()
