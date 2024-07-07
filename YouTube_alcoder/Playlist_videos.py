from PyQt6 import QtWidgets as qt
from PyQt6 import QtGui as qt1
from PyQt6 import QtCore as qt2
import Video_high_quality,Video_low_quality,Audio_high_quality,Audio_low_quality
import yt_dlp, pyperclip, pytube
from youtube_comment_downloader import YoutubeCommentDownloader
from description_window import DescriptionWindow
from comments_window import CommentsWindow
from low_quality_video import LowQualityVideoWindow
from high_quality_video import HighQualityVideoWindow
from low_quality_audio import LowQualityAudioWindow
from high_quality_audio import HighQualityAudioWindow
class PlaylistVideosWindow(qt.QDialog):
    def __init__(self, playlist_url):
        super().__init__()
        self.setWindowTitle("فيديوهات قائمة التشغيل")
        self.showFullScreen()
        self.playlist_url = playlist_url
        self.setup_ui()
        self.load_playlist_info()
        self.load_videos_threaded()  # Use threaded loading
    def setup_ui(self):
        self.videos_list=qt.QListWidget()
        self.videos_list.setContextMenuPolicy(qt2.Qt.ContextMenuPolicy.CustomContextMenu)
        self.videos_list.customContextMenuRequested.connect(self.show_context_menu)
        self.playlist_title=qt.QLineEdit()
        self.playlist_title.setAccessibleName("العنوان")
        self.playlist_title.setReadOnly(True)
        self.playlist_description=qt.QLineEdit()
        self.playlist_description.setReadOnly(True)
        self.playlist_description.setAccessibleName("الوصف")
        qt1.QShortcut("escape",self).activated.connect(lambda: qt.QMessageBox.warning(self,"تنبيه","للخروج إستخدم إختصار alt + F4"))
        layout=qt.QVBoxLayout()
        layout.addWidget(qt.QLabel("عنوان القائمة:"))
        layout.addWidget(self.playlist_title)
        layout.addWidget(qt.QLabel("وصف القائمة:"))
        layout.addWidget(self.playlist_description)
        layout.addWidget(self.videos_list)
        self.setLayout(layout)
    def load_playlist_info(self):
        try:
            playlist=pytube.Playlist(self.playlist_url)
            playlist_title = playlist.title
            playlist_description = playlist.description
            self.playlist_title.setText(playlist_title)
            self.playlist_description.setText(playlist_description)
        except Exception as e:
            qt.QMessageBox.warning(self, "تنبيه", f"حدث خطأ أثناء جلب معلومات قائمة التشغيل: {str(e)}")
    def show_context_menu(self, position):
        item=self.videos_list.itemAt(position)
        if item:
            menu=qt.QMenu()
            play_video_action=menu.addAction("تشغيل كفيديو بأعلى جودة")
            play_audio_action=menu.addAction("تشغيل كصوت بأعلى جودة")
            play_video_action1=menu.addAction("تشغيل كفيديو بأقل جودة")
            play_audio_action1=menu.addAction("تشغيل كصوت بأقل جودة")
            تنزيل_فيديو=menu.addAction("تنزيل كفيديو بأعلى جودة")
            تنزيل_صوت=menu.addAction("تنزيل كصوت بأعلى جودة")
            تنزيل_فيديو_ضعيف=menu.addAction("تنزيل كفيديو بأقل جودة")
            تنزيل_صوت_ضعيف=menu.addAction("تنزيل كصوت بأقل جودة")
            copy_link_action=menu.addAction("نسخ الرابط")
            الوصف=menu.addAction("عرض الوصف")
            التعليقات=menu.addAction("عرض التعليقات")            
            play_video_action.triggered.connect(lambda: self.open_window('high_quality_video'))
            play_audio_action.triggered.connect(lambda: self.open_window('high_quality_audio'))
            play_video_action1.triggered.connect(lambda: self.open_window('low_quality_video'))
            play_audio_action1.triggered.connect(lambda: self.open_window('low_quality_audio'))
            copy_link_action.triggered.connect(lambda: self.copy_link(item.data(qt2.Qt.ItemDataRole.UserRole)))
            الوصف.triggered.connect(lambda: self.show_video_description(item.data(qt2.Qt.ItemDataRole.UserRole)))
            التعليقات.triggered.connect(lambda: self.get_video_comments(item.data(qt2.Qt.ItemDataRole.UserRole)))
            تنزيل_فيديو.triggered.connect(lambda: self.download_video_high_quality())
            تنزيل_صوت.triggered.connect(lambda: self.download_audio_high_quality())
            تنزيل_فيديو_ضعيف.triggered.connect(lambda: self.download_video_low_quality())
            تنزيل_صوت_ضعيف.triggered.connect(lambda: self.download_audio_low_quality())
            menu.exec(self.videos_list.viewport().mapToGlobal(position))
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
    def open_window(self, window_type):
        url=self.get_selected_item_link()
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
    def get_selected_item_link(self):
        selected_item=self.videos_list.currentItem()
        if selected_item:
            return selected_item.data(qt2.Qt.ItemDataRole.UserRole)
        return None
    def load_videos_threaded(self):
        self.video_thread=qt2.QThread()
        self.video_worker=VideoLoaderWorker(self.playlist_url)
        self.video_worker.moveToThread(self.video_thread)
        self.video_thread.started.connect(self.video_worker.run)
        self.video_worker.finished.connect(self.video_thread.quit)
        self.video_worker.finished.connect(self.video_worker.deleteLater)
        self.video_thread.finished.connect(self.video_thread.deleteLater)
        self.video_worker.video_loaded.connect(self.add_video_item)
        self.video_thread.start()
    def add_video_item(self, video_info):
        video_item=qt.QListWidgetItem(video_info["text"])
        video_item.setData(qt2.Qt.ItemDataRole.UserRole, video_info["url"])
        self.videos_list.addItem(video_item)
    def format_duration(self, duration_seconds):
        minutes, seconds=divmod(duration_seconds, 60)
        hours, minutes=divmod(minutes, 60)
        if hours>0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"
    def copy_link(self, url):
        try:
            pyperclip.copy(url)
            qt.QMessageBox.information(self, "تم", "تم نسخ الرابط بنجاح")
        except Exception as e:
            qt.QMessageBox.warning(self, "تنبيه", f"حدث خطأ أثناء النسخ: {str(e)}")
    def show_video_description(self, video_url):
        description=self.get_video_description(video_url)
        if description:
            description_window = DescriptionWindow(description, self)
            description_window.exec()
    def show_comments_window(self, comments):
        self.comments_window=CommentsWindow(comments)
        self.comments_window.exec()
    def get_video_comments(self, url):
        try:
            downloader=YoutubeCommentDownloader()
            comments=downloader.get_comments_from_url(url)
            comment_list=[]
            for comment in comments:
                if 'reply' not in comment or not comment['reply']:
                    comment_list.append(comment['text'])
            comments_text="\n".join(comment_list)
            self.show_comments_window(comments_text)
        except Exception as e:
            qt.QMessageBox.warning(self, "تنبيه", f"حدث خطأ أثناء جلب التعليقات: {str(e)}")
    def get_video_description(self, video_url):
        try:
            ydl=yt_dlp.YoutubeDL({'extract_flat': True, 'force_generic_extractor': True})
            info=ydl.extract_info(video_url, download=False)
            description=info.get('description', '')
            return description
        except Exception as e:
            print(f"Error fetching video description: {e}")
            return None
class VideoLoaderWorker(qt2.QObject):
    video_loaded=qt2.pyqtSignal(dict)
    finished=qt2.pyqtSignal()
    def __init__(self, playlist_url):
        super().__init__()
        self.playlist_url=playlist_url
    def run(self):
        try:
            playlist=pytube.Playlist(self.playlist_url)
            for video in playlist.videos:
                video_info={
                    "text": f"{video.title} - Duration: {self.format_duration(video.length)} - Views: {video.views}",
                    "url": video.watch_url
                }
                self.video_loaded.emit(video_info)
            self.finished.emit()
        except Exception as e:
            print(f"Error loading videos: {e}")
            self.finished.emit()
    def format_duration(self, duration_seconds):
        minutes, seconds=divmod(duration_seconds, 60)
        hours, minutes=divmod(minutes, 60)
        if hours>0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"