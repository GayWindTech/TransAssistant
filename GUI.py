import sys
from system_hotkey import SystemHotkey
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
import PyQt5.QtCore as QtCore
from PyQt5.QtCore import pyqtSignal, QThread, QMutex
from OCR_style import Ui_OCR_Window
from Screenshot import getScreenPos, getScreenshot
from OCR import getOCRResult
from TranslatorAPI import YoudaoTranslator, CaiYunTranslator, BaiduTranslator, TencentTranslator
from MojiAPI import searchWord, fetchWord
from Segmentation import splitWords
from dict_style import Ui_dict_Window
from var_dump import var_dump

JPNameDict = {
    "モブ美": "林品如",
    "モブ男": "洪世贤",
    "モブくん": "陈睿",
    "失恋フラグ": "武则天",
    "フラグちゃん": "李旎",
    "死亡フラグ": "张美玉",
    "恋愛フラグ": "张作霖",
    "生存フラグ": "段祺瑞",
}
ZhNameDict = {
    "林品如": "路人美",
    "洪世贤": "路人男",
    "陈睿": "路人君",
    "武则天": "失恋Flag",
    "李旎": "Flag酱",
    "张美玉": "死亡Flag",
    "张作霖": "恋爱Flag",
    "段祺瑞": "生存Flag",
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
            replacement.lower() if lower_values else replacement,
        )
    return replaced_string


def nameReplace(string: str, reverse=False):
    _dict = ZhNameDict if reverse else JPNameDict
    return keymap_replace(string, _dict)

class dictWindow_class(QtWidgets.QMainWindow, Ui_dict_Window):
    selectionTextChange = pyqtSignal(str)

    def __init__(self):
        super(dictWindow_class, self).__init__()
        self.setupUi(self)
        self._wordList = []

    def setupUi(self, dictMain):
        super(dictWindow_class, self).setupUi(dictMain)
        dictMain.setWindowOpacity(0.9)
        dictMain.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

    def searchWord(self):
        source = self.inputTextEdit.toPlainText()
        self._wordList = searchWord(source)
        tempItemList = (each[0] for each in searchWord(source))
        self.wordsList.addItems(tempItemList)
        self.wordsList.setCurrentItem(self.wordsList.item(0))

    def setQueryWord(self,word):
        self.inputTextEdit.setPlainText(word)

    def fromtHtml(self,sourceList) -> str:
        try:
            html = f'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd"><html><head><meta name="qrichtext" content="1" /><style type="text/css">p, li {{ white-space: pre-wrap; }}</style></head><body><p style="margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style="font-family:\'微软雅黑\'; font-size:25pt; font-weight:600; color:#111111;">{sourceList[0][0]}</span></p><p style="margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style="font-family:\'微软雅黑\'; font-size:15pt; color:#111111;">{sourceList[0][2]} {sourceList[0][3]}</span></p><p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'微软雅黑\'; font-size:10pt; color:#111111;"><br /></p>'
            for eachId in sourceList[1][0]:
                html += '<p style="margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style="font-family:\'微软雅黑\'; font-size:23px; font-weight:600; color:#111111;">'+ sourceList[1][1][eachId][0] +'：</span></p><ul style="margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;">'
                for eachSubId in sourceList[1][1][eachId][1]:
                    html += '<li style="margin-top:6px; margin-bottom:6px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style="font-family:\'微软雅黑\'; font-size:17px; color:#111111; text-decoration: underline;">'+ sourceList[1][1][eachId][2][eachSubId][0] +'</span></li><ul style="margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 2;">'
                    for eachExampleList in sourceList[1][1][eachId][2][eachSubId][1]:
                        html += '<li style="margin-top:6px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style="font-family:\'微软雅黑\'; font-size:17px; color:#111111;">'+ eachExampleList[0] +'</span></li><p style="margin-top:0px; margin-bottom:6px; margin-left:0px; margin-right:0px; -qt-block-indent:2; text-indent:0px;"><span style="font-family:\'微软雅黑\'; font-size:17px; color:#444444;">'+ eachExampleList[1] +'</span></p>'
                    html += '</ul>'
            html += '<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'微软雅黑\'; font-size:10pt; color:#111111;"><br /></p><p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'微软雅黑\'; font-size:10pt; color:#111111;"><br /></p><p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'微软雅黑\'; font-size:10pt; color:#111111;"><br /></p></ul></body></html>'
        except Exception:
            return sourceList
        return html

    def showWordDetails(self,index):
        self.resultText.setHtml(self.fromtHtml(fetchWord(self._wordList[index][1])))

MutexList = [QMutex(),QMutex(),QMutex(),QMutex()]

class TranslatorThread(QThread):
    _signal = pyqtSignal(int, str)

    def __init__(self, source: str, translatorType: int, aimTextEdit: int):
        super().__init__()
        self.TranslatorList = [
            YoudaoTranslator, CaiYunTranslator, BaiduTranslator, TencentTranslator]
        self.source = source
        self.translatorType = translatorType
        self.aimTextEdit = aimTextEdit

    def run(self):
        MutexList[self.aimTextEdit].lock()
        result = self.TranslatorList[self.translatorType](self.source)
        self._signal.emit(self.aimTextEdit, result)
        MutexList[self.aimTextEdit].unlock()

class TransAssistant_class(QtWidgets.QMainWindow, Ui_OCR_Window):
    ocrHotkeyPressed = pyqtSignal()

    def setupUi(self, OCR_Window):
        super(TransAssistant_class, self).setupUi(OCR_Window)
        OCR_Window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        OCR_Window.setWindowOpacity(0.8)
        OCR_Window.OCRButton.setEnabled(self.AreaInit)
        OCR_Window.OCRButtonPlus.setEnabled(self.AreaInit)
        DesktopSize = QApplication.desktop()
        OCR_Window.move(DesktopSize.width() * 0.54, DesktopSize.height() * 0.41)
        # OCR_Window.setAttribute(QtCore.Qt.WA_TranslucentBackground,True)

    def __init__(self):
        super(TransAssistant_class, self).__init__()
        self.AreaInit = False
        self.ScreenPos = [(0, 0), (0, 0)]
        self.selectionText = str()
        self.OCRText = str()
        self.SplitMode = "sudachi"
        self.Hotkey_OCR = ["control", "space"]
        SystemHotkey().register(
            self.Hotkey_OCR,
            callback=lambda x: self.sendHotkeyPressedSig(self.Hotkey_OCR),
        )
        Dict_Window = dictWindow_class()
        self.selectionTextChange = Dict_Window.selectionTextChange
        self.dictWindow = Dict_Window
        self.setupUi(self)
        self.autoDict = self.autoDictCheckBox.isChecked()
        self.resultTextEditList = self.TransResult_0,self.TransResult_1,self.TransResult_2,self.TransResult_3

    def updateSelectionText(self):
        if(self.OCRResultTextEdit.hasFocus()):
            self.selectionText = self.OCRResultTextEdit.textCursor().selectedText()
        elif(self.splitTextEdit.hasFocus()):
            self.selectionText = self.splitTextEdit.textCursor().selectedText()
        if(self.autoDict):
            self.showDictWindow()

    def updateAutoDictBool(self,_bool):
        self.autoDict = _bool

    def closeEvent(self, event):
        self.dictWindow.close()

    def sendHotkeyPressedSig(self, Hotkeys):
        if Hotkeys is self.Hotkey_OCR:
            self.ocrHotkeyPressed.emit()

    def getScreenPos(self):
        self.hide()
        self.ScreenPos = getScreenPos()
        self.PosText.setText(
            f'{(self.ScreenPos[0], self.ScreenPos[1])},'
            + str(
                (
                    self.ScreenPos[0] + self.ScreenPos[2],
                    self.ScreenPos[1] + self.ScreenPos[3],
                )
            )
        )

        self.show()
        self.AreaInit = True
        self.OCRButton.setEnabled(self.AreaInit)
        self.OCRButtonPlus.setEnabled(self.AreaInit)
        # print(self.ScreenPos)

    def getOCRText(self):
        if self.AreaInit:
            self.OCRText = getOCRResult(getScreenshot(self.ScreenPos))
            self.OCRResultTextEdit.setPlainText(self.OCRText)

    def appendOCRText(self):
        if self.AreaInit:
            self.OCRText += getOCRResult(getScreenshot(self.ScreenPos))
            self.OCRResultTextEdit.setPlainText(self.OCRText)

    def updateResultTextEdit(self,aimTextEdit:int,text:str):
        text = nameReplace(text,True)
        self.resultTextEditList[aimTextEdit].setPlainText(text)

    def updateResults(self):
        source = self.OCRResultTextEdit.toPlainText()
        if source != "":
            self.updateSplitTextEdit(source)
            source = nameReplace(source)
            self.t0,self.t1,self.t2,self.t3 = TranslatorThread(source,0,0),TranslatorThread(source,1,1),TranslatorThread(source,2,2),TranslatorThread(source,3,3)
            self.t0._signal.connect(self.updateResultTextEdit)
            self.t1._signal.connect(self.updateResultTextEdit)
            self.t2._signal.connect(self.updateResultTextEdit)
            self.t3._signal.connect(self.updateResultTextEdit)
            self.t0.start()
            self.t1.start()
            self.t2.start()
            self.t3.start()

    def updateSplitMode(self, mode):
        self.SplitMode = mode
        source = self.OCRResultTextEdit.toPlainText()
        if source != "":
            self.updateSplitTextEdit(source)

    def updateSplitTextEdit(self, source):
        self.splitTextEdit.setPlainText(splitWords(source, self.SplitMode))

    def updateOCRHotkey(self, text):
        print(text)
        self.keyPressEvent

    def showDictWindow(self):
        self.dictWindow.show()
        self.selectionTextChange.emit(self.selectionText)


def runGUI():
    GUI_APP = QtWidgets.QApplication(sys.argv)
    GUI_mainWindow = TransAssistant_class()
    GUI_mainWindow.setFixedSize(GUI_mainWindow.width(), GUI_mainWindow.height())
    GUI_mainWindow.show()
    GUI_APP.exec_()


if __name__ == "__main__":
    # print(runGUI())
    runGUI()
