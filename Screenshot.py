import pyautogui
import cv2
import numpy as np
# from IUOCR_mix_OCR import OCR
# img = pyautogui.screenshot(region=[48,30,328,734])#x,y,w,h

global WindowName
WindowName = "Please choose the subtitle area"

def mouse(event, x, y, flags, param):
    global counts
    global PosList
    # global img
    if event == cv2.EVENT_LBUTTONDOWN:
        xy = "%d,%d" % (x, y)
        PosList.append((x, y))
        # print(xy)
        cv2.circle(img, (x, y), 1, (255, 255, 255), thickness = -1)
        cv2.putText(img, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,
                    1.0, (255, 255, 255), thickness = 1)
        cv2.imshow(WindowName, img)
        counts += 1
        if(counts == 2):
            cv2.destroyAllWindows()

def getScreenPos():
    global counts
    global img
    global PosList
    PosList = list()
    img = pyautogui.screenshot()#x,y,w,h
    img=cv2.cvtColor(np.asarray(img),cv2.COLOR_RGB2BGR)
    counts = 0
    cv2.namedWindow(WindowName, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(WindowName, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow(WindowName, img)
    cv2.setMouseCallback(WindowName, mouse)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return PosList


def getScreenshot(Pos):
    x1,y1 = Pos[0][0], Pos[0][1]
    x2,y2 = Pos[1][0], Pos[1][1]
    x,y = min(x1,x2),min(y1,y2)
    w,h = max(x1,x2)-x,max(y1,y2)-y
    Screenshot = pyautogui.screenshot(region=(x,y,w,h))#x,y,w,h
    Screenshot = cv2.cvtColor(np.asarray(Screenshot),cv2.COLOR_RGB2BGR)
    return Screenshot

# cv2.imshow('1',getScreenshot(getScreenPos()))
# cv2.waitKey(0)
# print(OCR(getScreenshot(getScreenPos())))