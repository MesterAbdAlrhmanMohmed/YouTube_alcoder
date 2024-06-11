from PyQt6 import QtWidgets as qt
from PyQt6 import QtGui as qt1
from PyQt6 import QtCore as qt2
import Video_high_quality,Video_low_quality,Audio_high_quality,Audio_low_quality
class dialog(qt.QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("تنزيل مقطع")
        self.الخيارات=qt.QListWidget()
        self.الخيارات.clicked.connect(self.ch)
        qt1.QShortcut("return",self).activated.connect(self.ch)
        self.الخيارات.addItem("تنزيل صوت بأعلا جودة")
        self.الخيارات.addItem("تنزيل صوت بأقل جودة")
        self.الخيارات.addItem("تنزيل فيديو بأعلا جودة")
        self.الخيارات.addItem("تنزيل فيديو بأقل جودة")
        l=qt.QVBoxLayout(self)                            
        l.addWidget(self.الخيارات)
    def ch(self):
        العناصر=self.الخيارات.currentRow()
        if العناصر==0:
            Audio_high_quality.dialog(self).exec()
        elif العناصر==1:
            Audio_low_quality.dialog(self).exec()
        elif العناصر==2:
            Video_high_quality.dialog(self).exec()
        elif العناصر==3:
            Video_low_quality.dialog(self).exec()