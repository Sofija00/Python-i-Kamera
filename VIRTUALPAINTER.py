import cv2
import numpy as np
import time
import os
import HandTrackingModule as htm

brushThickness = 15
eraserThickness = 50


folderPath = "Header"
myList = os.listdir(folderPath)
print(myList)

#provera koiko ima slika, u ovom slucaju 4
overLayList = []
for imPath in myList:
    image = cv2.imread(os.path.join(folderPath, imPath))
    overLayList.append(image)

print(len(overLayList))
header = overLayList[0]
drawColor=(255,0,255)


#kamera
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)


#ovamo povezujemo htm kod sa ovim
detector = htm.HandDetector()
detector.detectionCon = 0.85

xp,yp = 0,0

imgCanvas = np.zeros((720,1280,3),np.uint8)

#brojevi za prste
x1, y1, x2, y2 = 0, 0, 0, 0

while True:
    success, img = cap.read()
    #obrne se kako bi se lakse kontrolisalo
    img = cv2.flip(img, 1)
    #trazi mi ruku
    img = detector.find_hands(img)
    #brojke
    lmList=detector.find_position(img,draw=False)


    if len(lmList) != 0:
        if len(lmList) >= 9:
            x1, y1 = lmList[8][1:]
        if len(lmList) >= 13:
            x2, y2 = lmList[12][1:]
     
        #provera da li su prsti gore
        fingers = detector.fingers_up()

#proveravnje koji su prsti gore
        if len(fingers) >= 3:
            if fingers[1] and fingers[2]:
                xp,yp = 0,0
                print("Selection MODE")
                if y1 < 125:
                    if 250 < x1 < 415:
                        header = overLayList[0]
                        drawColor = (255,0,255)
                    elif 550 < x1 < 750:
                        header = overLayList[1]
                        drawColor=(255,0,0)
                    elif 800 < x1 < 950:
                        header = overLayList[2]
                        drawColor  (0,255,0)
                    elif 1050 < x1 < 1200:
                        header = overLayList[3]
                        drawColor = (0,0,0)
            cv2.rectangle(img, (x1, y1-25), (x2, y2+25), drawColor, cv2.FILLED)
        #vrh kaziprsta i srednji prst  
            if fingers[1] and not fingers[2]:
                cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
                print("Drawing MODE")

                #krecemo da crtamo   
                if xp==0 and yp==0:
                #gde god da si, pocni da crtas, linja
                    xp,yp = x1,y1

                if drawColor ==(0,0,0):
                    cv2.line(img, (xp,yp),(x1,y1),drawColor, eraserThickness)
                else:
                    cv2.line(img, (xp,yp),(x1,y1),drawColor, brushThickness)
                    cv2.line(imgCanvas, (xp,yp),(x1,y1),drawColor, brushThickness)    


                xp,yp = x1,y1
    #ovaj deo je za "preklapanje" dva "ekrana", iliti canvas i ekran..
    imgGray = cv2.cvtColor(imgCanvas,cv2.COLOR_BGR2GRAY)
    _, imgInv =cv2.threshold(imgGray,58,255,cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_or(img,imgCanvas)


    # Resize header menja velicinuda se slaze uz kameru
    header_resized = cv2.resize(header, (img.shape[1], header.shape[0]))
    # Overlay header odlazi na vrh
    img[0:header_resized.shape[0], 0:header_resized.shape[1]] = header_resized

    #img=cv2.addWeighted(img,0.5,imgCanvas,0.5,0)

    cv2.imshow("Image", img)
    cv2.imshow("Canvas", imgCanvas)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
