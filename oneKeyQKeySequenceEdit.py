from PyQt6.QtGui import QKeySequence
from PyQt6.QtWidgets import QKeySequenceEdit
from var_dump import var_dump

class oneKeyQKeySequenceEdit(QKeySequenceEdit):
    def __init__(self, parent=None):
        super(oneKeyQKeySequenceEdit, self).__init__(parent)
        self._string = ''
    def keyPressEvent(self, QKeyEvent):
        super(oneKeyQKeySequenceEdit, self).keyPressEvent(QKeyEvent)
        value = self.keySequence()
        self._string = self.keySequence().toString()
        self.setKeySequence(value)

