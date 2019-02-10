
# Importing libraries and haarcascade

import cv2
import numpy as np
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


def face_return(faces): # Removes background faces 
    maxx = faces[0,2]+faces[0,3]
    face = faces[0,:]
    for x,y,w,h in faces:
        if(h+w)>maxx:
            face = np.array([x,y,w,h])

    face = face.reshape(1,4)
    return face # Returning face closest to cam


def yes(): # Counts number of head nodes
    global flag_y,del_x,del_y,flag_f_y,Yes
    if flag_y>0:
        flag_y -= 1

    if del_y<=3 and del_y>=-3 and flag_y>0:
        Yes += 1
        flag_y = 0

    if del_y < -6:
        flag_y = 10
    else:
        flag_y -= 1


def no(): # Counts number of head shakes
    global sign_a,sign_b,flag_x,del_x,del_y,No
    if del_x > 6 and sign_a == 0:
        sign_a = 15
    elif del_x < -6 and sign_b == 0:
        sign_b = 15

    if sign_a > 0:
        sign_a -= 1
    elif sign_b > 0:
        sign_b -= 1

    if sign_a > 0 and sign_b > 0 and flag_x == 0:
        flag_x = 20

    if flag_x > 0:
        if(del_x > -4 and del_x < 4):
            No += 1
            flag_x = 0
            sign_a = 0
            sign_b = 0
        else:
            flag_x-=1
            if flag_x == 0:
                sign_a = 0
                sign_b = 0


video_capture = cv2.VideoCapture(0) # Capturing video

# Initializing variables and flags
var = 0
y_old = flag_y = x_old = flag_x = 0
sign_x = sign_y = sign_a = sign_b = 0
del_x = del_y = 0
Yes = No = 0

while True:
    _, frame = video_capture.read()

    cv2.putText(frame, "Yes = "+str(Yes), (30,50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,0), 2)
    cv2.putText(frame, "No = "+str(No), (30,76), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,0), 2)
    cv2.imshow("video",frame)
    
    # Taking every third frame
    if var%3 == 0:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        # Skips current iteration if no face is detected
        if str(type(faces)) != "<class 'tuple'>":
#             continue
        
            face = faces[0,:]
            face = face_return(faces) # Calling face_return function to remove background faces

            for (x,y,w,h) in face:

                # Code to calculate forehead position if user changes position
                if del_x > 5 or del_x < -5:
                    sign_x += 1
                    if sign_x > 20:
                        x_old = x+w/2
                        y_old = y+h/3
                        flag_f_y = sign_a = sign_b = flag_x = flag_y = 0
                else:
                    sign_x = 0

                if del_y > 5 or del_y < -5:
                    sign_y += 1
                    if sign_y > 20:
                        x_old = x+w/2
                        y_old = y+h/3
                        flag_f_y = sign_a = sign_b = flag_x = flag_y = 0
                else:
                    sign_y = 0

                # Calculating distance moved by forehead
                del_y = ((y_old - (y+h/3))/h) * 100
                del_x = ((x_old - (x+w/2))/w) * 100

                # Functions to calculate head nods and shakes
                yes()
                no()

    var = var+1
    if cv2.waitKey(1) == 27: # Press Escape to close program
            break
video_capture.release()
cv2.destroyAllWindows()

