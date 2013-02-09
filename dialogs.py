#!/usr/bin/env python
#-*- coding: utf-8 -*-

from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import Qt

class NewDialog(QtGui.QDialog):
    def __init__(self, w=64, h=64):
        QtGui.QDialog.__init__(self)
        self.setWindowTitle("new animation")

        ### instructions ###
        self.instL = QtGui.QLabel("Enter the size of the new animation :")
        ### width ###
        self.wL = QtGui.QLabel("width")
        self.wW = QtGui.QLineEdit(str(w), self)
        self.wW.setValidator(QtGui.QIntValidator(self.wW))
        ### height ###
        self.hL = QtGui.QLabel("height")
        self.hW = QtGui.QLineEdit(str(h), self)
        self.hW.setValidator(QtGui.QIntValidator(self.hW))
        ### error ###
        self.errorL = QtGui.QLabel("")
        ### apply, undo ###
        self.cancelW = QtGui.QPushButton('cancel', self)
        self.cancelW.clicked.connect(self.cancel_clicked)
        self.newW = QtGui.QPushButton('new', self)
        self.newW.clicked.connect(self.new_clicked)

        grid = QtGui.QGridLayout()
        grid.setSpacing(4)
        grid.addWidget(self.instL, 0, 0, 1, 2)
        grid.addWidget(self.wL, 1, 0)
        grid.addWidget(self.hL, 2, 0)
        grid.addWidget(self.wW, 1, 1)
        grid.addWidget(self.hW, 2, 1)
        grid.addWidget(self.errorL, 3, 0, 1, 2)

        okBox = QtGui.QHBoxLayout()
        okBox.addStretch(0)
        okBox.addWidget(self.cancelW)
        okBox.addWidget(self.newW)

        vBox = QtGui.QVBoxLayout()
        vBox.addLayout(grid)
        vBox.addStretch(0)
        vBox.addLayout(okBox)

        self.setLayout(vBox)
        self.exec_()

    def new_clicked(self):
        try:
            w = int(self.wW.text())
            h = int(self.hW.text())
        except ValueError:
            self.errorL.setText("ERROR : You must enter a number !")
            return
        if w > 0 and h > 0:
            self.w = w
            self.h = h
            self.accept()
        else:
            self.errorL.setText("ERROR : The size must be greater than 0 !")

    def cancel_clicked(self):
        self.reject()

    def get_return(self):
        if self.result():
            return True , self.w, self.h
        else:
            return False, None, None


class ResizeDialog(QtGui.QDialog):
    def __init__(self, size):
        QtGui.QDialog.__init__(self)
        self.setWindowTitle("resize animation")
        w, h = size[0], size[1]

        ### instructions ###
        self.wL = QtGui.QLabel("width")
        self.wL.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.hL = QtGui.QLabel("height")
        self.hL.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.actualSizeL = QtGui.QLabel("Actual size")
        self.actualSizeL.setAlignment(QtCore.Qt.AlignCenter)
        self.actualWL = QtGui.QLabel(str(w))
        self.actualHL = QtGui.QLabel(str(h))
        self.newSizeL = QtGui.QLabel("New size")
        self.newSizeL.setAlignment(QtCore.Qt.AlignCenter)
        self.newWW = QtGui.QLineEdit(str(w), self)
        self.newWW.setValidator(QtGui.QIntValidator(self.newWW))
        self.newHW = QtGui.QLineEdit(str(h), self)
        self.newHW.setValidator(QtGui.QIntValidator(self.newHW))
        ### offset ###
        self.offsetL = QtGui.QLabel("offset")
        self.offsetL.setAlignment(QtCore.Qt.AlignCenter)
        self.horizontalL = QtGui.QLabel("horizontal")
        self.horizontalL.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.horizontalOffsetW = QtGui.QLineEdit(str(0), self)
        self.horizontalOffsetW.setValidator(QtGui.QIntValidator(self.horizontalOffsetW))
        self.verticalL = QtGui.QLabel("vertical")
        self.verticalL.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.verticalOffsetW = QtGui.QLineEdit(str(0), self)
        self.verticalOffsetW.setValidator(QtGui.QIntValidator(self.verticalOffsetW))

        ### error ###
        self.errorL = QtGui.QLabel("")
        ### apply, undo ###
        self.cancelW = QtGui.QPushButton('cancel', self)
        self.cancelW.clicked.connect(self.cancel_clicked)
        self.resizeW = QtGui.QPushButton('resize', self)
        self.resizeW.clicked.connect(self.resize_clicked)

        grid = QtGui.QGridLayout()
        grid.setSpacing(8)
        grid.addWidget(self.wL, 1, 0)
        grid.addWidget(self.hL, 2, 0)

        grid.addWidget(self.actualSizeL, 0, 1)
        grid.addWidget(self.actualWL, 1, 1)
        grid.addWidget(self.actualHL, 2, 1)

        grid.addWidget(self.newSizeL, 0, 2)
        grid.addWidget(self.newWW, 1, 2)
        grid.addWidget(self.newHW, 2, 2)

        grid.addWidget(self.offsetL, 3, 2)

        grid.addWidget(self.horizontalL, 4, 1)
        grid.addWidget(self.verticalL, 5, 1)
        grid.addWidget(self.horizontalOffsetW, 4, 2)
        grid.addWidget(self.verticalOffsetW, 5, 2)

        grid.addWidget(self.errorL, 6, 0, 1, 3)

        okBox = QtGui.QHBoxLayout()
        okBox.addStretch(0)
        okBox.addWidget(self.cancelW)
        okBox.addWidget(self.resizeW)

        vBox = QtGui.QVBoxLayout()
        vBox.addLayout(grid)
        vBox.addStretch(0)
        vBox.addLayout(okBox)

        self.setLayout(vBox)
        self.exec_()

    def resize_clicked(self):
        try:
            w = int(self.newWW.text())
            h = int(self.newHW.text())
        except ValueError:
            self.errorL.setText("ERROR : You must enter a number !")
            return
        try:
            wOffset = int(self.horizontalOffsetW.text())
        except ValueError:
            wOffset = 0
        try:
            hOffset = int(self.verticalOffsetW.text())
        except ValueError:
            hOffset = 0

        if w > 0 and h > 0:
            self.w = w
            self.h = h
            self.wOffset = wOffset
            self.hOffset = hOffset
            self.accept()
        else:
            self.errorL.setText("ERROR : The size must be greater than 0 !")

    def cancel_clicked(self):
        self.reject()

    def get_return(self):
        if self.result():
            return True , (self.w, self.h), (self.wOffset, self.hOffset)
        else:
            return False, None, None