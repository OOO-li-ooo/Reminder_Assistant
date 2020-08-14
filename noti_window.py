import sys
import threading
import webbrowser
import time

import PyQt5
import pyautogui
from PyQt5.QtCore import Qt, QPropertyAnimation, QPoint, QTimer, pyqtSignal, pyqtSlot, QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QDesktopWidget, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtMultimedia import QAudio, QAudioDeviceInfo, QAudioFormat, QAudioOutput
from PyQt5 import QtWidgets, QtCore, QtGui
from setting_window import *

class WindowNotify(QtWidgets.QMainWindow):

    SignalClosed = pyqtSignal()  # 弹窗关闭信号
    isShow=False
    showTime=datetime.datetime.now()
    notiStart=False

    def __init__(self, title="", content="", timeout=5000, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.setupUi(self)
        # self.setTitle(title).setContent(content)
        # self._timeout = timeout
        self.desktop = QDesktopWidget()
        self.resize(300, 300)
        self._init()
        self.move((self.desktop.availableGeometry().width() - self.width()), pyautogui.size()[1])
        self.label = QtWidgets.QLabel(self)
        # self.setWindowFlags(Qt.FramelessWindowHint)  # 去边框
        # self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.label.setGeometry(QtCore.QRect(0, 0, self.width(), self.height()))
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("background:rgb(241,241,241);"
                                 "font:bold 20px Microsoft YaHei;"
                                 "border: 3px solid rgb(96,96,96);"
                                 "padding:12px")
        self.label.setText(content)
        # self.label.setPixmap(QtGui.QPixmap("C:/Users/Administrator/Desktop/background.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")

        self.btn = QtWidgets.QPushButton('关闭',self)

        self.btn.setGeometry(QtCore.QRect(self.width() - 55, 5, 50, 25))
        # btn.setToolTip('这是按钮提示')
        # self.setStyleSheet("background-color: rgb(229,229,229);")
        # self.btn.set
        self.btn.setStyleSheet("QPushButton{\n"
                    "    background:rgba(206,0,0,0.5);\n"
                    "    box-shadow: -10px 2px 4px rgba(0,255,0,0.5);"
                          "border-radius: 12px;"
                    "}\n"
                    "QPushButton:hover{                    \n"
                    "    background:#FF2D2D;\n"
                    "}\n"
                    "QPushButton:pressed{\n"
                    "    border: 1px solid #3C3C3C!important;\n"
                    "    background:#AE0000;\n"
                    "}")
        self.btn.setObjectName("btn_close")
        self.btn.clicked.connect(self.onClose)
        # self.showAnimation()
        self.mSysTrayIcon = QSystemTrayIcon(self)
        icon = QIcon("h.png")
        self.mSysTrayIcon.setIcon(icon)

        self.sound_file = 'noti.wav'
        self.sound = PyQt5.QtMultimedia.QSoundEffect()  # t2 = threading.Thread(target=ischecked)
        self.sound.setSource(PyQt5.QtCore.QUrl.fromLocalFile(self.sound_file))  # t2.start()
        # self.sound.setLoopCount(PyQt5.QtMultimedia.QSoundEffect.)  # shownoti()
        self.sound.setVolume(0.1)

    def startNoti(self,settingButton):
        # print(settingButton.StartButton)
        if settingButton!=None:
            if self.notiStart==False:
                for i in range(0, len(noti_checkBox_list)):
                    noti_pre_time_list[i] = datetime.datetime.now()
                self.id = self.startTimer(1000)
                settingButton.setText('点击暂停')
                settingButton.setStyleSheet("background-color: rgb(255,177,178);"
                                       "border-radius:5px;"
                                       "height:30px;"
                                       "font:bold;"
                                       "border: 1px solid #000;")
                self.notiStart=True
            else:
                self.killTimer(self.id)
                settingButton.setText('点击开始')
                settingButton.setStyleSheet("background-color: rgb(177,255,218);"
                                            "border-radius:5px;"
                                            "height:30px;"
                                            "font:bold;"
                                            "border: 1px solid #000;")
                self.notiStart=False
    def timerEvent(self, evt):
        for i in range(0, len(noti_checkBox_list)):
                if noti_checkBox_list[i].isChecked():
                    dTime = datetime.datetime.now() - noti_pre_time_list[i]
                    if (int(dTime.total_seconds()) > int(noti_delayinput_list[i].text())) and self.isShow==False:
                        noti_pre_time_list[i] = datetime.datetime.now()
                        self.showTime= datetime.datetime.now()
                        self.showAnimation()
                        self.sound.play()
                        self.isShow=True
                        showTime = datetime.datetime.now()
                        self.label.setText(noti_contentinput_list[i].toPlainText())
                    elif self.isShow==True:
                        dTime=int((datetime.datetime.now()-self.showTime).total_seconds())
                        if dTime>3:
                            self.onClose()




    def m(self):
        self.hide()

        self.mSysTrayIcon.setToolTip("我在这里哦！")
        self.tray_menu = QMenu(QApplication.desktop())  # 创建菜单
        self.RestoreAction = QAction(u'还原 ', self, triggered=self.show_w)  # 添加一级菜单动作选项(还原主窗口)
        self.QuitAction = QAction(u'退出 ', self, triggered=self.onActivated)
        self.tray_menu.addAction(self.RestoreAction)  # 为菜单添加动作
        self.tray_menu.addAction(self.QuitAction)
        self.mSysTrayIcon.setContextMenu(self.tray_menu)
        self.mSysTrayIcon.activated.connect(self.onActivated)
        self.mSysTrayIcon.show()
    def show_w(self, reason):
        self.show()
        self.mSysTrayIcon.hide()

    def onActivated(self, reason):
        if reason == self.mSysTrayIcon.Trigger:
            self.show()
            # self.mSysTrayIcon.hide()
    def showAnimation(self):
        # 显示弹出框动画
        # print("open")
        self.isShow = True


        self.animation = QPropertyAnimation(self, b"pos")
        self.animation.setDuration(200)
        self.animation.setStartValue(QPoint(self.x(), self.y()))
        self.animation.setEndValue(QPoint((self.desktop.availableGeometry().width() - self.width()-5), (
                    self.desktop.availableGeometry().height() - self.height() )))
        self.animation.start()
        # 设置弹出框1秒弹出，然后渐隐
        self.remainTimer = QTimer()
        # self.connect(self.remainTimer, SIGNAL("timeout()"), self, SLOT("closeAnimation()"))
        self.remainTimer.start(10000)  # 定时器10秒

    @pyqtSlot()
    def closeAnimation(self):
        # 清除Timer和信号槽
        # self.remainTimer.stop()
        # # self.disconnect(self.remainTimer, SIGNAL("timeout()"), self, SLOT("closeAnimation()"))
        # self.remainTimer.deleteLater()
        # self.remainTimer = None
        # 弹出框渐隐
        # self.animation = QPropertyAnimation(self, b'windowOpacity')
        # self.animation.setDuration(1000)
        # self.animation.setStartValue(1)
        # self.animation.setEndValue(1)
        # self.animation.start()
        self.isShow = False
        self.animation = QPropertyAnimation(self, b"pos")
        self.animation.setDuration(200)

        self.animation.setStartValue(QPoint(self.x(), self.y()))
        self.animation.setEndValue(QPoint((self.desktop.availableGeometry().width() - self.width() - 5),  pyautogui.size()[1]))
        self.animation.start()
        # self.cl()
        # self.animation.finished.connect(QCoreApplication.instance().quit)
        # 动画完成后清理
        # self.connect(self.animation, SIGNAL("finished()"), self, SLOT("clearAll()"))

        # 清理及退出
    def cl(self):
        # QCoreApplication.instance().quit
        self.close()
        # sys.exit()
    @pyqtSlot()
    def clearAll(self):
        # self.disconnect(self.animation, SIGNAL("finished()"), self, SLOT("clearAll()"))
        sys.exit()  # 退出

    def onClose(self):
        #点击关闭按钮时
        # print("onClose")
        self.isShow = False
        QTimer.singleShot(100, self.closeAnimation)#启动弹回动画

    def _init(self):
        # 隐藏任务栏|去掉边框|顶层显示
        self.setWindowFlags(Qt.Tool | Qt.X11BypassWindowManagerHint | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        self.setStyleSheet(
                    "    background-color:rgb(255,255,255);\n"
                    "    box-shadow: -10px 2px 4px rgba(0,255,0,0.5);"
                          "border-radius: 12px;"
                    )

def shownoti():
    app2 = QApplication(sys.argv)
    demo = WindowNotify()
    demo.show()
    # demo.startcheck()
    app2.exec_()
# app2 = QApplication(sys.argv)
# demo = WindowNotify()
# # demo.show()
# app2.exec_()