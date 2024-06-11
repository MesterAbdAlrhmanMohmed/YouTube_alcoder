from PyQt6 import QtWidgets as qt
from PyQt6 import QtGui as qt1
from PyQt6 import QtCore as qt2
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube
class dialog(qt.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("تنزيل ترجمات الفيديوهات subtitles")
        self.تنبيه=qt.QLabel("عند حفظ الملف بالرجاء كتابة إسم الملف.txt")
        self.حفظ=qt.QPushButton("تحديد مكان الحفظ أولا O")
        self.حفظ.setShortcut("o")
        self.حفظ.setDefault(True)
        self.حفظ.clicked.connect(self.opinFile)
        self.حفظ.setAccessibleDescription("عند حفظ الملف بالرجاء كتابة إسم الملف بامتداد T,X,T")
        self.إظهار1=qt.QLabel("مسار الحفظ")
        self.التعديل=qt.QLineEdit()
        self.التعديل.setReadOnly(True)
        self.التعديل.setAccessibleName("مسار الحفظ")                
        self.إظهار2=qt.QLabel("إدخال الرابط هنا")
        self.الرابط=qt.QLineEdit()
        self.الرابط.setAccessibleName("إدخال الرابط هنا")
        self.التحميل=qt.QPushButton("بدء التحميل D")
        self.التحميل.setDefault(True)
        self.التحميل.setShortcut("d")
        self.التحميل.clicked.connect(self.dl)
        l=qt.QVBoxLayout(self)                            
        l.addWidget(self.تنبيه)
        l.addWidget(self.حفظ)
        l.addWidget(self.إظهار1)
        l.addWidget(self.التعديل)        
        l.addWidget(self.إظهار2)
        l.addWidget(self.الرابط)
        l.addWidget(self.التحميل)        
    def opinFile(self):        
        file=qt.QFileDialog()
        file.setAcceptMode(qt.QFileDialog.AcceptMode.AcceptSave)
        if file.exec()==qt.QFileDialog.DialogCode.Accepted:
            self.التعديل.setText(file.selectedFiles()[0])                                 
    def dl(self):
        try:
            url=self.الرابط.text()
            yt=YouTube(url)
            id=yt.video_id
            transcript_list = YouTubeTranscriptApi.get_transcript(id)
            result=[]
            for transcript in transcript_list:
                result.append(transcript["text"])
            with open(self.التعديل.text(), "w", encoding="utf-8") as file:
                file.write("\n".join(result))
                qt.QMessageBox.information(self,"تم","تم تحميل ملف الترجمة وحفظه")
        except:
            qt.QMessageBox.warning(self,"تنبيه","لقد فشلت عملية تنزيل الترجمة,ربما تكون المشكلة في الرابط أو الإنترنيت أو أنك نسيت تحديد مكان الحفظ أو أن الفيديو لا يحتوي على ترجمات")