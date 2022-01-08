import sys
from pathlib import Path
from system_hotkey import SystemHotkey
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QApplication
import PyQt5.QtCore as QtCore
from PyQt5.QtCore import pyqtSignal, QEventLoop
from PyQt5 import QtGui
from OCR_style import Ui_OCR_Window
from Screenshot import getScreenPos,getScreenshot
from OCR import getOCRResult
from YoudaoAPI import YoudaoTranslator
from CaiYunAPI import CaiYunTranslator
from BaiduAPI import BaiduTranslator
from TencentAPI import TencentTranslator
from Segmentation import splitWords

global ZhNameDict,JPNameDict
JPNameDict = {
    'モブ美': "林品如",
    'モブ男': "洪世贤",
    'モブくん': "陈睿",
    '失恋フラグ': "武则天",
    'フラグちゃん': "李旎",
    '死亡フラグ': "张美玉",
    '恋愛フラグ': "张作霖",
    '生存フラグ': "段祺瑞"
}
ZhNameDict = {
    "林品如": '路人美',
    "洪世贤": '路人男',
    "陈睿": '路人君',
    "武则天": '失恋Flag',
    "李旎": 'Flag酱',
    "张美玉": '死亡Flag',
    "张作霖": '恋爱Flag',
    "段祺瑞": '生存Flag'
}

def keymap_replace(
        string: str, 
        mappings: dict,
        lower_keys=False,
        lower_values=False,
        lower_string=False,
    ) -> str:
    """Replace parts of a string based on a dictionary.

    This function takes a string a dictionary of
    replacement mappings. For example, if I supplied
    the string "Hello world.", and the mappings 
    {"H": "J", ".": "!"}, it would return "Jello world!".

    Keyword arguments:
    string       -- The string to replace characters in.
    mappings     -- A dictionary of replacement mappings.
    lower_keys   -- Whether or not to lower the keys in mappings.
    lower_values -- Whether or not to lower the values in mappings.
    lower_string -- Whether or not to lower the input string.
    """
    replaced_string = string.lower() if lower_string else string
    for character, replacement in mappings.items():
        replaced_string = replaced_string.replace(
            character.lower() if lower_keys else character,
            replacement.lower() if lower_values else replacement
        )
    return replaced_string

def nameReplace(string,reverse=False):
    _dict = ZhNameDict if reverse else JPNameDict
    return keymap_replace(string,_dict)


class TransAssistant_class(QtWidgets.QMainWindow, Ui_OCR_Window):
    ocrHotkeyPressed = pyqtSignal()
    
    def setupUi(self,OCR_Window):
        super(TransAssistant_class,self).setupUi(OCR_Window)
        OCR_Window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        OCR_Window.setWindowOpacity(0.8)
        OCR_Window.OCRButton.setEnabled(self.AreaInit)
        OCR_Window.OCRButtonPlus.setEnabled(self.AreaInit)
        DesktopSize = QApplication.desktop()
        OCR_Window.move(DesktopSize.width()*0.54, DesktopSize.height()*0.41)
        # OCR_Window.setAttribute(QtCore.Qt.WA_TranslucentBackground,True)
    def  __init__ (self):
        super(TransAssistant_class, self).__init__()
        self.AreaInit = False
        self.ScreenPos = [(0,0),(0,0)]
        self.OCRText = str()
        self.SplitMode = "sudachi"
        self.Hotkey_OCR = ['control','space']
        SystemHotkey().register(self.Hotkey_OCR,callback=lambda x:self.sendHotkeyPressedSig(self.Hotkey_OCR))
        self.setupUi(self)
        
        def keyPressEvent(self,e):
            if e.key() == QtCore.Qt.Key_Escape:
                self.close()    
        
    def sendHotkeyPressedSig(self,Hotkeys):
        if(Hotkeys is self.Hotkey_OCR):
            self.ocrHotkeyPressed.emit()
        
    def getScreenPos(self):
        self.hide()
        self.ScreenPos = getScreenPos()
        self.PosText.setText(str((self.ScreenPos[0],self.ScreenPos[1]))+","+str((self.ScreenPos[0]+self.ScreenPos[2],self.ScreenPos[1]+self.ScreenPos[3])))
        self.show()
        self.AreaInit = True
        self.OCRButton.setEnabled(self.AreaInit)
        self.OCRButtonPlus.setEnabled(self.AreaInit)
        # print(self.ScreenPos)
    
    def getOCRText(self):
        if(self.AreaInit):
            self.OCRText = getOCRResult(getScreenshot(self.ScreenPos))
            self.OCRResultTextEdit.setPlainText(self.OCRText)
    
    def appendOCRText(self):
        if(self.AreaInit):
            self.OCRText += getOCRResult(getScreenshot(self.ScreenPos))
            self.OCRResultTextEdit.setPlainText(self.OCRText)
        
    def updateResult_1(self,source):
        translatorResult = nameReplace(YoudaoTranslator(source),True)
        self.TransResult_1.setPlainText(translatorResult)
    
    def updateResult_2(self,source):
        translatorResult = nameReplace(CaiYunTranslator(source),True)
        self.TransResult_2.setPlainText(translatorResult)
    
    def updateResult_3(self,source):
        translatorResult = nameReplace(BaiduTranslator(source),True)
        self.TransResult_3.setPlainText(translatorResult)
    
    def updateResult_4(self,source):
        translatorResult = nameReplace(TencentTranslator(source),True)
        self.TransResult_4.setPlainText(translatorResult)
    
    def updateResults(self):
        source = self.OCRResultTextEdit.toPlainText()
        if(source != ''):
            self.updateSplitTextEdit(source)
            source = nameReplace(source)
            self.updateResult_1(source)
            self.updateResult_2(source)
            self.updateResult_3(source)
            self.updateResult_4(source)
        
    def updateSplitMode(self,mode):
        self.SplitMode = mode
        source = self.OCRResultTextEdit.toPlainText()
        if(source != ''):
            self.updateSplitTextEdit(source)
        
    def updateSplitTextEdit(self,source):
        self.splitTextEdit.setPlainText(splitWords(source,self.SplitMode))
    
    def updateOCRHotkey(self,text):
        print(text)
        self.keyPressEvent






def runGUI():
    GUI_APP=QtWidgets.QApplication(sys.argv)
    GUI_mainWindow = TransAssistant_class()
    GUI_mainWindow.setFixedSize(GUI_mainWindow.width(), GUI_mainWindow.height())
    GUI_mainWindow.show()
    GUI_APP.exec_()

if __name__ == "__main__":
    # print(runGUI())
    runGUI()