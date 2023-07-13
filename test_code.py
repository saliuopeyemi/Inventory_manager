from PyQt5.QtWidgets import QSplashScreen,QApplication,QMainWindow,QLabel
from PyQt5.QtGui import QPixmap
import time

app = QApplication([])

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.msgs=["Initializing storage objects","Updating json files","Creating an update menu","Creating user interfaces"]
        self.pix = QPixmap("icon.png")
        self.lbl =  QSplashScreen(self.pix)
        self.lbl.show()
        for i in self.msgs:
            self.lbl.showMessage(f"<font color=Gold size=4><b>{i}</b></font>")
            time.sleep(4)
        self.lbl.close()

smtin=Main()

app.exec()