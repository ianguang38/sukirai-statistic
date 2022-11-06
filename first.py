from db import server
import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication,QLineEdit,
                                QGridLayout,QWidget,QLabel,
                                QPushButton)
from PyQt5.QtCore import Qt

class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):      
        self.statusBar()

        self.qle1 = QLineEdit()
        self.qle2 = QLineEdit()
        self.qle1.setText("剣持刀也")
        self.qle2.setText("咎人")
        self.qle1.returnPressed.connect(self.next)
        self.qle2.returnPressed.connect(self.yes)
        self.rfb=QPushButton("refresh")
        self.rfb.clicked.connect(self.refresh)
        

        self.lbl = QLabel()

        self.layout_work()
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('Event sender')
        self.show()
        
        self.next()

    def yes(self):
        self.lbl.setText(self.qle2.text())
        ans=server.query(self.qle1.text(),self.qle2.text())
        # print(ans)
        s="\n".join([str(i['cid'])+i['comment'] for i in ans])
        self.lbl.setText(s)

    def next(self):
        self.qle2.setFocus()
    
    def refresh(self):
        server.fresh()
        

    def layout_work(self):
        central = QWidget()
        self.setCentralWidget(central)

        # self.lbl.setGeometry()

        grid = QGridLayout(central)
        grid.setSpacing(10)
        grid.addWidget(self.qle1, 0, 0)
        grid.addWidget(self.qle2, 0, 1)
        grid.addWidget(self.lbl, 2, 0, 1, 3)
        grid.addWidget(self.rfb, 1, 2 )
        
        

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())