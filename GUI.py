# -*- coding: utf-8 -*-
import sys
from PyQt6 import QtWidgets
from PyQt6.QtCore import pyqtSignal, QThread, QMutex, Qt
from OCR_style import Ui_OCR_Window
from Screenshot import getScreenPos, getScreenshot
from OCR import getOCRResult
from TranslatorAPI import YoudaoTranslator, CaiYunTranslator, BaiduTranslator, TencentTranslator, reloadConfig
from MojiAPI import searchWord, fetchWord
from Segmentation import splitWords
from dict_style import Ui_dict_Window
from config_style import Ui_Config
from Config import readConfig, writeConfig, isInit
import keyboard
# from var_dump import var_dump


# 字典的要求
# 1.中间词不能是常用词汇
# 2.中间词要尽量保证在中日互译时不会产生歧义
# 3.中间词不能在中日互译时发生繁简转换
# 4.要实现贪婪匹配，子串应在母串之后出现
JPNameDict = {
    "モブ美さん": "佐藤",
    "モブ美": "佐藤",
    "モブ男さん": "田中",
    "モブ男くん": "田中",
    "モブ男": "田中",
    "モブくん": "中村",
    "失恋フラグさん": "井上",
    "失恋フラグ": "井上",
    "フラグちゃん": "山本",
    "死亡フラグさん": "小林",
    "死亡フラグ": "小林",
    "恋愛フラグさん": "伊藤",
    "恋愛フラグ": "伊藤",
    "生存フラグさん": "加藤",
    "生存フラグ": "加藤",
    "しーちゃん": "森中",
    "せーちゃん": "石川",
    "れんれん": "松下",
}
ZhNameDict = {
    "佐藤": "小美",
    "田中": "路人男",
    "中村": "路人君",
    "井上": "失恋flag",
    "山本": "flag酱",
    "小林": "死亡flag",
    "伊藤": "恋爱flag",
    "加藤": "生存flag",
    "森中": "死酱",
    "石川": "生酱",
    "松下": "恋恋",
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
    the string "Hello.", and the mappings
    {"He": "Cia", ".": "!"}, it would return " Ciallo!".

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

class configWidget_class(QtWidgets.QWidget, Ui_Config):
    def __init__(self, parent) -> None:
        super().__init__()
        self.setupUi(self)
        self.parent = parent
        self.Hotkey_OCR = parent.Hotkey_OCR
        self.OCRKeyEdit.hide(); self.cancelHotKeyButton.hide(); self.confirmHotKeyButton.hide();

    def closeEvent(self, event):
        self.parent.Status = True

    def setupUi(self, Config):
        super().setupUi(Config)
        Config.setWindowOpacity(0.9)
        Config.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
    
    def replaceWithCurrentConfig(self):
        self.Label_ShortcutKeyText.setText(self.parent.Hotkey_OCR)
        configDict = readConfig()
        self.LineEdit_YoudaoKEY.setText(configDict["YOUDAO_KEY"])
        self.LineEdit_YoudaoSECRET.setText(configDict["YOUDAO_SECRET"])
        self.LineEdit_CaiYunSECRET.setText(configDict["CAIYUN_TOKEN"])
        self.LineEdit_BaiduKEY.setText(configDict["BAIDU_APPID"])
        self.LineEdit_BaiduSECRET.setText(configDict["BAIDU_SECRETKEY"])
        self.LineEdit_TencentKEY.setText(configDict["TENCENT_SECERTID"])
        self.LineEdit_TencentSECRET.setText(configDict["TENCENT_SECERTKEY"])
    
    def getIntoHotKeyChangeMode(self):
        print('请摁下快捷键!')
        self.OCRKeyEdit.show(); self.confirmHotKeyButton.show(); self.cancelHotKeyButton.show(); self.changeHotKeyButton.hide(); self.Label_ShortcutKeyText.hide()
    
    def confirmHotkey(self):
        if(not self.OCRKeyEdit._string):
            self.cancelHotKey()
            return
        self.Hotkey_OCR = self.OCRKeyEdit._string.replace('+',' + ')
        self.Label_ShortcutKeyText.setText(self.OCRKeyEdit._string)
        print(f'热键已更改为: {self.Hotkey_OCR}')
        self.OCRKeyEdit.hide(); self.confirmHotKeyButton.hide(); self.cancelHotKeyButton.hide(); self.changeHotKeyButton.show(); self.Label_ShortcutKeyText.show()
    
    def cancelHotKey(self):
        self.OCRKeyEdit.hide(); self.confirmHotKeyButton.hide(); self.cancelHotKeyButton.hide(); self.changeHotKeyButton.show(); self.Label_ShortcutKeyText.show()
        print('已取消更改热键')
    
    def saveConfig(self):
        data = {'YOUDAO_KEY': self.LineEdit_YoudaoKEY.text(), 
                'YOUDAO_SECRET': self.LineEdit_YoudaoSECRET.text(), 
                'CAIYUN_TOKEN': self.LineEdit_CaiYunSECRET.text(),
                'BAIDU_APPID': self.LineEdit_BaiduKEY.text(), 
                'BAIDU_SECRETKEY': self.LineEdit_BaiduSECRET.text(), 
                'TENCENT_SECERTID': self.LineEdit_TencentKEY.text(), 
                'TENCENT_SECERTKEY': self.LineEdit_TencentSECRET.text()
                }
        writeConfig(data)
        self.parent.changeHotkey(self.Hotkey_OCR)
        reloadConfig()
        self.close()


class dictWindow_class(QtWidgets.QMainWindow, Ui_dict_Window):
    selectionTextChange = pyqtSignal(str)

    def __init__(self):
        super(dictWindow_class, self).__init__()
        self.setupUi(self)
        self.autoSearch = self.autoSearchCheckBox.isChecked()
        self._wordList = []
        self.needToSearch = False

    def setupUi(self, Config):
        super(dictWindow_class, self).setupUi(Config)
        Config.setWindowOpacity(0.9)
        Config.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)

    def updateAutoSearch(self,_bool):
        self.autoSearch = _bool

    def showEvent(self,event):
        super(dictWindow_class,self).showEvent(event)

    def searchWord(self):
        self.wordsList.clear()
        source = self.inputLineEdit.text()
        if(source):
            self._wordList = searchWord(source)
            tempItemList = tuple(each[0] for each in self._wordList)
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

    def setupUi(self, Config):
        super(TransAssistant_class, self).setupUi(Config)
        Config.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        Config.setWindowOpacity(0.8)
        Config.OCRButton.setEnabled(self.AreaInit)
        Config.OCRButtonPlus.setEnabled(self.AreaInit)
        DesktopSize = self.screen().availableSize()
        Config.move(DesktopSize.width() * 0.54, DesktopSize.height() * 0.41)
        # Config.setAttribute(QtCore.Qt.WA_TranslucentBackground,True)

    def __init__(self):
        super(TransAssistant_class, self).__init__()
        self.AreaInit = False
        self.Status = True
        self.ScreenPos = [(0, 0), (0, 0)]
        self.selectionText = str()
        self.OCRText = str()
        self.setupUi(self)
        self.SplitMode = "sudachi"
        self.Hotkey_OCR = "Ctrl + Space"
        self.ShortcutKeyText.setText(self.Hotkey_OCR)
        self.registerHotkey(self.Hotkey_OCR)
        self.dictWindow = dictWindow_class()
        self.configWidget = configWidget_class(self)
        self.selectionTextChange = self.dictWindow.selectionTextChange
        self.autoDict = self.autoDictCheckBox.isChecked()
        self.resultTextEditList = self.TransResult_0,self.TransResult_1,self.TransResult_2,self.TransResult_3
        self.autoTrans = True
        if(not isInit):
            self.showConfig()

    def registerHotkey(self,hotkeys):
        keyboard.add_hotkey(hotkeys,lambda: self.sendHotkeyPressedSig(hotkeys))

    def getIntoHotKeyChangeMode(self):
        self.showConfig()

    def changeHotkey(self,_hotkey):
        _hotkeyTemp = self.Hotkey_OCR
        keyboard.clear_hotkey(self.Hotkey_OCR)
        self.Hotkey_OCR = _hotkey
        self.registerHotkey(self.Hotkey_OCR)
        self.ShortcutKeyText.setText(self.Hotkey_OCR)
        print(f'热键已由 {_hotkeyTemp} 更改为 {self.Hotkey_OCR}')

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

    def showConfig(self):
        self.Status = False
        self.configWidget.replaceWithCurrentConfig()
        self.configWidget.show()

    def getScreenPos(self):
        self.hide()
        self.ScreenPos = getScreenPos()
        self.PosText.setText(f'{(self.ScreenPos[0], self.ScreenPos[1])},'+ str((self.ScreenPos[0] + self.ScreenPos[2],self.ScreenPos[1] + self.ScreenPos[3])))
        self.show()
        self.AreaInit = True
        if(((self.ScreenPos[0], self.ScreenPos[1])==(self.ScreenPos[0] + self.ScreenPos[2],self.ScreenPos[1] + self.ScreenPos[3])) or 0 in (self.ScreenPos[2],self.ScreenPos[3])):
            self.AreaInit = False
            print('非法选区，请重选！')
            QtWidgets.QMessageBox.critical(self,"非法选区","选区不合法，请重选！")
        self.OCRButton.setEnabled(self.AreaInit)
        self.OCRButtonPlus.setEnabled(self.AreaInit)

    def doAutoTrans(self):
        if(self.autoTrans):
            self.updateResults()

    def getOCRText(self):
        if(self.AreaInit and self.Status):
            self.OCRText = getOCRResult(getScreenshot(self.ScreenPos))
            self.OCRResultTextEdit.setPlainText(self.OCRText)
            self.doAutoTrans()

    def updateOCRText(self):
        self.OCRText = self.OCRResultTextEdit.toPlainText()

    def appendOCRText(self):
        if(self.AreaInit and self.Status):
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
            source = nameReplace(source, False)
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

if __name__ == "__main__":
    runGUI()
