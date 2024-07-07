from PyQt6 import QtWidgets as qt
from PyQt6 import QtGui as qt1
from PyQt6 import QtCore as qt2
from Playlist_videos import PlaylistVideosWindow
from description_window import DescriptionWindow
from comments_window import CommentsWindow
from low_quality_video import LowQualityVideoWindow
from high_quality_video import HighQualityVideoWindow
from low_quality_audio import LowQualityAudioWindow
from high_quality_audio import HighQualityAudioWindow
from pytube import YouTube
import Playlist_audio_high_quality,Playlist_audio_low_quality,Playlist_video_high_quality,Playlist_video_low_quality
import Video_high_quality,Video_low_quality,Audio_high_quality,Audio_low_quality
import youtubesearchpython, about,pyperclip,pytube,yt_dlp,dic,winsound,subtitle,Playlist,clip
import youtubesearchpython as ytsearch
import speech_recognition as sr
class WorkerThread(qt2.QThread):
    result_signal=qt2.pyqtSignal(object)
    error_signal=qt2.pyqtSignal(str)
    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func=func
        self.args=args
        self.kwargs=kwargs
    def run(self):
        try:
            result=self.func(*self.args, **self.kwargs)
            self.result_signal.emit(result)
        except Exception as e:
            self.error_signal.emit(str(e))
class tab1(qt.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()    
    def init_ui(self):
        self.next_page_token=None
        self.عرض_فئة=qt.QLabel("تحديد فئة البحث")
        self.الفئة=qt.QComboBox()
        self.الفئة.setAccessibleName("تحديد فئة البحث")
        self.الفئة.addItem("الفيديوهات")
        self.الفئة.addItem("قوائم التشغيل")        
        self.عرض_اللغات=qt.QLabel("قم باختيار لغة الإدخال الصوتي")
        self.اللغة=qt.QComboBox()
        self.اللغة.setAccessibleName("قم باختيار لغة الإدخال الصوتي")
        self.اللغة.addItems(dic.languages.keys())
        self.الصوتي=qt.QPushButton("بدء الإدخال الصوتي")
        self.الصوتي.setDefault(True)
        self.الصوتي.clicked.connect(self.record_and_recognize)
        self.عرض_البحث=qt.QLabel("أكتب محتوى البحث")
        self.البحث=qt.QLineEdit()
        self.البحث.setAccessibleName("أكتب محتوى البحث")
        self.بدء=qt.QPushButton("بدء البحث")
        self.بدء.setDefault(True)
        self.بدء.clicked.connect(self.results)
        self.النتيجة=qt.QListWidget()
        self.النتيجة.setAccessibleName("نتائج البحث")                
        self.النتيجة.verticalScrollBar().valueChanged.connect(self.load_more_results)
        self.النتيجة.setContextMenuPolicy(qt2.Qt.ContextMenuPolicy.CustomContextMenu)        
        self.النتيجة.customContextMenuRequested.connect(self.player)        
        qt1.QShortcut("ctrl+q",self).activated.connect(lambda: self.البحث.setFocus())
        layout=qt.QVBoxLayout()
        layout.addWidget(self.عرض_فئة)
        layout.addWidget(self.الفئة)
        layout.addWidget(self.عرض_اللغات)
        layout.addWidget(self.اللغة)
        layout.addWidget(self.الصوتي)
        layout.addWidget(self.عرض_البحث)
        layout.addWidget(self.البحث)
        layout.addWidget(self.بدء)
        layout.addWidget(self.النتيجة)
        self.setLayout(layout)    
    def player(self, position):
        القائمة=qt.QMenu(self)
        فئة_البحث=self.الفئة.currentText()
        if فئة_البحث == "الفيديوهات":
            فيديو=القائمة.addAction("تشغيل كفيديو بأعلى جودة")
            صوت=القائمة.addAction("تشغيل كصوت بأعلى جودة")
            فيديو_ضعيف=القائمة.addAction("تشغيل كفيديو بأقل جودة")
            صوت_ضعيف=القائمة.addAction("تشغيل كصوت بأقل جودة")
            تنزيل_فيديو=القائمة.addAction("تنزيل كفيديو بأعلى جودة")
            تنزيل_صوت=القائمة.addAction("تنزيل كصوت بأعلى جودة")
            تنزيل_فيديو_ضعيف=القائمة.addAction("تنزيل كفيديو بأقل جودة")
            تنزيل_صوت_ضعيف=القائمة.addAction("تنزيل كصوت بأقل جودة")
            رابط=القائمة.addAction("نسخ الرابط")
            الوصف=القائمة.addAction("عرض الوصف")
            التعليقات=القائمة.addAction("عرض التعليقات")
            فيديو.triggered.connect(lambda: self.open_window('high_quality_video'))
            صوت.triggered.connect(lambda: self.open_window('high_quality_audio'))
            فيديو_ضعيف.triggered.connect(lambda: self.open_window('low_quality_video'))
            صوت_ضعيف.triggered.connect(lambda: self.open_window('low_quality_audio'))
            رابط.triggered.connect(self.copy_link)
            الوصف.triggered.connect(self.show_video_description)
            التعليقات.triggered.connect(self.show_comments_window)
            تنزيل_فيديو.triggered.connect(lambda: self.download_video_high_quality())
            تنزيل_صوت.triggered.connect(lambda: self.download_audio_high_quality())
            تنزيل_فيديو_ضعيف.triggered.connect(lambda: self.download_video_low_quality())
            تنزيل_صوت_ضعيف.triggered.connect(lambda: self.download_audio_low_quality())
        elif فئة_البحث == "قوائم التشغيل":
            رابط_القائمة=القائمة.addAction("نسخ رابط قائمة التشغيل")
            فتح_القائمة=القائمة.addAction("عرض فيديوهات قائمة التشغيل")
            تنزيل_فيديو_قائمة=القائمة.addAction("تنزيل قائمة التشغيل كفيديو بأعلى جودة")
            تنزيل_صوت_قائمة=القائمة.addAction("تنزيل قائمة التشغيل كصوت بأعلى جودة")
            تنزيل_فيديو_قائمة_ضعيف=القائمة.addAction("تنزيل قائمة التشغيل كفيديو بأقل جودة")            
            تنزيل_صوت_قائمة_ضعيف=القائمة.addAction("تنزيل قائمة التشغيل كصوت بأقل جودة")
            رابط_القائمة.triggered.connect(self.copy_link)
            فتح_القائمة.triggered.connect(lambda: self.open_playlist_videos(self.get_selected_item_link()))
            تنزيل_فيديو_قائمة.triggered.connect(lambda: self.download_playlist_video_high_quality())
            تنزيل_فيديو_قائمة_ضعيف.triggered.connect(lambda: self.download_playlist_video_low_quality())
            تنزيل_صوت_قائمة.triggered.connect(lambda: self.download_playlist_audio_high_quality())
            تنزيل_صوت_قائمة_ضعيف.triggered.connect(lambda: self.download_playlist_audio_low_quality())
        القائمة.exec(self.النتيجة.viewport().mapToGlobal(position))
    def handle_error(self, error):
        qt.QMessageBox.warning(self, "تنبيه", f"حدث خطأ: {error}")
    def results(self):
        self.next_page_token=None
        self.النتيجة.clear()
        self.النتيجة.setFocus()
        self.load_more_results()
    def download_playlist_video_high_quality(self):
        url=self.get_selected_item_link()
        if not url:
            return
        dlg=Playlist_video_high_quality.dialog()
        dlg.الرابط.setText(url)
        dlg.exec()
    def download_playlist_video_low_quality(self):
        url=self.get_selected_item_link()
        if not url:
            return
        dlg=Playlist_video_low_quality.dialog()
        dlg.الرابط.setText(url)
        dlg.exec()
    def download_playlist_audio_high_quality(self):
        url=self.get_selected_item_link()
        if not url:
            return
        dlg=Playlist_audio_high_quality.dialog()
        dlg.الرابط.setText(url)
        dlg.exec()
    def download_playlist_audio_low_quality(self):
        url=self.get_selected_item_link()
        if not url:
            return
        dlg=Playlist_audio_low_quality.dialog()
        dlg.الرابط.setText(url)
        dlg.exec()
    def download_video_high_quality(self):
        url=self.get_selected_item_link()
        if not url:
            return
        dlg=Video_high_quality. HighQualityVideoDownloadDialog()
        dlg.الرابط.setText(url)
        dlg.exec()
    def download_video_low_quality(self):
        url=self.get_selected_item_link()
        if not url:
            return
        dlg=Video_low_quality. LowQualityVideoDownloadDialog()
        dlg.الرابط.setText(url)
        dlg.exec()
    def download_audio_high_quality(self):
        url=self.get_selected_item_link()
        if not url:
            return
        dlg=Audio_high_quality. HighQualityAudioDownloadDialog()
        dlg.الرابط.setText(url)
        dlg.exec()
    def download_audio_low_quality(self):
        url=self.get_selected_item_link()
        if not url:
            return
        dlg=Audio_low_quality. LowQualityAudioDownloadDialog()
        dlg.الرابط.setText(url)
        dlg.exec()
    def load_more_results(self):
        if self.النتيجة.verticalScrollBar().value() == self.النتيجة.verticalScrollBar().maximum():
            self.thread=WorkerThread(self._load_more_results)
            self.thread.result_signal.connect(self.handle_results)
            self.thread.error_signal.connect(self.handle_error)
            self.thread.start()
    def _load_more_results(self):
        try:
            نتيجة_البحث=self.البحث.text()
            فئة_البحث=self.الفئة.currentText()
            if not نتيجة_البحث:
                raise ValueError("يرجى إدخال كلمات للبحث")
            if فئة_البحث == "الفيديوهات":
                search=ytsearch.VideosSearch(نتيجة_البحث, limit=20)
            elif فئة_البحث == "قوائم التشغيل":
                search=ytsearch.PlaylistsSearch(نتيجة_البحث, limit=20)            
            النتائج=[]
            for صفحة in range(10):
                if صفحة>0:
                    search.next()                    
                النتائج.extend(search.result()['result'])
            return النتائج
        except Exception as e:
            raise e
    def handle_results(self, النتائج):
        try:
            فئة_البحث=self.الفئة.currentText()
            for عنصر in النتائج:
                if فئة_البحث == "الفيديوهات":
                    title=عنصر['title']
                    duration=عنصر.get('duration', 'No duration available')
                    views=عنصر.get('viewCount', {}).get('text', 'No views available')
                    channel_name=عنصر['channel'].get('name', 'No channel name available')
                    link=عنصر['link']
                    item=f"{title} - المدة {duration} - {channel_name} - {views}"
                    item_obj=qt.QListWidgetItem(item)
                    item_obj.setData(qt2.Qt.ItemDataRole.UserRole, link)
                    self.النتيجة.addItem(item_obj)
                elif فئة_البحث == "قوائم التشغيل":
                    title=عنصر['title']
                    video_count=عنصر.get('videoCount', 'No video count available')
                    channel_name=عنصر['channel'].get('name', 'No channel name available')
                    link=عنصر['link']
                    item=f"{title} - {video_count} - {channel_name}"
                    item_obj=qt.QListWidgetItem(item)
                    item_obj.setData(qt2.Qt.ItemDataRole.UserRole, link)
                    self.النتيجة.addItem(item_obj)                
        except Exception as e:
            qt.QMessageBox.warning(self, "تنبيه", f"حدث خطأ أثناء عرض النتائج: {e}")
    def record_and_recognize(self):
        self.thread=WorkerThread(self._record_and_recognize)
        self.thread.result_signal.connect(self.handle_recognition_result)
        self.thread.error_signal.connect(self.handle_error)
        self.thread.start()
    def _record_and_recognize(self):
        lang=dic.languages[self.اللغة.currentText()]
        التعرف=sr.Recognizer()
        with sr.Microphone() as source:
            winsound.PlaySound("data/1.wav", winsound.SND_FILENAME)
            الصوت=التعرف.listen(source)
            try:
                winsound.PlaySound("data/2.wav", winsound.SND_FILENAME)
                النص=التعرف.recognize_google(الصوت, language=lang)
                return النص
            except sr.UnknownValueError:
                raise ValueError("لم أستطع فهم الصوت")
            except sr.RequestError as e:
                raise ValueError("حدثت مشكلة أثناء جلب النص")
    def handle_recognition_result(self, النص):
        self.البحث.setText(النص)
        self.البحث.setFocus()    
    def show_video_description(self):
        video_url=self.get_selected_item_link()
        if not video_url:
            return
        description_window=DescriptionWindow(video_url)
        description_window.exec()
    def open_playlist_videos(self, playlist_url):
        playlist_videos_window=PlaylistVideosWindow(playlist_url)
        playlist_videos_window.exec()    
    def open_window(self, window_type):
        url = self.get_selected_item_link()
        if not url:
            return
        if window_type=='high_quality_video':
            self.video_window=HighQualityVideoWindow(url)
            self.video_window.exec()
        elif window_type=='high_quality_audio':
            self.audio_window=HighQualityAudioWindow(url)
            self.audio_window.exec()
        elif window_type=='low_quality_video':
            self.low_video_window=LowQualityVideoWindow(url)
            self.low_video_window.exec()
        elif window_type=='low_quality_audio':
            self.low_audio_window=LowQualityAudioWindow(url)
            self.low_audio_window.exec()
    def show_comments_window(self):
        video_url=self.get_selected_item_link()
        if not video_url:
            return
        comments_window=CommentsWindow(video_url)
        comments_window.exec()    
    def get_selected_item_link(self):
        try:
            selected_item=self.النتيجة.currentItem()
            url=selected_item.data(qt2.Qt.ItemDataRole.UserRole)
            return url
        except Exception:
            qt.QMessageBox.warning(self, "تنبيه", "لم يتم تحديد عنصر")
            return None
    def copy_link(self):
        try:
            selected_item=self.النتيجة.currentItem()
            url=selected_item.data(qt2.Qt.ItemDataRole.UserRole)
            pyperclip.copy(url)
            qt.QMessageBox.information(self, "تم", "تم نسخ الرابط بنجاح")
        except Exception:
            qt.QMessageBox.warning(self, "تنبيه", "حدث خطأ أثناء النسخ")
class tab2(qt.QWidget):
    def __init__(self):
        super().__init__()        
        self.إظهار1=qt.QLabel("إدخال رابط قائمة تشغيل")
        self.قائمة=qt.QLineEdit()
        self.قائمة.setAccessibleName("إدخال رابط قائمة تشغيل")
        self.فتح_قائمة=qt.QPushButton("فتح قائمة التشغيل")
        self.فتح_قائمة.setDefault(True)
        self.فتح_قائمة.clicked.connect(self.playlist)
        self.إظهار_الوصف=qt.QLabel("إدخال رابط فيديو أو قائمة تشغيل")
        self.فيديو_الوصف=qt.QLineEdit()
        self.فيديو_الوصف.setAccessibleName("إدخال رابط فيديو أو قائمة تشغيل")
        self.الوصف=qt.QPushButton("عرض الوصف")
        self.الوصف.setDefault(True)
        self.الوصف.clicked.connect(self.DX)
        self.إظهار_التعليقات=qt.QLabel("إدخال رابط فيديو")
        self.فيديو_التعليقات=qt.QLineEdit()
        self.فيديو_التعليقات.setAccessibleName("إدخال رابط فيديو")
        self.التعليقات=qt.QPushButton("عرض التعليقات")
        self.التعليقات.setDefault(True)
        self.التعليقات.clicked.connect(self.CO)
        self.إظهار2=qt.QLabel("إدخال رابط فيديو")
        self.فيديو=qt.QLineEdit()
        self.فيديو.setAccessibleName("إدخال رابط فيديو")
        self.تشغيل_فيديو_أعلى=qt.QPushButton("تشغيل فيديو بأعلى جودة")
        self.تشغيل_فيديو_أقل=qt.QPushButton("تشغيل فيديو بأقل جودة")
        self.تشغيل_صوت_أعلى=qt.QPushButton("تشغيل صوت بأعلى جودة")
        self.تشغيل_صوت_أقل=qt.QPushButton("تشغيل صوت بأقل جودة")
        self.تشغيل_صوت_أقل.setDefault(True)
        self.تشغيل_صوت_أعلى.setDefault(True)
        self.تشغيل_فيديو_أعلى.setDefault(True)
        self.تشغيل_فيديو_أقل.setDefault(True)
        self.تشغيل_صوت_أعلى.clicked.connect(self.HA)
        self.تشغيل_صوت_أقل.clicked.connect(self.LA)
        self.تشغيل_فيديو_أقل.clicked.connect(self.LV)
        self.تشغيل_فيديو_أعلى.clicked.connect(self.HV)        
        l=qt.QVBoxLayout()
        l.addWidget(self.إظهار1)
        l.addWidget(self.قائمة)
        l.addWidget(self.فتح_قائمة)
        l.addWidget(self.إظهار_الوصف)
        l.addWidget(self.فيديو_الوصف)
        l.addWidget(self.الوصف)
        l.addWidget(self.إظهار_التعليقات)
        l.addWidget(self.فيديو_التعليقات)
        l.addWidget(self.التعليقات)
        l.addWidget(self.إظهار2)
        l.addWidget(self.فيديو)
        l.addWidget(self.تشغيل_فيديو_أعلى)
        l.addWidget(self.تشغيل_صوت_أعلى)
        l.addWidget(self.تشغيل_فيديو_أقل)
        l.addWidget(self.تشغيل_صوت_أقل)        
        self.setLayout(l)    
    def playlist(self):
        playlist_url=self.قائمة.text()
        if playlist_url:
          PlaylistVideos=PlaylistVideosWindow(playlist_url)
          PlaylistVideos.exec()
        else:
            qt.QMessageBox.warning(self,"تنبيه","الرجاء إدخال رابط قائمة التشغيل")
    def DX(self):
        url=self.فيديو_الوصف.text()
        if url:
            Video=DescriptionWindow(url)
            Video.exec()
        else:
            qt.QMessageBox.warning(self,"تنبيه","الرجاء إدخال رابط فيديو أو قائمة تشغيل")
    def CO(self):
        url=self.فيديو_التعليقات.text()
        if url:
            Video=CommentsWindow(url)
            Video.exec()
        else:
            qt.QMessageBox.warning(self,"تنبيه","الرجاء إدخال رابط الفيديو")
    def HV(self):
        url=self.فيديو.text()
        if url:
            Video=HighQualityVideoWindow(url)
            Video.exec()
        else:
            qt.QMessageBox.warning(self,"تنبيه","الرجاء إدخال رابط الفيديو")
    def LV(self):
        url=self.فيديو.text()
        if url:
            Video=LowQualityVideoWindow(url)
            Video.exec()
        else:
            qt.QMessageBox.warning(self,"تنبيه","الرجاء إدخال رابط الفيديو")
    def HA(self):
        url=self.فيديو.text()
        if url:
            Video=HighQualityAudioWindow(url)
            Video.exec()
        else:
            qt.QMessageBox.warning(self,"تنبيه","الرجاء إدخال رابط الفيديو")
    def LA(self):
        url=self.فيديو.text()
        if url:
            Video=LowQualityAudioWindow(url)
            Video.exec()
        else:
            qt.QMessageBox.warning(self,"تنبيه","الرجاء إدخال رابط الفيديو")
class tab3(qt.QWidget):
    def __init__(self):
        super().__init__()        
        self.الخيارات=qt.QListWidget()        
        self.الخيارات.clicked.connect(self.ch)
        qt1.QShortcut("return",self).activated.connect(self.ch)
        self.الخيارات.addItem("تنزيل مقطع")        
        self.الخيارات.addItem("تنزيل قائمة تشغيل")
        self.الخيارات.addItem("تنزيل ترجمات الفيديوهات subtitles")        
        l=qt.QVBoxLayout()
        l.addWidget(self.الخيارات)
        self.setLayout(l)    
    def ch(self):
        العناصر=self.الخيارات.currentRow()        
        if العناصر==0:
            clip.dialog(self)            .exec()
        elif العناصر==1:
            Playlist.dialog(self).exec()
        elif العناصر==2:
            subtitle.dialog(self).exec()        
class tab4(qt.QWidget):
    def __init__(self):
        super().__init__()                        
        self.الدليل=qt.QListWidget()        
        self.الدليل.addItem("زر المسافة: تشغيل/إيقاف مؤقت.")
        self.الدليل.addItem("home  إيقاف.")
        self.الدليل.addItem("التقديم السريع لمدة 5 ثواني: alt+ السهم الأيمن.")
        self.الدليل.addItem("الترجيع السريع لمدة 5 ثواني: alt+ السهم الأيسر.")
        self.الدليل.addItem("التقديم السريع لمدة 10 ثواني: alt+ السهم الأعلى.")
        self.الدليل.addItem("الترجيع السريع لمدة 10 ثواني: alt+ السهم الأسفل.")
        self.الدليل.addItem("التقديم السريع لمدة 30 ثانية: CTRL+السهم الأيمن.")
        self.الدليل.addItem("الترجيع السريع لمدة 30 ثانية: CTRL+السهم الأيسر.")
        self.الدليل.addItem("التقديم السريع لمدة دقيقة: CTRL+السهم الأعلا.")
        self.الدليل.addItem("الترجيع السريع لمدة دقيقة: CTRL+السهم الأسفل.")
        self.الدليل.addItem("اختصارات Ctrl + الرقم للانتقال مباشرة إلى نسبة محددة من المقطع، على سبيل المثال، Ctrl + 1 للانتقال إلى 10% من المقطع، Ctrl + 2 للانتقال إلى 20%، وهكذا.")
        self.الدليل.addItem("رفع الصوت: shift+ السهم الأعلى.")
        self.الدليل.addItem("خفض الصوت: shift+ السهم الأسفل.")        
        self.الدليل.addItem("CTRL+Q الانتقال سريعا لمربع البحث")
        self.الدليل.addItem("C لنسخ التعليق, ونسخ سطر من الوصف")
        self.الدليل.addItem("A لنسخ كل الوصف")
        self.الدليل.addItem("ملاحظة هامة, عند الخروج من نافذة تشغيل المقطع يرجى الخروج بزر الهروب escape")
        l=qt.QVBoxLayout()
        l.addWidget(self.الدليل)        
        self.setLayout(l)                
class main(qt.QMainWindow):
    def __init__(self):
        super().__init__()
        self.showFullScreen()
        self.setWindowTitle("YouTube alcoder")
        self.التاب = qt.QTabWidget()
        self.التاب.setAccessibleName("الخيارات")
        self.التاب.addTab(tab1(), "البحث في YouTube")
        self.التاب.addTab(tab2(), "التشغيل السريع")
        self.التاب.addTab(tab3(), "التنزيل")
        self.التاب.addTab(tab4(), "دليل المستخدم")
        self.عن = qt.QPushButton("عن المطور")
        self.عن.setDefault(True)
        self.عن.clicked.connect(self.about)        
        l=qt.QVBoxLayout()
        l.addWidget(self.التاب)
        l.addWidget(self.عن)        
        w=qt.QWidget()
        w.setLayout(l)
        self.setCentralWidget(w)        
    def about(self):
        about.dialog(self).exec()
app=qt.QApplication([])
app.setStyle('fusion')
w=main()        
w.show()
app.exec()