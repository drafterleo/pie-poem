# pyuic4 markupform.ui >> ui_markupform.py

import sys
from PyQt4 import QtGui
from ui_markupform import Ui_MarkupForm
import data_model


class Window(QtGui.QWidget, Ui_MarkupForm):
    pmodel = {}
    curr_idx = 0

    def __init__(self):
        super(Window, self).__init__()
        Ui_MarkupForm.__init__(self)
        self.setupUi(self)
        self.setGeometry(50, 50, 500, 300)
        self.setWindowTitle("Markup")

        self.loadModelBtn.clicked.connect(self.loadModel)
        self.saveModelBtn.clicked.connect(self.saveModel)
        self.poemNumSpin.valueChanged[str].connect(self.poemSpinValueChanged)
        self.nextPoemBtn.clicked.connect(self.nextPoem)
        self.prevPoemBtn.clicked.connect(self.prevPoem)

    def poemCount(self):
        return len(self.pmodel['poems'])

    def poemByIdx(self, idx):
        return self.pmodel['poems'][idx]

    def rateByIdx(self, idx):
        return self.pmodel['rate'][idx]

    def setPoemByIdx(self, idx):
        self.poemLabel.setText(self.poemByIdx(idx))

    def loadModel(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open Model', '')
        self.modelFileNameLabel.setText(fname)
        self.pmodel = data_model.read_data_model(fname)
        if not ('rate' in self.pmodel.keys()):
            self.pmodel['rate'] = [0.0 for _ in range(self.poemCount())]
        self.curr_idx = 0
        self.poemNumSpin.setMinimum(1)
        self.poemNumSpin.setMaximum(self.poemCount())
        self.poemNumSpin.setValue(1)

    def saveModel(self):
        fname = QtGui.QFileDialog.getSaveFileName(self, 'Save Model', '')
        data_model.write_data_model(fname, self.pmodel)
        self.modelFileNameLabel.setText(fname)
        return

    def poemSpinValueChanged(self, val):
        self.pmodel['rate'][self.curr_idx] = self.rateSlider.value() / self.rateSlider.maximum()
        self.curr_idx = self.poemNumSpin.value() - 1
        self.setPoemByIdx(self.curr_idx)
        self.rateSlider.setValue(self.rateByIdx(self.curr_idx) * self.rateSlider.maximum())

    def nextPoem(self):
        self.poemNumSpin.stepUp()

    def prevPoem(self):
        self.poemNumSpin.stepDown()


def main():
    app = QtGui.QApplication(sys.argv)
    gui = Window()
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

