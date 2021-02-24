from PyQt5.QtWidgets import QMainWindow, QSizePolicy, QFrame, QFormLayout, QWidget, QTabWidget, QGridLayout, QCheckBox, QLabel, \
    QSpinBox, QHBoxLayout, QLineEdit, QMenuBar, QMenu, QGroupBox, QTextEdit, QPushButton, QAction, QSpacerItem, QTableWidget, \
    QTableWidgetItem, QAbstractItemView, QComboBox, QDoubleSpinBox
from PyQt5.QtCore import QMetaObject, QRect, QThread, QSize, Qt, pyqtSlot
from PyQt5.QtGui import QPixmap, QFont, QIcon
import os
import sys

from base.https.session import Session
from base.output import OutputSender
from base.common import is_admin
from app.cache import Database
from app import path, __version__

class TassomaiUI(object):
    def __init__(self, main_window: QMainWindow):
        self.win = main_window

    def setupUi(self):
        self.win.setWindowTitle(f"Tassomai Automation v{__version__}")
        self.win.setWindowIcon(QIcon(path('images', 'logo.png')))
        self.win.resize(665, 580)

        self.centralwidget = QWidget(self.win)

        self.formLayout = QFormLayout(self.centralwidget)
        self.formLayout.setContentsMargins(5, 0, 5, -1)

        self.topFrame = QFrame(self.centralwidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.topFrame.sizePolicy().hasHeightForWidth())
        self.topFrame.setSizePolicy(sizePolicy)
        self.topFrame.setAutoFillBackground(True)
        self.topFrame.setFrameShape(QFrame.StyledPanel)
        self.topFrame.setFrameShadow(QFrame.Raised)

        self.gridLayout = QGridLayout(self.topFrame)

        self.tassomaiImage = QLabel(self.topFrame)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tassomaiImage.sizePolicy().hasHeightForWidth())
        self.tassomaiImage.setSizePolicy(sizePolicy)
        self.tassomaiImage.setPixmap(QPixmap(path('images', 'banner.png')))
        self.gridLayout.addWidget(self.tassomaiImage, 0, 0, 1, 1)

        self.formLayout.setWidget(0, QFormLayout.SpanningRole, self.topFrame)

        self.tab = QTabWidget(self.centralwidget)

        self.main_tab = QWidget()
        self.automation_tab = QWidget()

        self.gridLayout_4 = QGridLayout(self.main_tab)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)

        self.main_frame = QFrame(self.main_tab)
        self.main_frame.setAutoFillBackground(True)
        self.main_frame.setFrameShape(QFrame.StyledPanel)
        self.main_frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.main_frame)
        self.gridLayout_2.setContentsMargins(5, 6, 2, -1)
        self.gridLayout_2.setVerticalSpacing(10)

        self.gridLayout_5 = QGridLayout(self.automation_tab)
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)

        self.automation_frame = QFrame(self.automation_tab)
        self.automation_frame.setAutoFillBackground(True)
        self.automation_frame.setFrameShape(QFrame.StyledPanel)
        self.automation_frame.setFrameShadow(QFrame.Raised)

        self.delayLayout = QHBoxLayout()
        self.delayLayout.setContentsMargins(0, 0, 0, 0)
        self.delayLayout.setSpacing(3)

        self.delay = QCheckBox(self.main_frame)
        font = QFont()
        font.setPointSize(10)
        self.delay.setFont(font)

        self.delayLayout.addWidget(self.delay)

        self.amountOfDelay = QDoubleSpinBox(self.main_frame)
        self.amountOfDelay.setMinimumWidth(70)
        self.amountOfDelay.setMaximum(25.00)

        self.delayLayout.addWidget(self.amountOfDelay)

        self.label03 = QLabel(self.main_frame)
        self.label03.setSizePolicy(sizePolicy)
        self.label03.setFont(font)

        self.delayLayout.addWidget(self.label03)

        self.amountOfDelay2 = QDoubleSpinBox(self.main_frame)
        self.amountOfDelay2.setMinimumWidth(70)
        self.amountOfDelay2.setMaximum(25.00)

        self.delayLayout.addWidget(self.amountOfDelay2)

        self.label3 = QLabel(self.main_frame)
        self.label3.setSizePolicy(sizePolicy)
        self.label3.setFont(font)

        self.delayLayout.addWidget(self.label3)

        self.whenDelay = QComboBox(self.main_frame)
        self.whenDelay.addItem("question")
        self.whenDelay.addItem("quiz")
        self.whenDelay.setMaximumWidth(100)

        self.delayLayout.addWidget(self.whenDelay)

        self.verticalSpacer1 = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.delayLayout.addItem(self.verticalSpacer1)

        self.gridLayout_2.addLayout(self.delayLayout, 2, 0, 1, 1)

        self.randomnessLayout = QHBoxLayout()
        self.randomnessLayout.setContentsMargins(0, 0, 0, 0)
        self.randomnessLayout.setSpacing(3)

        self.randomness = QCheckBox(self.main_frame)
        self.randomness.setFont(font)
        self.randomness.setMaximumWidth(338)

        self.randomnessLayout.addWidget(self.randomness)

        self.randomnessAmount = QSpinBox(self.main_frame)
        self.randomnessAmount.setMinimumWidth(70)
        self.randomnessAmount.setMaximum(600)

        self.randomnessLayout.addWidget(self.randomnessAmount)

        self.label4 = QLabel(self.main_frame)
        self.label4.setSizePolicy(sizePolicy)
        self.label4.setFont(font)

        self.randomnessLayout.addWidget(self.label4)

        self.gridLayout_2.addLayout(self.randomnessLayout, 3, 0, 1, 1)

        self.dailyGoal = QCheckBox(self.main_frame)
        font = QFont()
        font.setPointSize(10)
        self.dailyGoal.setFont(font)
        self.gridLayout_2.addWidget(self.dailyGoal, 4, 0, 1, 1)

        self.bonusGoal = QCheckBox(self.main_frame)
        self.bonusGoal.setFont(font)
        self.gridLayout_2.addWidget(self.bonusGoal, 5, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()

        self.label1 = QLabel(self.main_frame)
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label1.sizePolicy().hasHeightForWidth())
        self.label1.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(10)
        self.label1.setFont(font)
        self.horizontalLayout.addWidget(self.label1)

        self.maxQuizes = QSpinBox(self.main_frame)
        self.maxQuizes.setMinimum(1)
        self.maxQuizes.setMaximum(1000000)
        self.maxQuizes.setProperty("value", 1000)
        self.horizontalLayout.addWidget(self.maxQuizes)

        self.label2 = QLabel(self.main_frame)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label2.sizePolicy().hasHeightForWidth())
        self.label2.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(10)
        self.label2.setFont(font)
        self.horizontalLayout.addWidget(self.label2)
        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.userBox = QGroupBox(self.main_frame)
        font = QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.userBox.setFont(font)
        self.gridLayout_3 = QGridLayout(self.userBox)

        self.emailTassomaiLabel = QLabel(self.userBox)
        self.gridLayout_3.addWidget(self.emailTassomaiLabel, 0, 0, 1, 1)
        self.emailTassomai = QLineEdit(self.userBox)
        self.gridLayout_3.addWidget(self.emailTassomai, 0, 1, 1, 1)

        self.passwordTassomaiLabel = QLabel(self.userBox)
        self.gridLayout_3.addWidget(self.passwordTassomaiLabel, 1, 0, 1, 1)
        self.passwordTassomai = QLineEdit(self.userBox)
        self.passwordTassomai.setEchoMode(QLineEdit.Password)
        self.gridLayout_3.addWidget(self.passwordTassomai, 1, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout_3.addItem(self.verticalSpacer, 2, 0, 1, 1)

        self.gridLayout_4.addWidget(self.main_frame, 0, 0, 1, 1)
        self.gridLayout_5.addWidget(self.automation_frame, 0, 0, 1, 1)

        self.tab.addTab(self.main_tab, "")
        self.tab.addTab(self.automation_tab, "")

        self.formLayout.setWidget(1, QFormLayout.SpanningRole, self.tab)

        self.gridLayout_2.addWidget(self.userBox, 0, 0, 1, 1)

        self.buttonsLayout = QHBoxLayout()

        self.bottom_frame = QFrame(self.centralwidget)
        self.bottom_frame.setFrameShape(QFrame.StyledPanel)
        self.bottom_frame.setFrameShadow(QFrame.Raised)

        self.gridLayout_7 = QGridLayout(self.bottom_frame)
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)


        self.startButton = QPushButton(self.bottom_frame)
        self.buttonsLayout.addWidget(self.startButton)

        self.stopButton = QPushButton(self.bottom_frame)
        self.buttonsLayout.addWidget(self.stopButton)

        self.gridLayout_7.addLayout(self.buttonsLayout, 0, 0, 1, 1)

        self.output = QTextEdit(self.bottom_frame)
        self.gridLayout_7.addWidget(self.output, 1, 0, 1, 1)

        self.formLayout.setWidget(2, QFormLayout.SpanningRole, self.bottom_frame)

        self.win.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(self.win)
        self.menubar.setGeometry(QRect(0, 0, 665, 21))

        self.tools_menu = QMenu(self.menubar)

        self.uninstall_option = QAction()

        self.tools_menu.addAction(self.uninstall_option)

        self.menubar.addAction(self.tools_menu.menuAction())

        self.win.setMenuBar(self.menubar)

        self.createTable()
        self.retranslateUi()

        self.tab.setCurrentIndex(0)
        self.tab.currentChanged['int'].connect(lambda k: self.bottom_frame.hide() if k != 0 else self.bottom_frame.show())

        QMetaObject.connectSlotsByName(self.win)

    def retranslateUi(self):
        self.dailyGoal.setChecked(True)
        self.dailyGoal.setText("Finish when daily goal complete")
        self.bonusGoal.setText("Finish when bonus goal complete")
        self.delay.setText("Add a delay between")
        self.label03.setText("and")
        self.label3.setText("seconds between each")
        self.randomness.setText("Make it so that you answer a question incorrectly every")
        self.label4.setText("questions")
        self.label1.setText("Only do a maximum of ")
        self.label2.setText(" quiz(s)")
        self.userBox.setTitle("User Settings")
        self.passwordTassomaiLabel.setText("Password for Tassomai login")
        self.emailTassomaiLabel.setText("Email for Tassomai login")
        self.tab.setTabText(self.tab.indexOf(self.main_tab), "General")
        self.tab.setTabText(self.tab.indexOf(self.automation_tab), "Automation")
        self.startButton.setText("Start Automation")
        self.stopButton.setText("Stop Automation")
        self.tools_menu.setTitle("Tools")
        self.uninstall_option.setText("Uninstall (coming soon)")
        self.output.setReadOnly(True)
        self.startButton.setEnabled(True)
        self.stopButton.setEnabled(False)
        self.output.setHtml("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">-------------------------------------------</p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:600; text-decoration: underline; color:#14860a;\">All output will go here<br /></span></p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">-------------------------------------------</p>\n"
)

    def createTable(self):
        self.table = QTableWidget(self.automation_tab)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.table.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.table.setShowGrid(True)
        self.table.setGridStyle(Qt.DashLine)
        self.table.setRowCount(999999)
        self.table.setColumnCount(6)
        for i in range(6):
            self.table.setHorizontalHeaderItem(i, QTableWidgetItem())
            self.table.horizontalHeaderItem(i).setTextAlignment(Qt.AlignLeft)
        for i in range(6):
            self.table.setItem(0, i, QTableWidgetItem())
            self.table.setItem(1, i, QTableWidgetItem())
        self.table.horizontalHeader().setVisible(True)
        self.table.horizontalHeader().setHighlightSections(True)
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setHighlightSections(True)
        self.gridLayout_5.addWidget(self.table, 0, 0, 1, 1)
        headers = ["Quiz", "Num", "Question", "Correct", "Time", "Answer"]
        for header in headers:
            item = self.table.horizontalHeaderItem(headers.index(header))
            item.setText(header)
            item.setSizeHint(QSize(25, 25))
        self.table.setColumnWidth(0, 40)
        self.table.setColumnWidth(1, 40)
        self.table.setColumnWidth(2, 175)
        self.table.setColumnWidth(3, 80)
        self.table.setColumnWidth(4, 80)
        self.table.setColumnWidth(5, 230)

class Window(QMainWindow):
    def __init__(self, show_stats=True, close=False, parent=None):
        super().__init__(parent)
        self.showStats = show_stats
        self.shouldClose = close
        self.row = 0

        self.ui = TassomaiUI(self)
        self.ui.setupUi()

        self.outputSender = OutputSender(self.ui.output)

        self.database = Database(f'{os.environ["USERPROFILE"]}/AppData/Local/tassomai-automation/', 'answers.lzma')
        self.cache = Database(f'{os.environ["USERPROFILE"]}/AppData/Local/tassomai-automation/', 'info.lzma')
        if os.path.isfile(f'{os.environ["USERPROFILE"]}/AppData/Local/tassomai-automation/answers.json'):
            os.remove(f'{os.environ["USERPROFILE"]}/AppData/Local/tassomai-automation/answers.json')
        if os.path.isfile(f'{os.environ["USERPROFILE"]}/AppData/Local/tassomai-automation/info.json'):
            os.remove(f'{os.environ["USERPROFILE"]}/AppData/Local/tassomai-automation/info.json')
        all_ = self.database.all()
        keys = list(all_.keys())
        for key in keys:
            if type(all_[key]) != dict: # making sure they dont have an old version of the database
                self.database.clear()
                break

        self.ui.emailTassomai.setText(self.cache.get('email'))
        self.ui.passwordTassomai.setText(self.cache.get('password'))

        self.createWorkers()

        if is_admin():
            self.showUpdateDialog()
    def closeEvent(self, event):
        if self.session_thread.isRunning():
            self.session.running = False
            try:
                self.session_thread.terminate()
                self.session_thread.wait()
            except:
                pass

    def createWorkers(self):
        # Session
        self.session = Session(self)
        self.session_thread = QThread()
        self.session.moveToThread(self.session_thread)
        self.session_thread.start()

        self.session.logger.connect(self.updateLog)
        self.session.show.connect(self.show)
        self.session.close.connect(sys.exit)
        self.ui.startButton.clicked.connect(self.session.actually_start)
        self.ui.stopButton.clicked.connect(self.terminate_session)

    @pyqtSlot(str, dict)
    def updateLog(self, text, kwargs):
        return self.outputSender.send_html(text, **kwargs)

    def resizeEvent(self, event):
        width = event.size().width()-260
        if self.ui.table.columnWidth(0) > 40: return
        if self.ui.table.columnWidth(1) > 40: return
        if self.ui.table.columnWidth(3) > 80: return
        if self.ui.table.columnWidth(4) > 80: return
        if width >= 240:
            self.ui.table.setColumnWidth(2, width//2)
            self.ui.table.setColumnWidth(5, width//2)

    def terminate_session(self):
        self.session.logger.emit('TYPES=[(#c8001a, BOLD), Successfully terminated script.]', {'newlinesafter': 2})
        self.ui.startButton.setEnabled(True)
        self.ui.stopButton.setEnabled(False)
        self.session.running = False

        if not self.session.shownStats:
            if hasattr(self.session, 'tassomai'):
                self.session.show_stats()