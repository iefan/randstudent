from PyQt4.QtGui import QDialog, QIcon, QFont, QMenu, QColor, QComboBox, QLayout, QApplication, QTabWidget, QButtonGroup, QWidget, QPushButton, QStandardItem
from PyQt4.QtGui import QHBoxLayout, QVBoxLayout, QGridLayout, QSizePolicy, QLabel, QDesktopWidget
from PyQt4.QtGui import QTableView, QDialogButtonBox, QMessageBox, QAbstractItemView, QItemDelegate
from PyQt4.QtCore import SIGNAL, Qt, QSize, QTimer,  pyqtProperty, QParallelAnimationGroup, QPropertyAnimation, QEasingCurve, QPyNullVariant, QDir
from PyQt4.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel, QSqlRelationalTableModel, QSqlRelation
import random, datetime
import sqlite3
# import ui_10_1,ui_10_2,ui_10_3
# import sys

class ComboBoxDelegate(QItemDelegate):
    def __init__(self, parent, itemslist=["a", "b", "c"]):
        QItemDelegate.__init__(self, parent)
        # itemslist = ["a", "b", "c"]
        self.itemslist = itemslist
        self.parent = parent

    def createEditor(self, parent, option, index):
        self.editor = QComboBox(parent)
        self.editor.addItems(self.itemslist)
        self.editor.setCurrentIndex(0)
        self.editor.installEventFilter(self)    
        # self.connect(self.editor, SIGNAL("currentIndexChanged(int)"), self.editorChanged)

        return self.editor

    def setEditorData(self, editor, index): 
        curtxt = index.data(Qt.DisplayRole)
        # print(type(curtxt)== QPyNullVariant )
        if type(curtxt) == type(1):
            curindx = int(index.data(Qt.DisplayRole))
            curtxt = self.itemslist[curindx]
        elif type(curtxt)== QPyNullVariant:
            curtxt = ""
        pos = self.editor.findText(curtxt)
        if pos == -1:  
            pos = 0
        self.editor.setCurrentIndex(pos)


    def setModelData(self,editor,model,index):
        curindx = self.editor.currentIndex()
        text = self.itemslist[curindx]
        model.setData(index, text)

g_cols = 8   

stylesheetstr_old = "border: 1px solid rgb(60,200,255,200);color:rgba(0,0,0,80);\
                background-color: rgba(255,255,255,60);\
                font-size:16px;\
                QPushButton::menu-indicator {image:None; width:1px;}"
stylesheetstr_new = "border: 4px solid rgba(255,0,0,255);color:black;\
                background-color: rgba(255,255,255,60);\
                font-size:26px;\
                QPushButton::menu-indicator {image:None; width:1px;}"

def groupAnimation(ws, btngroup):
    # 建立一个平行的动作组
    ag = QParallelAnimationGroup()
    for w in ws:
        # print(w)
        tmpbtn = btngroup.button(int(w[0]))
        # 对于每个按钮, 都生成一个进入的动作
        a = QPropertyAnimation(tmpbtn, "alpha")
        a.setDuration(200)
        a.setKeyValueAt(0, 10)
        # a.setKeyValueAt(0.5, 200)
        a.setKeyValueAt(1, 255)
        a.setLoopCount(-1)
        a.setEasingCurve(QEasingCurve.OutQuad)
        # a.setStartValue(QRect(-100, w.y(), w.width(), w.height()))
        # a.setEndValue(w.geometry())
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
        # print(1)
        if event.button() == Qt.LeftButton:
            # print(2)
            QPushButton.mousePressEvent(self,event)
            return
        # print ("!!!!!Processing right click event")
        self.emit(SIGNAL("myslot(PyQt_PyObject)"), self._item)

    def get_alpha(self):
        return self._alpha

    def set_alpha(self, alpha):
        self._alpha = alpha
        # print(self._alpha)
        # print("======", "background-color: rgba(0,200,0,"+str(self._alpha) + ")")
        self.setStyleSheet("background-color: rgba(180,105,255,"+str(self._alpha) + ")")

    alpha = pyqtProperty(int, fset=set_alpha)

class QuestionDlg(QDialog):
    def __init__(self, parent=None):
        super(QuestionDlg,self).__init__(parent)
        # self.setStyleSheet("background-image:url('image/panelbg.jpg'); border: 2px; border-radius 2px;")
        # self.createDb()
        # return

        self.db = QSqlDatabase.addDatabase("QSQLITE");  
        self.db.setDatabaseName("studentNew.db")
        if not self.db.open():
            QMessageBox.warning(None, "错误",  "数据库连接失败: %s" % self.db.lastError().text())
            sys.exit(1)

        self.g_curClassName = ""
        self.deleteTmpdata()

        self.setWindowFlags(Qt.CustomizeWindowHint)
        # self.setStyleSheet("border: 2px; border-radius 2px;")
        # self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet("background-color: rgba(132, 171, 208, 200);")

        self.tabWidget=QTabWidget(self)
        self.tabWidget.currentChanged.connect(self.changeTab)
        # tabWidget.setTabShape(QTabWidget.Triangular)
        self.tabWidget.setStyleSheet("QTabWidget::pane{border-width:1px;border-color:rgb(48, 104, 151);\
            border-style: outset;background-color: rgb(132, 171, 208);\
            background: transparent;} \
            QTabWidget::tab-bar{border-width:0px;}\
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

        # Create the first tab page.
        self.w1=QWidget()
        self.w1.setAccessibleName("w1tab")
        self.genOneTab()
        
        # Create the second tab page.
        self.w2=QWidget()
        self.w2.setAccessibleName("w2tab")        
        self.genTwoTab()

        self.tabWidget.addTab(self.w1,"")
        self.tabWidget.addTab(self.w2,"班级学生信息管理")
        self.tabWidget.resize(940,700)

        btnclose = QPushButton(self)
        btnclose.setToolTip("关闭")
        btnclose.setText("╳")
        btnclose.setGeometry(915, 5, 20, 20)
        btnclose.setStyleSheet("background-color:rgb(0,100,0); color:rgb(255,255,255)")
        btnclose.clicked.connect(self.close)
        btnMinimized = QPushButton(self)
        btnMinimized.setToolTip("最小化")
        btnMinimized.setText("▁")
        btnMinimized.setGeometry(890, 5, 20, 20)
        btnMinimized.setStyleSheet("background-color:rgb(0,100,0); color:rgb(255,255,255)")
        btnMinimized.clicked.connect(lambda: self.showMinimized())
        self.btnSysMenu = QPushButton(self)
        # self.btnSysMenu.setText("▼")
        self.btnSysMenu.setGeometry(865, 5, 20, 20)
        self.btnSysMenu.setToolTip("系统设置")
        self.btnSysMenu.clicked.connect(lambda: self.showMinimized())
        menufont = QFont("宋体", 10)
        popMenu = QMenu(self)
        entry1 = popMenu.addAction("所有学生提问信息清零")
        entry1.setFont(menufont)
        self.connect(entry1,SIGNAL('triggered()'), self.initStudent)
        entry2 = popMenu.addAction("清除本堂课提问人员")
        entry2.setFont(menufont)
        self.connect(entry2,SIGNAL('triggered()'), self.deleteTmpdata)
        entry3 = popMenu.addAction("关于...")
        entry3.setFont(menufont)
        self.connect(entry3,SIGNAL('triggered()'), self.aboutMe)
        entry4 = popMenu.addAction("导出...")
        entry4.setFont(menufont)
        self.connect(entry4,SIGNAL('triggered()'), self.exportNotice)

        self.btnSysMenu.setMenu(popMenu)
        self.btnSysMenu.setStyleSheet("QPushButton::menu-indicator {image: url('image/sysmenu.png');subcontrol-position: right center;} ")
        # self.btnSysMenu.setStyleSheet("background-color:rgb(0,100,0); color:rgb(255,255,255);")

        authorinfo = QLabel(self.tabWidget)
        # authorinfo.setToolTip("关闭")
        authorinfo.setText("程序设计：汕头市大华路第一小学 赵小娜，有任何问题请反馈至mybsppp@163.com。")
        authorinfo.setGeometry(20, 665, 470, 26)
        authorinfo.setFont(QFont('Courier New'))
        authorinfo.setStyleSheet("background-color:rgba(255, 255, 255,160); font-size:12px;border: 1px solid rgb(60,200,255,200);color:rgba(0,0,0,220);border-radius:12px;")

        self.setWindowTitle("课堂随机提问")
        self.setWindowIcon(QIcon("image/start.ico"))
        self.setGeometry(100, 20, 940, 700)

        # self.changeTab()

        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)

        self.btn_start.setMyarg('start')
        
        # print(self.btn_start.getMyarg())

        self.connect(self.btn_start, SIGNAL("clicked()"), self.startChoice)
        # self.connect(self.w1title, SIGNAL("currentIndexChanged(int)"), self.changeTitle)
        # self.connect(self.btn_start2, SIGNAL("clicked()"), self.startChoice)
        # self.connect(self.w2title, SIGNAL("currentIndexChanged(int)"), self.changeTitle)
        self.btngroup.buttonClicked[int].connect(self.btns_click)
        # self.connect(self.btn_start,  SIGNAL("myslot(PyQt_PyObject)"), self.myslot)  
        # self.connect(self.btngroup, SIGNAL("buttonClicked(int)"), lambda:self.btns_click())

    def myslot(self, text):  
        # print(text, self.dict_choices)
        self.g_curbtn = text
        if self.g_curbtn not in self.dict_choices:
            self.btnSysMenu.setFocus()
            return

        # print(self.btngroup.button(int(self.g_curbtn)).parent())
        # print(type(self.btngroup.button(int(self.g_curbtn)).parentWidget()))
        pos = self.btngroup.button(int(self.g_curbtn)).parent().mapToGlobal(self.btngroup.button(int(self.g_curbtn)).pos())
        width = self.btngroup.button(int(self.g_curbtn)).rect().height()
        # print("-----", pos, width)
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
        # curclassname = self.tabWidget.tabText(0)
        query = QSqlQuery(self.db)
        # cur = conn.cursor()
        today = datetime.date.today()
        self.g_curbtn = str(btnid).zfill(2)
        if self.g_curbtn not in self.dict_choices:
            self.btngroup.button(int(self.g_curbtn)).setStyleSheet(stylesheetstr_new)
            query.exec_("select count(*) from tmprecord where stusn='" + str(self.g_curbtn) + "'")
            query.next()            
            if query.value(0) == 0:
                query.prepare("insert into tmprecord (classname, stusn, datequestion) values (:classname, :stusn, :datequestion)")
                query.bindValue(":classname", self.g_curClassName)
                query.bindValue(":stusn", self.g_curbtn)
                query.bindValue(":datequestion", today)
                query.exec_() 
                
            self.dict_choices[self.g_curbtn] = "111"
        else:
            self.btngroup.button(int(self.g_curbtn)).setStyleSheet(stylesheetstr_old)
            self.btngroup.button(int(self.g_curbtn)).setIcon(QIcon())            
            query.exec_("delete from tmprecord where stusn='"+ str(self.g_curbtn) + "'")            
            self.dict_choices.pop(self.g_curbtn)

        self.btnSysMenu.setFocus()

    def exportNotice(self):
        query = QSqlQuery(self.db)
        query.exec_("select stusn, stuname, classname, rightquestions, wrongquestions from student" ) 
        lstInfo = [["学号","姓名", "班级", "回答正确次数", "回答错误次数"]]
        while(query.next()):
            lstInfo.append([query.value(0),query.value(1),query.value(2),query.value(3),query.value(4)])

        from xlwt import Workbook,easyxf
        book = Workbook(encoding='ascii')
            # 'pattern: pattern solid,  fore_colour white;'
        style = easyxf(
            'font: height 280, name 黑体;'
            'align: vertical center, horizontal center;'
            )
        style2 = easyxf('font: height 260, name 仿宋_GB2312, bold True; align: vertical center, horizontal left;')
        style3 = easyxf('font: height 260, name 仿宋_GB2312, bold True; align: vertical center, horizontal left, wrap True;')

        sheet1 = book.add_sheet('学生提问情况汇总',cell_overwrite_ok=True)
        # sheet1.write(0,7,flagtxt, easyxf('font: height 200, name 黑体;align: vertical center, horizontal right;'))
        sheet1.write_merge(0,0,0,4, '学生提问情况汇总表',style)
        sheet1.row(0).height_mismatch = 1
        sheet1.row(0).height = 5*256

        sheet1.col(0).width = 10*256
        sheet1.col(1).width = 25*256
        sheet1.col(2).width = 25*256
        sheet1.col(3).width = 20*256
        sheet1.col(4).width = 20*256
        
        tmprows = 1
        for item in lstInfo:
            stusn               = item[0]
            stuname             = item[1]
            classname           = item[2]
            rightquestions      = item[3]
            wrongquestions      = item[4]

            sheet1.write(tmprows,0,stusn, style2)
            sheet1.write(tmprows,1,stuname, style2)
            sheet1.write(tmprows,2,classname, style2)
            sheet1.write(tmprows,3,rightquestions, style2)
            sheet1.write(tmprows,4,wrongquestions, style2)
            tmprows += 1
        # print(tmprows)
        sheet1.header_str = "".encode()
        sheet1.footer_str = "".encode()

        # book.save('d:/simple.xls')
        # print(QDir.home().dirName() , QDir.homePath ())
        filename = QDir.homePath () + "\学生提问情况汇总表.xls" 
        try:
            book.save(filename)
        except  Exception as e:
            QMessageBox.warning(self, "写入错误", "错误号："+str(e.errno)+"\n错误描述："+e.strerror+"\n请关闭已经打开的%s文档!" % filename)
        QMessageBox.about (self, "导出成功", "请查看文档：%s" % filename)

    def aboutMe(self):
        strinfo = """本软件采用python3.4编写，界面采用qt4.8的python绑定。
                    \n版本所有：汕头市大华路第一小学赵小娜老师。
                    \n有任何问题请反馈至mybsppp@163.com。
                    """
        QMessageBox.information(None, "关于", strinfo)
        
    def initStudent(self):
        query = QSqlQuery(self.db)
        ret = query.exec_("update student set wrongquestions=0") 
        ret = query.exec_("update student set rightquestions=0")  
        QMessageBox.information(None, "提示", "已清除所有学生的累计提问情况。")


    def deleteTmpdata(self):
        query = QSqlQuery(self.db)
        ret = query.exec_("delete from tmprecord where 1=1" )   
        if self.g_curClassName != "":     
            QMessageBox.information(None, "提示", "已清除本次软件启动后的所有已提问过的学生。")
  
    def changeTab(self):
        # pass
        curtab = self.tabWidget.currentIndex()
        # print(curtab, "-")
        if curtab == 1:  ## when click the second tab page ,then pass.
            return
            
        # cur = conn.cursor()
        query = QSqlQuery(self.db)

        ## if current classname is null, then set current tabpage display the first class of classtable
        if self.g_curClassName == "":
            ret = query.exec_("select classname from classtable")
            query.next()
            self.g_curClassName = query.value(0)
            
        self.tabWidget.setTabText(0, self.g_curClassName)
        # print(1)
        strwhere = " and classname like '" + self.g_curClassName + "'"

        self.g_curbtn = ""
        self.dict_choices = {}
        self.studentSnlst = []

        ## clearn the question data of temp record .
        ret= query.exec_("delete from tmprecord where 1=1")
        ret = query.exec_("select stusn, stuname from student where 1=1 " + strwhere)

        ## now update the global data "self.btngroup"
        for indx in range(0, 56):
            self.btngroup.button(indx+1).setText("")
            self.btngroup.button(indx+1).setMyarg(None)       
            self.btngroup.button(indx+1).setStyleSheet(stylesheetstr_old)
            self.btngroup.button(indx+1).setIcon(QIcon())
            self.btngroup.button(indx+1).setEnabled(False)
            self.studentSnlst.append([indx+1,])

        inum = 0
        while (query.next()): 
            inum += 1            
            self.btngroup.button(inum).setText(query.value(1))
            self.btngroup.button(inum).setMyarg(query.value(0))       
            self.btngroup.button(inum).setStyleSheet(stylesheetstr_old)
            self.btngroup.button(inum).setIcon(QIcon())
            self.btngroup.button(inum).setEnabled(True)

        # print(inum, len(self.btngroup.buttons()))        

        self.group_animation = groupAnimation(self.studentSnlst, self.btngroup)

    def mousePressEvent(self, event):
        # print('a')
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

    #######======= studentModel ============###############
    def newStudent(self):
        row = self.StudentModel.rowCount()
        self.StudentModel.insertRow(row)
        self.StudentView.scrollToBottom()
        self.StudentModel.setData(self.StudentModel.index(row, 1), self.g_curClassName)

    def removeStudent(self):
        index = self.StudentView.currentIndex()
        row = index.row()             
        if QMessageBox.question(self, "删除确认", "是否要删除当前选中记录？", "确定", "取消") == 0:
            self.StudentModel.removeRows(row, 1)
            self.StudentModel.submitAll()
            self.StudentModel.database().commit()

    def revertStudent(self):
        self.StudentModel.revertAll()
        self.StudentModel.database().rollback()

    def saveStudent(self):
        self.StudentModel.database().transaction()
        if self.StudentModel.submitAll():
            self.StudentModel.database().commit()
            # print("save success!  ->commit")
        else:
            self.StudentModel.revertAll()
            self.StudentModel.database().rollback()

    #######======= classModel ============###############
    def newClass(self):
        row = self.ClassnameModel.rowCount()
        self.ClassnameModel.insertRow(row)

    def removeClass(self):
        index = self.ClassnameView.currentIndex()
        row = index.row()   
        curClassname =  index.sibling(index.row(),0).data()
        strwhere = "classname like '" + curClassname + "'"
        self.StudentModel.setFilter(strwhere)
        self.StudentModel.select()
        # print(self.StudentModel.rowCount(), "----", )
        if QMessageBox.question(self, "删除确认", "删除班级意味着会删除本班所有人员信息。是否要删除当前选中记录？", "确定", "取消") == 0:
            self.ClassnameModel.removeRows(row, 1)
            self.ClassnameModel.submitAll()
            self.ClassnameModel.database().commit()

            self.StudentModel.removeRows(0, self.StudentModel.rowCount())
            self.StudentModel.submitAll()
            self.StudentModel.database().commit()

    def revertClass(self):
        self.ClassnameModel.revertAll()
        self.ClassnameModel.database().rollback()

    def saveClass(self):
        query = QSqlQuery(self.db)

        # record the old class name
        lstOldClassName = {}
        lstOldClassid = []
        query.exec_("select rowid, classname from classtable" )        
        while(query.next()):
            lstOldClassName[query.value(0)] = query.value(1)
            lstOldClassid.append(query.value(0))
        # print(lstOldClassName)

        # print(lstOldClassName)

        # index = self.ClassnameView.currentIndex()
        # row = index.row()   
        # curClassname =  index.sibling(index.row(),1).data()
        # print(curClassname, '---------------------------------')
        # return

        # Update the class Table
        self.ClassnameModel.database().transaction()
        if self.ClassnameModel.submitAll():
            self.ClassnameModel.database().commit()
            # print("save success!  ->commit")
        else:
            QMessageBox.warning(None, "错误",  "请检查班级中名称，不能出现同名班级！")
            self.ClassnameModel.revertAll()
            self.ClassnameModel.database().rollback()

        # print(lstOldClassid)

        lstNewClassName = {}
        query.exec_("select rowid, classname from classtable where rowid in " + str(tuple(lstOldClassid)) )        
        while(query.next()):
            lstNewClassName[query.value(0)] = query.value(1)            

        # print(lstOldClassName, '=========')
        # print(lstNewClassName, '~~~~~~~~~')

        for i in lstOldClassName:
            oldclassname = lstOldClassName[i]
            newclassname = lstNewClassName[i]
            if oldclassname != newclassname:
                # print(oldclassname, newclassname, '++++++++')
                # print("update student set classname=" + newclassname + " where classname='" + oldclassname + "'")
                query.exec_("update student set classname='" + newclassname + "' where classname='" + oldclassname + "'")
                self.StudentModel.setFilter("classname = '" + newclassname + "'")
                self.StudentModel.select()

        lstClassName = []      
        query.exec_("select classname from classtable" ) 
        while(query.next()):
            lstClassName.append(query.value(0))
        self.StudentView.setItemDelegateForColumn(1,  ComboBoxDelegate(self, lstClassName))

    def dbclick(self, indx):
        if type(indx.sibling(indx.row(),0).data()) != QPyNullVariant:
            classname = indx.sibling(indx.row(),0).data()
            
            strwhere = "classname like '" + classname + "'"
            self.StudentModel.setFilter(strwhere)
            self.StudentModel.select()
            
            self.g_curClassName = classname
            self.tabWidget.setTabText(0, self.g_curClassName)


    def genTwoTab(self, tabtitle=""):
        # Create the tab title sytle.
        tabtitle = QLabel()
        tabtitle.setFont(QFont('Courier New', 20))
        tabtitle.setText("班级学生信息管理")
        tabtitle.setStyleSheet("border: 1px solid blue; color:rgba(0,0,255, 220);\
            background-color:rgba(201,201,201,60);\
            border-radius: 6px; \
            padding: 1px 18px 1px 20px;\
            min-width: 8em;")
        tabtitle.setMinimumHeight(50);
        titleLayout = QHBoxLayout()
        titleLayout.addWidget(tabtitle)
        titleLayout.setAlignment(tabtitle, Qt.AlignCenter)

       
        # Create the classnameView
        self.ClassnameView = QTableView()
        self.ClassnameModel = QSqlTableModel(self.ClassnameView)
        self.ClassnameModel.setTable("classtable")
        # self.ClassnameModel.setRelation(2, QSqlRelation("mentalmodel", "id", "name"));
        self.ClassnameModel.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.ClassnameModel.select()

        self.ClassnameModel.setHeaderData(0, Qt.Horizontal, "班级名称")

        # for indx, iheader in enumerate(["classid", "classname"]):
        #     self.ClassnameModel.setHeaderData(indx+1, Qt.Horizontal, iheader)
    
        self.ClassnameView.setModel(self.ClassnameModel)
        # self.ClassnameView.setColumnHidden(0, True)
        # self.ClassnameView.show()
        self.ClassnameView.verticalHeader().setFixedWidth(30)
        self.ClassnameView.verticalHeader().setStyleSheet("color: red;font-size:20px; ");
        self.ClassnameView.setStyleSheet("QTableView{background-color: rgb(250, 250, 200, 0);"  
                    "alternate-background-color: rgb(141, 163, 0);}"
                    "QTableView::item:hover {background-color: rgba(100,200,220,100);} ") 
        self.ClassnameView.setStyleSheet("font-size:16px; ");
        self.ClassnameView.setSelectionMode(QAbstractItemView.SingleSelection)
        # self.ClassnameView.dataChanged.connect(self.dataChanged)

        # self.ClassnameView.setSizePolicy(QSizePolicy.Expanding,     QSizePolicy.Expanding)

        # the second list
        self.StudentView = QTableView()
        self.StudentModel = QSqlTableModel(self.StudentView)
        self.StudentModel.setTable("student")
        # self.StudentModel.setRelation(2, QSqlRelation("mentalmodel", "id", "name"));
        self.StudentModel.setEditStrategy(QSqlTableModel.OnManualSubmit)
        # self.StudentModel.select()

        query = QSqlQuery(self.db)
        strwhere = " 1=1 "
        if self.g_curClassName == "":
            ret = query.exec_("select classname from classtable")
            query.next()
            firstClassName = query.value(0)
            strwhere += " and classname like '" + firstClassName + "'"
            
        self.StudentModel.setFilter(strwhere)
        self.StudentModel.select()

        for indx, iheader in enumerate(["班级名称", "学生编号", "学生姓名", "答对次数", "答错次数"]):
            self.StudentModel.setHeaderData(indx+1, Qt.Horizontal, iheader)
    
        self.StudentView.setModel(self.StudentModel)
        self.StudentView.setColumnHidden(0, True)

        # query = QSqlQuery(self.db)  
        lstClassName = []      
        query.exec_("select classname from classtable" ) 
        while(query.next()):
            lstClassName.append(query.value(0))

        self.StudentView.setItemDelegateForColumn(1,  ComboBoxDelegate(self, lstClassName))
        # self.StudentView.show()
        self.StudentView.verticalHeader().setFixedWidth(30)
        self.StudentView.verticalHeader().setStyleSheet("color: red;font-size:20px; background-color: rgb(250, 250, 200, 100)");
        self.StudentView.setStyleSheet("QTableView{background-color: rgb(250, 250, 200, 0);"  
                    "alternate-background-color: rgb(141, 163, 250);}"
                    "QTableView::item:hover {background-color: rgba(10,200,100,200);} "
                    ) 
        self.StudentView.setStyleSheet("font-size:16px;")
        self.StudentView.setSelectionMode(QAbstractItemView.SingleSelection)

        btn_lst1_layout = QGridLayout()
        newusrbtn       = QPushButton("新增")
        savebtn         = QPushButton("保存")
        revertbtn       = QPushButton("撤销")
        removebtn       = QPushButton("删除")
        btn_lst1_layout.addWidget(newusrbtn, 0, 0)
        btn_lst1_layout.addWidget(savebtn, 0, 1)
        btn_lst1_layout.addWidget(revertbtn, 1, 0)
        btn_lst1_layout.addWidget(removebtn, 1, 1)

        newusrbtn.clicked.connect(self.newClass)
        savebtn.clicked.connect(self.saveClass)
        revertbtn.clicked.connect(self.revertClass)
        removebtn.clicked.connect(self.removeClass)

        self.ClassnameView.doubleClicked.connect(self.dbclick)
        

        btnbox2 = QDialogButtonBox(Qt.Horizontal)
        newusrbtn2       = QPushButton("新增")
        savebtn2         = QPushButton("保存")
        revertbtn2       = QPushButton("撤销")
        removebtn2       = QPushButton("删除")
        btnbox2.addButton(newusrbtn2, QDialogButtonBox.ActionRole);
        btnbox2.addButton(savebtn2, QDialogButtonBox.ActionRole);
        btnbox2.addButton(revertbtn2, QDialogButtonBox.ActionRole);
        btnbox2.addButton(removebtn2, QDialogButtonBox.ActionRole);

        newusrbtn2.clicked.connect(self.newStudent)
        savebtn2.clicked.connect(self.saveStudent)
        revertbtn2.clicked.connect(self.revertStudent)
        removebtn2.clicked.connect(self.removeStudent)

        # left list layout
        lst_layout_1 = QVBoxLayout()
        lst_layout_1.addWidget(self.ClassnameView)
        lst_layout_1.addLayout(btn_lst1_layout)

        lst_layout_2 = QVBoxLayout()
        lst_layout_2.addWidget(self.StudentView)
        lst_layout_2.addWidget(btnbox2)
        
        lstlayout = QHBoxLayout()
        lstlayout.setMargin(5)
        # lstlayout.addLayout(findbox)
        lstlayout.addLayout(lst_layout_1, 2)
        lstlayout.setMargin(5)
        lstlayout.addLayout(lst_layout_2, 5)
            
        labelClass = QLabel("")
        labelClass.setStyleSheet("background-color:rgba(255, 255, 255,0); color:rgba(0,0,0,0);")
        labelClass.setFixedHeight(40)
        # labelClass.setFixedWidth(100)
        # labelClass.setFont(QFont('宋体', 10))

        bottomlayout = QHBoxLayout()        
        bottomlayout.addWidget(labelClass)        

        tab2layout = QVBoxLayout()
        tab2layout.addLayout(titleLayout)       
        tab2layout.addLayout(lstlayout)
        tab2layout.addLayout(bottomlayout)
        self.w2.setLayout(tab2layout)
        self.w2.setStyleSheet("background-color: QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffffff, stop: 1 #228888);")
      
    def genOneTab(self):

        tabtitle = QLabel()
        # tabtitle.setFixedHeight(40)
        # tabtitle.setFixedWidth(160)        
        self.btn_start = MyButton("开始")
        self.choicenum_text = QComboBox()
        self.choicenum_text.setObjectName('w1combonums')
        # self.w1title.setStyleSheet("background-image:url('image/panelbg.jpg');")
        
        # Set the title style                
        tabtitle.setFont(QFont('Courier New', 20))
        tabtitle.setText("随堂提问演板")
        tabtitle.setStyleSheet("border: 1px solid blue; color:rgba(0,0,255, 220);\
            background-color:rgba(201,201,201,60);\
            border-radius: 6px; \
            padding: 1px 18px 1px 20px;\
            min-width: 8em;")
        tabtitle.setMinimumHeight(50);
        titleLayout = QHBoxLayout()
        titleLayout.addWidget(tabtitle)
        titleLayout.setAlignment(tabtitle, Qt.AlignCenter)
       
        btnlayout = QGridLayout()
        tmpnum = 0
        for inum in range(0,56):
            irow = tmpnum // g_cols
            icol = tmpnum % g_cols
            tmpnum += 1
            btnlayout.setRowMinimumHeight(irow, 80)
            tmpbtn = MyButton("")
            tmpbtn.setMyarg(None)
            # tmpbtn.setFixedHeight(20)
            tmpbtn.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding))
            tmpbtn.setStyleSheet("border: 1px solid rgb(55,55,255,100);background-color: rgba(255,255,255,20);font-size:16px;")
            self.connect(tmpbtn,  SIGNAL("myslot(PyQt_PyObject)"), self.myslot)
            tmpbtn.setAutoDefault(False)
            self.btngroup.addButton(tmpbtn, inum+1) # stusn is from 1 start

            btnlayout.addWidget(tmpbtn, irow, icol)


        self.btn_start.setIcon(QIcon("image/start.png"))
        self.btn_start.setStyleSheet("border: 1px solid yellow;")
        self.btn_start.setFixedHeight(40)
        self.btn_start.setFixedWidth(100)
        self.btn_start.setFont(QFont('宋体', 18))
        # self.choicenum_text.setFixedHeight(45)
        # self.choicenum_text.setFixedWidth(60)

        ## Set the combox number style
        self.choicenum_text.setFont(QFont('Courier New', 20))
        self.choicenum_text.setFixedHeight(45)
        self.choicenum_text.setStyleSheet("border: 2px solid blue; color:red;font-weight:light;font-size:26px;\
            border-radius: 6px; \
            min-width: 2em; ")
        self.choicenum_text.setEditable(True)
        self.choicenum_text.lineEdit().setReadOnly(True);
        self.choicenum_text.lineEdit().setAlignment(Qt.AlignCenter);

        model = self.choicenum_text.model()
        for row in list(range(1, 7)):
            item = QStandardItem(str(row))
            item.setTextAlignment(Qt.AlignCenter)
            item.setForeground(QColor('red'))
            item.setBackground(QColor(0,200,50, 130))
            model.appendRow(item)
        self.choicenum_text.setCurrentIndex(2)
        # self.choicenum_text.setStyleSheet ("QComboBox::drop-down {border-width: 100px;}")
        # self.choicenum_text.setStyleSheet ("QComboBox::down-arrow {image: url(image/downarrow.png);top: 10px;left: 1px;}")

        bottomlayout = QHBoxLayout()
        bottomlayout.setSizeConstraint(QLayout.SetFixedSize)
        bottomlayout.addStretch(10)
        bottomlayout.addWidget(self.btn_start)
        bottomlayout.setSpacing(5)
        bottomlayout.addWidget(self.choicenum_text)

        tab1layout = QVBoxLayout()
        tab1layout.addLayout(titleLayout)       
        tab1layout.addLayout(btnlayout)
        tab1layout.addLayout(bottomlayout)
                
        self.w1.setLayout(tab1layout)
        self.w1.setStyleSheet("background-color: QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffffff, stop: 1 #228888);")
         
    def startChoice(self, usernum="", oldbtn=""): 
        # print(oldbtn, 1)

        if oldbtn == "":
            self.dict_choices = {}

        strwhere = " and classname like '" + self.g_curClassName + "'"

        allstudent = []
        lstrecord = []
        query = QSqlQuery(self.db)        
        query.exec_("select stusn from tmprecord where 1=1 " + strwhere) 
        while(query.next()):
            lstrecord.append(query.value(0))
        # print(lstrecord, 'record', "select stusn from student where stusn not in " + str(tuple(lstrecord)))

        query.exec_("select stusn from student where stusn not in " + str(tuple(lstrecord)) + strwhere)
        while(query.next()):
            allstudent.append(query.value(0))

        if usernum == "":
            nums = int(self.choicenum_text.currentText())
        else:
            nums = usernum
        if nums >= len(allstudent):
            query.exec_("delete from tmprecord where 1=1 " + strwhere) #delete tmp date no today            
            allstudent = []
            query.exec_("select stusn from student where 1=1 " + strwhere)
            while(query.next()):
                allstudent.append(query.value(0))
        
        if oldbtn == "":
            random.seed()
            lstchoices = random.sample(allstudent, nums)
            for ibtn in lstchoices:
                self.dict_choices[ibtn] = "111"

            self.group_animation.start()
            QTimer.singleShot(1200, self.stopmovie)
        else:
            random.seed()
            otherbtn = random.sample(allstudent, 1)[0]
            # self.btngroup.button(int(otherbtn)).setFocus()
            self.dict_choices.pop(oldbtn)
            self.dict_choices[otherbtn] = '111'
            self.stopmovie()
        self.btnSysMenu.setFocus()

    def stopmovie(self):
        self.group_animation.stop()
        for isn in self.studentSnlst:
            # print(isn)
            self.btngroup.button(int(isn[0])).setStyleSheet(stylesheetstr_old)
            self.btngroup.button(int(isn[0])).setIcon(QIcon())
        
        classname = self.tabWidget.tabText(0)
        query = QSqlQuery(self.db)        
        today = datetime.date.today()
        for ibtn in self.dict_choices:
            self.btngroup.button(int(ibtn)).setStyleSheet(stylesheetstr_new)
            query.exec_("select count(*) from tmprecord where stusn='" + str(ibtn) + "'")
            query.next()
            if query.value(0) == 0:               
                query.prepare("insert into tmprecord (classname, stusn, datequestion) values (:classname, :stusn, :datequestion)")
                query.bindValue(":classname", classname)
                query.bindValue(":stusn", ibtn)
                query.bindValue(":datequestion", today)
                query.exec_()
    
    def answerRight(self):
        # print(self.g_curbtn)
        value = self.g_curbtn
        if value not in self.dict_choices:
            return

        self.btngroup.button(int(value)).setIcon(QIcon("image/smile.png"))
        self.btngroup.button(int(value)).setIconSize(QSize(20,20))
        
        query = QSqlQuery(self.db)
        query.exec_("select rightquestions from student where stusn='" + value + "'")
        query.next()
        studentRightQuestions = query.value(0) + 1
        query.exec_("update student set rightquestions=" + str(studentRightQuestions) + " where stusn='" + value + "'")
                
        ###########
        if self.dict_choices[value] == "101":
            query.exec_("select wrongquestions from student where stusn='" + value + "'")
            query.next()
            studentWrongQuestions = query.value(0) - 1
            query.exec_("update student set wrongquestions=" + str(studentWrongQuestions) + " where stusn='" + value + "'")
            
        self.dict_choices[value] = "011"

    def answerWrong(self):
        value = self.g_curbtn
        if value not in self.dict_choices:
            return

        self.btngroup.button(int(value)).setIcon(QIcon("image/cry.png"))
        self.btngroup.button(int(value)).setIconSize(QSize(20,20))
        # self.btngroup.button(int(value)).setStyleSheet("border-image: url(image/ex_stu.png);")
        
        query = QSqlQuery(self.db)
        query.exec_("select wrongquestions from student where stusn='" + value + "'")
        query.next()
        studentWrongQuestions = query.value(0) + 1
        query.exec_("update student set wrongquestions=" + str(studentWrongQuestions) + " where stusn='" + value + "'")
        
        if self.dict_choices[value] == "011":
            query.exec_("select rightquestions from student where stusn='" + value + "'")
            query.next()
            studentRightQuestions = query.value(0) - 1
            query.exec_("update student set rightquestions=" + str(studentRightQuestions) + " where stusn='" + value + "'")
            
        self.dict_choices[value] = "101"

    def resetStudent(self):
        value = self.g_curbtn
        if value not in self.dict_choices:
            return

        query = QSqlQuery(self.db)

        if self.dict_choices[value] == "011":        
            query.exec_("select rightquestions from student where stusn='" + value + "'")
            query.next()
            studentRightQuestions = query.value(0) - 1
            query.exec_("update student set rightquestions=" + str(studentRightQuestions) + " where stusn='" + value + "'")

        if self.dict_choices[value] == "101":
            query.exec_("select wrongquestions from student where stusn='" + value + "'")
            query.next()
            studentWrongQuestions = query.value(0) - 1
            query.exec_("update student set wrongquestions=" + str(studentWrongQuestions) + " where stusn='" + value + "'")
            
        self.startChoice(usernum=1, oldbtn=value)
        # print("---reset___")

        # curmenu.actions()[0].setEnabled(True)
        # curmenu.actions()[1].setEnabled(True)
        # self.choiceOneStudent(value)

    def createDb(self):
        conn = sqlite3.connect("studentNew.db") 
        cur = conn.cursor()
        sqlstr = 'create table student (id integer primary key, \
            classname varchar(20), \
            stusn varchar(20), \
            stuname varchar(20), \
            rightquestions integer, \
            wrongquestions integer, \
            FOREIGN KEY(classname) REFERENCES classtable(classname))'
        # print(sqlstr)

        sqlstr2 = 'create table tmprecord (id integer primary key, \
            classname varchar(20), \
            stusn varchar(20), \
            datequestion date)'

        sqlstr3 = 'create table classtable (classname varchar(20) PRIMARY KEY)'
        
        cur.execute(sqlstr3)
        conn.commit()
        cur.execute(sqlstr2)
        conn.commit()
        cur.execute(sqlstr)
        conn.commit()

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
        strsql = "insert into classtable values (?)"
        cur.execute(strsql, ("三（3）班",))
        conn.commit()
        cur.execute(strsql, ("三（4）班",))
        conn.commit()


        a03lst = ["曾忆谊","赵佳泉","翁文秀","林珑","郑铭洁","林泽思","吴崇霖","陈思嘉","欧阳月孜","郭展羽","詹伟哲","黄佳仪","杨秋霞","周奕子","林楚杰","欧伊涵","许腾誉","陈唯凯","陈树凯","林彦君","张钰佳","高锴","杨博凯","林妙菲","林楚鸿","陈展烯","姚静茵","吴欣桐","范思杰","肖佳","马思广","许一帆","姚奕帆","陈海珣","吴黛莹","吴育桐","肖凯帆","林欣阳","叶茂霖","姚楷臻","陈嘉豪","陈琦","杨子楷","陈炎宏","陈幸仪","杨景畅","罗暖婷","郑馨"]
        a04lst = ["罗恩琪","王可","曾祥威","谢濡婷","温嘉凯","许洁仪","肖欣淇","陈凯佳","林天倩","李乐海","吴文慧","黄文婷","万誉","陈进盛","张裕涵","陈振嘉","王巧玲","林珮琪","陈炜楷","杨健","赵泽锴","张凤临","蔡子丹","陈烨杰","廖妍希","林树超","夏培轩","陈锦森","李星","蔡依婷","姚容创","姚凯扬","沈嘉克","周凡","张玉川","邱金迅","陈菲敏","陈星翰","朱煜楷","郑泽洪","钱剑非","罗奕丰","陈杜炜","林知钦"]
        strsql = "insert into student values (?, ?, ?, ?,?,?)" 
        for i in list(range(0,len(a03lst))):
            cur.execute(strsql, (None, "三（3）班", str(i+1).zfill(2), a03lst[i], 0, 0))
            conn.commit()
        strsql = "insert into student values (?, ?, ?, ?,?,?)" 
        for i in list(range(0,len(a04lst))):
            cur.execute(strsql, (None, "三（4）班", str(i+1).zfill(2), a04lst[i], 0, 0))
            conn.commit()
        cur.close()
        
if __name__ == "__main__":    
    import sys
    app=QApplication(sys.argv)
    dialog=QuestionDlg()
    dialog.show()
    app.exec_()