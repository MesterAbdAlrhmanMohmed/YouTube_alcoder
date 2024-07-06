from PyQt6 import QtWidgets as qt
from PyQt6 import QtGui as qt1
from PyQt6 import QtCore as qt2
from pytube import Playlist, YouTube
class YoutubeObjects(qt2.QObject):
    Finish = qt2.pyqtSignal(bool)
class YoutubeThread(qt2.QRunnable):
    def __init__(self, url, path, progress_bar):
        super().__init__()
        self.objects = YoutubeObjects()
        self.url = url
        self.path = path
        self.progress_bar = progress_bar
    def run(self):
        try:
            playlist = Playlist(self.url)
            if not playlist.video_urls:
                raise Exception("This is not a playlist")
            total_videos = len(playlist.video_urls)
            current_video = 0
            for video_url in playlist.video_urls:
                try:
                    self.download_video(video_url)
                    current_video += 1
                    self.progress_bar.setValue((current_video / total_videos) * 100)
                except Exception as e:
                    print(f"Failed to download {video_url}: {e}")
            self.objects.Finish.emit(True)
        except Exception as e:
            print(e)
            self.objects.Finish.emit(False)
    def download_video(self, video_url):
        yt = YouTube(video_url)
        stream = yt.streams.get_highest_resolution()
        stream.download(output_path=self.path)
class dialog(qt.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("تنزيل قائمة التشغيل كفيديو بأعلى جودة")
        self.حفظ = qt.QPushButton("تحديد مكان الحفظ أولاً (O)")
        self.حفظ.setShortcut("o")
        self.حفظ.setDefault(True)
        self.حفظ.clicked.connect(self.opinFile)
        self.إظهار1 = qt.QLabel("مسار الحفظ")
        self.التعديل = qt.QLineEdit()
        self.التعديل.setReadOnly(True)
        self.التعديل.setAccessibleName("مسار الحفظ")
        self.إظهار3 = qt.QLabel("إدخال الرابط هنا")
        self.الرابط = qt.QLineEdit()
        self.الرابط.setAccessibleName("إدخال الرابط هنا")
        self.التحميل = qt.QPushButton("بدء التحميل (D)")
        self.التحميل.setDefault(True)
        self.التحميل.setShortcut("d")
        self.التحميل.clicked.connect(self.dl)
        self.progress_bar = qt.QProgressBar()
        self.progress_bar.setValue(0)
        layout = qt.QVBoxLayout(self)
        layout.addWidget(self.حفظ)
        layout.addWidget(self.إظهار1)
        layout.addWidget(self.التعديل)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.إظهار3)
        layout.addWidget(self.الرابط)
        layout.addWidget(self.التحميل)
    def opinFile(self):
        file_dialog = qt.QFileDialog()
        file_dialog.setFileMode(qt.QFileDialog.FileMode.Directory)
        if file_dialog.exec() == qt.QFileDialog.DialogCode.Accepted:
            self.التعديل.setText(file_dialog.selectedFiles()[0])
    def dl(self):
        if not self.الرابط.text():
            qt.QMessageBox.warning(self, "تنبيه", "الرجاء إدخال رابط القائمة")
            return
        if not self.التعديل.text():
            qt.QMessageBox.warning(self, "تنبيه", "الرجاء تحديد مكان الحفظ")
            return
        qt.QMessageBox.information(self, "تنبيه", "لقد بدأ التحميل الآن، الرجاء الانتظار حتى يتم التحميل")
        self.التحميل.setDisabled(True)
        thread = YoutubeThread(self.الرابط.text(), self.التعديل.text(), self.progress_bar)
        thread.objects.Finish.connect(self.onFinish)
        qt2.QThreadPool(self).start(thread)
    def onFinish(self, state):
        if state:
            qt.QMessageBox.information(self, "تم", "تم التحميل بنجاح والحفظ")
        else:
            qt.QMessageBox.warning(self, "تنبيه", "فشلت عملية التحميل، ربما تكون المشكلة من الرابط أو الإنترنت أو أنك نسيت تحديد مكان الحفظ")
        self.التحميل.setDisabled(False)
        self.progress_bar.setValue(0)