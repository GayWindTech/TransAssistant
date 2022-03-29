import sys
from system_hotkey import SystemHotkey
from PyQt6 import QtWidgets
from PyQt6.QtCore import pyqtSignal, QThread, QMutex, Qt
from OCR_style import Ui_OCR_Window
from Screenshot import getScreenPos, getScreenshot
from OCR import getOCRResult
from TranslatorAPI import YoudaoTranslator, CaiYunTranslator, BaiduTranslator, TencentTranslator
from MojiAPI import searchWord, fetchWord
from Segmentation import splitWords
from dict_style import Ui_dict_Window
# from var_dump import var_dump
import logging
#QGuiApplication::screens

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
        self.autoSearch = self.autoSearchCheckBox.isChecked()
        self._wordList = []
        self.needToSearch = False

    def setupUi(self, dictMain):
        super(dictWindow_class, self).setupUi(dictMain)
        dictMain.setWindowOpacity(0.9)
        dictMain.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)

    def updateAutoSearch(self,_bool):
        self.autoSearch = _bool

    def showEvent(self,event):
        super(dictWindow_class,self).showEvent(event)

    def searchWord(self):
        self.wordsList.clear()
        source = self.inputLineEdit.text()
        if(source):
            self._wordList = searchWord(source)
            tempItemList = (each[0] for each in searchWord(source))
            self.wordsList.addItems(tempItemList)
            self.wordsList.setCurrentItem(self.wordsList.item(0))

    def setQueryWord(self,word):
        self.inputLineEdit.setText(word)

    def editingFinished(self):
        if(self.autoSearch):
            self.searchWord()

    def returnPressed(self):
        if(not self.autoSearch):
            self.searchWord()

    def fromtHtml(self,sourceList) -> str:
        try:
            html = f'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd"><html><head><meta name="qrichtext" content="1" /><style type="text/css">p, li {{ white-space: pre-wrap; }}</style></head><body><p style="margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style="font-family:\'Microsoft Yahei\'; font-size:25pt; font-weight:600; color:#111111;">{sourceList[0][0]}</span></p><p style="margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style="font-family:\'Microsoft Yahei\'; font-size:15pt; color:#111111;">{sourceList[0][2]} {sourceList[0][3]}</span></p><p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Microsoft Yahei\'; font-size:10pt; color:#111111;"><br /></p>'
            for eachId in sourceList[1][0]:
                html += '<p style="margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style="font-family:\'Microsoft Yahei\'; font-size:23px; font-weight:600; color:#111111;">'+ sourceList[1][1][eachId][0] +'：</span></p><ul style="margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;">'
                for eachSubId in sourceList[1][1][eachId][1]:
                    html += '<li style="margin-top:6px; margin-bottom:6px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style="font-family:\'Microsoft Yahei\'; font-size:17px; color:#111111; text-decoration: underline;">'+ sourceList[1][1][eachId][2][eachSubId][0] +'</span></li><ul style="margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 2;">'
                    for eachExampleList in sourceList[1][1][eachId][2][eachSubId][1]:
                        html += '<li style="margin-top:6px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style="font-family:\'Microsoft Yahei\'; font-size:17px; color:#111111;">'+ eachExampleList[0] +'</span></li><p style="margin-top:0px; margin-bottom:6px; margin-left:0px; margin-right:0px; -qt-block-indent:2; text-indent:0px;"><span style="font-family:\'Microsoft Yahei\'; font-size:17px; color:#444444;">'+ eachExampleList[1] +'</span></p>'
                    html += '</ul>'
            html += '<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Microsoft Yahei\'; font-size:10pt; color:#111111;"><br /></p><p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Microsoft Yahei\'; font-size:10pt; color:#111111;"><br /></p><p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Microsoft Yahei\'; font-size:10pt; color:#111111;"><br /></p></ul></body></html>'
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
        OCR_Window.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        OCR_Window.setWindowOpacity(0.8)
        OCR_Window.OCRButton.setEnabled(self.AreaInit)
        OCR_Window.OCRButtonPlus.setEnabled(self.AreaInit)
        DesktopSize = self.screen().availableSize()
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
        self.registerHotkey(self.Hotkey_OCR)
        Dict_Window = dictWindow_class()
        self.selectionTextChange = Dict_Window.selectionTextChange
        self.dictWindow = Dict_Window
        self.setupUi(self)
        self.OCRKeyEdit.hide()
        self.autoDict = self.autoDictCheckBox.isChecked()
        self.resultTextEditList = self.TransResult_0,self.TransResult_1,self.TransResult_2,self.TransResult_3
        self.autoTrans = True

    def registerHotkey(self,hotkeys):
        SystemHotkey().register(
            hotkeys,
            callback=lambda x: self.sendHotkeyPressedSig(hotkeys),
        )

    def print(self,text):
        print(self.OCRKeyEdit._string)

    def updateSelectionText(self):
        if(self.OCRResultTextEdit.hasFocus()):
            self.selectionText = self.OCRResultTextEdit.textCursor().selectedText()
        elif(self.splitTextEdit.hasFocus()):
            self.selectionText = self.splitTextEdit.textCursor().selectedText()
        if(self.autoDict):
            self.showDictWindow()

    def updateAutoTransBool(self,_bool):
        self.autoTrans = _bool

    def updateAutoDictBool(self,_bool):
        self.autoDict = _bool

    def closeEvent(self, event):
        self.dictWindow.close()

    def sendHotkeyPressedSig(self, Hotkeys):
        if(Hotkeys is self.Hotkey_OCR):
            self.ocrHotkeyPressed.emit()

    def getScreenPos(self):
        self.hide()
        self.ScreenPos = getScreenPos()
        self.PosText.setText(f'{(self.ScreenPos[0], self.ScreenPos[1])},'+ str((self.ScreenPos[0] + self.ScreenPos[2],self.ScreenPos[1] + self.ScreenPos[3])))

        self.show()
        if(((self.ScreenPos[0], self.ScreenPos[1])==(self.ScreenPos[0] + self.ScreenPos[2],self.ScreenPos[1] + self.ScreenPos[3])) or 0 in (self.ScreenPos[2],self.ScreenPos[3])):
            print('非法选区，请重选！')
        else:
            self.AreaInit = True
        self.OCRButton.setEnabled(self.AreaInit)
        self.OCRButtonPlus.setEnabled(self.AreaInit)

    def doAutoTrans(self):
        if(self.autoTrans):
            self.updateResults()

    def getOCRText(self):
        if(self.AreaInit):
            self.OCRText = getOCRResult(getScreenshot(self.ScreenPos))
            self.OCRResultTextEdit.setPlainText(self.OCRText)
        self.doAutoTrans()

    def appendOCRText(self):
        if(self.AreaInit):
            self.OCRText += getOCRResult(getScreenshot(self.ScreenPos))
            self.OCRResultTextEdit.setPlainText(self.OCRText)
        self.doAutoTrans()

    def updateResultTextEdit(self,aimTextEdit:int,text:str):
        text = nameReplace(text,True)
        self.resultTextEditList[aimTextEdit].setPlainText(text)

    def updateResults(self):
        source = self.OCRResultTextEdit.toPlainText()
        self.updateSplitTextEdit(True)
        if(source):
            source = nameReplace(source)
            self.t0,self.t1,self.t2,self.t3 = TranslatorThread(source,0,0),TranslatorThread(source,1,1),TranslatorThread(source,2,2),TranslatorThread(source,3,3)
            self.t0._signal.connect(self.updateResultTextEdit)
            self.t1._signal.connect(self.updateResultTextEdit)
            self.t2._signal.connect(self.updateResultTextEdit)
            self.t3._signal.connect(self.updateResultTextEdit)
            self.t0.start(); self.t1.start(); self.t2.start(); self.t3.start()

    def updateSplitMode(self, mode):
        self.SplitMode = mode
        self.updateSplitTextEdit()

    def updateSplitTextEdit(self,Force=False):
        source = self.OCRResultTextEdit.toPlainText()
        if(source and (Force or self.SplitMode != 'kuromoji')):
            self.splitTextEdit.setPlainText(splitWords(source, self.SplitMode))

    def updateOCRHotkey(self, text):
        print(text)
        self.keyPressEvent

    def showDictWindow(self):
        self.selectionTextChange.emit(self.selectionText)
        self.dictWindow.inputLineEdit.editingFinished.emit()
        self.dictWindow.show()

def runGUI():
    GUI_APP = QtWidgets.QApplication(sys.argv)
    GUI_mainWindow = TransAssistant_class()
    GUI_mainWindow.setFixedSize(GUI_mainWindow.width(), GUI_mainWindow.height())
    GUI_mainWindow.show()
    GUI_APP.exec()

class stdLog(object):
    def __init__(self, name, log_level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.log_level = log_level
        # self.logger.addHandler(logging.FileHandler('log.log',mode='a+'))
        self.logger.addHandler(logging.StreamHandler(sys.__stdout__))
        self.linebuf = ''
    
    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())
    
    def flush(self):
        pass
    
    logging.basicConfig(
        level=logging.DEBUG,
        format='[%(asctime)s][%(levelname)s] %(message)s',
        filename='log.log'
    )

if __name__ == "__main__":
    _stdout = stdLog('STDOUT', logging.INFO)
    sys.stdout = _stdout
    _stderr = stdLog('STDERR', logging.ERROR)
    sys.stderr = _stderr
    runGUI()
