from PyQt6 import QtWidgets as qt
from PyQt6 import QtGui as qt1
from PyQt6 import QtCore as qt2
import pyperclip,yt_dlp
class DescriptionLoaderWorker(qt2.QObject):
    description_loaded=qt2.pyqtSignal(str)
    finished=qt2.pyqtSignal()
    def __init__(self, video_url):
        super().__init__()
        self.video_url=video_url
        self._is_running=True
    def run(self):
        try:
            ydl=yt_dlp.YoutubeDL({'extract_flat': True, 'force_generic_extractor': True})
            info=ydl.extract_info(self.video_url, download=False)
            description=info.get('description', '')
            for line in description.split('\n'):
                if not self._is_running:
                    break
                self.description_loaded.emit(line)
            self.finished.emit()
        except Exception as e:
            print(f"Error loading description: {e}")
            self.finished.emit()
    def stop(self):
        self._is_running = False
class DescriptionWindow(qt.QDialog):
    def __init__(self, video_url, parent=None):
        super().__init__(parent)
        self.setWindowTitle("الوصف")
        self.showFullScreen()
        self.video_url=video_url
        self.setup_ui()
        self.load_description_threaded()
    def setup_ui(self):
        qt1.QShortcut("escape", self).activated.connect(lambda: qt.QMessageBox.warning(self, "تنبيه", "للخروج استخدم اختصار alt + F4"))
        qt1.QShortcut("a",self).activated.connect(self.copy_all)
        qt1.QShortcut("c",self).activated.connect(self.copy_selected_line)
        self.الوصف=qt.QListWidget()        
        self.الوصف.setAccessibleName("الوصف")
        layout=qt.QVBoxLayout(self)
        layout.addWidget(self.الوصف)
    def load_description_threaded(self):
        self.description_thread=qt2.QThread()
        self.description_worker=DescriptionLoaderWorker(self.video_url)
        self.description_worker.moveToThread(self.description_thread)
        self.description_thread.started.connect(self.description_worker.run)
        self.description_worker.finished.connect(self.description_thread.quit)
        self.description_worker.finished.connect(self.description_worker.deleteLater)
        self.description_thread.finished.connect(self.description_thread.deleteLater)
        self.description_worker.description_loaded.connect(self.add_description_item)
        self.description_thread.start()
    def add_description_item(self, description_line):
        description_item=qt.QListWidgetItem(description_line)
        self.الوصف.addItem(description_item)
    def copy_selected_line(self):
        try:
            selected_items=self.الوصف.selectedItems()
            if selected_items:
                selected_line=selected_items[0].text()
                pyperclip.copy(selected_line)
                qt.QMessageBox.information(self, "تم", "تم نسخ السطر")
        except:
            qt.QMessageBox.warning(self,"تنبيه","حدثت مشكلة أثناء النسخ")
    def copy_all(self):
        try:
            all_text="\n".join([self.الوصف.item(i).text() for i in range(self.الوصف.count())])
            pyperclip.copy(all_text)
            qt.QMessageBox.information(self, "تم", "تم نسخ الوصف كاملاً")
        except:
            qt.QMessageBox.warning(self,"تنبيه","حدثت مشكلة أثناء النسخ")