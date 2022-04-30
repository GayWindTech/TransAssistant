# -*- coding: utf-8 -*-
import contextlib
import sys
from PyQt6 import QtWidgets
from PyQt6.QtCore import pyqtSignal, QThread, QMutex, Qt
from OCR_style import Ui_OCR_Window
from getSecret_style import Ui_getSecretWidget
from Screenshot import getScreenPos, getScreenshot
from OCR import getOCRResult, getOCRSecret, checkSecretAvailable, reloadOCRConfig
from TranslatorAPI import TranslatorMapping, reloadTranslatorConfig
from MojiAPI import searchWord, fetchWord
from Segmentation import splitWords
from dict_style import Ui_dict_Window
from config_style import Ui_Config
from Config import readConfig, writeConfig, isInit
import keyboard
from customerDefineDict import ZhNameDict, JPNameDict
# from var_dump import var_dump

def keymap_replace(
    string: str,
    mappings: dict,
    lower_keys=False,
    lower_values=False,
    lower_string=False,
) -> str:
    """Replace parts of a string based on a dictionary.

    This function takes a string a dictionary of replacement mappings. 
    For example, if I supplied the string "Hello." and the mappings {"He": "Cia", ".": "!"}, 
    it would return " Ciallo!".

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

class getSecretWidget_class(QtWidgets.QWidget, Ui_getSecretWidget):
    def __init__(self, parent) -> None:
        super().__init__()
        self.setupUi(self)
        self.parent = parent
    
    def setupUi(self, Config):
        super().setupUi(Config)
        Config.setWindowOpacity(0.9)
        Config.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
    
    def fillListWithSecret(self):
        self.secretList = getOCRSecret()
        self.ListWidget_Secrets.addItems((each[1] for each in self.secretList))
    
    def checkSecret(self):
        _tempList = self.secretList[self.ListWidget_Secrets.currentRow()]
        self.ListWidget_Secrets.item(self.ListWidget_Secrets.currentRow()).setBackground(Qt.GlobalColor.gray)
        if(checkSecretAvailable(_tempList[0], _tempList[1], _tempList[2])):
            self.ListWidget_Secrets.item(self.ListWidget_Secrets.currentRow()).setBackground(Qt.GlobalColor.green)
            self.PushButton_Confirm.setEnabled(True)
            return
        self.ListWidget_Secrets.item(self.ListWidget_Secrets.currentRow()).setBackground(Qt.GlobalColor.red)
        self.PushButton_Confirm.setEnabled(False)
    
    def checkCurrectIsAvailable(self):
        if(self.ListWidget_Secrets.item(self.ListWidget_Secrets.currentRow()).background().color() == Qt.GlobalColor.green):
            self.PushButton_Confirm.setEnabled(True)
            return
        self.PushButton_Confirm.setEnabled(False)
    
    def save(self):
        _APPID, _SECRET, _KEY = self.secretList[self.ListWidget_Secrets.currentRow()]
        self.parent.LineEdit_OCRAPPID.setText(_APPID)
        self.parent.LineEdit_OCRSECRET.setText(_SECRET)
        self.parent.LineEdit_OCRKEY.setText(_KEY)
        print('OCR密钥已设置！')
        self.close()

class configWidget_class(QtWidgets.QWidget, Ui_Config):
    def __init__(self, parent) -> None:
        super().__init__()
        self.setupUi(self)
        self.ListWidget_SelectedSource.setDragDropMode(QtWidgets.QAbstractItemView.DragDropMode.InternalMove)
        self.parent = parent
        self.Hotkey_OCR = parent.Hotkey_OCR
        self.OCRKeyEdit.hide(); self.cancelHotKeyButton.hide(); self.confirmHotKeyButton.hide()
        self.LineEditMapping = {
            'YOUDAO_KEY': self.LineEdit_YoudaoKEY,
            'YOUDAO_SECRET': self.LineEdit_YoudaoSECRET,
            'CAIYUN_TOKEN': self.LineEdit_CaiYunTOKEN,
            'BAIDU_APPID': self.LineEdit_BaiduAPPID,
            'BAIDU_SECRETKEY': self.LineEdit_BaiduSECRETKEY,
            'TENCENT_SECERTID': self.LineEdit_TencentKEY,
            'TENCENT_SECERTKEY': self.LineEdit_TencentSECRET,
            'XIAONIU_KEY': self.LineEdit_XiaoNiuKEY,
            'ALIYUN_KEY': self.LineEdit_AliYunKEY,
            'ALIYUN_SECRET': self.LineEdit_AliYunSECRET,
            'OCR_APPID': self.LineEdit_OCRAPPID,
            'OCR_SECRET': self.LineEdit_OCRSECRET,
            'OCR_KEY': self.LineEdit_OCRKEY,
        }
        self.FreeRiderMapping = {
                'YOUDAO_FREE_RIDER': self.CheckBox_Youdao,
                'CAIYUN_FREE_RIDER': self.CheckBox_CaiYun,
                'BAIDU_FREE_RIDER': self.CheckBox_Baidu,
                'TENCENT_FREE_RIDER': self.CheckBox_Tencent,
        }
        self.getSecretWidget = getSecretWidget_class(self)

    def closeEvent(self, event):
        self.parent.Status = True
        self.parent.setEnabled(True)

    def setupUi(self, Config):
        super().setupUi(Config)
        Config.setWindowOpacity(0.9)
        Config.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
    
    def replaceWithCurrentConfig(self):
        self.ListWidget_SelectableSource.clear()
        self.ListWidget_SelectedSource.clear()
        self.Label_ShortcutKeyText.setText(self.parent.Hotkey_OCR)
        configDict = readConfig()
        [self.LineEditMapping[each].setText(configDict[each]) for each in self.LineEditMapping]
        [self.FreeRiderMapping[each].setChecked(configDict[each]) for each in self.FreeRiderMapping]
        for eachTranslator in [each for each in TranslatorMapping if each not in configDict['SELECTED_TRANSLATORS']]:
            self.ListWidget_SelectableSource.addItem(eachTranslator)
        for each in configDict['SELECTED_TRANSLATORS']:
            self.ListWidget_SelectedSource.addItem(each)

    def addTranslator(self):
        if(self.ListWidget_SelectableSource.currentItem()):
            self.ListWidget_SelectedSource.addItem(self.ListWidget_SelectableSource.currentItem().text())
            self.ListWidget_SelectableSource.takeItem(self.ListWidget_SelectableSource.currentRow())
        self.checkSelectedTranslatorCount()

    def removeTranslator(self):
        if(self.ListWidget_SelectedSource.currentItem()):
            self.ListWidget_SelectableSource.addItem(self.ListWidget_SelectedSource.currentItem().text())
            self.ListWidget_SelectedSource.takeItem(self.ListWidget_SelectedSource.currentRow())
        self.checkSelectedTranslatorCount()

    def upTranslator(self):
        if(self.ListWidget_SelectedSource.currentItem()):
            _currentRow = self.ListWidget_SelectedSource.currentRow()
            self.ListWidget_SelectedSource.insertItem(self.ListWidget_SelectedSource.currentRow()-1, self.ListWidget_SelectedSource.takeItem(self.ListWidget_SelectedSource.currentRow()))
            self.ListWidget_SelectedSource.setCurrentRow(_currentRow-1)

    def downTranslator(self):
        if(self.ListWidget_SelectedSource.currentItem()):
            _currentRow = self.ListWidget_SelectedSource.currentRow()
            self.ListWidget_SelectedSource.insertItem(self.ListWidget_SelectedSource.currentRow()+1, self.ListWidget_SelectedSource.takeItem(self.ListWidget_SelectedSource.currentRow()))
            self.ListWidget_SelectedSource.setCurrentRow(_currentRow+1)

    def getCurrentSelectedTranslator(self):
        return [self.ListWidget_SelectedSource.item(i).text() for i in range(self.ListWidget_SelectedSource.count())]

    def checkSelectedTranslatorCount(self):
        if self.ListWidget_SelectedSource.count() >= 4:
            self.PushButton_SourceEnable.setEnabled(False)
        else:
            self.PushButton_SourceEnable.setEnabled(True)

    def getIntoHotKeyChangeMode(self):
        print('请摁下快捷键!')
        self.OCRKeyEdit.show(); self.confirmHotKeyButton.show(); self.cancelHotKeyButton.show(); self.changeHotKeyButton.hide(); self.Label_ShortcutKeyText.hide()
    
    def confirmHotkey(self):
        if(not self.OCRKeyEdit._string):
            self.cancelHotKey()
            return
        self.Hotkey_OCR = self.OCRKeyEdit._string.replace('+',' + ')
        self.Label_ShortcutKeyText.setText(self.OCRKeyEdit._string)
        print(f'热键将更改为: {self.Hotkey_OCR}')
        self.OCRKeyEdit.hide(); self.confirmHotKeyButton.hide(); self.cancelHotKeyButton.hide(); self.changeHotKeyButton.show(); self.Label_ShortcutKeyText.show()
    
    def cancelHotKey(self):
        self.OCRKeyEdit.hide(); self.confirmHotKeyButton.hide(); self.cancelHotKeyButton.hide(); self.changeHotKeyButton.show(); self.Label_ShortcutKeyText.show()
        print('已取消更改热键')
    
    def showGetSecretWidget(self):
        self.getSecretWidget.show()
    
    def saveConfig(self):
        if(not self.getCurrentSelectedTranslator()):
            QtWidgets.QMessageBox.critical(self,"配置有误","至少选择一个翻译源！")
            return
        data = {each: self.LineEditMapping[each].text() for each in self.LineEditMapping}
        data.update({each: self.FreeRiderMapping[each].isChecked() for each in self.FreeRiderMapping})
        data['SELECTED_TRANSLATORS'] = self.getCurrentSelectedTranslator()
        data['Hotkey_OCR'] = self.Hotkey_OCR
        writeConfig(data)
        self.parent.changeHotkey(self.Hotkey_OCR)
        self.parent.updateTranslatorList(self.getCurrentSelectedTranslator())
        reloadOCRConfig(); reloadTranslatorConfig()
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

    def __init__(self, source: str, translatorType: str, aimTextEdit: int):
        super().__init__()
        self.source = source
        self.translatorType = translatorType
        self.aimTextEdit = aimTextEdit

    def run(self):
        MutexList[self.aimTextEdit].lock()
        self._signal.emit(self.aimTextEdit, '')
        result = TranslatorMapping[self.translatorType](self.source)
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
        self.ConfigDict = readConfig()
        self.AreaInit = False
        self.Status = True
        self.ScreenPos = [(0, 0), (0, 0)]
        self.selectionText = str()
        self.OCRText = str()
        self.setupUi(self)
        self.defaultWidth, self.defaultHeight = self.width(), self.height()
        self.defaultX, self.defaultY = self.geometry().x(), self.geometry().y()
        self.OCRResultTextEdit.setPlainText('')
        self.SplitMode = "sudachi"
        self.Hotkey_OCR = self.ConfigDict['Hotkey_OCR']
        self.changeHotkey(self.Hotkey_OCR)
        self.dictWindow = dictWindow_class()
        self.configWidget = configWidget_class(self)
        self.selectionTextChange = self.dictWindow.selectionTextChange
        self.autoDict = self.autoDictCheckBox.isChecked()
        self.resultTextEditList = self.TransResult_0,self.TransResult_1,self.TransResult_2,self.TransResult_3
        self.updateTranslatorList(self.ConfigDict['SELECTED_TRANSLATORS'])
        self.autoTrans = True
        if(not isInit):
            self.showConfig()

    def registerHotkey(self,hotkeys):
        keyboard.add_hotkey(hotkeys,lambda: self.sendHotkeyPressedSig(hotkeys))

    def getIntoHotKeyChangeMode(self):
        self.showConfig()

    def changeHotkey(self,_hotkey):
        _hotkeyTemp = self.Hotkey_OCR
        with contextlib.suppress(Exception):
            keyboard.clear_hotkey(self.Hotkey_OCR)
        try:
            self.registerHotkey(_hotkey)
            self.Hotkey_OCR = _hotkey
            self.ShortcutKeyText.setText(self.Hotkey_OCR)
            print(f'当前快捷键： {self.Hotkey_OCR}')
        except Exception:
            with contextlib.suppress(Exception):
                self.registerHotkey(_hotkeyTemp)
            print(f'设置{_hotkey}为快捷键失败')

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
        self.setEnabled(self.Status)
        self.configWidget.replaceWithCurrentConfig()
        self.configWidget.show()

    def getScreenPos(self):
        self.hide()
        self.ScreenPos = getScreenPos()
        self.PosText.setText(f'{(self.ScreenPos[0], self.ScreenPos[1])},{(self.ScreenPos[0] + self.ScreenPos[2], self.ScreenPos[1] + self.ScreenPos[3])}')
        self.show()
        self.AreaInit = True
        if(((self.ScreenPos[0], self.ScreenPos[1])==(self.ScreenPos[0] + self.ScreenPos[2],self.ScreenPos[1] + self.ScreenPos[3])) or 0 in (self.ScreenPos[2],self.ScreenPos[3])):
            self.AreaInit = False
            print('非法选区，请重选！')
            QtWidgets.QMessageBox.critical(self,"非法选区","选区不合法，请重选！")
        if self.AreaInit: self.OCRResultTextEdit.setPlaceholderText('')
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
            self.TranslatorTreadList = [TranslatorThread(source, eachTranslator, n) for n, eachTranslator in enumerate(self.TranslatorList)]
            for eachTread in self.TranslatorTreadList:
                eachTread._signal.connect(self.updateResultTextEdit)
                eachTread.start()

    def updateTranslatorList(self, _list:list):
        self.TranslatorList = _list
        print(f'当前翻译源为：{self.TranslatorList}')
        [self.resultTextEditList[n].setPlaceholderText(eachTranslator) for n, eachTranslator in enumerate(self.TranslatorList)]
        _len = _list.__len__()
        if _len < 4:
            if _len == 0: _len = 1
            [each.setVisible(False) for each in self.resultTextEditList[_len-4:]]
            n = 80*(4-_len)
            self.setFixedSize(self.defaultWidth, self.defaultHeight-n)
            self.move(self.defaultX, self.defaultY+n)
        else:
            [each.setVisible(True) for each in self.resultTextEditList]
            self.setFixedSize(self.defaultWidth, self.defaultHeight)
            self.move(self.defaultX, self.defaultY)

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
    GUI_mainWindow.show()
    GUI_APP.exec()

if __name__ == "__main__":
    runGUI()
