from PyQt4.QtGui import QDialog, QApplication, QPushButton, QVBoxLayout
from PyQt4.QtCore import QPropertyAnimation


class test(QDialog):
    def __init__(self,parent=None):
        super(test,self).__init__(parent)
        self.pushbutton = QPushButton('Popup Button')
        self.pushbutton.setAutoFillBackground(False)
        self.pushbutton.move(0, 50)
        self._alpha = 255
        # self.pushbutton.setStyle('plastique')

        animation = QPropertyAnimation(self, "alpha")
        animation.setDuration(1000)
        animation.setKeyValueAt(0, 255)
        animation.setKeyValueAt(0.5, 100)
        animation.setKeyValueAt(1, 255)
        animation.setLoopCount(-1)
        animation.start()

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
    def alpha(self):
        return self._alpha

    def setalpha(self, a_alpha):
        self._alpha = a_alpha
        self.pushbutton.setStyle("background-color: rgba(0,200,0,"+str(self._alpha))

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