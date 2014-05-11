from PyQt4.QtGui import *
from PyQt4.QtCore import *
# import ui_10_1,ui_10_2,ui_10_3
# import sys

class QuestionDlg(QDialog):
    def __init__(self,parent=None):
        super(QuestionDlg,self).__init__(parent)
        
        tabWidget=QTabWidget(self)
        w1=QWidget()

        w1title = QLabel("<font size='20'><b>随机抽取</b></font>")
        self.student = QLabel("姓名")
        btn1_right = QPushButton("回答正确")
        btn1_right.setAutoDefault(False)
        btn1_wrong = QPushButton("回答错误")
        btn1_wrong.setAutoDefault(False)
        yesnoLayout = QHBoxLayout()
        yesnoLayout.addWidget(btn1_right)
        yesnoLayout.addWidget(btn1_wrong)
        
        toplayout = QVBoxLayout()
        toplayout.addWidget(w1title)
        toplayout.addWidget(self.student)
        toplayout.setAlignment(w1title, Qt.AlignCenter)
        toplayout.setAlignment(self.student, Qt.AlignCenter)
        toplayout.addLayout(yesnoLayout)

        self.btngroup = QButtonGroup()
        btnlayout = QGridLayout()
        tmpnum = 0
        for i in list(range(1,10)):
            for j in list(range(1,6)):
                tmpnum += 1
                tmpbtn = QPushButton(str(tmpnum))
                tmpbtn.setAutoDefault(False)
                # tmpbtn.setEnabled(False)
                self.btngroup.addButton(tmpbtn, tmpnum)
                btnlayout.addWidget(tmpbtn, i-1, j-1)

        # print(self.btngroup.buttons()[0])
        self.btngroup.buttons()[5].setStyleSheet("background-color: red; color:white;")
        line = QFrame()
        line.setFrameStyle(QFrame.HLine|QFrame.Sunken)

        self.btn_start = QPushButton("开始")

        tab1layout = QVBoxLayout()
        tab1layout.addLayout(toplayout)
        tab1layout.addSpacing(10)
        # tab1layout.addStretch(1)
        tab1layout.addWidget(line)
        tab1layout.addSpacing(10)
        # tab1layout.addStretch(1)
        tab1layout.addLayout(btnlayout)
        tab1layout.addWidget(self.btn_start)
        # tab1layout.setAlignment(self.btn_start,Qt.AlignCenter)
                
        w1.setLayout(tab1layout)
        # firstUi.setupUi(w1)
        w2=QWidget()
        # secondUi.setupUi(w2)

        tabWidget.addTab(w1,"随机抽取")
        tabWidget.addTab(w2,"统计结果")
        tabWidget.resize(800,600)

        # self.connect(self.btngroup, SIGNAL("buttonClicked(int)"), self.buttonJudge)
        self.btngroup.buttonClicked[int].connect(self.buttonJudge)
        # self.connect(self.btngroup, SIGNAL("buttonClicked(int)"), self.buttonJudge)

        # buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)

        # self.connect(firstUi.childPushButton,SIGNAL("clicked()"),self.slotChild)
        # self.connect(secondUi.closePushButton,SIGNAL("clicked()"),self,SLOT("reject()"))
      
    def buttonJudge(self, id):
        print(id)
        btn = self.btngroup.buttons()[id-1]
        self.student.setText(btn.text())
        # print(btn.text())

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