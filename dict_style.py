# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\dict_style.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_dict_Window(object):
    def setupUi(self, dict_Window):
        dict_Window.setObjectName("dict_Window")
        dict_Window.resize(809, 420)
        self.dictMain = QtWidgets.QWidget(dict_Window)
        self.dictMain.setObjectName("dictMain")
        self.wordsList = QtWidgets.QListWidget(self.dictMain)
        self.wordsList.setGeometry(QtCore.QRect(10, 50, 261, 361))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.wordsList.setFont(font)
        self.wordsList.setObjectName("wordsList")
        self.dictSourceChoose = QtWidgets.QComboBox(self.dictMain)
        self.dictSourceChoose.setGeometry(QtCore.QRect(100, 10, 121, 21))
        self.dictSourceChoose.setObjectName("dictSourceChoose")
        self.dictSourceChoose.addItem("")
        self.dictSourceChoose.addItem("")
        self.DictSourceLabel = QtWidgets.QLabel(self.dictMain)
        self.DictSourceLabel.setGeometry(QtCore.QRect(20, 10, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.DictSourceLabel.setFont(font)
        self.DictSourceLabel.setObjectName("DictSourceLabel")
        self.inputTextEdit = QtWidgets.QPlainTextEdit(self.dictMain)
        self.inputTextEdit.setGeometry(QtCore.QRect(280, 10, 521, 51))
        font = QtGui.QFont()
        font.setFamily("思源黑体")
        font.setPointSize(19)
        font.setKerning(True)
        self.inputTextEdit.setFont(font)
        self.inputTextEdit.setPlainText("")
        self.inputTextEdit.setObjectName("inputTextEdit")
        self.resultText = QtWidgets.QTextBrowser(self.dictMain)
        self.resultText.setGeometry(QtCore.QRect(280, 70, 521, 341))
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setBold(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.resultText.setFont(font)
        self.resultText.setObjectName("resultText")
        self.pushButton = QtWidgets.QPushButton(self.dictMain)
        self.pushButton.setGeometry(QtCore.QRect(230, 20, 31, 23))
        self.pushButton.setObjectName("pushButton")
        dict_Window.setCentralWidget(self.dictMain)

        self.retranslateUi(dict_Window)
        self.pushButton.clicked.connect(dict_Window.searchWord) # type: ignore
        dict_Window.selectionTextChange.connect(dict_Window.setQueryWord) # type: ignore
        self.wordsList.currentRowChanged['int'].connect(dict_Window.showWordDetails) # type: ignore
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
"</style></head><body style=\" font-family:\'等线\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.pushButton.setText(_translate("dict_Window", "PushButton"))