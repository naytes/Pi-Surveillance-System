from imutils.video import VideoStream
import os
import argparse
import datetime
import imutils
import time
import cv2


#arguments 
ap = argparse.ArgumentParser()
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())

#capture camera feed
vs = cv2.VideoCapture(0)

#give yourself time to leave the room and not get caught by your own trap
time.sleep(10.0)

#init
firstFrame = None
frame_width = int(vs.get(3))
frame_height = int(vs.get(4))

#video writer init
out = cv2.VideoWriter('clip.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))

#flag for occupy state and iterater for amount of disturbances
occupiedFlag = False
occurances = 1

#loop through video by frame
while True:
    #get current frame
    ret, frame = vs.read()

    #init
    text = "Unoccupied"
    
    #gray and blur to prep for mtion detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    
    #initialize first frame
    if firstFrame is None:
        firstFrame = gray
        continue
    
    #compute absolute difference between the current frame and gray
    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
    
    #dilate thresh image to find contours better
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    
    #loop over the contours
    for c in cnts:
        #if the change is insignificant ignore it
        if cv2.contourArea(c) < args["min_area"] and ret ==True:
            continue
        #could put motion box here to be cool if desired
        text = "Occupied"
        occupiedFlag = True
    
    #draw text to frame
    cv2.putText(frame, "Disturbances: {}".format(str(occurances)), (10, frame.shape[0] -30), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)
    cv2.putText(frame, datetime.datetime.now().strftime("%A, %B %d, %Y %I:%M:%S%p"),(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)
    
    if text == "Occupied":
        out.write(frame)
    elif text != "Occupied" and occupiedFlag == True:
        occurances+=1
        occupiedFlag = False
        out.release()
        print("sending email...")
        exec(open("sendEmail.py").read())  
        print("sent")
        out = cv2.VideoWriter('clip.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
        
    #show frames
    cv2.imshow("Security Feed", frame)
    #cv2.imshow("Thresh", thresh)
    #cv2.imshow("Delta", frameDelta)
    
    #exit program on 'q' key
    #used waitkey(60) to get rid of slowmo affect
    key = cv2.waitKey(60) & 0xFF
    if key == ord("q"):
        out.release()
        vs.release()
        break
    
#destroy windows and delete empty avi file
cv2.destroyAllWindows()
os.remove("clip.avi")