import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout,
    QSlider, QPushButton, QStyle, QFrame, QLineEdit, QMenu, QDialog, QSizePolicy, QSplitter
)
from PyQt6.QtGui import QPixmap, QAction, QIcon, QMouseEvent
from PyQt6.QtCore import Qt, QSize, QTimer
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from ui.main_window import Ui_MainWindow
from config import load_config, save_config, DEFAULT_CONFIG
from utils.file_utils import is_image_file, is_video_file

THUMB_SIZE = 128

class OverlayWidget(QWidget):
    """Overlay with icon tabs, slider, and toggle logic."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setStyleSheet("background: rgba(0,0,0,0.3);")
        self.setMouseTracking(True)
        self.icons = ["brightness", "contrast", "saturation"]
        self.icon_buttons = []
        self.sliders = []
        self.active_index = 0
        self.slider_values = [50, 50, 50]
        self.toggles = [False, False, False]
        self.init_ui()
        self.hide_timer = QTimer(self)
        self.hide_timer.setInterval(1500)
        self.hide_timer.timeout.connect(self.hide)
        self.hide()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        icon_row = QHBoxLayout()
        for i, icon in enumerate(self.icons):
            btn = QPushButton()
            btn.setIcon(self.style().standardIcon(getattr(QStyle.StandardPixmap, f"SP_DialogYesButton")))
            btn.setCheckable(True)
            btn.setToolTip(icon.capitalize())
            btn.setFixedSize(48, 48)
            btn.clicked.connect(lambda checked, idx=i: self.toggle_tab(idx))
            self.icon_buttons.append(btn)
            icon_row.addWidget(btn)
        layout.addLayout(icon_row)
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.setValue(50)
        self.slider.valueChanged.connect(self.slider_changed)
        layout.addWidget(self.slider)
        self.setLayout(layout)

    def showEvent(self, event):
        self.hide_timer.start()

    def enterEvent(self, event):
        self.hide_timer.stop()
        self.show()

    def leaveEvent(self, event):
        self.hide_timer.start()

    def toggle_tab(self, idx):
        self.toggles[idx] = not self.toggles[idx]
        self.icon_buttons[idx].setChecked(self.toggles[idx])
        self.active_index = idx
        self.slider.setValue(self.slider_values[idx])
        self.slider.setEnabled(self.toggles[idx])
        # TODO: Update file preview and metadata here

    def slider_changed(self, value):
        self.slider_values[self.active_index] = value
        # TODO: Update file preview and metadata here

    def update_overlay(self):
        for i, btn in enumerate(self.icon_buttons):
            btn.setChecked(self.toggles[i])
        self.slider.setValue(self.slider_values[self.active_index])
        self.slider.setEnabled(self.toggles[self.active_index])

class SettingsDialog(QDialog):  # Change QWidget to QDialog
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        from config import load_config, set_config_value
        self.config = load_config()
        layout = QVBoxLayout(self)
        # Thumbnail size
        self.thumb_slider = QSlider(Qt.Orientation.Horizontal)
        self.thumb_slider.setRange(32, 512)
        self.thumb_slider.setValue(self.config.get("thumbnail_size", 128))
        self.thumb_slider.valueChanged.connect(self.on_thumb_size_changed)
        layout.addWidget(QLabel("Thumbnail Size"))
        layout.addWidget(self.thumb_slider)
        # Supported file types
        self.img_types = QLineEdit(", ".join(self.config.get("supported_image_types", [])))
        self.img_types.editingFinished.connect(self.on_img_types_changed)
        self.vid_types = QLineEdit(", ".join(self.config.get("supported_video_types", [])))
        self.vid_types.editingFinished.connect(self.on_vid_types_changed)
        layout.addWidget(QLabel("Image Types (comma separated)"))
        layout.addWidget(self.img_types)
        layout.addWidget(QLabel("Video Types (comma separated)"))
        layout.addWidget(self.vid_types)
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        self.setLayout(layout)

    def on_thumb_size_changed(self, value):
        from config import set_config_value
        set_config_value("thumbnail_size", value)

    def on_img_types_changed(self):
        from config import set_config_value
        types = [s.strip() for s in self.img_types.text().split(",") if s.strip()]
        set_config_value("supported_image_types", types)

    def on_vid_types_changed(self):
        from config import set_config_value
        types = [s.strip() for s in self.vid_types.text().split(",") if s.strip()]
        set_config_value("supported_video_types", types)

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.config = load_config()
        self.setupUi(self)
        self.setWindowTitle("Python Pixel Porter (P³)")
        self.current_dir = self.config.get("default_directory", os.path.expanduser("~"))
        self.file_list = []
        self.single_view_widget = None
        self.overlay = None
        self.video_player = None
        self.video_widget = None
        self.show_hidden_files = False
        self.showMaximized()

        # --- Replace only the lower part with a splitter ---
        # Remove widgets from the old layout
        self.mainVerticalLayout.removeWidget(self.listWidgetDirs)
        self.mainVerticalLayout.removeWidget(self.scrollArea)
        self.listWidgetDirs.setParent(None)
        self.scrollArea.setParent(None)

        # Create splitter for file browser and thumbnail gallery
        self.splitter = QSplitter(Qt.Orientation.Vertical)
        self.splitter.addWidget(self.listWidgetDirs)
        self.splitter.addWidget(self.scrollArea)
        self.splitter.setSizes([150, 600])

        # Insert the splitter below the location bar (which is at index 0)
        self.mainVerticalLayout.insertWidget(1, self.splitter)
        # ---------------------------------------

        # Add "Back to Thumbnails" button to toolbar
        self.actionBack = QAction(QIcon(), "Back", self)
        self.toolBar.addAction(self.actionBack)
        self.actionBack.triggered.connect(self.show_thumbnail_view)
        self.actionBack.setVisible(False)

        # --- Add this block to push following actions to the right ---
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.toolBar.addWidget(spacer)
        # ------------------------------------------------------------

        # Hamburger menu
        self.menu = QMenu()
        self.actionSettings = QAction("Settings", self)
        self.menu.addAction(self.actionSettings)
        self.actionSettings.triggered.connect(self.open_settings)
        self.hamburger = QAction(QIcon.fromTheme("application-menu"), "", self)
        self.hamburger.setIconText("☰")
        self.toolBar.addAction(self.hamburger)
        self.toolBar.actionTriggered.connect(self.handle_toolbar_action)

        # Location bar: use editable combo box for both history and entry
        self.comboBoxLocation.setEditText(self.current_dir)
        self.comboBoxLocation.activated.connect(self.on_location_selected)
        self.comboBoxLocation.lineEdit().returnPressed.connect(self.on_location_entered)
        self.listWidgetDirs.itemDoubleClicked.connect(self.on_dir_selected)
        self.listWidgetDirs.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.listWidgetDirs.customContextMenuRequested.connect(self.on_filebrowser_context_menu)
        self.populate_dir_list()
        self.populate_thumbnails()

    def handle_toolbar_action(self, action):
        if action == self.hamburger:
            self.menu.exec(self.toolBar.mapToGlobal(self.toolBar.actionGeometry(self.hamburger).bottomLeft()))

    def open_settings(self):
        dlg = SettingsDialog(self)
        dlg.exec()

    def populate_dir_list(self):
        self.listWidgetDirs.clear()
        # Add parent directory entry
        if os.path.dirname(self.current_dir) != self.current_dir:
            self.listWidgetDirs.addItem("../")
        try:
            dirs = [d for d in os.listdir(self.current_dir)
                    if os.path.isdir(os.path.join(self.current_dir, d))]
            # Hide hidden files unless show_hidden_files is True
            if not self.show_hidden_files:
                dirs = [d for d in dirs if not d.startswith('.')]
            dirs.sort()
            for d in dirs:
                self.listWidgetDirs.addItem(d)
        except Exception as e:
            self.statusBar().showMessage(f"Error listing directories: {e}", 3000)

    def populate_thumbnails(self):
        layout = self.gridLayoutThumbnails
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        thumb_size = self.config.get("thumbnail_size", DEFAULT_CONFIG["thumbnail_size"])
        try:
            self.file_list = [f for f in os.listdir(self.current_dir)
                              if is_image_file(f) or is_video_file(f)]
        except Exception as e:
            self.statusBar().showMessage(f"Error reading directory: {e}", 3000)
            self.file_list = []
            return

        # Set minimal spacing for a tight grid
        layout.setHorizontalSpacing(4)
        layout.setVerticalSpacing(4)
        layout.setContentsMargins(4, 4, 4, 4)

        # Dynamically calculate columns based on available width
        area_width = self.scrollArea.viewport().width()
        columns = max(1, area_width // (thumb_size + 8))  # 8 for spacing/margin

        row, col = 0, 0
        for idx, fname in enumerate(self.file_list):
            thumb = QLabel()
            thumb.setFixedSize(thumb_size, thumb_size)
            thumb.setAlignment(Qt.AlignmentFlag.AlignCenter)
            thumb.setStyleSheet("border: 1px solid #888; background: #222;")
            try:
                if is_image_file(fname):
                    pixmap = QPixmap(os.path.join(self.current_dir, fname)).scaled(
                        thumb_size, thumb_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                    thumb.setPixmap(pixmap)
                elif is_video_file(fname):
                    thumb.setText("🎬")
                    thumb.setStyleSheet("font-size: 48px; border: 1px solid #888; background: #222; color: #fff;")
            except Exception as e:
                thumb.setText("Err")
                thumb.setToolTip(str(e))
            thumb.mousePressEvent = lambda e, idx=idx: self.show_single_file_view(idx)
            layout.addWidget(thumb, row, col)
            col += 1
            if col >= columns:
                col = 0
                row += 1

    def show_single_file_view(self, idx):
        fname = self.file_list[idx]
        full_path = os.path.join(self.current_dir, fname)

        # Remove the current lower widget (either scrollArea or previous single_view_widget)
        if self.splitter.count() > 1:
            widget = self.splitter.widget(1)
            widget.setParent(None)
        if self.overlay:
            self.overlay.setParent(None)
            self.overlay.deleteLater()
            self.overlay = None
        if self.video_player:
            self.video_player.stop()
            self.video_player.deleteLater()
            self.video_player = None
        if self.video_widget:
            self.video_widget.setParent(None)
            self.video_widget.deleteLater()
            self.video_widget = None
        self.single_view_widget = None

        if is_image_file(fname):
            label = QLabel()
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet("background: #111;")
            label.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            label.customContextMenuRequested.connect(lambda pos, path=full_path: self.open_context_menu(pos, path))
            self.single_view_widget = label

            def resize_pixmap():
                pixmap = QPixmap(full_path)
                if not pixmap.isNull():
                    scaled = pixmap.scaled(
                        label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                    label.setPixmap(scaled)
            label.resizeEvent = lambda event: resize_pixmap()
            resize_pixmap()
            self.splitter.insertWidget(1, self.single_view_widget)
        elif is_video_file(fname):
            self.video_widget = QVideoWidget()
            self.video_player = QMediaPlayer()
            audio_output = QAudioOutput()
            self.video_player.setAudioOutput(audio_output)
            self.video_player.setVideoOutput(self.video_widget)
            self.video_player.setSource(full_path)
            self.video_player.play()
            self.video_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            self.video_widget.customContextMenuRequested.connect(lambda pos, path=full_path: self.open_context_menu(pos, path))
            self.single_view_widget = self.video_widget
            self.splitter.insertWidget(1, self.single_view_widget)
            # QVideoWidget automatically scales video to fit its area
        else:
            return  # Not supported

        # Overlay editing UI
        self.overlay = OverlayWidget(self.single_view_widget)
        self.overlay.setGeometry(40, 40, 400, 120)
        self.overlay.show()
        self.single_view_widget.installEventFilter(self)
        self.actionBack.setVisible(True)

    def eventFilter(self, obj, event):
        if obj == self.single_view_widget:
            if event.type() == event.Type.Enter:
                self.overlay.show()
            elif event.type() == event.Type.Leave:
                self.overlay.hide()
        return super().eventFilter(obj, event)

    def show_thumbnail_view(self):
        if self.splitter.count() > 1:
            widget = self.splitter.widget(1)
            widget.setParent(None)
        if self.overlay:
            self.overlay.setParent(None)
            self.overlay.deleteLater()
            self.overlay = None
        if self.video_player:
            self.video_player.stop()
            self.video_player.deleteLater()
            self.video_player = None
        if self.video_widget:
            self.video_widget.setParent(None)
            self.video_widget.deleteLater()
            self.video_widget = None
        self.single_view_widget = None
        self.splitter.insertWidget(1, self.scrollArea)
        self.scrollArea.show()
        self.actionBack.setVisible(False)

    def on_location_selected(self, idx):
        path = self.comboBoxLocation.itemText(idx)
        self.comboBoxLocation.setEditText(path)
        self.change_directory(path)

    def on_location_entered(self):
        path = self.comboBoxLocation.currentText()
        self.change_directory(path)

    def on_dir_selected(self, item):
        text = item.text()
        if text == "../":
            new_dir = os.path.dirname(self.current_dir)
        else:
            new_dir = os.path.join(self.current_dir, text)
        if os.path.isdir(new_dir):
            self.change_directory(new_dir)

    def on_filebrowser_context_menu(self, pos):
        menu = QMenu(self)
        toggle_action = QAction(
            "Show Hidden Files" if not self.show_hidden_files else "Hide Hidden Files", self)
        menu.addAction(toggle_action)
        toggle_action.triggered.connect(self.toggle_hidden_files)
        menu.exec(self.listWidgetDirs.mapToGlobal(pos))

    def toggle_hidden_files(self):
        self.show_hidden_files = not self.show_hidden_files
        self.populate_dir_list()

    def change_directory(self, path):
        if os.path.isdir(path):
            self.current_dir = path
            if self.comboBoxLocation.findText(path) == -1:
                self.comboBoxLocation.addItem(path)
            self.comboBoxLocation.setEditText(path)
            self.populate_dir_list()
            self.populate_thumbnails()
        else:
            self.statusBar().showMessage("Invalid directory", 2000)

    def open_context_menu(self, pos, path):
        menu = QMenu(self)
        open_action = QAction("Open in Default Viewer", self)
        edit_action = QAction("Open in Editor", self)
        menu.addAction(open_action)
        menu.addAction(edit_action)
        open_action.triggered.connect(lambda: self.open_external(path))
        edit_action.triggered.connect(lambda: self.open_external(path, edit=True))
        menu.exec(self.mapToGlobal(pos))

    def open_external(self, path, edit=False):
        import subprocess
        try:
            if edit:
                # Try to open with default editor (platform dependent)
                if sys.platform.startswith("linux"):
                    subprocess.Popen(["xdg-open", path])
                elif sys.platform == "darwin":
                    subprocess.Popen(["open", "-e", path])
                elif sys.platform == "win32":
                    os.startfile(path)
            else:
                if sys.platform.startswith("linux"):
                    subprocess.Popen(["xdg-open", path])
                elif sys.platform == "darwin":
                    subprocess.Popen(["open", path])
                elif sys.platform == "win32":
                    os.startfile(path)
        except Exception as e:
            self.statusBar().showMessage(f"Failed to open: {e}", 3000)

    def resizeEvent(self, event):
        # Repopulate thumbnails on resize for responsive grid
        if hasattr(self, "gridLayoutThumbnails"):
            self.populate_thumbnails()
        super().resizeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())