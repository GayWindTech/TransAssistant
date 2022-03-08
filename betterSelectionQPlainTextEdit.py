from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal, Qt

class betterSelectionQPlainTextEdit(QtWidgets.QPlainTextEdit):
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
