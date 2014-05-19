from PyQt4.QtCore import Qt, QByteArray, QSize
from PyQt4.QtGui import QWidget, QApplication, QLabel, QMovie, QSizePolicy, QVBoxLayout, QHBoxLayout, QMenu,QPushButton, QIcon

class ImagePlayer(QWidget):
    def __init__(self, filename, title, parent=None):
        QWidget.__init__(self, parent)
 
        # Load the file into a QMovie
        self.movie = QMovie(filename, QByteArray(), self)
        print(filename)
 
        size = self.movie.scaledSize()
        self.setGeometry(200, 200, size.width(), size.height())
        self.setWindowTitle(title)
 
        self.movie_screen = QLabel()
        # Make label fit the gif
        self.movie_screen.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.movie_screen.setAlignment(Qt.AlignCenter)
        self.btn_ex = QPushButton()
        self.btn_ex.setFixedWidth(100)
        self.btn_ex.setFixedHeight(100)
        # self.btn_ex.setIcon(QIcon("image/ex_stu.gif"))
        self.btn_ex.setStyleSheet("background-color: rgba(255,255,255,20);")
        self.btn_ex.setIcon(QIcon("image/smile.png"))
        self.btn_ex.setIconSize(QSize(80,80))
        self.btn_ex.setFlat(True)

        popMenu = QMenu(self)
        entry1 = popMenu.addAction("正确")
        # self.connect(entry1,SIGNAL('triggered()'), lambda item=item[0]: self.answerRight(item))
        entry2 = popMenu.addAction("错误")
        # self.connect(entry2,SIGNAL('triggered()'), lambda item=item[0]: self.answerWrong(item))
        entry3 = popMenu.addAction("替换")
        # self.connect(entry3,SIGNAL('triggered()'), lambda item=item[0]: self.resetStudent(item))
        self.btn_ex.setMenu(popMenu)


 
        # Create the layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.movie_screen)
        # main_layout.addWidget(self.btn_ex)
 
        self.setLayout(main_layout)
 
        # Add the QMovie object to the label
        self.movie.setCacheMode(QMovie.CacheAll)
        # self.movie.setSpeed(100)
        self.movie_screen.setMovie(self.movie)
        self.movie_screen.setLayout(QHBoxLayout())
        self.movie_screen.layout().addWidget(self.btn_ex)

        popMenu = QMenu(self)
        entry1 = popMenu.addAction("正确")
        # self.movie_screen.setMenu(popMenu)

        self.movie.start()
        # self.movie.stop()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    l = ImagePlayer('image/ex_stu.gif', '学生')
    l.show()
    app.exec_()