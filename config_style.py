# Form implementation generated from reading ui file '.\config_style.ui'
#
# Created by: PyQt6 UI code generator 6.5.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Config(object):
    def setupUi(self, Config):
        Config.setObjectName("Config")
        Config.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        Config.resize(459, 503)
        Config.setMaximumSize(QtCore.QSize(459, 1000))
        Config.setMouseTracking(True)
        Config.setAccessibleName("")
        self.scrollArea = QtWidgets.QScrollArea(parent=Config)
        self.scrollArea.setGeometry(QtCore.QRect(-10, 0, 471, 501))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setMaximumSize(QtCore.QSize(471, 16777215))
        self.scrollArea.setFocusPolicy(QtCore.Qt.FocusPolicy.WheelFocus)
        self.scrollArea.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(False)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, -551, 450, 1050))
        self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(450, 600))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.Label_MasterTitle = QtWidgets.QLabel(parent=self.scrollAreaWidgetContents)
        self.Label_MasterTitle.setGeometry(QtCore.QRect(20, 10, 361, 31))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(21)
        self.Label_MasterTitle.setFont(font)
        self.Label_MasterTitle.setObjectName("Label_MasterTitle")
        self.Label_HelpLink = QtWidgets.QLabel(parent=self.scrollAreaWidgetContents)
        self.Label_HelpLink.setGeometry(QtCore.QRect(350, 50, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.Label_HelpLink.setFont(font)
        self.Label_HelpLink.setOpenExternalLinks(True)
        self.Label_HelpLink.setObjectName("Label_HelpLink")
        self.LineEdit_CaiYunTOKEN = QtWidgets.QLineEdit(parent=self.scrollAreaWidgetContents)
        self.LineEdit_CaiYunTOKEN.setGeometry(QtCore.QRect(30, 190, 411, 31))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.LineEdit_CaiYunTOKEN.setFont(font)
        self.LineEdit_CaiYunTOKEN.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        self.LineEdit_CaiYunTOKEN.setObjectName("LineEdit_CaiYunTOKEN")
        self.LineEdit_BaiduAPPID = QtWidgets.QLineEdit(parent=self.scrollAreaWidgetContents)
        self.LineEdit_BaiduAPPID.setGeometry(QtCore.QRect(30, 240, 411, 31))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.LineEdit_BaiduAPPID.setFont(font)
        self.LineEdit_BaiduAPPID.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        self.LineEdit_BaiduAPPID.setObjectName("LineEdit_BaiduAPPID")
        self.confirmHotKeyButton = QtWidgets.QPushButton(parent=self.scrollAreaWidgetContents)
        self.confirmHotKeyButton.setGeometry(QtCore.QRect(240, 570, 41, 21))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        self.confirmHotKeyButton.setFont(font)
        self.confirmHotKeyButton.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.confirmHotKeyButton.setStatusTip("")
        self.confirmHotKeyButton.setWhatsThis("")
        self.confirmHotKeyButton.setAccessibleDescription("")
        self.confirmHotKeyButton.setObjectName("confirmHotKeyButton")
        self.LineEdit_TencentSECRET = QtWidgets.QLineEdit(parent=self.scrollAreaWidgetContents)
        self.LineEdit_TencentSECRET.setGeometry(QtCore.QRect(30, 350, 411, 31))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.LineEdit_TencentSECRET.setFont(font)
        self.LineEdit_TencentSECRET.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        self.LineEdit_TencentSECRET.setObjectName("LineEdit_TencentSECRET")
        self.changeHotKeyButton = QtWidgets.QPushButton(parent=self.scrollAreaWidgetContents)
        self.changeHotKeyButton.setGeometry(QtCore.QRect(240, 570, 41, 21))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        self.changeHotKeyButton.setFont(font)
        self.changeHotKeyButton.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.changeHotKeyButton.setStatusTip("")
        self.changeHotKeyButton.setWhatsThis("")
        self.changeHotKeyButton.setAccessibleDescription("")
        self.changeHotKeyButton.setObjectName("changeHotKeyButton")
        self.OCRKeyEdit = oneKeyQKeySequenceEdit(parent=self.scrollAreaWidgetContents)
        self.OCRKeyEdit.setGeometry(QtCore.QRect(100, 570, 131, 20))
        self.OCRKeyEdit.setKeySequence("")
        self.OCRKeyEdit.setObjectName("OCRKeyEdit")
        self.Label_XiaoNiu = QtWidgets.QLabel(parent=self.scrollAreaWidgetContents)
        self.Label_XiaoNiu.setGeometry(QtCore.QRect(30, 380, 91, 20))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.Label_XiaoNiu.setFont(font)
        self.Label_XiaoNiu.setObjectName("Label_XiaoNiu")
        self.Label_CaiYun = QtWidgets.QLabel(parent=self.scrollAreaWidgetContents)
        self.Label_CaiYun.setGeometry(QtCore.QRect(30, 170, 91, 20))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.Label_CaiYun.setFont(font)
        self.Label_CaiYun.setObjectName("Label_CaiYun")
        self.LineEdit_YoudaoSECRET = QtWidgets.QLineEdit(parent=self.scrollAreaWidgetContents)
        self.LineEdit_YoudaoSECRET.setGeometry(QtCore.QRect(30, 140, 411, 31))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.LineEdit_YoudaoSECRET.setFont(font)
        self.LineEdit_YoudaoSECRET.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        self.LineEdit_YoudaoSECRET.setObjectName("LineEdit_YoudaoSECRET")
        self.Button_Save = QtWidgets.QPushButton(parent=self.scrollAreaWidgetContents)
        self.Button_Save.setGeometry(QtCore.QRect(380, 10, 51, 31))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.Button_Save.setFont(font)
        self.Button_Save.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.Button_Save.setObjectName("Button_Save")
        self.Label_Baidu = QtWidgets.QLabel(parent=self.scrollAreaWidgetContents)
        self.Label_Baidu.setGeometry(QtCore.QRect(30, 220, 91, 20))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.Label_Baidu.setFont(font)
        self.Label_Baidu.setObjectName("Label_Baidu")
        self.LineEdit_TencentKEY = QtWidgets.QLineEdit(parent=self.scrollAreaWidgetContents)
        self.LineEdit_TencentKEY.setGeometry(QtCore.QRect(30, 320, 411, 31))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.LineEdit_TencentKEY.setFont(font)
        self.LineEdit_TencentKEY.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        self.LineEdit_TencentKEY.setObjectName("LineEdit_TencentKEY")
        self.LineEdit_YoudaoKEY = QtWidgets.QLineEdit(parent=self.scrollAreaWidgetContents)
        self.LineEdit_YoudaoKEY.setGeometry(QtCore.QRect(30, 110, 411, 31))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.LineEdit_YoudaoKEY.setFont(font)
        self.LineEdit_YoudaoKEY.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        self.LineEdit_YoudaoKEY.setObjectName("LineEdit_YoudaoKEY")
        self.LineEdit_XiaoNiuKEY = QtWidgets.QLineEdit(parent=self.scrollAreaWidgetContents)
        self.LineEdit_XiaoNiuKEY.setGeometry(QtCore.QRect(30, 400, 411, 31))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.LineEdit_XiaoNiuKEY.setFont(font)
        self.LineEdit_XiaoNiuKEY.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        self.LineEdit_XiaoNiuKEY.setObjectName("LineEdit_XiaoNiuKEY")
        self.Label_ShortcutKeyText = QtWidgets.QLabel(parent=self.scrollAreaWidgetContents)
        self.Label_ShortcutKeyText.setGeometry(QtCore.QRect(100, 570, 131, 20))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        font.setUnderline(True)
        self.Label_ShortcutKeyText.setFont(font)
        self.Label_ShortcutKeyText.setText("")
        self.Label_ShortcutKeyText.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.Label_ShortcutKeyText.setObjectName("Label_ShortcutKeyText")
        self.Label_Tencent = QtWidgets.QLabel(parent=self.scrollAreaWidgetContents)
        self.Label_Tencent.setGeometry(QtCore.QRect(30, 300, 101, 20))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.Label_Tencent.setFont(font)
        self.Label_Tencent.setObjectName("Label_Tencent")
        self.LineEdit_BaiduSECRETKEY = QtWidgets.QLineEdit(parent=self.scrollAreaWidgetContents)
        self.LineEdit_BaiduSECRETKEY.setGeometry(QtCore.QRect(30, 270, 411, 31))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.LineEdit_BaiduSECRETKEY.setFont(font)
        self.LineEdit_BaiduSECRETKEY.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        self.LineEdit_BaiduSECRETKEY.setObjectName("LineEdit_BaiduSECRETKEY")
        self.cancelHotKeyButton = QtWidgets.QPushButton(parent=self.scrollAreaWidgetContents)
        self.cancelHotKeyButton.setGeometry(QtCore.QRect(280, 570, 41, 21))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        self.cancelHotKeyButton.setFont(font)
        self.cancelHotKeyButton.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.cancelHotKeyButton.setStatusTip("")
        self.cancelHotKeyButton.setWhatsThis("")
        self.cancelHotKeyButton.setAccessibleDescription("")
        self.cancelHotKeyButton.setObjectName("cancelHotKeyButton")
        self.Label_OCRHotkey = QtWidgets.QLabel(parent=self.scrollAreaWidgetContents)
        self.Label_OCRHotkey.setGeometry(QtCore.QRect(30, 570, 71, 20))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.Label_OCRHotkey.setFont(font)
        self.Label_OCRHotkey.setObjectName("Label_OCRHotkey")
        self.Label_Youdao = QtWidgets.QLabel(parent=self.scrollAreaWidgetContents)
        self.Label_Youdao.setGeometry(QtCore.QRect(30, 90, 91, 20))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.Label_Youdao.setFont(font)
        self.Label_Youdao.setObjectName("Label_Youdao")
        self.ListWidget_SelectableSource = QtWidgets.QListWidget(parent=self.scrollAreaWidgetContents)
        self.ListWidget_SelectableSource.setGeometry(QtCore.QRect(20, 670, 201, 171))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.ListWidget_SelectableSource.setFont(font)
        self.ListWidget_SelectableSource.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.ListWidget_SelectableSource.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.ListWidget_SelectableSource.setObjectName("ListWidget_SelectableSource")
        self.ListWidget_SelectedSource = QtWidgets.QListWidget(parent=self.scrollAreaWidgetContents)
        self.ListWidget_SelectedSource.setGeometry(QtCore.QRect(240, 670, 201, 171))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.ListWidget_SelectedSource.setFont(font)
        self.ListWidget_SelectedSource.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.ListWidget_SelectedSource.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.ListWidget_SelectedSource.setDragEnabled(True)
        self.ListWidget_SelectedSource.setObjectName("ListWidget_SelectedSource")
        self.Line_3 = QtWidgets.QFrame(parent=self.scrollAreaWidgetContents)
        self.Line_3.setGeometry(QtCore.QRect(10, 600, 441, 21))
        self.Line_3.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.Line_3.setLineWidth(2)
        self.Line_3.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.Line_3.setObjectName("Line_3")
        self.Line_2 = QtWidgets.QFrame(parent=self.scrollAreaWidgetContents)
        self.Line_2.setGeometry(QtCore.QRect(10, 520, 441, 21))
        self.Line_2.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.Line_2.setLineWidth(2)
        self.Line_2.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.Line_2.setObjectName("Line_2")
        self.Line_1 = QtWidgets.QFrame(parent=self.scrollAreaWidgetContents)
        self.Line_1.setGeometry(QtCore.QRect(10, 40, 441, 20))
        self.Line_1.setLineWidth(2)
        self.Line_1.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.Line_1.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.Line_1.setObjectName("Line_1")
        self.Label_TranslatorAPISecretSetting = QtWidgets.QLabel(parent=self.scrollAreaWidgetContents)
        self.Label_TranslatorAPISecretSetting.setGeometry(QtCore.QRect(20, 60, 171, 20))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(16)
        font.setUnderline(False)
        self.Label_TranslatorAPISecretSetting.setFont(font)
        self.Label_TranslatorAPISecretSetting.setObjectName("Label_TranslatorAPISecretSetting")
        self.Label_HotkeySetting = QtWidgets.QLabel(parent=self.scrollAreaWidgetContents)
        self.Label_HotkeySetting.setGeometry(QtCore.QRect(20, 540, 111, 20))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(16)
        font.setUnderline(False)
        self.Label_HotkeySetting.setFont(font)
        self.Label_HotkeySetting.setObjectName("Label_HotkeySetting")
        self.Label_TranslatorSourcesSetting = QtWidgets.QLabel(parent=self.scrollAreaWidgetContents)
        self.Label_TranslatorSourcesSetting.setGeometry(QtCore.QRect(20, 620, 151, 20))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(16)
        font.setUnderline(False)
        self.Label_TranslatorSourcesSetting.setFont(font)
        self.Label_TranslatorSourcesSetting.setObjectName("Label_TranslatorSourcesSetting")
        self.Line_Source = QtWidgets.QFrame(parent=self.scrollAreaWidgetContents)
        self.Line_Source.setGeometry(QtCore.QRect(220, 670, 21, 171))
        self.Line_Source.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.Line_Source.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.Line_Source.setObjectName("Line_Source")
        self.Label_SelectableSource = QtWidgets.QLabel(parent=self.scrollAreaWidgetContents)
        self.Label_SelectableSource.setGeometry(QtCore.QRect(20, 650, 101, 20))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.Label_SelectableSource.setFont(font)
        self.Label_SelectableSource.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.Label_SelectableSource.setObjectName("Label_SelectableSource")
        self.Label_SelectedSource = QtWidgets.QLabel(parent=self.scrollAreaWidgetContents)
        self.Label_SelectedSource.setGeometry(QtCore.QRect(240, 650, 101, 20))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.Label_SelectedSource.setFont(font)
        self.Label_SelectedSource.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.Label_SelectedSource.setObjectName("Label_SelectedSource")
        self.PushButton_SourceUP = QtWidgets.QPushButton(parent=self.scrollAreaWidgetContents)
        self.PushButton_SourceUP.setGeometry(QtCore.QRect(330, 840, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        self.PushButton_SourceUP.setFont(font)
        self.PushButton_SourceUP.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        self.PushButton_SourceUP.setObjectName("PushButton_SourceUP")
        self.PushButton_SourceDown = QtWidgets.QPushButton(parent=self.scrollAreaWidgetContents)
        self.PushButton_SourceDown.setGeometry(QtCore.QRect(390, 840, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        self.PushButton_SourceDown.setFont(font)
        self.PushButton_SourceDown.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        self.PushButton_SourceDown.setObjectName("PushButton_SourceDown")
        self.PushButton_SourceDisable = QtWidgets.QPushButton(parent=self.scrollAreaWidgetContents)
        self.PushButton_SourceDisable.setGeometry(QtCore.QRect(360, 650, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        self.PushButton_SourceDisable.setFont(font)
        self.PushButton_SourceDisable.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        self.PushButton_SourceDisable.setObjectName("PushButton_SourceDisable")
        self.PushButton_SourceEnable = QtWidgets.QPushButton(parent=self.scrollAreaWidgetContents)
        self.PushButton_SourceEnable.setGeometry(QtCore.QRect(140, 650, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        self.PushButton_SourceEnable.setFont(font)
        self.PushButton_SourceEnable.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        self.PushButton_SourceEnable.setObjectName("PushButton_SourceEnable")
        self.Label_SourceSort = QtWidgets.QLabel(parent=self.scrollAreaWidgetContents)
        self.Label_SourceSort.setGeometry(QtCore.QRect(240, 840, 81, 20))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.Label_SourceSort.setFont(font)
        self.Label_SourceSort.setObjectName("Label_SourceSort")
        self.Label_SourceTips = QtWidgets.QLabel(parent=self.scrollAreaWidgetContents)
        self.Label_SourceTips.setGeometry(QtCore.QRect(20, 840, 131, 20))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        self.Label_SourceTips.setFont(font)
        self.Label_SourceTips.setObjectName("Label_SourceTips")
        self.Label_AliYun = QtWidgets.QLabel(parent=self.scrollAreaWidgetContents)
        self.Label_AliYun.setGeometry(QtCore.QRect(30, 430, 101, 20))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.Label_AliYun.setFont(font)
        self.Label_AliYun.setObjectName("Label_AliYun")
        self.LineEdit_AliYunSECRET = QtWidgets.QLineEdit(parent=self.scrollAreaWidgetContents)
        self.LineEdit_AliYunSECRET.setGeometry(QtCore.QRect(30, 480, 411, 31))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.LineEdit_AliYunSECRET.setFont(font)
        self.LineEdit_AliYunSECRET.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        self.LineEdit_AliYunSECRET.setObjectName("LineEdit_AliYunSECRET")
        self.LineEdit_AliYunKEY = QtWidgets.QLineEdit(parent=self.scrollAreaWidgetContents)
        self.LineEdit_AliYunKEY.setGeometry(QtCore.QRect(30, 450, 411, 31))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.LineEdit_AliYunKEY.setFont(font)
        self.LineEdit_AliYunKEY.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        self.LineEdit_AliYunKEY.setObjectName("LineEdit_AliYunKEY")
        self.CheckBox_Youdao = QtWidgets.QCheckBox(parent=self.scrollAreaWidgetContents)
        self.CheckBox_Youdao.setGeometry(QtCore.QRect(330, 90, 111, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.CheckBox_Youdao.setFont(font)
        self.CheckBox_Youdao.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        self.CheckBox_Youdao.setObjectName("CheckBox_Youdao")
        self.CheckBox_CaiYun = QtWidgets.QCheckBox(parent=self.scrollAreaWidgetContents)
        self.CheckBox_CaiYun.setGeometry(QtCore.QRect(330, 170, 111, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.CheckBox_CaiYun.setFont(font)
        self.CheckBox_CaiYun.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        self.CheckBox_CaiYun.setObjectName("CheckBox_CaiYun")
        self.CheckBox_Baidu = QtWidgets.QCheckBox(parent=self.scrollAreaWidgetContents)
        self.CheckBox_Baidu.setGeometry(QtCore.QRect(330, 220, 111, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.CheckBox_Baidu.setFont(font)
        self.CheckBox_Baidu.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        self.CheckBox_Baidu.setObjectName("CheckBox_Baidu")
        self.CheckBox_Tencent = QtWidgets.QCheckBox(parent=self.scrollAreaWidgetContents)
        self.CheckBox_Tencent.setEnabled(False)
        self.CheckBox_Tencent.setGeometry(QtCore.QRect(330, 300, 111, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.CheckBox_Tencent.setFont(font)
        self.CheckBox_Tencent.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        self.CheckBox_Tencent.setCheckable(True)
        self.CheckBox_Tencent.setObjectName("CheckBox_Tencent")
        self.Line_4 = QtWidgets.QFrame(parent=self.scrollAreaWidgetContents)
        self.Line_4.setGeometry(QtCore.QRect(10, 870, 441, 21))
        self.Line_4.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.Line_4.setLineWidth(2)
        self.Line_4.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.Line_4.setObjectName("Line_4")
        self.Label_TranslatorAPISecretSetting_2 = QtWidgets.QLabel(parent=self.scrollAreaWidgetContents)
        self.Label_TranslatorAPISecretSetting_2.setGeometry(QtCore.QRect(20, 890, 221, 20))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(16)
        font.setUnderline(False)
        self.Label_TranslatorAPISecretSetting_2.setFont(font)
        self.Label_TranslatorAPISecretSetting_2.setObjectName("Label_TranslatorAPISecretSetting_2")
        self.LineEdit_OCRAPPID = QtWidgets.QLineEdit(parent=self.scrollAreaWidgetContents)
        self.LineEdit_OCRAPPID.setGeometry(QtCore.QRect(30, 940, 411, 31))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.LineEdit_OCRAPPID.setFont(font)
        self.LineEdit_OCRAPPID.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        self.LineEdit_OCRAPPID.setClearButtonEnabled(False)
        self.LineEdit_OCRAPPID.setObjectName("LineEdit_OCRAPPID")
        self.LineEdit_OCRSECRET = QtWidgets.QLineEdit(parent=self.scrollAreaWidgetContents)
        self.LineEdit_OCRSECRET.setGeometry(QtCore.QRect(30, 970, 411, 31))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.LineEdit_OCRSECRET.setFont(font)
        self.LineEdit_OCRSECRET.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        self.LineEdit_OCRSECRET.setObjectName("LineEdit_OCRSECRET")
        self.LineEdit_OCRKEY = QtWidgets.QLineEdit(parent=self.scrollAreaWidgetContents)
        self.LineEdit_OCRKEY.setGeometry(QtCore.QRect(30, 1000, 411, 31))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.LineEdit_OCRKEY.setFont(font)
        self.LineEdit_OCRKEY.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        self.LineEdit_OCRKEY.setObjectName("LineEdit_OCRKEY")
        self.Label_Tencent_2 = QtWidgets.QLabel(parent=self.scrollAreaWidgetContents)
        self.Label_Tencent_2.setGeometry(QtCore.QRect(30, 920, 131, 20))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.Label_Tencent_2.setFont(font)
        self.Label_Tencent_2.setObjectName("Label_Tencent_2")
        self.PushButton_GetFreeOCRKEY = QtWidgets.QPushButton(parent=self.scrollAreaWidgetContents)
        self.PushButton_GetFreeOCRKEY.setGeometry(QtCore.QRect(340, 900, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        self.PushButton_GetFreeOCRKEY.setFont(font)
        self.PushButton_GetFreeOCRKEY.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        self.PushButton_GetFreeOCRKEY.setObjectName("PushButton_GetFreeOCRKEY")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.retranslateUi(Config)
        self.confirmHotKeyButton.clicked.connect(Config.confirmHotkey) # type: ignore
        self.cancelHotKeyButton.clicked.connect(Config.cancelHotKey) # type: ignore
        self.changeHotKeyButton.clicked.connect(Config.getIntoHotKeyChangeMode) # type: ignore
        self.Button_Save.clicked.connect(Config.saveConfig) # type: ignore
        self.PushButton_SourceEnable.clicked.connect(Config.addTranslator) # type: ignore
        self.PushButton_SourceDisable.clicked.connect(Config.removeTranslator) # type: ignore
        self.PushButton_SourceUP.clicked.connect(Config.upTranslator) # type: ignore
        self.PushButton_SourceDown.clicked.connect(Config.downTranslator) # type: ignore
        self.PushButton_GetFreeOCRKEY.clicked.connect(Config.showGetSecretWidget) # type: ignore
        self.ListWidget_SelectableSource.doubleClicked['QModelIndex'].connect(Config.addTranslator) # type: ignore
        self.ListWidget_SelectedSource.doubleClicked['QModelIndex'].connect(Config.removeTranslator) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Config)

    def retranslateUi(self, Config):
        _translate = QtCore.QCoreApplication.translate
        Config.setWindowTitle(_translate("Config", "配置"))
        self.Label_MasterTitle.setText(_translate("Config", "配置界面 - 请填写以下配置↓"))
        self.Label_HelpLink.setText(_translate("Config", "<a href=\"https://github.com/GayWindTech/TransAssistant/blob/main/README.md\">查看填写帮助</a>"))
        self.LineEdit_CaiYunTOKEN.setPlaceholderText(_translate("Config", "请输入彩云小译API_TOKEN"))
        self.LineEdit_BaiduAPPID.setPlaceholderText(_translate("Config", "请输入百度翻译API_APPID"))
        self.confirmHotKeyButton.setToolTip(_translate("Config", "<html><head/><body><p>确认更改快捷键</p></body></html>"))
        self.confirmHotKeyButton.setText(_translate("Config", "确认"))
        self.LineEdit_TencentSECRET.setPlaceholderText(_translate("Config", "请输入腾讯云翻译API_SECRET"))
        self.changeHotKeyButton.setToolTip(_translate("Config", "<html><head/><body><p>确认更改快捷键</p></body></html>"))
        self.changeHotKeyButton.setText(_translate("Config", "更改"))
        self.OCRKeyEdit.setToolTip(_translate("Config", "摁下快捷键以键入"))
        self.Label_XiaoNiu.setText(_translate("Config", "小牛翻译API"))
        self.Label_CaiYun.setText(_translate("Config", "彩云小译API"))
        self.LineEdit_YoudaoSECRET.setPlaceholderText(_translate("Config", "请输入有道翻译API_SECRET"))
        self.Button_Save.setText(_translate("Config", "保存"))
        self.Label_Baidu.setText(_translate("Config", "百度翻译API"))
        self.LineEdit_TencentKEY.setPlaceholderText(_translate("Config", "请输入腾讯云翻译API_KEY"))
        self.LineEdit_YoudaoKEY.setPlaceholderText(_translate("Config", "请输入有道翻译API_KEY"))
        self.LineEdit_XiaoNiuKEY.setPlaceholderText(_translate("Config", "请输入小牛翻译API_KEY"))
        self.Label_Tencent.setText(_translate("Config", "腾讯云翻译API"))
        self.LineEdit_BaiduSECRETKEY.setPlaceholderText(_translate("Config", "请输入百度翻译API_SECRETKEY"))
        self.cancelHotKeyButton.setToolTip(_translate("Config", "<html><head/><body><p>确认更改快捷键</p></body></html>"))
        self.cancelHotKeyButton.setText(_translate("Config", "取消"))
        self.Label_OCRHotkey.setText(_translate("Config", "OCR热键："))
        self.Label_Youdao.setText(_translate("Config", "有道翻译API"))
        self.Label_TranslatorAPISecretSetting.setText(_translate("Config", "翻译API密钥设置："))
        self.Label_HotkeySetting.setText(_translate("Config", "热键设置："))
        self.Label_TranslatorSourcesSetting.setText(_translate("Config", "翻译源 & 顺序："))
        self.Label_SelectableSource.setText(_translate("Config", "可使用翻译源"))
        self.Label_SelectedSource.setText(_translate("Config", "已启用翻译源"))
        self.PushButton_SourceUP.setText(_translate("Config", "上移"))
        self.PushButton_SourceDown.setText(_translate("Config", "下移"))
        self.PushButton_SourceDisable.setText(_translate("Config", "禁用选中源"))
        self.PushButton_SourceEnable.setText(_translate("Config", "启用选中源"))
        self.Label_SourceSort.setText(_translate("Config", "翻译源排序："))
        self.Label_SourceTips.setText(_translate("Config", "*最多可选四个翻译源"))
        self.Label_AliYun.setText(_translate("Config", "阿里云翻译API"))
        self.LineEdit_AliYunSECRET.setPlaceholderText(_translate("Config", "请输入阿里云翻译API_SECRET"))
        self.LineEdit_AliYunKEY.setPlaceholderText(_translate("Config", "请输入阿里云翻译API_KEY"))
        self.CheckBox_Youdao.setText(_translate("Config", "白嫖有道翻译"))
        self.CheckBox_CaiYun.setText(_translate("Config", "白嫖彩云小译"))
        self.CheckBox_Baidu.setText(_translate("Config", "白嫖百度翻译"))
        self.CheckBox_Tencent.setText(_translate("Config", "白嫖腾讯翻译君"))
        self.Label_TranslatorAPISecretSetting_2.setText(_translate("Config", "文字识别API密钥设置："))
        self.LineEdit_OCRAPPID.setPlaceholderText(_translate("Config", "请输入科大讯飞OCR AppId"))
        self.LineEdit_OCRSECRET.setPlaceholderText(_translate("Config", "请输入科大讯飞OCR Secret"))
        self.LineEdit_OCRKEY.setPlaceholderText(_translate("Config", "请输入科大讯飞OCR Key"))
        self.Label_Tencent_2.setText(_translate("Config", "科大讯飞OCRAPI"))
        self.PushButton_GetFreeOCRKEY.setText(_translate("Config", "获取白嫖密钥"))
from customerDefineQtClass import oneKeyQKeySequenceEdit
