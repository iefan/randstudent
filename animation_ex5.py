#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
module: example2
"""
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class MyButton(QPushButton):
    def __init__(self, title, parent=None):
        # QPushButton.__init__(self, parent)
        super(MyButton, self).__init__(title, parent)
        self.setText(title)
        self._alpha = "100"
        # self.studentsn = studentsn

    def get_alpha(self):
        return self._alpha

    def set_alpha(self, alpha):
        self._alpha = alpha
        print("======", "background-color: rgba(0,200,0,"+str(self._alpha) + ")")
        self.setStyleSheet("background-color: rgba(0,200,0,"+str(self._alpha) + ")")

    alpha = pyqtProperty(int, fset=set_alpha)


def fadeIn(ws):
    # 建立一个平行的动作组
    ag = QParallelAnimationGroup()
    for w in ws:
        # 对于每个按钮, 都生成一个进入的动作
        a = QPropertyAnimation(w, "geometry")
        a.setDuration(1000)
        a.setEasingCurve(QEasingCurve.OutQuad)
        a.setStartValue(QRect(-100, w.y(), w.width(), w.height()))
        a.setEndValue(w.geometry())
        # 添加到组里面去
        ag.addAnimation(a)
    return ag

class W(QDialog):
    def init(self):
        self.resize(600,500)
        #生成一堆按钮, 不同的初始位置
        self.pbs = []
        for i in range(8):
            pb = MyButton(str(i), self)
            pb.move((i*100) % 600, i*40 + 10)
            self.pbs.append(pb)
        #生成动作, 并执行
        self.fadeIn = fadeIn(self.pbs)
        self.fadeIn.start()

def main():
    app = QApplication([])
    w = W()
    w.init()
    w.exec_()

if __name__=="__main__":
    main()