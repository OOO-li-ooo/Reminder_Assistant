import json
import sys
import datetime
import threading

from PyQt5.QtCore import Qt, QPropertyAnimation, QPoint, QTimer, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
import R_Ass
from PyQt5 import QtWidgets, QtCore, QtGui

# from noti_window import WindowNotify


class settingWindow(QWidget):
    def __init__(self, title="", content="", timeout=5000, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.setTitle(title).setContent(content)
        self.initUI()
        self.desktop = QDesktopWidget()
        self.move(int((self.desktop.availableGeometry().width() - self.width())/2), int((self.desktop.availableGeometry().height()-self.height())/2))
        self.m()
    def closeEvent(self, Event) -> None:
        Event.ignore()
        # self.setWindowFlags(QtCore.Qt.SplashScreen | QtCore.Qt.FramelessWindowHint)
        self.hide()
    def show_setting(self,reason):
        if reason==2:
            self.show()
    def hide_setting(self):
        self.hide()
    def quit_setting(self):
        sys.exit(0)
    def m(self):
        self.hide()
        self.mSysTrayIcon = QSystemTrayIcon(self)
        icon = QIcon("h.png")
        self.mSysTrayIcon.setIcon(icon)
        self.mSysTrayIcon.setToolTip("我在这里哦！")
        self.tray_menu = QMenu(QApplication.desktop())  # 创建菜单
        self.RestoreAction = QAction(u'还原 ', self, triggered=lambda:self.show_setting(2))
        self.hideAction = QAction(u'隐藏 ', self, triggered=self.hide_setting)
        self.QuitAction = QAction(u'退出 ', self, triggered=self.quit_setting)
        self.tray_menu.addAction(self.RestoreAction)  # 为菜单添加动作
        self.tray_menu.addAction(self.hideAction)
        self.tray_menu.addAction(self.QuitAction)
        self.mSysTrayIcon.setContextMenu(self.tray_menu)
        self.mSysTrayIcon.activated.connect(self.show_setting)
        self.mSysTrayIcon.show()
    def initUI(self):
        self.setWindowTitle('提醒助手')
        self.resize(650, 400)
        self.setWindowIcon(QIcon('pig.png'))

        groupBox = QGroupBox("Checkboxes")
        groupBox.setFlat(False)
        mainlayout=QVBoxLayout()
        headlayout = QGridLayout()
        layout = QVBoxLayout()
        headlayout.setColumnStretch(0,2)
        headlayout.setColumnStretch(1,6)
        headlayout.setColumnStretch(2,5)
        self.addHead(headlayout)

        with open("Noti.json", encoding='utf-8')as load_f:
            load_d = json.load(load_f)
        for i in range(0,len(load_d)):
            Notilinelayout=QHBoxLayout()
            NotiName=load_d[i]['name']
            self.addNotify(NotiName, load_d[i]['content'], load_d[i]['delay'], load_d[i]['checked'])

            Notilinelayout.addWidget(noti_checkBox_list[i])
            Notilinelayout.addWidget(noti_contentinput_list[i])
            Notilinelayout.addWidget(noti_delayinput_list[i])

            Notiline=QWidget()
            Notiline.setLayout(Notilinelayout)
            layout.addWidget(Notiline)

        self.addNotiButton=QPushButton('添加',self)
        self.addNotiButton.setEnabled(False)
        layout.addWidget(self.addNotiButton)
            # Notilinelayout.setRowStretch(i, 0)
        # self.addNotify('提醒喝水2')
        # self.input=QtWidgets.QLineEdit(self)
        # self.input2=QtWidgets.QLineEdit(self)


        # layout.addWidget(QLabel('123',self), 2, 0,1,2)


        hwg = QWidget()
        hwg.setLayout(headlayout)
        mainlayout.addWidget(hwg)
        gwg = QWidget()
        gwg.setLayout(layout)
        self.scroll = QScrollArea()
        self.scroll.setWidget(gwg)
        mBox=QVBoxLayout()
        # mBox.addWidget(self.scroll)
        mainlayout.addWidget(self.scroll)


        ButtonLayout=QGridLayout();
        self.addmainButton(ButtonLayout)
        MBwg=QWidget()
        MBwg.setLayout(ButtonLayout)
        mainlayout.addWidget(MBwg)


        self.setLayout(mainlayout)
    def addNotify(self,title="?",content='?',delay=60,checked=False):
        mCheckBox=QCheckBox(title,self)
        # mCheckBox.setMaximumSize(50,50)
        mCheckBox.setStyleSheet("width:80px;")
        mCheckBox.setChecked(checked)
        mCheckBox.stateChanged.connect(self.choose)
        noti_checkBox_list.append(mCheckBox)

        mTextEdit=QTextEdit(content,self)
        mTextEdit.setMaximumSize(250,80)
        # mTextEdit.toPlainText()
        noti_contentinput_list.append(mTextEdit)
        noti_delayinput_list.append(QLineEdit(str(delay),self))
        noti_pre_time_list.append(datetime.datetime.now())

    def addHead(self, layout=None):
        self.headlabel1 = QLabel(self)
        self.headlabel1.setText('提醒开关')
        # self.headlabel1.resize(50,50)
        self.headlabel1.setAlignment(Qt.AlignCenter)
        # self.headlabel1.setAutoFillBackground(True)
        self.headlabel1.setStyleSheet("background:rgb(224,224,224);"
                                      "font:bold 15px;"
                                      "padding:10px");
        layout.addWidget(self.headlabel1, 0, 0)

        self.headlabel2 = QLabel(self)
        self.headlabel2.setText('提醒内容')
        # self.headlabel1.resize(250,50)
        self.headlabel2.setAlignment(Qt.AlignCenter)
        self.headlabel2.setStyleSheet("background:rgb(224,224,224);"
                                      "font:bold 15px;"
                                      "padding-left:10px");
        layout.addWidget(self.headlabel2, 0, 1, )

        self.headlabel3 = QLabel(self)
        self.headlabel3.setText('提醒间隔')
        self.headlabel3.setAlignment(Qt.AlignCenter)
        self.headlabel3.setStyleSheet("background:rgb(224,224,224);"
                                      "font:bold 15px;"
                                      "padding:10px");
        layout.addWidget(self.headlabel3, 0, 2)

    def addmainButton(self,layout=None):

        self.StartButton=QPushButton('点击开始',self)
        self.StartButton.setStyleSheet("background-color:rgb(177,255,218);"
                                       "border-radius:5px;"
                                       "height:30px;"
                                       "font:bold;"
                                       "border: 1px solid #000;")
        layout.addWidget(self.StartButton,0,0)
        self.SaveButton = QPushButton('保存', self)
        self.SaveButton.setEnabled(False)
        layout.addWidget(self.SaveButton,0,1)

    def choose(self):

        choice_1 = noti_checkBox_list[0].text() if noti_checkBox_list[0].isChecked() else ''
        # choice_2 = self.check_2.text() if self.check_2.isChecked() else ''
        # choice_3 = self.check_3.text() if self.check_3.isChecked() else ''
        print (choice_1 )


    mOK = 0
title="提醒助手"
content="设置"

noti_checkBox_list=[]
noti_contentinput_list=[]
noti_delayinput_list=[]
noti_pre_time_list=[]
