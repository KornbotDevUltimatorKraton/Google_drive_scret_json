import cv2
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import time
import datetime 
import os 
cascPath = r'C:\Users\Asus\AppData\Local\Programs\Python\Python38\Webcam-Face-Detect'
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eyeCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
video_capture = cv2.VideoCapture(0)
try:
   gauth = GoogleAuth()
   gauth.LocalWebserverAuth()
   drive = GoogleDrive(gauth)
except:
   print("Terminate connection google drive")
Image_path = r"C:\Users\Asus\AppData\Local\Programs\Python\Python38"
img_counter = 0
mem_current_pict = [] 
while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    face = faceCascade.detectMultiScale(gray,1.1,4)
    eye = faceCascade.detectMultiScale(gray,1.1,4)
    for(x,y,w,h) in face:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color=frame[y:y+h, x:x+w]
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, 'Detecting face',(55,280), font,1,(0,255,0),2)
            for(x,y,w,h) in eye:
                   cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),1)
                   roi_gray = gray[y:y+h, x:x+w] 
                   roi_color=frame[y:y+h, x:x+w]
                   font = cv2.FONT_HERSHEY_SIMPLEX
                   cv2.putText(frame, 'Detecting eyes',(350,280), font,1,(0,255,0),2)    
                   #os.system("Shutdown/r")
                   img_name =  "camdetected_.png".format(img_counter) #"buundit_detected_{}.jpg".format(datetime.datetime.now()) 
                   cv2.imwrite(img_name,frame)
                   #video_capture.release()
                   list_image = os.listdir(Image_path)
                   #print(list_image)
                   print(mem_current_pict)
                   try:
                     for pic in list_image: 
                        if pic.split(".")[1] == 'png':
                             if pic not in mem_current_pict:
                               mem_current_pict.append(pic)
                               #print(mem_current_pict)
                               if len(mem_current_pict) >1:
                                      os.remove(mem_current_pict[0])
                                     
                   except: 
                        print("No image in the directory")
                
                   print("{} written!".format(img_name))
                   img_counter += 1
                   time.sleep(0.2)
                
                   #cv2.waitKey(30)
                   
                   file1 = drive.CreateFile({'title':str(datetime.datetime.now())}) 
                   file1.SetContentFile("camdetected_.png")
                   file1.Upload()
    

    font = cv2.FONT_HERSHEY_SIMPLEX
        
    #cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()