from PyQt4.QtGui import *
from PyQt4.QtCore import *
import random
# import ui_10_1,ui_10_2,ui_10_3
# import sys

class MyThread(QThread):
    trigger = pyqtSignal(int)
  
    def __init__(self, parent=None):
        super(MyThread, self).__init__(parent)
  
    def setup(self, thread_no):
        self.thread_no = thread_no
  
    def run(self):
        time.sleep(random.random()*5)  # random sleep to imitate working
        self.trigger.emit(self.thread_no)

class QuestionDlg(QDialog):
    def __init__(self,parent=None):
        super(QuestionDlg,self).__init__(parent)
        
        tabWidget=QTabWidget(self)
        w1=QWidget()

        w1title = QLabel("<font size='20'><b>随机抽取</b></font>")
        titleLayout = QHBoxLayout()
        w1title.setMinimumHeight(50);
        titleLayout.addWidget(w1title)
        titleLayout.setAlignment(w1title, Qt.AlignCenter)
       
        self.btngroup = QButtonGroup()
        btnlayout = QGridLayout()
        tmpnum = 0
        for i in list(range(1,10)):
            btnlayout.setRowMinimumHeight(i-1, 60)
            # btnlayout.setRowStretch(i-1, 10)
            for j in list(range(1,6)):
                # btnlayout.setColumnStretch(j-1, 1)
                tmpnum += 1
                tmpbtn = QPushButton(str(tmpnum))
                # tmpbtn.setGeometry(QRect(0,0,50,50))
                tmpbtn.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding))
                # tmpbtn.resize(50,50)

                popMenu = QMenu(self)

                entry1 = popMenu.addAction("正确")
                self.connect(entry1,SIGNAL('triggered()'), lambda item=tmpnum: self.answerRight(item))
                entry2 = popMenu.addAction("错误")
                self.connect(entry2,SIGNAL('triggered()'), lambda item=tmpnum: self.answerWrong(item))
                entry3 = popMenu.addAction("替换")
                self.connect(entry3,SIGNAL('triggered()'), lambda item=tmpnum: self.resetStudent(item))
                tmpbtn.setMenu(popMenu)

                tmpbtn.setAutoDefault(False)
                # tmpbtn.setEnabled(False)
                self.btngroup.addButton(tmpbtn, tmpnum)
                btnlayout.addWidget(tmpbtn, i-1, j-1)
     
        # line = QFrame()
        # line.setFrameStyle(QFrame.HLine|QFrame.Sunken)

        self.btn_start = QPushButton("开始")

        tab1layout = QVBoxLayout()
        tab1layout.addLayout(titleLayout)       
        tab1layout.addLayout(btnlayout)
        tab1layout.addWidget(self.btn_start)
                
        w1.setLayout(tab1layout)
        # firstUi.setupUi(w1)
        w2=QWidget()
        # secondUi.setupUi(w2)

        tabWidget.addTab(w1,"随机抽取")
        tabWidget.addTab(w2,"统计结果")
        tabWidget.resize(600,600)

        for i in list(range(0, 45)):
            self.btngroup.buttons()[i].setStyleSheet("background-color: rgb(120,220,220);")

        self.connect(self.btn_start, SIGNAL("clicked()"), self.testSleep)
     
    def testSleep(self):        
        allstudent = list(range(1, 45))

        QTimer.singleShot(1000, lambda: self.choicestudent(allstudent, 4))

    def choicestudent(self, allstudent, num):       
        for i in list(range(0, 45)):
            self.btngroup.buttons()[i].setStyleSheet("background-color: rgb(120,220,220);")

        lstchoices = random.sample(allstudent, num)
        for ibtn in lstchoices:
            self.btngroup.buttons()[ibtn].setStyleSheet("background-color: red; color:white;")

    def answerRight(self, value):
        print("right", value)

    def answerWrong(self, value):
        print("wrong",value)

    def resetStudent(self, value):
        print("resetStudent",value)
     
    def slotChild(self):
        dlg=QDialog()
        self.thirdUi.setupUi(dlg)
        dlg.exec_()
        
if __name__ == "__main__":
    import sys
    app=QApplication(sys.argv)
    dialog=QuestionDlg()
    dialog.show()
    app.exec_()