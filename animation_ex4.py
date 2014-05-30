from PyQt4.QtGui import QDialog, QApplication, QPushButton, QVBoxLayout
from PyQt4.QtCore import QPropertyAnimation, pyqtProperty, QRect

class MyButton(QPushButton):
    def __init__(self, title, parent=None):
        # QPushButton.__init__(self, parent)
        super(MyButton, self).__init__(title, parent)
        self.setText(title)
        self._item = "1"
        self._alpha = "100"
        # self.studentsn = studentsn

    def setMyarg(self, item):
        self._item = item

    def getMyarg(self):
        return self._item

    def get_alpha(self):
        return self._alpha

    def set_alpha(self, alpha):
        self._alpha = alpha
        # print(self._alpha)
        # print("======", "background-color: rgba(0,200,0,"+str(self._alpha) + ")")
        self.setStyleSheet("background-color: rgba(0,200,0,"+str(self._alpha) + ")")

    alpha = pyqtProperty(int, fset=set_alpha)

        # self.pushbutton.setStyleSheet("background-color: rgba(0,200,0,50)")

    # def mousePressEvent(self,event):
    #     if event.button() == Qt.LeftButton:
    #         QPushButton.mousePressEvent(self,event)
    #         return
    #     # print ("!!!!!Processing right click event")
    #     self.emit(SIGNAL("myslot(PyQt_PyObject)"), self._item)

class test(QDialog):
    def __init__(self,parent=None):
        super(test,self).__init__(parent)
        self.pushbutton = MyButton('Popup Button')
        # self.pushbutton.setAutoFillBackground(False)
        self.pushbutton.move(0, 50)
        # self._alpha = 255
        # self.pushbutton.setStyle('plastique')

        # self.animation = QPropertyAnimation(self.pushbutton, "geometry")

        # self.animation.setDuration(1000)
        # self.animation.setKeyValueAt(0, QRect(100, 100, 50, 30));
        # self.animation.setKeyValueAt(0.8, QRect(150, 150, 50, 30));
        # self.animation.setKeyValueAt(1, QRect(100, 100, 50, 30));

        self.animation = QPropertyAnimation(self.pushbutton, "alpha")
        self.animation.setDuration(1000)
        # self.animation.setStartValue(20)
        # self.animation.setEndValue(255)

        self.animation.setKeyValueAt(0, 10)
        self.animation.setKeyValueAt(0.5, 200)
        self.animation.setKeyValueAt(1, 255)
        self.animation.setLoopCount(5)
        self.animation.start()
        # print(self.pushbutton)

        layout = QVBoxLayout()
        layout.addWidget(self.pushbutton)       
        # layout.addLayout(btnlayout2)
        # layout.addLayout(bottomlayout2)
        self.setLayout(layout)
        self.setGeometry(100, 100, 200, 200)

        # menu = QtGui.QMenu()
        # menu.addAction('This is Action 1', self.Action1)
        # menu.addAction('This is Action 2', self.Action2)
        # pushbutton.setMenu(menu)
        # self.setCentralWidget(pushbutton)
    

    def Action1(self):
        print('You selected Action 1')

    def Action2(self):
        print('You selected Action 2')



if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    main = test()
    main.show()
    app.exec_()