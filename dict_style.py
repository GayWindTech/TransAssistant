# Form implementation generated from reading ui file '.\dict_style.ui'
#
# Created by: PyQt6 UI code generator 6.5.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_dict_Window(object):
    def setupUi(self, dict_Window):
        dict_Window.setObjectName("dict_Window")
        dict_Window.resize(809, 420)
        self.dictMain = QtWidgets.QWidget(parent=dict_Window)
        self.dictMain.setObjectName("dictMain")
        self.wordsList = QtWidgets.QListWidget(parent=self.dictMain)
        self.wordsList.setGeometry(QtCore.QRect(10, 70, 261, 341))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.wordsList.setFont(font)
        self.wordsList.setObjectName("wordsList")
        self.dictSourceChoose = QtWidgets.QComboBox(parent=self.dictMain)
        self.dictSourceChoose.setGeometry(QtCore.QRect(100, 10, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.dictSourceChoose.setFont(font)
        self.dictSourceChoose.setObjectName("dictSourceChoose")
        self.dictSourceChoose.addItem("")
        self.dictSourceChoose.addItem("")
        self.DictSourceLabel = QtWidgets.QLabel(parent=self.dictMain)
        self.DictSourceLabel.setGeometry(QtCore.QRect(30, 10, 61, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.DictSourceLabel.setFont(font)
        self.DictSourceLabel.setObjectName("DictSourceLabel")
        self.resultText = QtWidgets.QTextBrowser(parent=self.dictMain)
        self.resultText.setGeometry(QtCore.QRect(280, 70, 521, 341))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setBold(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.resultText.setFont(font)
        self.resultText.setObjectName("resultText")
        self.autoSearchCheckBox = QtWidgets.QCheckBox(parent=self.dictMain)
        self.autoSearchCheckBox.setGeometry(QtCore.QRect(100, 36, 71, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.autoSearchCheckBox.setFont(font)
        self.autoSearchCheckBox.setChecked(True)
        self.autoSearchCheckBox.setObjectName("autoSearchCheckBox")
        self.inputLineEdit = QtWidgets.QLineEdit(parent=self.dictMain)
        self.inputLineEdit.setGeometry(QtCore.QRect(280, 10, 521, 51))
        font = QtGui.QFont()
        font.setPointSize(19)
        self.inputLineEdit.setFont(font)
        self.inputLineEdit.setText("")
        self.inputLineEdit.setObjectName("inputLineEdit")
        dict_Window.setCentralWidget(self.dictMain)

        self.retranslateUi(dict_Window)
        dict_Window.selectionTextChange.connect(dict_Window.setQueryWord) # type: ignore
        self.wordsList.currentRowChanged['int'].connect(dict_Window.showWordDetails) # type: ignore
        self.autoSearchCheckBox.clicked['bool'].connect(dict_Window.updateAutoSearch) # type: ignore
        self.inputLineEdit.editingFinished.connect(dict_Window.editingFinished) # type: ignore
        self.inputLineEdit.returnPressed.connect(dict_Window.returnPressed) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(dict_Window)

    def retranslateUi(self, dict_Window):
        _translate = QtCore.QCoreApplication.translate
        dict_Window.setWindowTitle(_translate("dict_Window", "WordSearch"))
        self.dictSourceChoose.setItemText(0, _translate("dict_Window", "MojiDict"))
        self.dictSourceChoose.setItemText(1, _translate("dict_Window", "沪江小D词典"))
        self.DictSourceLabel.setText(_translate("dict_Window", "词典来源:"))
        self.resultText.setHtml(_translate("dict_Window", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Microsoft YaHei UI\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.autoSearchCheckBox.setText(_translate("dict_Window", "自动查词"))
