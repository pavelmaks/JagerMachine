import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout
from PyQt5.QtGui import QPixmap

class App(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def initUI(self):
         hbox = QHBoxLayout(self)
         
         pixmap = QPixmap('img1.png')
         
         lbl = QLabel(self)
         lbl.setPixmap(pixmap)
         
         hbox.addWidget(lbl)
         self.setLayout(hbox)
         
         self.setGeometry(300, 300, 300, 220)
         self.setWindowTitle('Test')
         self.show()
         
         
app = QApplication(sys.argv)
ex = App()
