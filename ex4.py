import sys
from PyQt4 import QtGui, QtCore

class MainForm(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)

        # create button
        self.button = QtGui.QPushButton("test button", self)       
        self.button.resize(100, 30)

        # set button context menu policy
        self.button.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.connect(self.button, QtCore.SIGNAL('customContextMenuRequested(const QPoint&)'), self.on_context_menu)

        # create context menu
        self.popMenu = QtGui.QMenu(self)
        self.popMenu.addAction('This is Action 1', self.Action1)
        self.popMenu.addAction('This is Action 2', self.Action2)
        # self.popMenu.addAction(QtGui.QAction('test0', self))
        # self.popMenu.addAction(QtGui.QAction('test1', self))
        # self.popMenu.addSeparator()
        # self.popMenu.addAction(QtGui.QAction('test2', self))        

    def Action1(self):
        print('You selected Action 1')
        print(self.title)

    def Action2(self):
        print('You selected Action 2')

    def on_context_menu(self, point):
        # show context menu
        self.popMenu.exec_(self.button.mapToGlobal(point))        

def main():
    app = QtGui.QApplication(sys.argv)
    form = MainForm()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()