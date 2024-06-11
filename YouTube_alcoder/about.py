from PyQt6 import QtWidgets as qt
from PyQt6 import QtGui as qt1
from PyQt6 import QtCore as qt2
import webbrowser
class dialog(qt.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.showFullScreen()
        self.setWindowTitle("عن المطور")
        self.القائمة=qt.QListWidget()
        self.القائمة.clicked.connect(self.about)
        self.القائمة.addItem("قناى المطور على YouTube")
        self.القائمة.addItem("حساب المطور على telegram")
        self.القائمة.addItem("حساب المطور على GitHub")        
        qt1.QShortcut("return",self).activated.connect(self.about)
        l=qt.QVBoxLayout(self)                            
        l.addWidget(self.القائمة)
    def about(self):
        العناصر=self.القائمة.currentRow()
        if العناصر==0:
            webbrowser.open("https://youtube.com/@Alcoder01?feature=shared")
        if العناصر==1:
            webbrowser.open("https://t.me/p1_1_1")
        if العناصر==2:
            webbrowser.open("https://github.com/MesterAbdAlrhmanMohmed")