import sys
from PyQt4 import QtGui

class Window(QtGui.QWidget):

    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50, 50, 500, 300)
        self.setWindowTitle("Markup")
        # self.setWindowIcon(QtGui.QIcon('pythonlogo.png'))

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.setBrush(QtGui.QColor(00, 00, 00))
        qp.drawRect(self.rect())
        qp.end()


def main():
    app = QtGui.QApplication(sys.argv)
    gui = Window()
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()