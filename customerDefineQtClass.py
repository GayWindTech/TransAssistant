from PyQt6.QtGui import QKeySequence
from PyQt6.QtWidgets import QKeySequenceEdit, QPlainTextEdit
from PyQt6.QtCore import pyqtSignal, Qt

class oneKeyQKeySequenceEdit(QKeySequenceEdit):
    def __init__(self, parent=None):
        super(oneKeyQKeySequenceEdit, self).__init__(parent)
        self._string = ''
    def keyPressEvent(self, QKeyEvent):
        super(oneKeyQKeySequenceEdit, self).keyPressEvent(QKeyEvent)
        value = self.keySequence()
        self._string = self.keySequence().toString()
        self.setKeySequence(value)

class betterSelectionQPlainTextEdit(QPlainTextEdit):
    mouseRelease = pyqtSignal()
    selectedFinish = pyqtSignal()
    focusOut = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
    def mouseReleaseEvent(self,event):
        super().mouseReleaseEvent(event)
        self.mouseRelease.emit()
        if(self.textCursor().hasSelection()):
            self.selectedFinish.emit()
    def focusOutEvent(self,event):
        super().focusOutEvent(event)
        self.focusOut.emit()
    def clearSelection(self):
        _cursor = self.textCursor()
        _cursor.clearSelection()
        self.setTextCursor(_cursor)
