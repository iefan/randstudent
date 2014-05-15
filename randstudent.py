from PyQt4.QtGui import QDialog, QIcon, QFont, QMenu, QColor, QComboBox, QLayout, QApplication, QTabWidget, QButtonGroup, QWidget, QPushButton, QStandardItem
from PyQt4.QtGui import QHBoxLayout, QVBoxLayout, QGridLayout, QSizePolicy
from PyQt4.QtCore import SIGNAL, QThread, pyqtSignal, Qt, QSize
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
        time.sleep(random.random()*0.8)  # random sleep to imitate working
        self.trigger.emit(self.thread_allstudents, self.thread_nums)

class QuestionDlg(QDialog):
    def __init__(self,parent=None):
        super(QuestionDlg,self).__init__(parent)
        self.setStyleSheet("background-image:url('image/panelbg.jpg'); border: 2px; border-radius 2px;")
        self.setWindowFlags(Qt.CustomizeWindowHint)
        # self.setStyleSheet("border: 2px; border-radius 2px;")
        # self.setWindowFlags(Qt.FramelessWindowHint)
        
        tabWidget=QTabWidget(self)
        tabWidget.currentChanged.connect(self.changeTab)
        # tabWidget.setTabShape(QTabWidget.Triangular)
        tabWidget.setStyleSheet("QTabWidget::pane{border:0px;}\
            QTabBar::tab { height: 40px; width: 200px; color:rgb(0, 0, 255); font-size:14px; font-weight:bold;} \
            QTabBar::tab:hover{background:rgb(255,255, 255, 100);} \
            QTabBar::tab:selected{border-color:white;background:white;color:green;}")
        # tabWidget.setStyleSheet("QTabBar::tab:hover{background:rgb(255,255, 255, 100);}")
        self.btngroup = QButtonGroup()

        w1=QWidget()
        w1.setAccessibleName("w1tab")
        self.w1title = QComboBox()
        self.btn_start = QPushButton("开始")
        self.choicenum_text = QComboBox()
        self.choicenum_text.setObjectName('w1combonums')
        # self.w1title.setStyleSheet("background-image:url('image/panelbg.jpg');")

        titleLayout, btnlayout, bottomlayout = self.genOneTab(tabtitle = self.w1title, tabbtn=self.btn_start, tabnums=self.choicenum_text)

        tab1layout = QVBoxLayout()
        tab1layout.addLayout(titleLayout)       
        tab1layout.addLayout(btnlayout)
        tab1layout.addLayout(bottomlayout)
                
        w1.setLayout(tab1layout)
        # w1.setStyleSheet("background-color: QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffffff, stop: 1 #228888);")
        # w1.setStyleSheet("border-image: url(image/bg2.gif);")
        w1.setStyleSheet("background-image: url(image/bg.gif);")
        # firstUi.setupUi(w1)
        w2=QWidget()
        w2.setAccessibleName("w2tab")
        self.w2title = QComboBox()
        self.btn_start2 = QPushButton("开始")
        self.choicenum_text2 = QComboBox()
        self.choicenum_text2.setObjectName('w2combonums')
        titleLayout2, btnlayout2, bottomlayout2 = self.genOneTab(tabtitle = self.w2title, tabbtn=self.btn_start2, tabnums=self.choicenum_text2, strwhere = "where studentsn like '04%' ")
        tab2layout = QVBoxLayout()
        tab2layout.addLayout(titleLayout2)       
        tab2layout.addLayout(btnlayout2)
        tab2layout.addLayout(bottomlayout2)
        w2.setLayout(tab2layout)
        w2.setStyleSheet("background-image: url(image/bg.gif);")

        tabWidget.addTab(w1,"三（3）班━板演|提问")
        tabWidget.addTab(w2,"三（4）班━板演|提问")
        tabWidget.resize(760,700)
        # print(tabWidget.parentWidget())
        btnclose = QPushButton(self)
        btnclose.setText("╳")
        btnclose.setGeometry(735, 5, 20, 20)
        btnclose.setStyleSheet("background-color:rgb(0,0,0); color:rgb(255,255,255)")
        btnclose.clicked.connect(self.close)
        btnMinimized = QPushButton(self)
        btnMinimized.setText("▁")
        btnMinimized.setGeometry(710, 5, 20, 20)
        btnMinimized.setStyleSheet("background-color:rgb(0,0,0); color:rgb(255,255,255)")
        btnMinimized.clicked.connect(lambda: self.showMinimized())

        self.lstchoices = []
        self.threadcounter = 0
        # self.createDb()
        cur = conn.cursor()
        today = datetime.date.today() 
        cur.execute("delete from tmprecord where datequestion= '" +str(today) + "'") #delete tmp date no today
        # cur.execute("delete from tmprecord where datequestion!= '" +str(today) + "'") #delete tmp date no today
        conn.commit()

        cur.execute("select studentsn from student ")
        self.studentSnlst = cur.fetchall()
        cur.close()

        # self.btncolor = self.btngroup.buttons()[0].palette().color(1).getRgb()
        # for i in list(range(0, self.studentNums)):
        for isn in self.studentSnlst:
            self.btngroup.button(int(isn[0])).setStyleSheet("border-image: url(image/ex_stu.png);")
            # print(isn)
        # for i in list(range(0, self.studentNums)):
            # self.btngroup.buttons()[i].setStyleSheet("background-color: rgb(120,220,220);")
            # self.btngroup.buttons()[i].setStyleSheet("border-image: url(image/ex_stu.png);")
            # self.btngroup.buttons()[i].setStyleSheet("background-image: url(image/ex_stu.png);background-size:20px 20px;")

        # print("background-color: rgb(120,220,220);", "background-color: rgb" + str(self.btncolor) + ";")
        self.setWindowTitle("课堂随机提问")
        self.setWindowIcon(QIcon("image/start.ico"))
        self.setGeometry(100, 20, 760, 700)

        self.connect(self.btn_start, SIGNAL("clicked()"), self.startChoice)
        self.connect(self.w1title, SIGNAL("currentIndexChanged(int)"), self.changeTitle)
        self.connect(self.btn_start2, SIGNAL("clicked()"), self.startChoice)
        self.connect(self.w2title, SIGNAL("currentIndexChanged(int)"), self.changeTitle)

    def changeTab(self, curtab):
        if curtab == 0:
            strwhere = " and studentsn like '03%' "
        elif curtab == 1:
            strwhere = " and studentsn like '04%' "

        self.lstchoices = []
        self.threadcounter = 0
        cur = conn.cursor()   
        cur.execute("select studentsn from student where 1=1 " + strwhere)
        self.studentSnlst = cur.fetchall()
        for isn in self.studentSnlst:
            self.btngroup.button(int(isn[0])).setStyleSheet("border-image: url(image/ex_stu.png);")
            self.btngroup.button(int(isn[0])).setIcon(QIcon())
            # self.btngroup.buttons()[i].setStyleSheet("background-color: rgb(120,220,220);")  
            # self.btngroup.buttons()[i].setStyleSheet("border-image: url(image/ex_stu.png);")
            curmenu = self.btngroup.button(int(isn[0])).menu()
            curmenu.actions()[0].setEnabled(True)
            curmenu.actions()[1].setEnabled(True)
            
        cur.close()

    def mousePressEvent(self, event):
        self.offset = event.pos()
        # print(self.offset)
    def mouseMoveEvent(self, event):
        x=event.globalX()
        y=event.globalY()
        x_w = self.offset.x()
        y_w = self.offset.y()
        self.move(x-x_w, y-y_w)

    def genOneTab(self, tabtitle="", tabbtn="", tabnums="", strwhere = "where studentsn like '03%' "):
        # tabtitle.setFixedHeight(40)
        # tabtitle.setFixedWidth(160)
        tabtitle.setFont(QFont('Courier New', 20))
        tabtitle.setStyleSheet("border: 3px solid blue;\
            border-radius: 6px; \
            padding: 1px 18px 1px 20px;\
            min-width: 8em;")
        model = tabtitle.model()
        for row in ["随堂板演", "随堂提问"]:
            item = QStandardItem(str(row))
            item.setForeground(QColor('blue'))
            font = item.font()
            font.setPointSize(20)
            item.setFont(font)
            model.appendRow(item)
        tabtitle.setCurrentIndex(0)
        titleLayout = QHBoxLayout()
        tabtitle.setMinimumHeight(50);
        titleLayout.addWidget(tabtitle)
        titleLayout.setAlignment(tabtitle, Qt.AlignCenter)
       
        btnlayout = QGridLayout()
        
        cur = conn.cursor()
        strsql = "select studentsn, studentname from student " + strwhere
        cur.execute(strsql)
     
        tmpnum = 0
        for item in cur.fetchall():
            irow = tmpnum // 7
            icol = tmpnum % 7
            tmpnum += 1
            btnlayout.setRowMinimumHeight(irow, 80)
            tmpbtn = QPushButton(item[1])
            tmpbtn.setFont(QFont('黑体', 20))
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

        tabbtn.setIcon(QIcon("image/start.png"))
        tabbtn.setStyleSheet("border: 5px solid green;")
        tabbtn.setFixedHeight(45)
        tabbtn.setFixedWidth(100)
        tabbtn.setFont(QFont('黑体', 20))
        # tabnums.setFixedHeight(40)
        # tabnums.setFixedWidth(60)
        tabnums.setFont(QFont('Courier New', 20))
        tabnums.setStyleSheet("border: 5px solid blue; color:red;font-weight:bold;font-size:26px;\
            border-radius: 6px; \
            padding: 1px 1px 1px 1px;\
            min-width: 2em; ")
        # tabnums.VerticalContentAlignment="Center"
        # tabnums.addItems(["1", "2", "3", "4", "5", "6"])
        model = tabnums.model()
        for row in list(range(1, 7)):
            item = QStandardItem(str(row))
            # item.setStyleSheet("background-color:rgb(0,0,255)")
            item.setForeground(QColor('red'))
            item.setBackground(QColor(0,200,50, 130))
            # font = item.font()
            # font.setPointSize(16)
            # item.setFont(font)
            model.appendRow(item)
        tabnums.setCurrentIndex(2)

        bottomlayout = QHBoxLayout()
        bottomlayout.setSizeConstraint(QLayout.SetFixedSize)
        bottomlayout.addStretch(10)
        bottomlayout.addWidget(tabbtn)
        bottomlayout.setSpacing(5)
        bottomlayout.addWidget(tabnums)
     
        cur.close()
        return(titleLayout, btnlayout, bottomlayout)

    def changeTitle(self, curindex):
        # whichtabpage = self.sender().parentWidget().parentWidget().parentWidget()
        # print(whichtabpage.tabText(0), whichtabpage1)
        for isn in self.studentSnlst:
            self.btngroup.button(int(isn[0])).setStyleSheet("border-image: url(image/ex_stu.png);")
            self.btngroup.button(int(isn[0])).setIcon(QIcon())
            # self.btngroup.buttons()[i].setStyleSheet("background-color: rgb(120,220,220);")  
            # self.btngroup.buttons()[i].setStyleSheet("border-image: url(image/ex_stu.png);")
            curmenu = self.btngroup.button(int(isn[0])).menu()
            curmenu.actions()[0].setEnabled(True)
            curmenu.actions()[1].setEnabled(True)

        whichtabpage = self.sender().parentWidget().accessibleName()
        if whichtabpage == "w1tab":
            if curindex == 1:
                self.choicenum_text.setCurrentIndex(0)
                self.choicenum_text.setEnabled(False)
            else:
                self.choicenum_text.setEnabled(True)
                self.choicenum_text.setCurrentIndex(2)
        else:
            if curindex == 1:
                self.choicenum_text2.setCurrentIndex(0)
                self.choicenum_text2.setEnabled(False)
            else:
                self.choicenum_text2.setEnabled(True)
                self.choicenum_text2.setCurrentIndex(2)

    def startChoice(self): 
        self.lstchoices = []
        self.threadcounter = 0
        whichtabpage = self.sender().parentWidget().accessibleName()
        if whichtabpage == "w1tab":
            strwhere = " and studentsn like '03%' "
            tabCombonums = self.findChild(QComboBox, 'w1combonums')
        else:
            strwhere = " and studentsn like '04%' "
            tabCombonums = self.findChild(QComboBox, 'w2combonums')

        # for i in list(range(0, self.studentNums)):
        cur = conn.cursor()   
        # cur.execute("select studentsn from student where 1=1 " + strwhere)
        # self.studentSnlst = cur.fetchall()

        # for isn in self.studentSnlst:
        #     self.btngroup.button(int(isn[0])).setStyleSheet("border-image: url(image/ex_stu.png);")
        #     self.btngroup.button(int(isn[0])).setIcon(QIcon())
        #     # self.btngroup.buttons()[i].setStyleSheet("background-color: rgb(120,220,220);")  
        #     # self.btngroup.buttons()[i].setStyleSheet("border-image: url(image/ex_stu.png);")
        #     curmenu = self.btngroup.button(int(isn[0])).menu()
        #     curmenu.actions()[0].setEnabled(True)
        #     curmenu.actions()[1].setEnabled(True)

        allstudent = []
        lstrecord = ['0000', '1111']
        if tabCombonums.isEnabled():
            cur.execute("select studentsn from tmprecord where 1=1 " + strwhere)  
            for item in cur.fetchall():
                lstrecord.append(item[0])
        # print(lstrecord, 'record', "select studentsn from student where studentsn like '03%' and studentsn not in " + str(tuple(lstrecord)))
        cur.execute("select studentsn from student where studentsn not in " + str(tuple(lstrecord)) + strwhere)
        for item in cur.fetchall():
            allstudent.append(item[0])

        nums = int(tabCombonums.currentText())
        if nums >= len(allstudent):
            cur.execute("delete from tmprecord where datequestion like '%%' ") #delete tmp date no today
            conn.commit()
            allstudent = []
            cur.execute("select studentsn from student where 1=1 " + strwhere)
            for item in cur.fetchall():
                allstudent.append(item[0])
        # print(tabCombonums.currentText())
        cur.close()
        for i in range(10):
            thread = MyThread(self)
            thread.trigger.connect(self.choicestudent)
            thread.setup(allstudent, nums)            # just setting up a parameter
            thread.start()

    def choicestudent(self, allstudent, num): 
        for isn in self.studentSnlst:
            self.btngroup.button(int(isn[0])).setStyleSheet("border-image: url(image/ex_stu.png);")
            # self.btngroup.buttons()[i].setStyleSheet("background-color: rgb(120,220,220);")
        self.lstchoices = random.sample(allstudent, num)
        for ibtn in self.lstchoices:
            self.btngroup.button(int(ibtn)).setStyleSheet("border-image: url(image/ex_stu_ok.png);")
            # self.btngroup.button(int(ibtn)).setStyleSheet("background-color: red; color:white;")
            # self.btngroup.buttons()[ibtn].setStyleSheet("background-color: red; color:white;")

        self.threadcounter += 1
        if self.threadcounter == 10:
            cur = conn.cursor()
            if self.choicenum_text.isEnabled():
                for ibtn in self.lstchoices:
                    today = datetime.date.today()
                    strsql = "insert into tmprecord values (?, ?, ?)" 
                    cur.execute(strsql, (None, ibtn, today))
                    conn.commit()

            # cur.execute("select * from tmprecord")
            # print(cur.fetchall())
            
            cur.close()
                # print(self.btngroup.buttons()[ibtn].text())
            self.threadcounter = 0

    def choiceOneStudent(self, curbtn, num=1):
        # print(self.findChildren(QComboBox))
        if curbtn[:2] == "03":
            strwhere = " and studentsn like '03%' "
            tabCombonums = self.findChild(QComboBox, 'w1combonums')
        elif  curbtn[:2] == "04":
            strwhere = " and studentsn like '04%' "
            tabCombonums = self.findChild(QComboBox, 'w2combonums')

        allstudent = []
        cur = conn.cursor()   
        lstrecord = ['0000', '1111']
        if tabCombonums.isEnabled():
            cur.execute("select studentsn from tmprecord where 1=1 " + strwhere)  
            for item in cur.fetchall():
                lstrecord.append(item[0])
        cur.execute("select studentsn from student where studentsn not in " + str(tuple(lstrecord)) + strwhere)
        for item in cur.fetchall():
            allstudent.append(item[0])

        # cur.execute("select * from tmprecord")
        # print(cur.fetchall(), '111111111111111111')
        otherbtn = random.sample(allstudent, num)[0]
        # self.btngroup.button(int(otherbtn)).setStyleSheet("background-color: red; color:white;")
        self.btngroup.button(int(otherbtn)).setStyleSheet("border-image: url(image/ex_stu_ok.png);")
        self.btngroup.button(int(otherbtn)).setFocus()

        # print(self.lstchoices, 'choice one another00000000000000001')
        self.lstchoices.remove(curbtn)
        self.lstchoices.append(otherbtn)
        # print(self.lstchoices, 'choice one another000000000000000002')

        # cur.execute("delete from tmprecord where studentsn='" + curbtn + "'") # can not delete ,because this student is ill.
        # conn.commit()
        if tabCombonums.isEnabled():
            today = datetime.date.today()
            cur.execute("insert into tmprecord values (?, ?, ?)", (None, otherbtn, today))
            conn.commit()
        # cur.execute("select * from tmprecord")
        # print(cur.fetchall(), '2222222222222')

        cur.close()

    def answerRight(self, value):
        if value not in self.lstchoices:
            return

        self.btngroup.button(int(value)).setIcon(QIcon("image/smile.png"))
        self.btngroup.button(int(value)).setIconSize(QSize(30,30))

        cur = conn.cursor()
        cur.execute("select rightquestions from student where studentsn='" + value + "'")
        studentRightQuestions = cur.fetchall()[0][0] + 1
        cur.execute("update student set rightquestions=" + str(studentRightQuestions) + " where studentsn='" + value + "'")
        conn.commit()
        
        curmenu = self.btngroup.button(int(value)).menu()
        if not curmenu.actions()[1].isEnabled (): # must delete wrongquestionnums
            cur.execute("select wrongquestions from student where studentsn='" + value + "'")
            studentWrongQuestions = cur.fetchall()[0][0] - 1
            cur.execute("update student set wrongquestions=" + str(studentWrongQuestions) + " where studentsn='" + value + "'")
            conn.commit()
        curmenu.actions()[0].setEnabled(False)
        curmenu.actions()[1].setEnabled(True)
        # curmenu.actions()[2].setEnabled(False)
        
        # cur.execute("select * from student where studentsn='" + value + "'")
        # print(cur.fetchall(), 'right-------')

        cur.close()

    def answerWrong(self, value):
        if value not in self.lstchoices:
            return

        self.btngroup.button(int(value)).setIcon(QIcon("image/cry.png"))
        self.btngroup.button(int(value)).setIconSize(QSize(30,30))
        # self.btngroup.button(int(value)).setStyleSheet("border-image: url(image/ex_stu.png);")

        cur = conn.cursor()
        cur.execute("select wrongquestions from student where studentsn='" + value + "'")
        studentWrongQuestions = cur.fetchall()[0][0] + 1
        cur.execute("update student set wrongquestions=" + str(studentWrongQuestions) + " where studentsn='" + value + "'")
        conn.commit()

        curmenu = self.btngroup.button(int(value)).menu()
        if not curmenu.actions()[0].isEnabled (): # must delete wrongquestionnums
            cur.execute("select rightquestions from student where studentsn='" + value + "'")
            studentRightQuestions = cur.fetchall()[0][0] - 1
            cur.execute("update student set rightquestions=" + str(studentRightQuestions) + " where studentsn='" + value + "'")
            conn.commit()
        curmenu.actions()[0].setEnabled(True)
        curmenu.actions()[1].setEnabled(False)

        # cur.execute("select * from student where studentsn='" + value + "'")
        # print(cur.fetchall(), 'wrong--')

        cur.close()

    def resetStudent(self, value):
        if value not in self.lstchoices:
            return

        # self.btngroup.button(int(value)).setStyleSheet("background-color: rgb(120,220,220);")
        self.btngroup.button(int(value)).setIcon(QIcon())
        self.btngroup.button(int(value)).setStyleSheet("border-image: url(image/ex_stu.png);")
        self.btngroup.button(int(value)).setAutoDefault(False)

        cur = conn.cursor()

        curmenu = self.btngroup.button(int(value)).menu()
        if not curmenu.actions()[0].isEnabled():
            cur.execute("select rightquestions from student where studentsn='" + value + "'")
            studentRightQuestions = cur.fetchall()[0][0] - 1
            cur.execute("update student set rightquestions=" + str(studentRightQuestions) + " where studentsn='" + value + "'")
            conn.commit()
        if not curmenu.actions()[1].isEnabled():
            cur.execute("select wrongquestions from student where studentsn='" + value + "'")
            studentWrongQuestions = cur.fetchall()[0][0] - 1
            cur.execute("update student set wrongquestions=" + str(studentWrongQuestions) + " where studentsn='" + value + "'")
            conn.commit()
        cur.close()

        curmenu.actions()[0].setEnabled(True)
        curmenu.actions()[1].setEnabled(True)
        self.choiceOneStudent(value)

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

        strdelete = "delete from student where 1=1"
        cur.execute(strdelete)
        conn.commit()
        strdelete = "delete from tmprecord where 1=1"
        cur.execute(strdelete)
        conn.commit()
        # print(sqlstr2)

        # cur.execute(sqlstr) 
        # conn.commit()
        # cur.execute(sqlstr2) 
        # conn.commit()

        # insert example data
        a03lst = ["曾忆谊","赵佳泉","翁文秀","林珑","郑铭洁","林泽思","吴崇霖","陈思嘉","欧阳月孜","郭展羽","詹伟哲","黄佳仪","杨秋霞","周奕子","林楚杰","欧伊涵","许腾誉","陈唯凯","陈树凯","林彦君","张钰佳","高锴","杨博凯","林妙菲","林楚鸿","陈展烯","姚静茵","吴欣桐","范思杰","肖佳","马思广","许一帆","姚奕帆","陈海珣","吴黛莹","吴育桐","肖凯帆","林欣阳","叶茂霖","姚楷臻","陈嘉豪","陈琦","杨子楷","陈炎宏","陈幸仪","杨景畅","罗暖婷","郑馨"]
        a04lst = ["罗恩琪","王可","曾祥威","谢濡婷","温嘉凯","许洁仪","肖欣淇","陈凯佳","林天倩","李乐海","吴文慧","黄文婷","万誉","陈进盛","张裕涵","陈振嘉","王巧玲","林珮琪","陈炜楷","杨健","赵泽锴","张凤临","蔡子丹","陈烨杰","廖妍希","林树超","夏培轩","陈锦森","李星","蔡依婷","姚容创","姚凯扬","沈嘉克","周凡","张玉川","邱金迅","陈菲敏","陈星翰","朱煜楷","郑泽洪","钱剑非","罗奕丰","陈杜炜","林知钦"]
        strsql = "insert into student values (?, ?, ?,?,?)" 
        for i in list(range(0,len(a03lst))):
            cur.execute(strsql, (None, "03"+str(i+1).zfill(2), a03lst[i], 0, 0))
            conn.commit()
        strsql = "insert into student values (?, ?, ?,?,?)" 
        for i in list(range(0,len(a04lst))):
            cur.execute(strsql, (None, "04"+str(i+1).zfill(2), a04lst[i], 0, 0))
            conn.commit()
        cur.close()
        
if __name__ == "__main__":
    import sys
    app=QApplication(sys.argv)
    dialog=QuestionDlg()
    dialog.show()
    app.exec_()