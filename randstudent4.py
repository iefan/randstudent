from PyQt4.QtGui import QDialog, QIcon, QFont, QMenu, QColor, QComboBox, QLayout, QApplication, QTabWidget, QButtonGroup, QWidget, QPushButton, QStandardItem
from PyQt4.QtGui import QHBoxLayout, QVBoxLayout, QGridLayout, QSizePolicy, QMovie, QLabel
from PyQt4.QtCore import SIGNAL, Qt, QSize, QByteArray, QTimer
import random, datetime
import sqlite3
# import ui_10_1,ui_10_2,ui_10_3
# import sys
        
conn = sqlite3.connect("student.db") 

def fadeIn(ws):
    # 建立一个平行的动作组
    ag = QParallelAnimationGroup()
    for w in ws:
        # 对于每个按钮, 都生成一个进入的动作
        a = QPropertyAnimation(w, "geometry")
        a.setDuration(1000)
        a.setEasingCurve(QEasingCurve.OutQuad)
        a.setStartValue(QRect(-100, w.y(), w.width(), w.height()))
        a.setEndValue(w.geometry())
        # 添加到组里面去
        ag.addAnimation(a)
    return ag

class MyButton(QPushButton):
    def __init__(self, title, parent=None):
        # QPushButton.__init__(self, parent)
        super(MyButton, self).__init__(title, parent)
        self.setText(title)
        self._item = "1"
        # self.studentsn = studentsn

    def setMyarg(self, item):
        self._item = item

    def getMyarg(self):
        return self._item

    def mousePressEvent(self,event):
        if event.button() == Qt.LeftButton:
            QPushButton.mousePressEvent(self,event)
            return
        # print ("!!!!!Processing right click event")
        self.emit(SIGNAL("myslot(PyQt_PyObject)"), self._item)

class QuestionDlg(QDialog):
    def __init__(self,parent=None):
        super(QuestionDlg,self).__init__(parent)
        # self.setStyleSheet("background-image:url('image/panelbg.jpg'); border: 2px; border-radius 2px;")
        self.setWindowFlags(Qt.CustomizeWindowHint)
        # self.setStyleSheet("border: 2px; border-radius 2px;")
        # self.setWindowFlags(Qt.FramelessWindowHint)
        
        tabWidget=QTabWidget(self)
        tabWidget.currentChanged.connect(self.changeTab)
        # tabWidget.setTabShape(QTabWidget.Triangular)
        tabWidget.setStyleSheet("QTabWidget::pane{border:0px;}\
            QTabBar::tab { height: 60px; width: 260px; color:rgb(0, 0, 255); font-size:20px; font-weight:bold;} \
            QTabBar::tab:hover{background:rgb(255,255, 255, 100);} \
            QTabBar::tab:selected{border-color:green;background-color:white;color:green;}")
        # tabWidget.setStyleSheet("QTabBar::tab:hover{background:rgb(255,255, 255, 100);}")
        self.btngroup = QButtonGroup()
        self.popMenu = QMenu(self)
        entry1 = self.popMenu.addAction("正确")
        self.connect(entry1,SIGNAL('triggered()'), lambda : self.answerRight())
        entry2 = self.popMenu.addAction("错误")
        self.connect(entry2,SIGNAL('triggered()'), lambda : self.answerWrong())
        entry3 = self.popMenu.addAction("替换")
        self.connect(entry3,SIGNAL('triggered()'), lambda : self.resetStudent())

        w1=QWidget()
        w1.setAccessibleName("w1tab")
        self.w1title = QLabel()
        self.btn_start = MyButton("开始")
        self.choicenum_text = QComboBox()
        self.choicenum_text.setObjectName('w1combonums')
        # self.w1title.setStyleSheet("background-image:url('image/panelbg.jpg');")

        titleLayout, btnlayout, bottomlayout = self.genOneTab(tabtitle = self.w1title, tabbtn=self.btn_start, tabnums=self.choicenum_text)

        tab1layout = QVBoxLayout()
        tab1layout.addLayout(titleLayout)       
        tab1layout.addLayout(btnlayout)
        tab1layout.addLayout(bottomlayout)
                
        w1.setLayout(tab1layout)
        # w1.setStyleSheet("background-image: url(image/bg.gif);")
        w1.setStyleSheet("background-color: QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffffff, stop: 1 #228888);")
        # w1.setStyleSheet("border-image: url(image/bg2.gif);")
        # firstUi.setupUi(w1)
        w2=QWidget()
        w2.setAccessibleName("w2tab")
        self.w2title = QLabel()
        self.btn_start2 = QPushButton("开始")
        self.choicenum_text2 = QComboBox()
        self.choicenum_text2.setObjectName('w2combonums')
        titleLayout2, btnlayout2, bottomlayout2 = self.genOneTab(tabtitle = self.w2title, tabbtn=self.btn_start2, tabnums=self.choicenum_text2, strwhere = "where studentsn like '04%' ")
        tab2layout = QVBoxLayout()
        tab2layout.addLayout(titleLayout2)       
        tab2layout.addLayout(btnlayout2)
        tab2layout.addLayout(bottomlayout2)
        w2.setLayout(tab2layout)
        # w2.setStyleSheet("background-image: url(image/bg.gif);")
        w2.setStyleSheet("background-color: QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffffff, stop: 1 #228888);")

        tabWidget.addTab(w1,"三（3）班")
        tabWidget.addTab(w2,"三（4）班")
        tabWidget.resize(740,700)
        # print(tabWidget.parentWidget())
        btnclose = QPushButton(self)
        btnclose.setToolTip("关闭")
        btnclose.setText("╳")
        btnclose.setGeometry(715, 5, 20, 20)
        btnclose.setStyleSheet("background-color:rgb(0,100,0); color:rgb(255,255,255)")
        btnclose.clicked.connect(self.close)
        btnMinimized = QPushButton(self)
        btnMinimized.setToolTip("最小化")
        btnMinimized.setText("▁")
        btnMinimized.setGeometry(690, 5, 20, 20)
        btnMinimized.setStyleSheet("background-color:rgb(0,100,0); color:rgb(255,255,255)")
        btnMinimized.clicked.connect(lambda: self.showMinimized())
        self.btnSysMenu = QPushButton(self)
        # self.btnSysMenu.setText("▼")
        self.btnSysMenu.setGeometry(665, 5, 20, 20)
        self.btnSysMenu.setToolTip("系统设置")
        self.btnSysMenu.setStyleSheet("background-color:rgb(0,100,0); color:rgb(255,255,255)")
        self.btnSysMenu.clicked.connect(lambda: self.showMinimized())
        menufont = QFont("宋体", 12)
        popMenu = QMenu(self)
        entry1 = popMenu.addAction("初始化")
        entry1.setFont(menufont)
        self.connect(entry1,SIGNAL('triggered()'), self.initStudent)
        entry2 = popMenu.addAction("清除提问人员")
        entry2.setFont(menufont)
        self.connect(entry2,SIGNAL('triggered()'), self.deleteTmpdata)
        self.btnSysMenu.setMenu(popMenu)
        self.btnSysMenu.setStyleSheet("QPushButton::menu-indicator {image: url('image/sysmenu.png');subcontrol-position: right center;}")

        self.setWindowTitle("课堂随机提问")
        self.setWindowIcon(QIcon("image/start.ico"))
        self.setGeometry(100, 20, 740, 700)

        self.btn_start.setMyarg('start')
        # print(self.btn_start.getMyarg())

        self.connect(self.btn_start, SIGNAL("clicked()"), self.startChoice)
        # self.connect(self.w1title, SIGNAL("currentIndexChanged(int)"), self.changeTitle)
        self.connect(self.btn_start2, SIGNAL("clicked()"), self.startChoice)
        # self.connect(self.w2title, SIGNAL("currentIndexChanged(int)"), self.changeTitle)
        self.btngroup.buttonClicked[int].connect(self.btns_click)
        # self.connect(self.btn_start,  SIGNAL("myslot(PyQt_PyObject)"), self.myslot)  
        # self.connect(self.btngroup, SIGNAL("buttonClicked(int)"), lambda:self.btns_click())

    def myslot(self, text):  
        # print(text)
        self.g_curbtn = text
        if self.g_curbtn not in self.dict_choices:
            self.btnSysMenu.setFocus()
            return

        pos = self.btngroup.button(int(self.g_curbtn)).mapToGlobal(self.btngroup.button(int(self.g_curbtn)).pos())
        width = self.btngroup.button(int(self.g_curbtn)).rect().height()
        # print(pos, width)
        pos.setY(pos.y()+width-5)

        indx = 0
        for istate in self.dict_choices[self.g_curbtn]:
            if istate == '1':
                self.popMenu.actions()[indx].setEnabled(True)
            elif istate == '0':
                self.popMenu.actions()[indx].setEnabled(False)
            indx += 1
        self.popMenu.exec_(pos)
        self.btnSysMenu.setFocus()
    # def on_context_menu(self, point):
    #     print(point)
    #     self.popMenu.exec_(self.button.mapToGlobal(point)) 

    def btns_click(self, btnid):
        # print(self.btngroup.button(btnid).rect())
        # print(self.mapToGlobal(self.btngroup.button(btnid).pos()))
        cur = conn.cursor()
        today = datetime.date.today()
        self.g_curbtn = str(btnid).zfill(4)
        if self.g_curbtn not in self.dict_choices:
            self.btngroup.button(int(self.g_curbtn)).parentWidget().setStyleSheet("border: 3px solid rgb(255,0,0); color:black; font-size:26px;")
            self.btngroup.button(int(self.g_curbtn)).setStyleSheet("border: 1px solid rgba(255,255,255,0);color:black; font-size:26px;")
            self.btngroup.button(int(self.g_curbtn)).setStyleSheet("QPushButton::menu-indicator {image:None; width:1px;}")
            cur.execute("select count(*) from tmprecord where studentsn='" + str(self.g_curbtn) + "'")
            if cur.fetchall()[0][0] == 0:
                strsql = "insert into tmprecord values (?, ?, ?)"
                cur.execute(strsql, (None, self.g_curbtn, today))
                conn.commit()
            self.dict_choices[self.g_curbtn] = "111"
        else:
            self.btngroup.button(int(self.g_curbtn)).parentWidget().setStyleSheet("border: 1px solid rgb(255,255,255,0);background-color: rgba(255,255,255,20);font-size:16px;")
            self.btngroup.button(int(self.g_curbtn)).setStyleSheet("border: 1px solid rgb(255,255,255,0);background-color: rgba(255,255,255,20);font-size:16px;")
            self.btngroup.button(int(self.g_curbtn)).setStyleSheet("QPushButton::menu-indicator {image:None; width:1px;}")
            self.btngroup.button(int(self.g_curbtn)).setIcon(QIcon())
            # cur.execute("select count(*) from tmprecord where studentsn='" + str(self.g_curbtn) + "'")
            # print(cur.fetchall())
            cur.execute("delete from tmprecord where studentsn='"+ str(self.g_curbtn) + "'")
            conn.commit()
            self.dict_choices.pop(self.g_curbtn)
        self.btnSysMenu.setFocus()
        cur.close()

    def initStudent(self):
        cur = conn.cursor()
        cur.execute("update student set wrongquestions=0")
        conn.commit()
        cur.execute("update student set rightquestions=0")
        conn.commit()

        # cur.execute("select * from student")
        # print(cur.fetchall())
        cur.close()

    def deleteTmpdata(self):
        cur = conn.cursor()
        cur.execute("delete from tmprecord where 1=1" )
        conn.commit()
        cur.close()

    def changeTab(self, curtab):
        if curtab == 0:
            strwhere = " and studentsn like '03%' "
        elif curtab == 1:
            strwhere = " and studentsn like '04%' "

        self.g_curbtn = ""
        self.dict_choices = {}

        cur = conn.cursor()
        cur.execute("delete from tmprecord where 1=1")
        conn.commit()
        cur.execute("select studentsn from student where 1=1 " + strwhere)
        self.studentSnlst = cur.fetchall()

        stylesheetstr = "border: 1px solid rgb(60,200,255,200);\
                background-color: rgba(255,255,255,60);\
                font-size:16px;\
                QPushButton::menu-indicator {image:None; width:1px;}"
        for isn in self.studentSnlst:
            self.btngroup.button(int(isn[0])).setStyleSheet(stylesheetstr)
            self.btngroup.button(int(isn[0])).setIcon(QIcon())

        cur.close()

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            QDialog.mousePressEvent(self,event)
            return
        # print(event.sender(), event.button())
        self.offset = event.pos()
        # print(self.offset)

    def mouseMoveEvent(self, event):
        if hasattr(self, 'offset'):
            x=event.globalX()
            y=event.globalY()
            x_w = self.offset.x()
            y_w = self.offset.y()
            self.move(x-x_w, y-y_w)
        else:
            pass

    def genOneTab(self, tabtitle="", tabbtn="", tabnums="", strwhere = "where studentsn like '03%' "):
        # tabtitle.setFixedHeight(40)
        # tabtitle.setFixedWidth(160)
        tabtitle.setFont(QFont('Courier New', 20))
        tabtitle.setText("随堂提问演板")
        tabtitle.setStyleSheet("border: 3px solid blue;\
            border-radius: 6px; \
            padding: 1px 18px 1px 20px;\
            min-width: 8em;")
        tabtitle.setMinimumHeight(50);
        titleLayout = QHBoxLayout()
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

            tmpbtn = MyButton(item[1])
            tmpbtn.setMyarg(item[0])
            # tmpbtn.setFixedHeight(20)
            tmpbtn.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding))
            # tmpbtn.setStyleSheet("border: 1px solid rgb(255,255,255,0);background-color: rgba(255,255,255,20);font-size:16px;")
            # tmpbtn.setFlat(True)
            self.connect(tmpbtn,  SIGNAL("myslot(PyQt_PyObject)"), self.myslot)
            # self.connect(tmpbtn, SIGNAL('customContextMenuRequested(const QPoint&)'), self.on_context_menu)

            tmpbtn.setAutoDefault(False)
            self.btngroup.addButton(tmpbtn, int(item[0]))

            # tmpmovie = QMovie('image/ex_stu.gif', QByteArray(), self)
            # tmplabel = QLabel()
            # tmplabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            # tmplabel.setAlignment(Qt.AlignCenter)
            # tmplabel.setMovie(tmpmovie)
            # tmplabel.setScaledContents(True)
            # tmplabel.setLayout(QHBoxLayout())
            # tmplabel.layout().setContentsMargins(0,0,0,0)
            # tmplabel.layout().addWidget(tmpbtn)
            # tmpmovie.start()
            # tmpmovie.stop()

            # btnlayout.addWidget(tmplabel, irow, icol)
            btnlayout.addWidget(tmpbtn, irow, icol)

        tabbtn.setIcon(QIcon("image/start.png"))
        tabbtn.setStyleSheet("border: 5px solid yellow;")
        tabbtn.setFixedHeight(40)
        tabbtn.setFixedWidth(100)
        tabbtn.setFont(QFont('宋体', 20))
        # tabnums.setFixedHeight(45)
        # tabnums.setFixedWidth(60)
        tabnums.setFont(QFont('Courier New', 20))
        tabnums.setStyleSheet("border: 5px solid blue; color:red;font-weight:bold;font-size:26px;\
            border-radius: 6px; \
            padding: 1px 1px 1px 1px;\
            min-width: 2em; ")
        tabnums.setEditable(True)
        tabnums.lineEdit().setReadOnly(True);
        tabnums.lineEdit().setAlignment(Qt.AlignCenter);

        model = tabnums.model()
        for row in list(range(1, 7)):
            item = QStandardItem(str(row))
            item.setTextAlignment(Qt.AlignCenter)
            item.setForeground(QColor('red'))
            item.setBackground(QColor(0,200,50, 130))
            model.appendRow(item)
        tabnums.setCurrentIndex(2)
        # tabnums.setStyleSheet ("QComboBox::drop-down {border-width: 100px;}")
        # tabnums.setStyleSheet ("QComboBox::down-arrow {image: url(image/downarrow.png);top: 10px;left: 1px;}")

        bottomlayout = QHBoxLayout()
        bottomlayout.setSizeConstraint(QLayout.SetFixedSize)
        bottomlayout.addStretch(10)
        bottomlayout.addWidget(tabbtn)
        bottomlayout.setSpacing(5)
        bottomlayout.addWidget(tabnums)
     
        cur.close()
        return(titleLayout, btnlayout, bottomlayout)
    
    def startChoice(self, usernum="", oldbtn=""): 
        if oldbtn != "":
            flag = str(int(oldbtn[:2]))
        else:
            self.dict_choices = {}
            whichtabpage = self.sender().parentWidget().accessibleName()
            flag = (whichtabpage == "w1tab") and "3" or "4"
            
        if flag== "3":
            strwhere = " and studentsn like '03%' "
            tabCombonums = self.findChild(QComboBox, 'w1combonums')
        else:
            strwhere = " and studentsn like '04%' "
            tabCombonums = self.findChild(QComboBox, 'w2combonums')

        cur = conn.cursor()   
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

        if usernum == "":
            nums = int(tabCombonums.currentText())
        else:
            nums = usernum
        if nums >= len(allstudent):
            cur.execute("delete from tmprecord where datequestion like '%%' ") #delete tmp date no today
            conn.commit()
            allstudent = []
            cur.execute("select studentsn from student where 1=1 " + strwhere)
            for item in cur.fetchall():
                allstudent.append(item[0])
        # print(tabCombonums.currentText())
        cur.close()

        stylesheetstr = "border: 1px solid rgb(60,200,255,200);\
                background-color: rgba(255,255,255,60);\
                font-size:16px;\
                QPushButton::menu-indicator {image:None; width:1px;}"
        for isn in self.studentSnlst:
            self.btngroup.button(int(isn[0])).setStyleSheet(stylesheetstr)
            self.btngroup.button(int(isn[0])).setIcon(QIcon())

        # for istu in self.studentSnlst:
        #     self.btngroup.button(int(istu[0])).parentWidget().movie().start()
            # print(istu)
        # print(allstudent)
        if oldbtn == "":
            random.seed()
            lstchoices = random.sample(allstudent, nums)
            for ibtn in lstchoices:
                self.dict_choices[ibtn] = "111"
            # QTimer.singleShot(1000, self.stopmovie)
        else:
            random.seed()
            otherbtn = random.sample(allstudent, 1)[0]
            # self.btngroup.button(int(otherbtn)).setFocus()
            self.dict_choices.pop(oldbtn)
            self.dict_choices[otherbtn] = '111'
            # self.stopmovie()
        self.btnSysMenu.setFocus()

    def stopmovie(self):
        # for istu in self.studentSnlst:
        #     self.btngroup.button(int(istu[0])).parentWidget().movie().stop()
        #     self.btngroup.button(int(istu[0])).parentWidget().movie().jumpToFrame(0)

        cur = conn.cursor()
        today = datetime.date.today()
        for ibtn in self.dict_choices:
            # print('1111', ibtn, self.btngroup.button(int(ibtn)))
            # print(self.btngroup.button(int(ibtn)).text())
            self.btngroup.button(int(ibtn)).parentWidget().setStyleSheet("border: 3px solid rgb(255,0,0); color:black; font-size:26px;")
            self.btngroup.button(int(ibtn)).setStyleSheet("border: 1px solid rgba(255,255,255,0);color:black; font-size:26px;")
            self.btngroup.button(int(ibtn)).setStyleSheet("QPushButton::menu-indicator {image:None; width:1px;}")
            cur.execute("select count(*) from tmprecord where studentsn='" + str(ibtn) + "'")
            if cur.fetchall()[0][0] == 0:
                strsql = "insert into tmprecord values (?, ?, ?)"
                cur.execute(strsql, (None, ibtn, today))
                conn.commit()

        # cur.execute("select * from tmprecord")
        # print(cur.fetchall())
        cur.close()

    def answerRight(self):
        # print(self.g_curbtn)
        value = self.g_curbtn
        if value not in self.dict_choices:
            return

        self.btngroup.button(int(value)).setIcon(QIcon("image/smile.png"))
        self.btngroup.button(int(value)).setIconSize(QSize(20,20))

        cur = conn.cursor()
        cur.execute("select rightquestions from student where studentsn='" + value + "'")
        studentRightQuestions = cur.fetchall()[0][0] + 1
        cur.execute("update student set rightquestions=" + str(studentRightQuestions) + " where studentsn='" + value + "'")
        conn.commit()
        
        ###########
        if self.dict_choices[value] == "101":
            cur.execute("select wrongquestions from student where studentsn='" + value + "'")
            studentWrongQuestions = cur.fetchall()[0][0] - 1
            cur.execute("update student set wrongquestions=" + str(studentWrongQuestions) + " where studentsn='" + value + "'")
            conn.commit()
        cur.close()

        self.dict_choices[value] = "011"

    def answerWrong(self):
        value = self.g_curbtn
        if value not in self.dict_choices:
            return

        self.btngroup.button(int(value)).setIcon(QIcon("image/cry.png"))
        self.btngroup.button(int(value)).setIconSize(QSize(20,20))
        # self.btngroup.button(int(value)).setStyleSheet("border-image: url(image/ex_stu.png);")

        cur = conn.cursor()
        cur.execute("select wrongquestions from student where studentsn='" + value + "'")
        studentWrongQuestions = cur.fetchall()[0][0] + 1
        cur.execute("update student set wrongquestions=" + str(studentWrongQuestions) + " where studentsn='" + value + "'")
        conn.commit()

        if self.dict_choices[value] == "011":
            cur.execute("select rightquestions from student where studentsn='" + value + "'")
            studentRightQuestions = cur.fetchall()[0][0] - 1
            cur.execute("update student set rightquestions=" + str(studentRightQuestions) + " where studentsn='" + value + "'")
            conn.commit()
        cur.close()
        self.dict_choices[value] = "101"

    def resetStudent(self):
        value = self.g_curbtn
        if value not in self.dict_choices:
            return

        # self.btngroup.button(int(value)).parentWidget().setStyleSheet("border: 1px solid rgb(255,255,255,0);background-color: rgba(255,255,255,20);font-size:16px;")
        # self.btngroup.button(int(value)).setStyleSheet("border: 1px solid rgb(255,255,255,0);background-color: rgba(255,255,255,20);font-size:16px;")
        # self.btngroup.button(int(value)).setAutoDefault(False)

        cur = conn.cursor()

        if self.dict_choices[value] == "011":        
            cur.execute("select rightquestions from student where studentsn='" + value + "'")
            studentRightQuestions = cur.fetchall()[0][0] - 1
            cur.execute("update student set rightquestions=" + str(studentRightQuestions) + " where studentsn='" + value + "'")
            conn.commit()
        if self.dict_choices[value] == "101":
            cur.execute("select wrongquestions from student where studentsn='" + value + "'")
            studentWrongQuestions = cur.fetchall()[0][0] - 1
            cur.execute("update student set wrongquestions=" + str(studentWrongQuestions) + " where studentsn='" + value + "'")
            conn.commit()
        cur.close()

        self.startChoice(usernum=1, oldbtn=value)

        # curmenu.actions()[0].setEnabled(True)
        # curmenu.actions()[1].setEnabled(True)
        # self.choiceOneStudent(value)

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