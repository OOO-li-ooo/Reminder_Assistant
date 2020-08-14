import sys
import threading
import time
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import *
from PyQt5.QtMultimedia import QAudio, QAudioDeviceInfo, QAudioFormat, QAudioOutput
from PyQt5 import QtWidgets, QtCore, QtGui
import noti_window
from noti_window import *
from setting_window import *

mOK=0
def start():
    app = QApplication(sys.argv)
    Window = settingWindow()
    Window.show()
    # global demo
    global mOK
    mOK=2
    global demo
    demo = WindowNotify()
    demo.show()
    # demo.StartButton=Window.StartButton
    Window.StartButton.clicked.connect(lambda:demo.startNoti(Window.StartButton))
    app.exec_()
def ischecked():
    time.sleep(5)
    demo.showAnimation()
    # while 1:
    #     time.sleep(1)
    #     # if demo==None:
    #     #     continue
    #     # print(mOK)
    #     if mOK>0:
    #         print("c")
    #         global demo
    #         demo.showAnimation()
    #         print("asdasdasd")

                        # time.sleep(1)


def noti():
    app = QApplication(sys.argv)
    demo = WindowNotify()
    demo.show()
    sys.exit(app.exec_())

if __name__=='__main__':
    # app = QApplication(sys.argv)

    t1 = threading.Thread(target=start)
    t1.start()



    # ischecked()

    # shownoti()
    # app2 = QApplication(sys.argv)
    # demo = WindowNotify()
    # demo.show()
    # app2.exec_()
    print("aaaaa")
    # sys.exit(app.exec_())
