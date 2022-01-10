from typing import Union
import pyautogui
import cv2
import numpy as np

global WindowName
WindowName = "Please choose the subtitle area"


def getScreenPos() -> tuple:
    PosList = list()
    img = pyautogui.screenshot()  # x,y,w,h
    img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
    cv2.namedWindow(WindowName, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(WindowName, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow(WindowName, img)
    PosList = cv2.selectROI(
        windowName=WindowName, img=img, showCrosshair=False, fromCenter=False
    )
    cv2.destroyAllWindows()
    return PosList


def getScreenshot(Pos: Union[list, tuple, set]):
    x, y, w, h = Pos
    Screenshot = pyautogui.screenshot(region=(x, y, w, h))  # x,y,w,h
    Screenshot = cv2.cvtColor(np.asarray(Screenshot), cv2.COLOR_RGB2BGR)
    return Screenshot


# cv2.imshow('1',getScreenshot(getScreenPos()))
# cv2.waitKey(0)
# print(OCR(getScreenshot(getScreenPos())))
