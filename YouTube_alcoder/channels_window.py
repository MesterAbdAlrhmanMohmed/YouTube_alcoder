from PyQt6 import QtWidgets as qt
from PyQt6 import QtGui as qt1
from PyQt6 import QtCore as qt2
from youtubesearchpython import Channel
import pyperclip
class Channels_window(qt.QDialog):
    def __init__(self, channel_url, parent=None):
        super().__init__(parent)
        self.setWindowTitle("معلومات حول القناة")
        self.showFullScreen()
        self.channel_url=channel_url
        self.channel_info_list = qt.QListWidget()
        self.copy_item_btn=qt.QPushButton("نسخ العنصر")
        self.copy_all_btn=qt.QPushButton("نسخ الكل")
        self.copy_item_btn.clicked.connect(self.copy_item)
        self.copy_all_btn.clicked.connect(self.copy_all)
        layout=qt.QVBoxLayout(self)
        layout.addWidget(self.channel_info_list)
        layout.addWidget(self.copy_item_btn)
        layout.addWidget(self.copy_all_btn)
        self.setLayout(layout)
        self.get_channel_info()
    def get_channel_info(self):
        try:
            channel=Channel.get(channel_id=self.channel_url.split("/")[-1])
            channel_name=channel['title']
            channel_description=channel['description']
            channel_subscribers=channel['subscribers']
            self.channel_info_list.addItem(f"اسم القناة: {channel_name}")
            self.channel_info_list.addItem(f"وصف القناة: {channel_description}")
            self.channel_info_list.addItem(f"{channel_subscribers}")
        except Exception as e:
            qt.QMessageBox.warning(self, "خطأ", f"حدث خطأ أثناء جلب معلومات القناة: {str(e)}")
    def copy_item(self):
        selected_item=self.channel_info_list.currentItem()
        if selected_item:
            pyperclip.copy(selected_item.text())
            qt.QMessageBox.information(self, "تم", "تم نسخ العنصر")
        else:
            qt.QMessageBox.warning(self, "خطأ", "يرجى اختيار عنصر لنسخه")
    def copy_all(self):
        text="\n".join([self.channel_info_list.item(i).text() for i in range(self.channel_info_list.count())])
        pyperclip.copy(text)
        qt.QMessageBox.information(self, "تم", "تم نسخ جميع معلومات القناة")