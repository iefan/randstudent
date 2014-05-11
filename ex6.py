import sys
from PyQt4 import QtGui, QtCore

class MyPushButton(QtGui.QPushButton):
    def __init__(self, popMenu,elementID, mainForm):
        super(MyPushButton, self).__init__()
        self.__elementID = elementID
        self.__mainForm = mainForm
        self.__popMenu = popMenu

        self.connect(self, QtCore.SIGNAL('customContextMenuRequested(const QPoint&)'), self.on_context_menu)   
        self.connect(self, QtCore.SIGNAL('clicked()'),  self,        QtCore.SLOT("triggerOutput()"))    

    def on_context_menu(self, point):
        # show context menu
        self.__popMenu.exec_(self.mapToGlobal(point)) 

    @QtCore.pyqtSlot()
    def triggerOutput(self):
        self.__mainForm.emit(QtCore.SIGNAL("buttonXclickedSignal(PyQt_PyObject)"), self.__elementID) # send signal to MainForm class



class MainForm(QtGui.QWidget):
    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)
        self.setGeometry(300, 300, 400, 200)
        VmasterLayout = QtGui.QVBoxLayout(self)
        self.Hbox = QtGui.QHBoxLayout()
        print(1)

        # Custom signal
        self.connect(self, QtCore.SIGNAL("buttonXclickedSignal(PyQt_PyObject)"),         self.buttonXclicked)
        item = "Item 1"

        for i in range(1,4):
            # create context menu as you like
            popMenu = QtGui.QMenu(self)
            entry = popMenu.addAction(item)
            self.connect(entry,QtCore.SIGNAL('triggered()'), lambda item=item: self.onFilmSet(item)) 

            popMenu.addAction(QtGui.QAction('button %s - test1'%(i), self))
            # popMenu.addSeparator()
            # popMenu.addAction(QtGui.QAction('button %s - test2'%(i), self))
            popMenu.addSeparator()
            popMenu.addAction('This is Action 1', self.Action1)
            # popMenu.addAction(QtGui.QAction('button %s - test2'%(i), self))

            # create button
            self.button = MyPushButton(popMenu, i, self)    
            self.button.setText("test button %s" %(i))    
            self.button.resize(100, 30)

            # set button context menu policy
            self.button.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)        

            self.Hbox.addWidget(self.button)

        VmasterLayout.addLayout(self.Hbox)

    def onFilmSet(self, value):
        print( 'Menu Clicked ', value)

    def Action1(self):
        print('You selected Action 1')
        # print(self.parent)

    def createAction(self, text, slot=None, shortcut=None, icon=None,tip=None, checkable=False, signal="triggered()"):
        action = QtGui.QAction(text, self)
        if icon is not None:
            action.setIcon(QtGui.QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
        action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, QtCore.SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action


    def buttonXclicked(self, buttonID):
        if buttonID == 1: 
            #do something , call some method ..
            print( "button with ID ", buttonID, " is clicked")
        if buttonID == 2: 
            #do something , call some method ..
            print( "button with ID ", buttonID, " is clicked")
        if buttonID == 3: 
            #do something , call some method ..
            print( "button with ID ", buttonID, " is clicked")

app = QtGui.QApplication(sys.argv)
form = MainForm()
form.show()
app.exec_()