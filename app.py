import sys
import os
import configparser
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QMenu, QAction, QActionGroup, QInputDialog, QDialog, QSpacerItem, QSizePolicy
from PyQt5.QtCore import QFile, Qt
from CDC import *

config = configparser.ConfigParser()
config.read("settings.ini")

Code.once_system_definer()

class FileDialogExample(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 400, 200)
        self.setWindowTitle('CodeDetect Compiler')
    
        # Text at the top of the window
        topLabel = QLabel('CodeDetect Compiler', self)
        topLabel.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        topLabel.setObjectName('firstLabel')

        # "Open" button
        self.openButton = QPushButton('Open file', self)
        self.openButton.setObjectName('openButton1')
        self.openButton.clicked.connect(self.showDialog)

        # Settings button
        settingsButton = QPushButton('Settings', self)
        settingsButton.setObjectName('settingsButton')
        settingsButton.clicked.connect(self.showSettings)

        # Horizontal layout for buttons
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.openButton)
        buttonLayout.addWidget(settingsButton)
        buttonLayout.setAlignment(Qt.AlignBottom)

        # Main vertical layout
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(topLabel)
        mainLayout.addLayout(buttonLayout)
        
        self.textWindow = None  # Variable to store the current window

        # Enable drag & drop support in the window
        self.setAcceptDrops(True)

        # Set the main layout to the central area of the window
        centralWidget = QWidget()
        centralWidget.setLayout(mainLayout)
        self.setCentralWidget(centralWidget)

        # Load external stylesheet
        style_file = QFile("style/style.css")
        style_file.open(QFile.ReadOnly | QFile.Text)
        style = style_file.readAll()
        self.setStyleSheet(str(style, encoding='utf-8'))

    def showDialog(self):
        try:
            fname = QFileDialog.getOpenFileName(self, 'Open File', '/home')

            if fname[0]:
                global code
                code = Code(fname[0])
                print(f'Selected file: {fname[0]}')

                # Close the previous window if it exists
                if self.textWindow:
                    self.textWindow.close()

                # Open a new window
                self.textWindow = TextWindow(fname[0])
                self.textWindow.show()

        except Exception as e:
            Code.err_out(e)
            errorWindow = ErrorWindow()
            errorWindow.exec_()

    def showSettings(self):
        # Open a new window with settings
        settingsWindow = SettingsWindow()
        # Connect signals and slots to execute functions when menu items are selected
        settingsWindow.action1.triggered.connect(self.handleOption1)
        settingsWindow.action2.triggered.connect(self.handleOption2)
        settingsWindow.action3.triggered.connect(self.handleOption3)
        settingsWindow.action4.triggered.connect(self.handleOption4)
        settingsWindow.exec_()  # Use exec_() to make the window modal (blocking)

    def handleOption1(self):
        try:
            file_path = r'settings.ini'
            if config['CDC']['your_system'].lower() == 'macos':
                os.system(f'open {file_path}')
            elif config['CDC']['your_system'].lower() == 'linux':
                os.system(f'xdg-open {file_path}')
            elif config['CDC']['your_system'].lower() == 'windows':
                os.system(f'start {file_path}')
        except Exception as e:
            Code.err_out(e)

    def handleOption2(self):
        import update

    def handleOption3(self):
        file_path = r'log.txt'
        try:
            if config['CDC']['your_system'].lower() == 'macos':
                os.system(f'open {file_path}')
            elif config['CDC']['your_system'].lower() == 'linux':
                os.system(f'xdg-open {file_path}')
            elif config['CDC']['your_system'].lower() == 'windows':
                os.system(f'start {file_path}')
        except Exception as e:
            Code.err_out(e)

    def handleOption4(self):
        pass

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        files = [url.toLocalFile() for url in event.mimeData().urls()]
        if files:
            self.showDialogWithFile(files[0])

    def showDialogWithFile(self, filename):
        try:
            global code
            code = Code(filename)
            print(f'Dropped file: {filename}')
            # Close the previous window if it exists
            if self.textWindow:
                self.textWindow.close()

            # Open a new window
            self.textWindow = TextWindow(filename)
            self.textWindow.show()
        except Exception as e:
            Code.err_out(e)
            errorWindow = ErrorWindow()
            errorWindow.exec_()

class TextWindow(QWidget):
    def __init__(self, filename):
        super().__init__()

        self.filename = filename

        self.initUI()

    def initUI(self):
        self.setWindowTitle('File info')
        layout = QVBoxLayout()

        label1 = QLabel(f'Select file: {self.filename}', self)
        label2 = QLabel(f'Detect language: {code.detect_lang}', self)

        saveButton = QPushButton('Save', self)
        saveButton.setObjectName('saveButton')
        openButton = QPushButton('Change open', self)
        openButton.setObjectName('openButton2')

        saveButton.clicked.connect(self.savewin)
        openButton.clicked.connect(self.showDialog)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(openButton)
        buttonLayout.addWidget(saveButton)
        buttonLayout.setAlignment(Qt.AlignBottom)

        layout.addWidget(label1)
        layout.addWidget(label2)
        layout.addLayout(buttonLayout)

        self.setLayout(layout)

        # Load external stylesheet
        style_file = QFile("style/style.css")
        style_file.open(QFile.ReadOnly | QFile.Text)
        style = style_file.readAll()
        self.setStyleSheet(str(style, encoding='utf-8'))

    def savewin(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        # Set the suggested file name and filters for extensions
        file_name, _ = QFileDialog.getSaveFileName(self, 'Save File', '', f'{code.detect_lang} ({str(code.filename[0])[1:]});;All Files (*)', options=options)

        if file_name:
            if not '.' in file_name:
                file_name = f'{file_name}{str(code.filename[0])[1:]}'
            Code.compile_and_save(code.temp_save, f'{file_name}')
            print('Save successfully!!!')

            popup_window = PopupWindow("Save Successful!")
            popup_window.exec_()

    def showDialog(self):
        try:
            fname = QFileDialog.getOpenFileName(self, 'Open File', '/home')

            if fname[0]:
                global code
                code = Code(fname[0])
                print(f'Selected file: {fname[0]}')

                # Close the previous window if it exists
                if self.textWindow:
                    self.textWindow.close()

                # Open a new window
                self.textWindow = TextWindow(fname[0])
                self.textWindow.show()

                # Close the current window
                self.close()

        except Exception as e:
            Code.err_out(e)
            errorWindow = ErrorWindow()
            errorWindow.exec_()

class SettingsWindow(QMenu):
    def __init__(self):
        super().__init__()

        radioGroup = QActionGroup(self)
        self.action1 = QAction('Open setting.ini', self)
        self.action1.setCheckable(True)
        self.action2 = QAction('Check update', self)
        self.action2.setCheckable(True)
        self.action3 = QAction('Open log.txt', self)
        self.action3.setCheckable(True)
        self.action4 = QAction('test', self)
        self.action4.setCheckable(True)
        radioGroup.addAction(self.action1)
        radioGroup.addAction(self.action2)
        radioGroup.addAction(self.action3)
        radioGroup.addAction(self.action4)
        self.addActions([self.action1, self.action2, self.action3, self.action4])

class PopupWindow(QDialog):
    def __init__(self, message):
        super().__init__()

        self.setWindowTitle('Save successfully!')
        self.setGeometry(400, 400, 300, 100)

        label = QLabel(message, self)
        okay_button = QPushButton('Okay', self)
        okay_button.clicked.connect(self.accept)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(okay_button)

        self.setLayout(layout)

class ErrorWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Error!')
        self.setGeometry(400, 400, 300, 100)

        label = QLabel("Error!", self)
        label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        label.setObjectName('err_log')
        ok_button = QPushButton('Ok', self)
        ok_button.clicked.connect(self.accept)
        ok_button.setObjectName('Ok')
        open_button = QPushButton('Open log', self)
        open_button.clicked.connect(self.errlogopen)
        open_button.setObjectName('Open')

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(ok_button)
        layout.addWidget(open_button)

        self.setLayout(layout)

        # Load external stylesheet
        style_file = QFile("style/style.css")
        style_file.open(QFile.ReadOnly | QFile.Text)
        style = style_file.readAll()
        self.setStyleSheet(str(style, encoding='utf-8'))
        
    def errlogopen(self):
        try:
            file_path = r'log.txt'
            if config['CDC']['your_system'].lower() == 'macos':
                os.system(f'open {file_path}')
            elif config['CDC']['your_system'].lower() == 'linux':
                os.system(f'xdg-open {file_path}')
            elif config['CDC']['your_system'].lower() == 'windows':
                os.system(f'start {file_path}')
            self.close()
            
        except Exception as e:
            Code.err_out(e)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FileDialogExample()
    ex.show()
    sys.exit(app.exec_())