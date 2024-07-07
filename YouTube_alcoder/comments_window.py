from PyQt6 import QtWidgets as qt
from PyQt6 import QtGui as qt1
from PyQt6 import QtCore as qt2
from youtube_comment_downloader import YoutubeCommentDownloader
import pyperclip
class CommentsLoaderWorker(qt2.QObject):
    comment_loaded=qt2.pyqtSignal(str)
    finished=qt2.pyqtSignal()
    def __init__(self, video_url):
        super().__init__()
        self.video_url=video_url
        self._is_running=True
    def run(self):
        try:
            downloader=YoutubeCommentDownloader()
            for comment in downloader.get_comments_from_url(self.video_url):
                if not self._is_running:
                    break
                if 'reply' not in comment or not comment['reply']:  # Skip replies
                    self.comment_loaded.emit(comment['text'])
            self.finished.emit()
        except Exception as e:
            print(f"Error loading comments: {e}")
            self.finished.emit()
    def stop(self):
        self._is_running = False
class CommentsWindow(qt.QDialog):
    def __init__(self, video_url, parent=None):
        super().__init__(parent)
        self.setWindowTitle("التعليقات")
        self.showFullScreen()
        self.video_url=video_url
        self.setup_ui()
        self.load_comments_threaded()
    def setup_ui(self):
        qt1.QShortcut("escape", self).activated.connect(lambda: qt.QMessageBox.warning(self, "تنبيه", "للخروج إستخدم إختصار alt + F4"))
        qt1.QShortcut("c",self).activated.connect(self.copy_selected_line)
        self.comments_list=qt.QListWidget()        
        layout=qt.QVBoxLayout(self)
        layout.addWidget(self.comments_list)        
        self.setLayout(layout)
    def load_comments_threaded(self):
        self.comment_thread=qt2.QThread()
        self.comment_worker=CommentsLoaderWorker(self.video_url)
        self.comment_worker.moveToThread(self.comment_thread)
        self.comment_thread.started.connect(self.comment_worker.run)
        self.comment_worker.finished.connect(self.comment_thread.quit)
        self.comment_worker.finished.connect(self.comment_worker.deleteLater)
        self.comment_thread.finished.connect(self.comment_thread.deleteLater)
        self.comment_worker.comment_loaded.connect(self.add_comment_item)
        self.comment_thread.start()
    def add_comment_item(self, comment_text):
        comment_item=qt.QListWidgetItem(comment_text)
        self.comments_list.addItem(comment_item)
    def copy_selected_line(self):
        try:
            selected_items=self.comments_list.selectedItems()
            if selected_items:
                selected_line = selected_items[0].text()
                pyperclip.copy(selected_line)
                qt.QMessageBox.information(self, "تم", "تم نسخ التعليق بنجاح")
        except:
            qt.QMessageBox.warning(self,"تنبيه","حدثت مشكلة أثناء النسخ")