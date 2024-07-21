from PyQt6 import QtWidgets as qt
from PyQt6 import QtGui as qt1
from PyQt6 import QtCore as qt2
import Playlist_audio_high_quality,Playlist_audio_low_quality,Playlist_video_high_quality,Playlist_video_low_quality
class dialog(qt.QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("تنزيل قائمة تشغيل")
        self.الخيارات=qt.QListWidget()
        self.الخيارات.clicked.connect(self.ch)
        qt1.QShortcut("return",self).activated.connect(self.ch)
        self.الخيارات.addItem("تنزيل قائمة تشغيل كصوت بأعلا جودة")
        self.الخيارات.addItem("تنزيل قائمة تشغيل كصوت بأقل جودة")
        self.الخيارات.addItem("تنزيل قائمة تشغيل كفيديو بأعلا جودة")
        self.الخيارات.addItem("تنزيل قائمة تشغيل كفيديو بأقل جودة")        
        l=qt.QVBoxLayout(self)                            
        l.addWidget(self.الخيارات)
    def ch(self):
        العناصر=self.الخيارات.currentRow()
        if العناصر==0        :
            Playlist_audio_high_quality.dialog(self).exec()
        elif العناصر==1:
            Playlist_audio_low_quality.dialog(self).exec()
        elif العناصر==2:
            Playlist_video_high_quality.dialog(self).exec()
        elif العناصر==3:
            Playlist_video_low_quality.dialog(self).exec()