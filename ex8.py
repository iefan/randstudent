import sys
from PyQt4 import QtGui, QtCore

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.menubar = self.menuBar()
        menuitems = ["Item 1","Item 2","Item 3"]
        menu = self.menubar.addMenu('&Stuff')
        for item in menuitems:
            entry = menu.addAction(item)
            self.connect(entry,QtCore.SIGNAL('triggered()'), lambda item=item: self.doStuff(item))       
            menu.addAction(entry)
        print( "init done")

    def doStuff(self, item):
        print( item)

app = QtGui.QApplication(sys.argv)
main = MainWindow()
main.show()
sys.exit(app.exec_())