import ctypes
import random
import time
import cv2
import pyautogui
import win32gui
import win32con
import sys
from PyQt6 import QtWidgets,QtGui
from PyQt6.QtWidgets import QApplication,QPushButton,QComboBox
from PyQt6.QtCore import QThread,QWaitCondition,QMutex,pyqtSignal
from PyQt6.QtGui import QImage,QPixmap
import minitouch
from cv import Finder
from pynput import keyboard
import test
from Utils import counter,ServerChan


class pictureOCR(QThread):

    signal = pyqtSignal(int)
    timeout_signal=pyqtSignal()
    send_key = "SCT291449TTW7hQ0QFBL9ibAQ9NVFSIgJE"
    notifier = ServerChan(send_key)
    def __init__(self, *args, **kwargs):
        super(pictureOCR, self).__init__()
        self.main_win = kwargs.get('main_win')
        self.signal.connect(self.refresh)
        self.timeout_signal.connect(self.timeout)
        self.hwnd = self.main_win.windowSelector.currentData()
        # self.hwnd=win32gui.FindWindow(None, 'MuMu模拟器12')
        print(self.hwnd)
        self.isPause = False
        self.isCancel=False
        self.cond = QWaitCondition()
        self.mutex = QMutex()
        self.counter = counter()
        self.res = None
        self.last_action_time = time.time()
        self.timeout_seconds = 60  # 超时响应时间
        if not self.hwnd:
            self.main_win.btnBegin.setEnabled(True)
            self.main_win.btnPause.setEnabled(False)
            self.main_win.btnResume.setEnabled(False)
            self.main_win.btnCancel.setEnabled(False)
            self.main_win.combox.setDisabled(False)
            self.cancel()
        win32gui.SendMessage(self.hwnd, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
    #暂停
    def pause(self):
        print("线程暂停")
        self.isPause = True
        
    #恢复
    def resume(self):
        print("线程恢复")
        self.isPause = False
        self.cond.wakeAll()
    #取消   
    def cancel(self):
        print("线程取消")
        
        self.isCancel=True
        


    # @test_time
    def run(self):
        minitouch.setup_minitouch()
        self.sock = minitouch.connect_to_minitouch()
        self.counter.clear()
        status=1
        i=True
        selected = False
        finder_start=Finder('strat.png')
        finder_tiaozhan = Finder('img\\tiaozhan.png')
        finder_xuanshang=Finder('xuanshang.png')
        finder_fanhui = Finder('img\\fanhui.png')
        finder_xuanzhong = Finder('img\\xuanzhong.png')

        if self.main_win.combox.currentText() == '白天':
            finder_end=Finder('img\\over.png')
        else:
            finder_end=Finder('over0303.png')
        while True:
            self.mutex.lock()
            if time.time() - self.last_action_time > self.timeout_seconds:
                print("超时未响应，自动取消任务")
                self.timeout_signal.emit()
                self.cancel()
            if self.isPause:
                self.cond.wait(self.mutex)
            if self.isCancel:
                self.signal.emit(self.counter.show())
                self.sock.close()
                break

            screen=QApplication.primaryScreen()
            rect = ctypes.wintypes.RECT()
            ctypes.windll.user32.GetWindowRect(self.hwnd, ctypes.byref(rect))
            
            x = rect.left
            y = rect.top
            # qimg=screen.grabWindow(self.hwnd).toImage()
            # qimg.save('screenshot.png')
            qimg=screen.grabWindow(self.hwnd)

            # res = finder_xuanshang.search('screenshot.png')
            self.res = finder_xuanshang.search(test.ToArray(qimg))
            if self.res.match_loc:
                    minitouch.send_touch(self.sock,y=self.res.match_loc[0]+random.randint(260,280),x=self.res.match_loc[1]-random.randint(10,30))
            elif self.res.match_loc is None:
                self.res = finder_fanhui.search(test.ToArray(qimg))
                if self.res.match_loc:
                    status = 1
                else:
                    status = 0

                if status==0:
                    
                    self.res=finder_start.search(test.ToArray(qimg),0.96,True)
                    # print(self.res.match_loc)
                    if self.res.match_loc:
                        i=True
                        # print("x=",self.res.match_loc[0],"y=",self.res.match_loc[1])
                        minitouch.send_touch(self.sock,y=self.res.match_loc[0]+random.randint(20,50),x=540-self.res.match_loc[1]+random.randint(20,50))
                        self.last_action_time = time.time()
                        
                            

                elif status==1:
                    pass
            self.res=finder_end.search(test.ToArray(qimg))
            self.start_time=time.time()
            if self.res.match_loc:
                if i:
                    self.counter.plus()
                    i=False
                minitouch.send_touch(self.sock,y=random.randint(810,840),x=260+random.randint(20,40))
                self.last_action_time = time.time()
                selected = False
                    

                        
            self.signal.emit(self.counter.show())
            self.mutex.unlock()
    def refresh(self, m):
        self.main_win.edit.setText(str(m))
        self.main_win.label.setPixmap(test.ToPixmap2(self.res.image))
    def timeout(self):
        self.notifier.send("超时异常", "脚本超时异常")
        self.main_win.btnBegin.setEnabled(True)
        self.main_win.btnCancel.setEnabled(False)
        self.main_win.btnPause.setEnabled(False)
class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        # self.setupUi(self)
        self.pressed_keys = set()
        self.resize(640, 410)

        self.label = QtWidgets.QLabel(self)
        self.label.pixmap()
        self.label.move(0,50)

        self.label.setScaledContents(True)
        self.label.setFixedSize(640,360)
        self.windowSelector = QComboBox(self)
        self.windowSelector.move(100, 380)
        self.windowSelector.resize(300, 25)

        self.refreshWindowList()


        self.btnBegin=QPushButton("开始",self)
        self.btnBegin.move(20,0)
        self.btnPause=QPushButton("暂停",self)
        self.btnPause.setEnabled(False)
        self.btnPause.move(120,0)
        self.btnResume=QPushButton("恢复",self)
        self.btnResume.setEnabled(False)
        self.btnResume.move(220,0)
        self.btnCancel=QPushButton("取消",self)
        self.btnCancel.setEnabled(False)
        self.btnCancel.move(320,0)
        self.combox=QComboBox(self)
        self.combox.addItem('白天')
        self.combox.addItem('晚上')
        self.combox.move(420,0)
        self.edit=QtWidgets.QLabel(self)
        self.edit.move(520,0)
        
        self.btnBegin.clicked.connect(self.__onClickedBtnbegin)
        self.btnPause.clicked.connect(self.__onClickedBtnpause)        
        self.btnResume.clicked.connect(self.__onClickedBtnresume)
        self.btnCancel.clicked.connect(self.__onClickedBtncancel)

        keyboard_listener = keyboard.Listener(on_release=self.on_release)
        keyboard_listener.start()
    #开始按钮被点击的槽函数
    def __onClickedBtnbegin(self):
        self.btnBegin.setEnabled(False)
        self.btnPause.setEnabled(True)
        self.btnResume.setEnabled(False)
        self.btnCancel.setEnabled(True)
        self.thread=pictureOCR(main_win=self)#创建线程
        self.combox.setDisabled(True)
        self.thread.start()
    #暂停按钮被点击的槽函数
    def __onClickedBtnpause(self):
        self.btnBegin.setEnabled(False)
        self.btnPause.setEnabled(False)
        self.btnResume.setEnabled(True)
        self.btnCancel.setEnabled(True)
        self.thread.pause()
    #恢复按钮被点击的槽函数
    def __onClickedBtnresume(self):
        self.btnBegin.setEnabled(False)
        self.btnPause.setEnabled(True)
        self.btnResume.setEnabled(False)
        self.btnCancel.setEnabled(True)
        self.thread.resume()
    #取消按钮被点击的槽函数
    def __onClickedBtncancel(self):
        self.btnBegin.setEnabled(True)
        self.btnPause.setEnabled(False)
        self.btnResume.setEnabled(False)
        self.btnCancel.setEnabled(False)
        self.combox.setDisabled(False)
        self.thread.cancel()


    def on_release(self,key):
        
        print(f'释放了按键：{key}')
        if str(key) == r"'\x03'":
            print('Ctrl + C 被按下。')
            if  self.btnBegin.isEnabled():
                self.btnBegin.click()
            else:
                self.btnCancel.click()
    
    def refreshWindowList(self):
        self.window_list = []

        def enum_callback(hwnd, _):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if "模拟器" in title:  # 根据你需求改关键词
                    self.window_list.append((title, hwnd))

        win32gui.EnumWindows(enum_callback, None)

        self.windowSelector.clear()
        for title, hwnd in self.window_list:
            self.windowSelector.addItem(title, userData=hwnd)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec())
