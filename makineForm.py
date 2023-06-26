from PyQt5 import QtWidgets
import sys
from makine1 import Ui_MainWindow

class Window(QtWidgets.QMainWindow):

    def hesapla(self):
        sender = self.sender().text()
        result = 0

        if sender == "Toplama":
            result = int(self.ui.ilksayi.text()) + int(self.ui.ikincisayi.text())
        elif sender == "Çıkarma":
            result = int(self.ui.ilksayi.text()) - int(self.ui.ikincisayi.text())
        elif sender == "Çarpma":
            result = int(self.ui.ilksayi.text()) * int(self.ui.ikincisayi.text())
        elif sender == "Bölme":
            result = int(self.ui.ilksayi.text()) / int(self.ui.ikincisayi.text())

        self.ui.sonuc_lbl.setText(str(result))

    def __init__(self):
        super(Window,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.bolme_btn.clicked.connect(self.hesapla)
        self.ui.carpma_btn.clicked.connect(self.hesapla)
        self.ui.cikarma_btn.clicked.connect(self.hesapla)
        self.ui.toplama_btn.clicked.connect(self.hesapla)


def app():
    app = QtWidgets.QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())
app()