import sys
from pathlib import Path
from system_hotkey import SystemHotkey
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import PyQt5.QtCore as QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtGui
from OCR_style import Ui_OCR_Window
from Screenshot import getScreenPos,getScreenshot
from OCR import getOCRResult


class TransAssistant_class(QtWidgets.QMainWindow, Ui_OCR_Window):
    ocrHotkeyPressed = pyqtSignal()
    def setupUi(self,OCR_Window):
        super(TransAssistant_class,self).setupUi(OCR_Window)
        OCR_Window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        OCR_Window.setWindowOpacity(0.8)
        # OCR_Window.setAttribute(QtCore.Qt.WA_TranslucentBackground,True)
    def  __init__ (self):
        super(TransAssistant_class, self).__init__()
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # self.sig_keyhot.connect(self.MKey_pressEvent)
        # self.hk_start, self.hk_stop = SystemHotkey(),SystemHotkey()
        self.ScreenPos = [(0,0),(0,0)]
        self.OCRText = str()
        #4. 绑定快捷键和对应的信号发送函数
        self.Hotkey_OCR = ('control','space')
        SystemHotkey().register(self.Hotkey_OCR,callback=lambda x:self.sendHotkeyPressedSig(self.Hotkey_OCR))
        # SystemHotkey().register(('control', '2'), callback=lambda x: self.test())
        self.setupUi(self)
        
    #热键信号发送函数(将外部信号，转化成qt信号)
    def sendHotkeyPressedSig(self,Hotkeys):
        # self.hotkeyPressed.emit(Hotkeys)
        if(Hotkeys is self.Hotkey_OCR):
            # self.getOCRText()
            self.ocrHotkeyPressed.emit()
        
    def getScreenPos(self):
        self.hide()
        self.ScreenPos = getScreenPos()
        self.PosText.setText(str(self.ScreenPos[0])+","+str(self.ScreenPos[1]))
        self.show()
        # print(self.ScreenPos)
    
    def getOCRText(self):
        self.OCRText = getOCRResult(getScreenshot(self.ScreenPos))
        # print(self.OCRText)
        self.OCRResultTextEdit.setPlainText(self.OCRText)
    
def runGUI():
    GUI_APP=QtWidgets.QApplication(sys.argv)
    GUI_mainWindow = TransAssistant_class()
    GUI_mainWindow.setFixedSize(GUI_mainWindow.width(), GUI_mainWindow.height())
    GUI_mainWindow.show()
    GUI_APP.exec_()

if __name__ == "__main__":
    # print(runGUI())
    runGUI()