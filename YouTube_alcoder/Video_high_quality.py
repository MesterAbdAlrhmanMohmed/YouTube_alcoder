from PyQt6 import QtWidgets as qt
from PyQt6 import QtGui as qt1
from PyQt6 import QtCore as qt2
from pytube import YouTube
import requests
class YoutubeObjects(qt2.QObject):
    Finish=qt2.pyqtSignal(bool)
class YoutubeThread(qt2.QRunnable):
    def __init__(self, url, path, progress_bar):
        super().__init__()
        self.objects=YoutubeObjects()
        self.url=url
        self.path=path
        self.progress_bar=progress_bar
    def run(self):
        try:
            yt=YouTube(self.url)
            stream=yt.streams.get_highest_resolution()
            file_size=stream.filesize
            response=requests.get(stream.url, stream=True)
            with open(self.path + '/' + yt.title + '.mp4', 'wb') as file:
                for data in response.iter_content(chunk_size=4096):
                    file.write(data)
                    self.progress_bar.setValue(file.tell() * 100 // file_size)
            self.objects.Finish.emit(True)
        except Exception as e:
            print(e)
            self.objects.Finish.emit(False)
class HighQualityVideoDownloadDialog(qt.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("تنزيل فيديو بأعلى جودة")
        self.حفظ=qt.QPushButton("تحديد مكان الحفظ أولاً (O)")
        self.حفظ.setShortcut("o")
        self.حفظ.setDefault(True)
        self.حفظ.clicked.connect(self.opinFile)
        self.إظهار1=qt.QLabel("مسار الحفظ")
        self.التعديل=qt.QLineEdit()
        self.التعديل.setReadOnly(True)
        self.التعديل.setAccessibleName("مسار الحفظ")
        self.إظهار3=qt.QLabel("إدخال الرابط هنا")
        self.الرابط=qt.QLineEdit()
        self.الرابط.setAccessibleName("إدخال الرابط هنا")
        self.التحميل=qt.QPushButton("بدء التحميل (D)")
        self.التحميل.setDefault(True)
        self.التحميل.setShortcut("d")
        self.التحميل.clicked.connect(self.dl)
        self.progress_bar=qt.QProgressBar()
        self.progress_bar.setValue(0)
        l=qt.QVBoxLayout(self)
        l.addWidget(self.حفظ)
        l.addWidget(self.إظهار1)
        l.addWidget(self.التعديل)
        l.addWidget(self.progress_bar)
        l.addWidget(self.إظهار3)
        l.addWidget(self.الرابط)
        l.addWidget(self.التحميل)
    def opinFile(self):
        file_dialog=qt.QFileDialog()
        file_dialog.setFileMode(qt.QFileDialog.FileMode.Directory)
        if file_dialog.exec() == qt.QFileDialog.DialogCode.Accepted:
            self.التعديل.setText(file_dialog.selectedFiles()[0])
    def dl(self):
        if not self.الرابط.text():
            qt.QMessageBox.warning(self, "تنبيه", "الرجاء إدخال رابط الفيديو")
            return
        if not self.التعديل.text():
            qt.QMessageBox.warning(self, "تنبيه", "الرجاء تحديد مكان الحفظ")
            return
        qt.QMessageBox.information(self, "تنبيه", "لقد بدأ التحميل الآن، الرجاء الانتظار حتى يتم التحميل")
        self.التحميل.setDisabled(True)
        thread=YoutubeThread(self.الرابط.text(), self.التعديل.text(), self.progress_bar)
        thread.objects.Finish.connect(self.onFinish)
        qt2.QThreadPool(self).start(thread)
    def onFinish(self, state):
        if state:
            qt.QMessageBox.information(self, "تم", "تم التحميل بنجاح والحفظ")
            self.التحميل.setDisabled(False)
            self.progress_bar.setValue(0)
        else:
            qt.QMessageBox.warning(self, "تنبيه", "فشلت عملية التحميل، ربما تكون المشكلة من الرابط أو الإنترنت أو أنك نسيت تحديد مكان الحفظ")
            self.التحميل.setDisabled(False)
            self.progress_bar.setValue(0)