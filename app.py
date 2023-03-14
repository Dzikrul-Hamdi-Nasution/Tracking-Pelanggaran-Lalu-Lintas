import numpy as np 
import cv2
import time 
import os

#diatas 50 dapat hanya mobil
min_contour_width = 40  
min_contour_height = 40  
offset = 1
line_height_1 = 350  
line_height_2 = 450 
line_range = 560
matches = []
cars = 0
hitung=0 

lokasi = 'bukti'
if not os.path.exists(lokasi):
	print('Carpeta creada: ', lokasi)
	os.makedirs(lokasi)
 
def get_centrolid(x, y, w, h):
   x1 = int(w / 2)
   y1 = int(h / 2)
 
   cx = x + x1
   cy = y + y1
   return cx, cy



url   = "https://www.youtube.com/watch?v=aooeDr13d9g"
#video = pafy.new(url)
#best  = video.getbest(preftype="mp4")
cars=0
 
#cap = cv2.VideoCapture(best.url)
cap = cv2.VideoCapture("road.mp4")
#cap = cv2.VideoCapture(1)

cap.set(3, 480)
cap.set(4, 480)
 
if cap.isOpened():
   ret, frame1 = cap.read()
else:
   ret = False
ret, frame1 = cap.read()
ret, frame2 = cap.read()
 
 
while ret:
   d = cv2.absdiff(frame1, frame2)
   grey = cv2.cvtColor(d, cv2.COLOR_BGR2GRAY)
 
   blur = cv2.GaussianBlur(grey, (5, 5), 0)
 
   ret, th = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
   dilated = cv2.dilate(th, np.ones((3, 3)))
   kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
 
   cv2.line(frame1, (0, line_height_1), (line_range, line_height_1), (0, 255, 255), 2)
   cv2.line(frame1, (0, line_height_2), (line_range, line_height_2), (0, 0, 255), 2)
   closing = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel)
   contours, h = cv2.findContours(
       closing, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
   for(i, c) in enumerate(contours):
       (x, y, w, h) = cv2.boundingRect(c)
       contour_valid = (w >= min_contour_width) and (
           h >= min_contour_height)
 
       if not contour_valid:
           continue
       
       cv2.rectangle(frame1, (x-10, y-10), (x+w+10, y+h+10), (255, 0, 0), 2)
       
       centrolid = get_centrolid(x, y, w, h)
       matches.append(centrolid)
       cv2.circle(frame1, centrolid, 5, (0, 255, 0), -1)

       cx, cy = get_centrolid(x, y, w, h)
       imAux = frame1.copy()
       objeto = imAux[y-10:y+h+10,x-10:x+w+10]
       hitung = hitung+1
       for (x, y) in matches:
           if y > (line_height_2):
           # print("dari bawah " + str(hitung))
            if y <= (line_height_1):
               if x < (line_range):
                 cars = cars+1
                 matches.remove((x, y))
                 
                 cv2.imwrite(lokasi+'/pelanggaran{}.jpg'.format(cars),objeto)
                 print(y)
       
   
 
   cv2.imshow("Vehicle Detection", frame1)
   if cv2.waitKey(1) == 27:
       break
   frame1 = frame2
   ret, frame2 = cap.read()
 
cv2.destroyAllWindows()
cap.release()