from PyQt6 import QtWidgets as qt
from PyQt6 import QtGui as qt1
from PyQt6 import QtCore as qt2
import pyperclip
class CommentsWindow(qt.QDialog):
    def __init__(self, comments, parent=None):
        super().__init__(parent)
        self.setWindowTitle("التعليقات")
        self.showFullScreen()
        self.setup_ui(comments)    
    def setup_ui(self, comments):
        self.comments_list=qt.QListWidget()
        lines = comments.split('\n')
        self.comments_list.addItems(lines)    
        self.copy_button=qt.QPushButton("نسخ التعليق")
        self.copy_button.clicked.connect(self.copy_selected_line)                
        layout=qt.QVBoxLayout(self)
        layout.addWidget(self.comments_list)
        layout.addWidget(self.copy_button)        
    def copy_selected_line(self):
        selected_items = self.comments_list.selectedItems()
        if selected_items:
            selected_line = selected_items[0].text()
            pyperclip.copy(selected_line)
            qt.QMessageBox.information(self, "تم", "تم نسخ التعليق بنجاح")