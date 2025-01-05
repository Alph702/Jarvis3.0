from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QStackedWidget, QWidget, QLineEdit, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton, QFrame, QLabel, QSizePolicy, QToolBar
from PyQt5.QtGui import QIcon, QPainter, QMovie, QColor, QTextCharFormat, QFont, QPixmap, QTextBlockFormat, QTextCursor, QPainterPath, QRegion
from PyQt5.QtCore import Qt, QSize, QTimer
from dotenv import get_key, dotenv_values
import sys
import os

env_vars = dotenv_values(".env")
AssistantName = env_vars.get("Assistantname")
current_dir = os.getcwd()
old_chat_message = ""
TempDirPath = f"{current_dir}/Frontend/Files"
GraphicsDirPath = f"{current_dir}/Frontend/Graphics"

def AnswerModifier(answer):
    lines = answer.split("\n")
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = "\n".join(non_empty_lines)
    return modified_answer

def QueryModifier(Query):
    # Convert to lowercase for consistent processing
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = ["how", "what", "who", "where", "when", "why", "which", "whose", "whom", "can you", "what's", "where's", "how's"]
    
    if any(word + " " in new_query for word in question_words):
        if query_words[-1][-1] in [".", "?", "!"]:
            new_query = new_query[:-1] + "?"
        else:
            new_query += "?"
    else:
        if query_words[-1][-1] in [".", "?", "!"]:
            new_query = new_query[:-1] + "."
        else:
            new_query += "."
            
    return new_query.capitalize()

def SetMicrophoneStatus(Command):
    with open(f"{TempDirPath}/Mic.data", "w", encoding="utf-8") as file:
        file.write(Command)

def GetMicrophoneStatus():
    with open(f"{TempDirPath}/Mic.data", "r", encoding="utf-8") as file:
        Status = file.read()
    return Status

def SetAssistantStatus(Status):
    with open(f"{TempDirPath}/status.data", "w", encoding="utf-8") as file:
        file.write(Status)

def GetAssistantStatus():
    with open(f"{TempDirPath}/status.data", "r", encoding="utf-8") as file:
        Status = file.read()
    return Status

def MicButtonInitiated():
    SetMicrophoneStatus("False")

def MicButtonClosed():
    SetMicrophoneStatus("True")

def GraphicsDirectoryPath(filename):
    Path = f"{GraphicsDirPath}/{filename}"
    return Path

def TempDirectoryPath(filename):
    Path = f"{TempDirPath}/{filename}"
    return Path

def ShowTextToScreen(Text):
    with open(f"{TempDirPath}/Responses.data", "w", encoding="utf-8") as file:
        file.write(Text)

class ChatSection(QWidget):
    def __init__(self):
        super(ChatSection, self).__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(-10, 40, 40, 100)
        layout.setSpacing(100)
        
        self.chat_text_edit = QTextEdit()
        self.chat_text_edit.setReadOnly(True)
        self.chat_text_edit.setTextInteractionFlags(Qt.NoTextInteraction)
        self.chat_text_edit.setFrameStyle(QFrame.NoFrame)
        layout.addWidget(self.chat_text_edit)
        self.setStyleSheet("background-color: black;")
        layout.setSizeConstraint(QVBoxLayout.SetDefaultConstraint)
        layout.setStretch(1, 1)
        
        # Set size policy for the chat section
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        
        # Set text color
        text_color = QColor(Qt.blue)
        text_color_text = QTextCharFormat()
        text_color_text.setForeground(text_color)
        self.chat_text_edit.setCurrentCharFormat(text_color_text)
        
        # Setup GIF label
        self.gif_label = QLabel()
        self.gif_label.setStyleSheet("border: none;")
        movie = QMovie(GraphicsDirectoryPath("Jarvis.gif"))
        max_gif_size_w = 480
        max_gif_size_h = 270
        movie.setScaledSize(QSize(max_gif_size_w, max_gif_size_h))
        self.gif_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        self.gif_label.setMovie(movie)
        movie.start()
        layout.addWidget(self.gif_label)
        
        # Setup status label
        self.label = QLabel("")
        self.label.setStyleSheet("color: white; font-size:16px; margin-right: 195px; border: none; margin-top: -30px;")
        self.label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.label)
        layout.setSpacing(-10)
        layout.addWidget(self.gif_label)
        
        # Setup font
        font = QFont()
        font.setPointSize(13)
        self.chat_text_edit.setFont(font)
        
        # Setup timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.loadMessages)
        self.timer.timeout.connect(self.SpeechRecogText)
        self.timer.start(5)
        
        # Setup scrollbar styling
        self.chat_text_edit.viewport().installEventFilter(self)
        self.setStyleSheet("""
            QScrollBar:vertical {
                border: none;
                background: black;
                width: 10px;
                margin: 0px 0px 0px 0px;
            }
            
            QScrollBar::handle:vertical {
                border: none;
                background: white;
                min-height: 20px;
            }
            
            QScrollBar::groove:vertical {
                background: black;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
                height: 10px;
            }
            
            QScrollBar::sub-line:vertical {
                background: black;
                subcontrol-position: top;
                subcontrol-origin: margin;
                height: 10px;
            }
            
            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                border: none;
                background: none;
                color: none;
            }
            
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
            """)

    def loadMessages(self):
        global old_chat_message
        
        with open(f"{TempDirPath}/Responses.data", "r", encoding="utf-8") as file:
            messages = file.read()
            
        if None==messages:
            pass
            
        elif len(messages)<=1:
            pass
            
        elif str(old_chat_message)==str(messages):
            pass
            
        else:
            self.addMessage(message=messages,color="White")
            old_chat_message = messages

    def SpeechRecogText(self):
        with open(f"{TempDirPath}/Status.data", "r", encoding="utf-8") as file:
            messages = file.read()
        self.label.setText(messages)

    def load_icon(self, path, width=60, height=60):
        pixmap = QPixmap(path)
        new_pixmap = pixmap.scaled(width, height)
        self.icon_label.setPixmap(new_pixmap)

    def toggle_icon(self, event=None):
        if self.toggled:
            self.load_icon(GraphicsDirectoryPath("voice.png"), 60, 60)
            MicButtonInitiated()
        else:
            self.load_icon(GraphicsDirectoryPath("mic.png"), 60, 60)
            MicButtonClosed()
        self.toggled = not self.toggled

    def addMessage(self, message, color=None):
        cursor = self.chat_text_edit.textCursor()
        cursor.movePosition(QTextCursor.End)
        
        # Set text format
        format = QTextCharFormat()
        format.setForeground(QColor(color if color else "white"))
        format.setFontFamily("Consolas")
        
        # Set block format for margins
        block_format = QTextBlockFormat()
        block_format.setTopMargin(10)
        block_format.setLeftMargin(10)
        
        # Apply formats and insert text
        cursor.setBlockFormat(block_format)
        cursor.setCharFormat(format)
        cursor.insertText(message + "\n")
        
        # Update cursor and scroll to bottom
        self.chat_text_edit.setTextCursor(cursor)
        self.chat_text_edit.ensureCursorVisible()

class InitialScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        desktop = QApplication.desktop()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        # Center container for GIF
        center_container = QWidget()
        center_layout = QVBoxLayout(center_container)
        center_container.setStyleSheet("background-color: black;")
        
        # GIF setup
        gif_label = QLabel()
        movie = QMovie(GraphicsDirectoryPath("Jarvis.gif"))
        max_gif_size_w = 480
        max_gif_size_h = 270
        movie.setScaledSize(QSize(max_gif_size_w, max_gif_size_h))
        gif_label.setMovie(movie)
        movie.start()
        
        # Center the GIF
        gif_label.setAlignment(Qt.AlignCenter)
        center_layout.addWidget(gif_label)
        center_layout.setAlignment(Qt.AlignCenter)
        
        # Status label
        self.label = QLabel("")
        self.label.setStyleSheet("color: white; font-size: 16px;")
        self.label.setAlignment(Qt.AlignCenter)
        
        # Microphone icon
        self.icon_label = QLabel()
        self.icon_label.setCursor(Qt.PointingHandCursor)
        self.icon_label.mousePressEvent = self.toggle_icon
        pixmap = QPixmap(GraphicsDirectoryPath("Mic_on.png"))
        new_pixmap = pixmap.scaled(60, 60)
        self.icon_label.setPixmap(new_pixmap)
        self.icon_label.setAlignment(Qt.AlignCenter)
        
        # Add widgets to main layout
        content_layout.addStretch()
        content_layout.addWidget(center_container)
        content_layout.addWidget(self.label)
        content_layout.addWidget(self.icon_label)
        content_layout.addStretch()
        
        self.setLayout(content_layout)
        self.setStyleSheet("background-color: black;")
        
        # Timer for status updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.SpeechRecogText)
        self.timer.start(5)
        
        # Initialize microphone status
        self.mic_status = True
        SetMicrophoneStatus("True")

    def SpeechRecogText(self):
        with open(TempDirectoryPath("Status.data"), "r", encoding="utf-8") as file:
            messages = file.read()
        self.label.setText(messages)

    def toggle_icon(self, event=None):
        self.mic_status = not self.mic_status
        if self.mic_status:
            self.load_icon(GraphicsDirectoryPath("Mic_on.png"))
            SetMicrophoneStatus("True")
        else:
            self.load_icon(GraphicsDirectoryPath("Mic_off.png"))
            SetMicrophoneStatus("False")

    def load_icon(self, path, width=60, height=60):
        pixmap = QPixmap(path)
        new_pixmap = pixmap.scaled(width, height)
        self.icon_label.setPixmap(new_pixmap)

class MessageScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        desktop = QApplication.desktop()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.status_label = QLabel("")
        layout.addWidget(self.status_label)
        chat_section = ChatSection()
        layout.addWidget(chat_section)
        self.setLayout(layout)
        self.setStyleSheet("background-color: black;")

class CustomTopBar(QWidget):
    def __init__(self, parent=None, stacked_widget=None):
        super(CustomTopBar, self).__init__(parent)
        self.parent = parent
        self.stacked_widget = stacked_widget
        self.draggable = True
        self.dragging_threshold = 5
        self.mousePressPos = None
        self.mouseMovePos = None
        self.restore_icon = QIcon(GraphicsDirectoryPath("Restore.png"))
        self.maximize_icon = QIcon(GraphicsDirectoryPath("Maximize.png"))
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Title bar container
        title_bar = QWidget()
        title_bar.setFixedHeight(40)
        title_bar_layout = QHBoxLayout(title_bar)
        title_bar_layout.setContentsMargins(10, 0, 10, 0)
        title_bar_layout.setSpacing(5)
        
        # Title
        title_label = QLabel(f" {str(AssistantName).capitalize()} AI ")
        title_label.setStyleSheet("color: black; font-size: 20px; background-color:white")
        
        # Navigation buttons
        home_button = QPushButton("  Home")
        home_button.setIcon(QIcon(GraphicsDirectoryPath("Home.png")))
        home_button.setStyleSheet("height:40px; background-color:white; color: black")
        
        message_button = QPushButton("  Chats")
        message_button.setIcon(QIcon(GraphicsDirectoryPath("Chats.png")))
        message_button.setStyleSheet("height:40px; background-color:white; color: black")
        
        # Window control buttons
        minimize_button = QPushButton()
        minimize_button.setIcon(QIcon(GraphicsDirectoryPath("Minimize2.png")))
        minimize_button.setStyleSheet("background-color:white")
        
        self.maximize_button = QPushButton()
        self.maximize_button.setIcon(self.maximize_icon)
        self.maximize_button.setStyleSheet("background-color:white")
        
        close_button = QPushButton()
        close_button.setIcon(QIcon(GraphicsDirectoryPath("Close.png")))
        close_button.setStyleSheet("background-color:white")
        
        # Add buttons to layout
        title_bar_layout.addWidget(title_label)
        title_bar_layout.addStretch(1)
        title_bar_layout.addWidget(home_button)
        title_bar_layout.addWidget(message_button)
        title_bar_layout.addStretch(1)
        title_bar_layout.addWidget(minimize_button)
        title_bar_layout.addWidget(self.maximize_button)
        title_bar_layout.addWidget(close_button)
        
        # Connect button signals
        home_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        message_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        minimize_button.clicked.connect(lambda: self.window().showMinimized())
        self.maximize_button.clicked.connect(self.toggleMaximize)
        close_button.clicked.connect(lambda: self.window().close())
        
        # Add title bar to main layout
        layout.addWidget(title_bar)
        
        self.setLayout(layout)
        self.setFixedHeight(40)
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                border: none;
            }
            QPushButton {
                padding: 5px;
                border: none;
                min-width: 30px;
                max-width: 100px;
                height: 30px;
            }
            QPushButton:hover {
                background-color: #e6e6e6;
            }
            QPushButton#close:hover {
                background-color: red;
            }
        """)

    def toggleMaximize(self):
        if self.window().isMaximized():
            self.window().showNormal()
            self.maximize_button.setIcon(self.maximize_icon)
        else:
            # Save the current geometry before maximizing
            self.window().showMaximized()
            self.maximize_button.setIcon(self.restore_icon)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mousePressPos = event.globalPos()
            self.mouseMovePos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.mousePressPos is not None:
            delta = event.globalPos() - self.mouseMovePos
            if not self.window().isMaximized():
                self.window().move(self.window().pos() + delta)
            self.mouseMovePos = event.globalPos()

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.toggleMaximize()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Set window flags for frameless but resizable window
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowMinimizeButtonHint)
        self.setAttribute(Qt.WA_TranslucentBackground, False)  # Disable transparency
        self.setMinimumSize(800, 600)
        self.initUI()

    def initUI(self):
        # Set initial window size to 80% of screen size
        desktop = QApplication.desktop()
        available_geometry = desktop.availableGeometry()  # This excludes taskbar area
        window_width = int(available_geometry.width() * 0.8)
        window_height = int(available_geometry.height() * 0.8)
        
        # Center the window in the available space
        self.setGeometry(
            available_geometry.x() + (available_geometry.width() - window_width) // 2,
            available_geometry.y() + (available_geometry.height() - window_height) // 2,
            window_width,
            window_height
        )
        
        # Create central widget and main layout
        central_widget = QWidget()
        central_widget.setObjectName("centralWidget")
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(1, 1, 1, 1)  # Add small border
        layout.setSpacing(0)
        
        # Create stacked widget for multiple screens
        self.stacked_widget = QStackedWidget()
        
        # Create and add custom title bar
        self.title_bar = CustomTopBar(self, self.stacked_widget)
        layout.addWidget(self.title_bar)
        
        # Add stacked widget to layout
        layout.addWidget(self.stacked_widget)
        
        # Create and add screens
        self.initial_screen = InitialScreen()
        self.message_screen = MessageScreen()
        
        self.stacked_widget.addWidget(self.initial_screen)
        self.stacked_widget.addWidget(self.message_screen)
        
        self.setStyleSheet("""
            QMainWindow {
                background-color: black;
            }
            QWidget#centralWidget {
                background-color: black;
                border: 1px solid #333;
            }
            QStackedWidget {
                background-color: black;
            }
        """)

def GraphicalUserInterface():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    GraphicalUserInterface()