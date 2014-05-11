from PyQt4 import QtGui
import sys
# from PyQt4 import QtCore
class Test(QtGui.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtGui.QVBoxLayout(self)

        # a = QtGui.QGroupBox()
        # layout.addWidget(a)

        b = QtGui.QButtonGroup(self)

        self.c1 = QtGui.QPushButton("a")
        b.addButton(self.c1)
        layout.addWidget(self.c1)

        self.c2 = QtGui.QPushButton("b")
        b.addButton(self.c2)
        layout.addWidget(self.c2)

        # c3 = QtGui.QGroupBox()
        # layout.addWidget(c3)

        d = QtGui.QButtonGroup(self)

        self.c4 = QtGui.QRadioButton()
        d.addButton (self.c4)
        layout.addWidget(self.c4)

        self.c5 = QtGui.QRadioButton()
        d.addButton (self.c5)
        layout.addWidget(self.c5)

a = QtGui.QApplication(sys.argv)
t = Test()
t.show()
a.exec_()