from PyQt6 import QtWidgets as qt
from PyQt6 import QtGui as qt1
from PyQt6 import QtCore as qt2
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
import yt_dlp    
class HighQualityVideoWindow(qt.QDialog):
    def __init__(self, url):
        super().__init__()
        self.setWindowTitle("تشغيل الفيديو بأعلى جودة")
        self.showFullScreen()
        self.mp=QMediaPlayer()
        self.ao=QAudioOutput()
        self.vw=QVideoWidget()
        self.mp.setAudioOutput(self.ao)
        self.mp.setVideoOutput(self.vw)                        
        qt1.QShortcut("escape",self).activated.connect(self.stop_exit)    
        qt1.QShortcut("home",self).activated.connect(lambda: self.mp.stop())
        qt1.QShortcut("space", self).activated.connect(self.play)
        qt1.QShortcut("alt+right", self).activated.connect(lambda: self.mp.setPosition(self.mp.position() + 5000))
        qt1.QShortcut("alt+left", self).activated.connect(lambda: self.mp.setPosition(self.mp.position() - 5000))
        qt1.QShortcut("alt+up", self).activated.connect(lambda: self.mp.setPosition(self.mp.position() + 10000))
        qt1.QShortcut("alt+down", self).activated.connect(lambda: self.mp.setPosition(self.mp.position() - 10000))
        qt1.QShortcut("ctrl+right", self).activated.connect(lambda: self.mp.setPosition(self.mp.position() + 30000))
        qt1.QShortcut("ctrl+left", self).activated.connect(lambda: self.mp.setPosition(self.mp.position() - 30000))
        qt1.QShortcut("ctrl+up", self).activated.connect(lambda: self.mp.setPosition(self.mp.position() + 60000))
        qt1.QShortcut("ctrl+down", self).activated.connect(lambda: self.mp.setPosition(self.mp.position() - 60000))
        qt1.QShortcut("s", self).activated.connect(lambda: self.mp.stop())
        qt1.QShortcut("ctrl+1", self).activated.connect(self.t10)
        qt1.QShortcut("ctrl+2", self).activated.connect(self.t20)
        qt1.QShortcut("ctrl+3", self).activated.connect(self.t30)
        qt1.QShortcut("ctrl+4", self).activated.connect(self.t40)
        qt1.QShortcut("ctrl+5", self).activated.connect(self.t50)
        qt1.QShortcut("ctrl+6", self).activated.connect(self.t60)
        qt1.QShortcut("ctrl+7", self).activated.connect(self.t70)
        qt1.QShortcut("ctrl+8", self).activated.connect(self.t80)
        qt1.QShortcut("ctrl+9", self).activated.connect(self.t90)
        qt1.QShortcut("shift+up", self).activated.connect(self.increase_volume)
        qt1.QShortcut("shift+down", self).activated.connect(self.decrease_volume)        
        self.التقدم=qt.QSlider(qt2.Qt.Orientation.Horizontal)                        
        self.التقدم.setRange(0,100)
        self.التقدم.setAccessibleName("االوقت المنقضي")
        self.mp.durationChanged.connect(self.update_slider)
        self.mp.positionChanged.connect(self.update_slider)        
        self.المدة=qt.QLineEdit()
        self.المدة.setReadOnly(True)
        self.المدة.setAccessibleName("مدة المقطع")
        layout=qt.QVBoxLayout()
        layout.addWidget(self.vw)
        layout.addWidget(self.التقدم)
        layout.addWidget(self.المدة)
        self.setLayout(layout)
        self.play_video(url)
    def stop_exit(self):
        self.close()
        self.mp.stop()
    def play_video(self, url):    
        ydl_opts={
            'format': 'best',
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict=ydl.extract_info(url, download=False)
                video_url=info_dict['url']
                self.mp.setSource(qt2.QUrl(video_url))
                self.mp.play()
        except Exception as e:
            qt.QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")
    def t10(self): 
        total_duration = self.mp.duration()
        self.mp.setPosition(int(total_duration * 0.1))
    def t20(self): 
        total_duration = self.mp.duration()
        self.mp.setPosition(int(total_duration * 0.2))
    def t30(self): 
        total_duration = self.mp.duration()
        self.mp.setPosition(int(total_duration * 0.3))
    def t40(self): 
        total_duration = self.mp.duration()
        self.mp.setPosition(int(total_duration * 0.4))
    def t50(self): 
        total_duration = self.mp.duration()
        self.mp.setPosition(int(total_duration * 0.5))
    def t60(self): 
        total_duration = self.mp.duration()
        self.mp.setPosition(int(total_duration * 0.6))
    def t70(self): 
        total_duration = self.mp.duration()
        self.mp.setPosition(int(total_duration * 0.7))
    def t80(self): 
        total_duration = self.mp.duration()
        self.mp.setPosition(int(total_duration * 0.8))
    def t90(self): 
        total_duration = self.mp.duration()
        self.mp.setPosition(int(total_duration * 0.9))            
    def play(self):
        if self.mp.isPlaying():
            self.mp.pause()
        else:
            self.mp.play()
    def increase_volume(self):
        current_volume=self.ao.volume()
        new_volume=current_volume+0.10
        self.ao.setVolume(new_volume)
    def decrease_volume(self):
        current_volume=self.ao.volume()
        new_volume=current_volume-0.10
        self.ao.setVolume(new_volume)        
    def update_slider(self):
        try:
            self.التقدم.setValue(int((self.mp.position()/self.mp.duration())*100))
            self.time_VA()
        except:
            self.المدة.setText("خطأ في الحصول على مدة المقطع, ربما هو بث مباشر")
    def time_VA(self):
        position=self.mp.position()
        duration=self.mp.duration()
        position_hours=(position // 3600000) % 24
        position_minutes=(position // 60000) % 60
        position_seconds=(position // 1000) % 60
        duration_hours=(duration // 3600000) % 24
        duration_minutes=(duration // 60000) % 60
        duration_seconds=(duration // 1000) % 60
        position_str=qt2.QTime(position_hours, position_minutes, position_seconds).toString("HH:mm:ss")
        duration_str=qt2.QTime(duration_hours, duration_minutes, duration_seconds).toString("HH:mm:ss")        
        self.المدة.setText(f"الوقت المنقضي: {position_str}، مدة المقطع: {duration_str}")