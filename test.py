import sys
import cv2
import numpy as np
from PyQt6.QtGui import QPixmap,QImage
from PyQt6.QtWidgets import QApplication,QLabel
from PIL import Image
from cv import Finder

def ToArray(pix):#pix是RGBA四通道QPixmap。额外使用PIL.Image模块
	#忘了是哪里看到的，然后翻历史记录死活找不到，作罢

    pImg=Image.fromqpixmap(pix)
    arr=np.array(pImg)
    arr=cv2.cvtColor(arr,cv2.COLOR_BGR2RGB)
    return arr
def ToPixmap(arr):#arr对应四通道图片。额外使用PIL.Image模块
    #https://blog.csdn.net/ielcome2016/article/details/105798279
    
    arr=cv2.cvtColor(arr,cv2.COLOR_BGR2RGB)
    return Image.fromarray(arr).toqpixmap()

def ToPixmap2(arr):#arr对应四通道图片。额外使用PIL.Image模块
    #https://blog.csdn.net/ielcome2016/article/details/105798279
    
    
    # arr = cv2.cvtColor(arr, cv2.COLOR_BGR2RGB)
    return QPixmap.fromImage(QImage(arr[:],arr.shape[1],arr.shape[0],arr.shape[1]*3,QImage.Format.Format_BGR888))
if __name__=='__main__':

    app = QApplication(sys.argv)
    
    wid_0=QLabel("ABCDE")
    wid_0.setStyleSheet("font-size:150px ; background-color:#FF0000")
    wid_0.setWindowTitle('Source')
    wid_0.show()
    template = cv2.imread('5450.png')
    pixmap = QPixmap('5450.png')
    arr = ToArray(pixmap)
    f = Finder('5450.png')
    res = f.search(arr)
    print(res.image)
    cv2.imwrite('test.png',arr)
    qpixmap = ToPixmap2(arr)
    cv2.imshow('out', arr)
    wid_0.setPixmap(qpixmap)
    sys.exit(app.exec())
