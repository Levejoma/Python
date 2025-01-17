# importing libraries
import os
import cv2
import numpy
import time
#import psutil
from time import sleep
from datetime import datetime


#psutil.disk_usage(python3)




# Defining a function motionDetection
def motionDetection():
    # capturing video in real time
    try:
        cap = cv2.VideoCapture(0)
        try:
            time = datetime.now().strftime('%d.%m.%y')
        except:
            print("time/datetime module error")
     
    except:
            print("Cant get camera")
    finally:
        i=0
        while os.path.exists(f"YOURPATHGOESHERE/{time}_{i}.avi"):
            i += 1
        #fh = open(f"YOURPATHGOESHERE/{time}_{i}.avi", "w")
    
    #If you want to manually set resolution, will affect performance
    """
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    """
    
    #Recording and counter for motion, create videowriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID') 
    Out = cv2.VideoWriter(f'YOURPATHGOESHERE/{time}_{i}.avi', fourcc, 60.0, (640,  480))
    #In = cv2.VideoCapture(f'YOURPATHGOESHERE/{time}_{i}.avi', fourcc, 30.0, (640,  480))
    counter = 0
    counter2 = 0


    # reading frames sequentially
    ret, frame1 = cap.read()
    ret, frame2 = cap.read()

    while cap.isOpened():

        time = datetime.now().strftime('%H.%M.%S')
        cv2.putText(frame2, f"{time}".format(str(counter)),
        (250, 20), cv2.FONT_HERSHEY_SIMPLEX,0.8, (0, 0, 255), 1)
        counter2 = bool(0)
        
        
        # difference between the frames
        diff = cv2.absdiff(frame1, frame2)
        diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(diff_gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(
            dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        #change cv2.contourarea(contour) value for more sensitivity, default: 900
        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)
            if cv2.contourArea(contour) < 900:
                continue
            
            counter += 1
            counter2 = bool(1)
            cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame1, "Recording", (10, 60), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 0, 255), 2)
        
        cv2.putText(frame1, "Motionframes: {}".format(str(counter)),
        (10, 460), cv2.FONT_HERSHEY_SIMPLEX,0.8, (150, 150, 150), 1)
        
        cv2.putText(frame1, "Motion: {}".format(str(counter2)),
        (470, 460), cv2.FONT_HERSHEY_SIMPLEX,0.8, (150, 150, 150), 1)
       
        
        cv2.imshow("Video", frame1)
        frame1 = frame2
        ret, frame2 = cap.read()
        #frame2 = cv2.rotate(frame2, cv2.ROTATE_180)
        if counter2 == True:
            Out.write(frame1)
            Out.write(frame2)
        
        #start new instance if video captures movemment more frames than counter value
        if counter >= 6000:
            counter = 0
            counter2 = 0
            cap.release()
            cv2.destroyAllWindows()
            motionDetection()
            break

        if cv2.waitKey(50) == 27:
            break
        


    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":

            
    motionDetection()
        
        

    
    
            