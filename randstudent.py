from PyQt4.QtGui import *
from PyQt4.QtCore import *
import random, time, datetime
import sqlite3
# import ui_10_1,ui_10_2,ui_10_3
# import sys
        
conn = sqlite3.connect("student.db") 

class MyThread(QThread):
    trigger = pyqtSignal(type([]), type(1))
  
    def __init__(self, parent=None):
        super(MyThread, self).__init__(parent)
  
    def setup(self, thread_allstudents, thread_nums):
        self.thread_allstudents = thread_allstudents
        self.thread_nums = thread_nums

    def run(self):
        time.sleep(random.random()*1)  # random sleep to imitate working
        self.trigger.emit(self.thread_allstudents, self.thread_nums)

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

        cur = conn.cursor()
        strsql = "select studentsn, studentname from student  where studentsn like '03%' "
        cur.execute(strsql)
        # print(cur.rowcount)
        # for item in cur.fetchall():
        #     print( item[0], item[1])
        # print(cur.fetchall())

        tmpnum = 0
        for item in cur.fetchall():
            irow = tmpnum // 7
            icol = tmpnum % 7
            tmpnum += 1
            btnlayout.setRowMinimumHeight(irow, 60)
            tmpbtn = QPushButton(item[1])
            tmpbtn.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding))

            popMenu = QMenu(self)
            entry1 = popMenu.addAction("正确")
            self.connect(entry1,SIGNAL('triggered()'), lambda item=item[0]: self.answerRight(item))
            entry2 = popMenu.addAction("错误")
            self.connect(entry2,SIGNAL('triggered()'), lambda item=item[0]: self.answerWrong(item))
            entry3 = popMenu.addAction("替换")
            self.connect(entry3,SIGNAL('triggered()'), lambda item=item[0]: self.resetStudent(item))
            tmpbtn.setMenu(popMenu)
            tmpbtn.setAutoDefault(False)
            self.btngroup.addButton(tmpbtn, int(item[0]))
            btnlayout.addWidget(tmpbtn, irow, icol)

        

        self.btn_start = QPushButton("开始")
        self.btn_start.setFixedHeight(40)
        self.btn_start.setFixedWidth(100)
        self.btn_start.setFont(QFont('宋体', 20))
        self.choicenum_text = QComboBox()
        self.choicenum_text.setFixedHeight(40)
        self.choicenum_text.setFixedWidth(60)
        self.choicenum_text.setFont(QFont('Courier New', 20))
        # self.choicenum_text.addItems(["1", "2", "3", "4", "5", "6"])
        model = self.choicenum_text.model()
        for row in list(range(1, 7)):
            item = QStandardItem(str(row))
            item.setForeground(QColor('red'))
            font = item.font()
            font.setPointSize(20)
            item.setFont(font)
            model.appendRow(item)

        bottomlayout = QHBoxLayout()
        bottomlayout.setSizeConstraint(QLayout.SetFixedSize)
        bottomlayout.addStretch(10)
        bottomlayout.addWidget(self.btn_start)
        bottomlayout.addStretch(1)
        bottomlayout.addWidget(self.choicenum_text)


        tab1layout = QVBoxLayout()
        tab1layout.addLayout(titleLayout)       
        tab1layout.addLayout(btnlayout)
        tab1layout.addLayout(bottomlayout)
                
        w1.setLayout(tab1layout)
        # firstUi.setupUi(w1)
        w2=QWidget()
        # secondUi.setupUi(w2)

        tabWidget.addTab(w1,"随机抽取")
        tabWidget.addTab(w2,"统计结果")
        tabWidget.resize(600,600)

        self.lstchoices = []
        self.threadcounter = 0
        # self.createDb()
        today = datetime.date.today() 
        cur.execute("delete from tmprecord where datequestion= '" +str(today) + "'") #delete tmp date no today
        # cur.execute("delete from tmprecord where datequestion!= '" +str(today) + "'") #delete tmp date no today
        conn.commit()

        cur.execute("select count(*) from student where studentsn like '03%' ")
        self.studentNums = cur.fetchall()[0][0]
        cur.close()

        # self.btncolor = self.btngroup.buttons()[0].palette().color(1).getRgb()
        for i in list(range(0, self.studentNums)):
            self.btngroup.buttons()[i].setStyleSheet("background-color: rgb(120,220,220);")
        # print("background-color: rgb(120,220,220);", "background-color: rgb" + str(self.btncolor) + ";")

        self.connect(self.btn_start, SIGNAL("clicked()"), self.startChoice)
     
    def startChoice(self):   
        allstudent = []
        cur = conn.cursor()   
        cur.execute("select studentsn from tmprecord where studentsn like '03%'")  
        lstrecord = ['0000', '1111']
        for item in cur.fetchall():
            lstrecord.append(item[0])
        # print(lstrecord, 'record', "select studentsn from student where studentsn like '03%' and studentsn not in " + str(tuple(lstrecord)))
        cur.execute("select studentsn from student where studentsn like '03%' and studentsn not in " + str(tuple(lstrecord)))
        for item in cur.fetchall():
            allstudent.append(item[0])

        nums = int(self.choicenum_text.currentText())
        if nums >= len(allstudent):
            cur.execute("delete from tmprecord where datequestion like '%%' ") #delete tmp date no today
            conn.commit()
            allstudent = []
            cur.execute("select studentsn from student where studentsn like '03%' ")
            for item in cur.fetchall():
                allstudent.append(item[0])
        # print(self.choicenum_text.currentText())
        cur.close()
        for i in range(10):
            thread = MyThread(self)
            thread.trigger.connect(self.choicestudent)
            thread.setup(allstudent, nums)            # just setting up a parameter
            thread.start()

    def choicestudent(self, allstudent, num): 
        for i in list(range(0, self.studentNums)):
            self.btngroup.buttons()[i].setStyleSheet("background-color: rgb(120,220,220);")
        self.lstchoices = random.sample(allstudent, num)
        for ibtn in self.lstchoices:
            self.btngroup.button(int(ibtn)).setStyleSheet("background-color: red; color:white;")
            # self.btngroup.buttons()[ibtn].setStyleSheet("background-color: red; color:white;")

        self.threadcounter += 1
        if self.threadcounter == 10:
            cur = conn.cursor()
            for ibtn in self.lstchoices:
                today = datetime.date.today()
                strsql = "insert into tmprecord values (?, ?, ?)" 
                cur.execute(strsql, (None, ibtn, today))
                conn.commit()

            cur.execute("select * from tmprecord")
            print(cur.fetchall())
            
            cur.close()
                # print(self.btngroup.buttons()[ibtn].text())
            self.threadcounter = 0

    def choiceOneStudent(self, curbtn, num=1): 
        allstudent = []
        cur = conn.cursor()   
        cur.execute("select studentsn from tmprecord where studentsn like '03%'")  
        lstrecord = ['0000', '1111']
        for item in cur.fetchall():
            lstrecord.append(item[0])
        cur.execute("select studentsn from student where studentsn like '03%' and studentsn not in " + str(tuple(lstrecord)))
        for item in cur.fetchall():
            allstudent.append(item[0])

        # cur.execute("select * from tmprecord")
        # print(cur.fetchall(), '111111111111111111')
        otherbtn = random.sample(allstudent, num)[0]
        self.btngroup.button(int(otherbtn)).setStyleSheet("background-color: red; color:white;")

        # print(self.lstchoices, 'choice one another00000000000000001')
        self.lstchoices.remove(curbtn)
        self.lstchoices.append(otherbtn)
        # print(self.lstchoices, 'choice one another000000000000000002')

        # cur.execute("delete from tmprecord where studentsn='" + curbtn + "'") # can not delete ,because this student is ill.
        # conn.commit()
        today = datetime.date.today()
        cur.execute("insert into tmprecord values (?, ?, ?)", (None, otherbtn, today))
        conn.commit()
        # cur.execute("select * from tmprecord")
        # print(cur.fetchall(), '2222222222222')

        cur.close()

    def answerRight(self, value):
        if value not in self.lstchoices:
            return
        
        cur = conn.cursor()
        cur.execute("select rightquestions from student where studentsn='" + value + "'")
        studentRightQuestions = cur.fetchall()[0][0] + 1
        cur.execute("update student set rightquestions=" + str(studentRightQuestions) + " where studentsn='" + value + "'")
        conn.commit()
        # cur.execute("select rightquestions from student where studentsn='" + value + "'")
        # print(cur.fetchall(), 'aaaaaaaaaa')
        cur.close()

    def answerWrong(self, value):
        if value not in self.lstchoices:
            return

        cur = conn.cursor()
        cur.execute("select wrongquestions from student where studentsn='" + value + "'")
        studentWrongQuestions = cur.fetchall()[0][0] + 1
        cur.execute("update student set wrongquestions=" + str(studentWrongQuestions) + " where studentsn='" + value + "'")
        conn.commit()

        # cur.execute("select wrongquestions from student where studentsn='" + value + "'")
        # print(cur.fetchall(), 'aaaaaaaaaa')
        # btnid = int(value)
        # print(self.btngroup.button(btnid), self.btngroup.button(btnid).text())
        # print("wrong",value)
        cur.close()

    def resetStudent(self, value):
        if value not in self.lstchoices:
            return
        # print(self.lstchoices, '111111111')
        # print("resetStudent",value-1)
        self.btngroup.button(int(value)).setStyleSheet("background-color: rgb(120,220,220);")
        self.choiceOneStudent(value)
        # print(self.lstchoices, '222222222')
     
    # def selectDb(self):
    #     cur = conn.cursor()
    #     strsql = "select * from student"
    #     cur.execute(strsql)
    #     print(cur.fetchall())
    #     cur.close()

    def createDb(self):
        cur = conn.cursor()
        sqlstr = 'create table student (id integer primary key, \
            studentsn varchar(20), \
            studentname varchar(20), \
            rightquestions integer, \
            wrongquestions integer)'
        # print(sqlstr)

        sqlstr2 = 'create table tmprecord (id integer primary key, \
            studentsn varchar(20), \
            datequestion date)'
        # print(sqlstr2)

        cur.execute(sqlstr) 
        conn.commit()
        cur.execute(sqlstr2) 
        conn.commit()

        # insert example data
        strsql = "insert into student values (?, ?, ?,?,?)" 
        for i in list(range(0,45)):
            cur.execute(strsql, (None, "03"+str(i+1).zfill(2), "张"+str(i+1), 0, 0))
            conn.commit()
        cur.close()
        
if __name__ == "__main__":
    import sys
    app=QApplication(sys.argv)
    dialog=QuestionDlg()
    dialog.show()
    app.exec_()