from PyQt6 import QtWidgets as qt
from PyQt6 import QtGui as qt1
from PyQt6 import QtCore as qt2
import pyperclip
class DescriptionWindow(qt.QDialog):
    def __init__(self, description, parent=None):
        super().__init__(parent)
        self.setWindowTitle("الوصف")
        self.showFullScreen()
        self.setup_ui(description)        
    def setup_ui(self, description):
        self.الوصف=qt.QListWidget()
        lines=description.split('\n')
        self.الوصف.addItems(lines)        
        self.نسخ_سطر=qt.QPushButton("نسخ هذا السطر")
        self.نسخ_سطر.setDefault(True)
        self.نسخ_سطر.clicked.connect(self.copy_selected_line)        
        self.نسخ_الكل=qt.QPushButton("نسخ الوصف")
        self.نسخ_الكل.clicked.connect(lambda: self.copyALL(description))
        layout=qt.QVBoxLayout(self)
        layout.addWidget(self.الوصف)
        layout.addWidget(self.نسخ_سطر)
        layout.addWidget(self.نسخ_الكل)        
    def copyALL(self, description):
        pyperclip.copy(description)
        qt.QMessageBox.information(self, "تم", "تم نسخ الوصف")
    def copy_selected_line(self):
        selected_items = self.الوصف.selectedItems()
        if selected_items:
            selected_line = selected_items[0].text()
            pyperclip.copy(selected_line)
            qt.QMessageBox.information(self, "تم", "تم نسخ السطر")