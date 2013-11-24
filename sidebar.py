#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from PyQt4 import QtCore
from PyQt4 import QtGui

from widget import Button, Viewer
from colorPicker import ColorDialog

class PaletteCanvas(QtGui.QWidget):
    """ Canvas where the palette is draw """
    def __init__(self, parent):
        QtGui.QWidget.__init__(self)
        self.parent = parent
        self.setFixedSize(164, 644)
        self.background = QtGui.QBrush(self.parent.project.bgColor)
        self.black = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        self.white = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        self.parent.project.updateBackgroundSign.connect(self.updateBackground)
        
    def updateBackground(self):
         self.background = QtGui.QBrush(self.parent.project.bgColor)
         self.update()
         
    def paintEvent(self, ev=''):
        p = QtGui.QPainter(self)
        p.fillRect (0, 0, self.width(), self.height(), self.background)
        for n, i in enumerate(self.parent.project.colorTable):
            if n > 0:
                y = (((n-1) // 8) * 20) + 2
                x = (((n-1) % 8) * 20) + 2
                if n == self.parent.project.color:
                    p.fillRect (x, y, 20, 20, self.black)
                    p.fillRect (x+1, y+1, 18, 18, self.white)
                p.fillRect(x+2, y+2, 16, 16, QtGui.QBrush(QtGui.QColor().fromRgba(i)))

    def event(self, event):
        if (event.type() == QtCore.QEvent.MouseButtonPress and
                       event.button()==QtCore.Qt.LeftButton):
            item = self.getItem(event.x(), event.y())
            if item is not None:
                self.parent.project.changeColor(item)
        elif (event.type() == QtCore.QEvent.MouseButtonDblClick and
                       event.button()==QtCore.Qt.LeftButton):
            item = self.getItem(event.x(), event.y())
            if item is not None:
                self.parent.editColor(item)
        return QtGui.QWidget.event(self, event)
        
    def getItem(self, x, y):
        x, y = ((x-2) // 20), ((y-2) // 20)
        if y == 0:
            s = x + 1
        else:
            s = (y * 8) + x + 1
        if s >= 0 and s < len(self.parent.project.colorTable):
            return s
        return None


class ColorWidget(QtGui.QWidget):
    """ widget for alpha and current color, select on clic"""
    def __init__(self, color, parent):
        QtGui.QWidget.__init__(self)
        self.parent = parent
        self.setFixedSize(26, 26)
        self.background = QtGui.QBrush(self.parent.project.bgColor)
        self.alpha = QtGui.QPixmap("icons/color_alpha.png")
        self.parent.project.updateBackgroundSign.connect(self.updateBackground)
        self.color = color
        self.parent.project.updatePaletteSign.connect(self.update)
        if color:
            self.setToolTip("current color (E)")
        else:
            self.setToolTip("alpha color (E)")
        
    def updateBackground(self):
         self.background = QtGui.QBrush(self.parent.project.bgColor)
         self.update()

    def event(self, event):
        if (event.type() == QtCore.QEvent.MouseButtonPress and
                       event.button()==QtCore.Qt.LeftButton):
            if self.color:
                self.parent.project.changeColor(self.parent.project.currentColor)
            else:
                self.parent.project.changeColor(0)
        elif event.type() == QtCore.QEvent.Paint:
            col, cur = self.parent.project.color, self.parent.project.currentColor
            p = QtGui.QPainter(self)
            p.fillRect (0, 0, self.width(), self.height(), 
                    QtGui.QBrush(QtGui.QColor(70, 70, 70)))
            p.fillRect (1, 1, self.width()-2, self.height()-2, self.background)
            if ((not self.color and self.parent.project.color == 0)
                or (self.color and col == cur)):
                p.fillRect (3, 3, 20, 20, QtGui.QBrush(QtGui.QColor(0, 0, 0)))
                p.fillRect (4, 4, 18, 18, QtGui.QBrush(QtGui.QColor(255, 255, 255)))
            if self.color:
                p.fillRect(5, 5, 16, 16, QtGui.QBrush(
                    QtGui.QColor().fromRgba(self.parent.project.colorTable[self.parent.project.currentColor])))
            else:
                p.drawPixmap(5, 5, self.alpha)
                # just to be sure alpha is the first color
                p.fillRect(5, 5, 16, 16, QtGui.QBrush(
                    QtGui.QColor().fromRgba(self.parent.project.colorTable[0])))
        return QtGui.QWidget.event(self, event)

    
class PenWidget(QtGui.QWidget):
    """ widget for pen, menu on clic """
    def __init__(self, parent, project):
        QtGui.QWidget.__init__(self)
        self.parent = parent
        self.project = project
        self.setToolTip("pen")
        self.setFixedSize(26, 26)
        self.project.updateBackgroundSign.connect(self.update)
        self.penMenu = QtGui.QMenu(self)
        self.currentAction = None
        self.loadPen()
        self.project.customPenSign.connect(self.setCustomPen)

    def loadPen(self):
        self.penMenu.clear()
        for name, icon in self.project.penList:
            action = QtGui.QAction(QtGui.QIcon(icon), name, self)
            action.pixmap = icon
            action.setIconVisibleInMenu(True)
            self.penMenu.addAction(action)
            if not self.currentAction:
                self.currentAction = action

    def event(self, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            self.changePen()
        elif event.type() == QtCore.QEvent.Paint:
            p = QtGui.QPainter(self)
            p.fillRect (0, 0, self.width(), self.height(), 
                    QtGui.QBrush(QtGui.QColor(70, 70, 70)))
            p.fillRect (1, 1, self.width()-2, self.height()-2, 
                    QtGui.QBrush(self.project.bgColor))
            if self.currentAction.pixmap:
                p.drawPixmap(5, 5, self.currentAction.pixmap)
        return QtGui.QWidget.event(self, event)
        
    def changePen(self):
        self.penMenu.setActiveAction(self.currentAction)
        action = self.penMenu.exec(self.mapToGlobal(QtCore.QPoint(26, 2)), self.currentAction)
        if action:
            self.currentAction = action
            self.project.pen = self.project.penDict[action.text()]
            self.project.penChangedSign.emit()
            self.update()
        
    def setCustomPen(self, li):
        nLi = []
        mY = len(li)//2
        mX = len(li[0])//2
        for y in range(len(li)):
            py = y - mY
            for x in range(len(li[y])):
                col = li[y][x]
                if col:
                    px = x - mX
                    nLi.append((px, py, col))
        if nLi:
            self.project.penDict["custom"] = nLi
            self.project.pen = self.project.penDict["custom"]
            self.icon = None
            self.update()
            self.project.penChangedSign.emit()
            self.parent.penClicked()


class BrushWidget(QtGui.QWidget):
    """ widget for brush, menu on clic """
    def __init__(self, parent, project):
        QtGui.QWidget.__init__(self)
        self.parent = parent
        self.project = project
        self.setToolTip("brush")
        self.setFixedSize(26, 26)
        self.project.updateBackgroundSign.connect(self.update)
        self.brushMenu = QtGui.QMenu(self)
        self.currentAction = None
        self.loadBrush()

    def loadBrush(self):
        self.brushMenu.clear()
        for name, icon in self.project.brushList:
            action = QtGui.QAction(QtGui.QIcon(icon), name, self)
            action.pixmap = icon
            action.setIconVisibleInMenu(True)
            self.brushMenu.addAction(action)
            if name == "solid":
                self.currentAction = action

    def event(self, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            self.changeBrush()
        elif event.type() == QtCore.QEvent.Paint:
            p = QtGui.QPainter(self)
            p.fillRect (0, 0, self.width(), self.height(), 
                    QtGui.QBrush(QtGui.QColor(70, 70, 70)))
            p.fillRect (1, 1, self.width()-2, self.height()-2, 
                    QtGui.QBrush(self.project.bgColor))
            if self.currentAction.pixmap:
                p.drawPixmap(5, 5, self.currentAction.pixmap)
        return QtGui.QWidget.event(self, event)
        
    def changeBrush(self):
        self.brushMenu.setActiveAction(self.currentAction)
        action = self.brushMenu.exec(self.mapToGlobal(QtCore.QPoint(26, 2)), self.currentAction)
        if action:
            self.currentAction = action
            self.project.brush = self.project.brushDict[action.text()]
            self.update()

            
class OptionFill(QtGui.QWidget):
    """ contextual option for the fill tool """
    def __init__(self, parent, project):
        QtGui.QVBoxLayout .__init__(self)
        self.project = project
        self.parent = parent
        
        self.adjacentFillRadio = QtGui.QRadioButton("adjacent colors", self)
        self.adjacentFillRadio.pressed.connect(self.adjacentPressed)
        self.adjacentFillRadio.setChecked(True)
        self.similarFillRadio = QtGui.QRadioButton("similar colors", self)
        self.similarFillRadio.pressed.connect(self.similarPressed)
        
        ### Layout ###
        layout = QtGui.QVBoxLayout()
        layout.setSpacing(0)
        layout.addWidget(self.adjacentFillRadio)
        layout.addWidget(self.similarFillRadio)
        layout.addStretch()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        
    def adjacentPressed(self):
        self.project.fillMode = "adjacent"
        
    def similarPressed(self):
        self.project.fillMode = "similar"
        
        
class OptionSelect(QtGui.QWidget):
    """ contextual option for the select tool """
    def __init__(self, parent, project):
        QtGui.QVBoxLayout .__init__(self)
        self.project = project
        
        self.cutFillRadio = QtGui.QRadioButton("cut", self)
        self.cutFillRadio.pressed.connect(self.cutPressed)
        self.cutFillRadio.setChecked(True)
        self.copyFillRadio = QtGui.QRadioButton("copy", self)
        self.copyFillRadio.pressed.connect(self.copyPressed)
        
        ### Layout ###
        layout = QtGui.QVBoxLayout()
        layout.setSpacing(0)
        layout.addWidget(self.cutFillRadio)
        layout.addWidget(self.copyFillRadio)
        layout.addStretch()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        
    def cutPressed(self):
        self.project.selectMode = "cut"
    
    def copyPressed(self):
        self.project.selectMode = "copy"
        
class PaletteWidget(QtGui.QWidget):
    """ side widget containing palette """
    def __init__(self, project):
        QtGui.QWidget.__init__(self)
        self.project = project

        ### palette ###
        self.paletteCanvas = PaletteCanvas(self)
        self.paletteV = Viewer()
        self.paletteV.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.paletteV.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.paletteV.setWidget(self.paletteCanvas)
        
        self.project.updatePaletteSign.connect(self.paletteCanvas.update)
        addColorB = Button("add color",
            "icons/color_add.png", self.addColor)
        delColorB = Button("delete color",
            "icons/color_del.png", self.delColor)
        moveLeftColorB = Button("move color left",
            "icons/color_move_left.png", self.moveColorLeft)
        moveRightColorB = Button("move color right",
            "icons/color_move_right.png", self.moveColorRight)

        ### Layout ###
        colorButtons = QtGui.QHBoxLayout()
        colorButtons.setSpacing(0)
        colorButtons.addWidget(addColorB)
        colorButtons.addWidget(delColorB)
        colorButtons.addWidget(moveLeftColorB)
        colorButtons.addWidget(moveRightColorB)
        self.layout = QtGui.QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.addWidget(self.paletteV)
        self.layout.addLayout(colorButtons)
        self.layout.setContentsMargins(6, 0, 6, 0)
        self.setLayout(self.layout)

    def showEvent(self, event):
        self.paletteV.setFixedWidth(self.paletteCanvas.width() + 
                    self.paletteV.verticalScrollBar().width() + 2)

    ######## Color #####################################################
    def editColor(self, n):
        col = self.project.colorTable[self.project.color]
        ok, color = ColorDialog(False, col).getRgba()
        if not ok:
            return
        self.project.saveToUndo("colorTable")
        self.project.colorTable[n] = color
        for i in self.project.timeline.getAllCanvas():
            i.setColorTable(self.project.colorTable)
        self.project.updateViewSign.emit()
        self.paletteCanvas.update()
        self.project.colorChangedSign.emit()

    def addColor(self):
        """ select a color and add it to the palette"""
        if not len(self.project.colorTable) >= 256:
            col = self.project.colorTable[self.project.color]
            ok, color = ColorDialog(False, col).getRgba()
            if not ok:
                return
            self.project.saveToUndo("colorTable_frames")
            self.project.colorTable.append(color)
            self.project.changeColor(len(self.project.colorTable)-1)
            for i in self.project.timeline.getAllCanvas():
                i.setColorTable(self.project.colorTable)
            self.project.updateViewSign.emit()

    def delColor(self):
        col, table = self.project.color, self.project.colorTable
        if col != 0:
            self.project.saveToUndo("colorTable_frames")
            table.pop(col)
            for i in self.project.timeline.getAllCanvas():
                i.delColor(col)
                i.setColorTable(table)
            self.project.changeColor(col-1)
            self.project.updateViewSign.emit()

    def moveColorLeft(self):
        col, table = self.project.color, self.project.colorTable
        if col != 0 and col != 1:
            self.project.saveToUndo("colorTable_frames")
            table[col], table[col-1] = table[col-1], table[col]
            for i in self.project.timeline.getAllCanvas():
                i.swapColor(col, col-1)
                i.setColorTable(table)
            self.project.changeColor(col-1)

    def moveColorRight(self):
        col, table = self.project.color, self.project.colorTable
        if col != len(table)-1 and col != 0:
            self.project.saveToUndo("colorTable_frames")
            table[col], table[col+1] = table[col+1], table[col]
            for i in self.project.timeline.getAllCanvas():
                i.swapColor(col, col+1)
                i.setColorTable(table)
            self.project.changeColor(col+1)

class OptionsWidget(QtGui.QWidget):
    """ side widget cantaining options """
    def __init__(self, project):
        QtGui.QWidget.__init__(self)
        self.project = project

        self.penWidget = PenWidget(self, self.project)
        self.brushWidget = BrushWidget(self, self.project)
        self.alphaWidget = ColorWidget(False, self)
        self.colorWidget = ColorWidget(True, self)
        
        self.optionFill = OptionFill(self, self.project)
        self.optionSelect = OptionSelect(self, self.project)
        self.project.toolChangedSign.connect(self.toolChanged)

        ### Layout ###
        context = QtGui.QHBoxLayout()
        context.setSpacing(8)
        context.addWidget(self.alphaWidget)
        context.addWidget(self.colorWidget)
        context.addStretch()
        context.addWidget(self.penWidget)
        context.addWidget(self.brushWidget)
        context.setContentsMargins(0, 0, 0, 0)
        layout = QtGui.QVBoxLayout()
        layout.setSpacing(4)
        layout.addLayout(context)
        layout.addWidget(self.optionFill)
        self.optionFill.hide()
        layout.addWidget(self.optionSelect)
        self.optionSelect.hide()
        layout.addStretch()
        
        self.setLayout(layout)
        
    def toolChanged(self):
        if self.project.tool == "fill":
            self.optionSelect.hide()
            self.optionFill.show()
        elif self.project.tool == "select":
            self.optionFill.hide()
            self.optionSelect.show()
        else:
            self.optionFill.hide()
            self.optionSelect.hide()
            
        
class ToolsWidget(QtGui.QWidget):
    """ side widget cantaining tools buttons """
    def __init__(self, project):
        QtGui.QWidget.__init__(self)
        self.project = project

        ### tools buttons ###
        self.penB = Button("pen (1)", "icons/tool_pen.png", self.penClicked, True)
        self.penB.setChecked(True)
        self.pipetteB = Button("pipette (2)", "icons/tool_pipette.png", self.pipetteClicked, True)
        self.fillB = Button("fill (3)", "icons/tool_fill.png", self.fillClicked, True)
        self.moveB = Button("move (4)", "icons/tool_move.png", self.moveClicked, True)
        self.selectB = Button("select (5)", "icons/tool_select.png", self.selectClicked, True)

        ### Layout ###
        layout = QtGui.QVBoxLayout()
        layout.setSpacing(0)
        layout.addWidget(self.penB)
        layout.addWidget(self.pipetteB)
        layout.addWidget(self.fillB)
        layout.addWidget(self.moveB)
        layout.addWidget(self.selectB)
        layout.addStretch()
        layout.setContentsMargins(6, 0, 6, 0)
        self.setLayout(layout)
        
    ######## Tools #####################################################
    def penClicked(self):
        self.project.tool = "pen"
        self.penB.setChecked(True)
        self.pipetteB.setChecked(False)
        self.fillB.setChecked(False)
        self.moveB.setChecked(False)
        self.selectB.setChecked(False)
        self.project.toolChangedSign.emit()

    def pipetteClicked(self):
        self.project.tool = "pipette"
        self.penB.setChecked(False)
        self.fillB.setChecked(False)
        self.pipetteB.setChecked(True)
        self.moveB.setChecked(False)
        self.selectB.setChecked(False)
        self.project.toolChangedSign.emit()

    def fillClicked(self):
        self.project.tool = "fill"
        self.fillB.setChecked(True)
        self.pipetteB.setChecked(False)
        self.penB.setChecked(False)
        self.moveB.setChecked(False)
        self.selectB.setChecked(False)
        self.project.toolChangedSign.emit()

    def moveClicked(self):
        self.project.tool = "move"
        self.fillB.setChecked(False)
        self.pipetteB.setChecked(False)
        self.penB.setChecked(False)
        self.moveB.setChecked(True)
        self.selectB.setChecked(False)
        self.project.toolChangedSign.emit()
        
    def selectClicked(self):
        self.project.tool = "select"
        self.fillB.setChecked(False)
        self.pipetteB.setChecked(False)
        self.penB.setChecked(False)
        self.moveB.setChecked(False)
        self.selectB.setChecked(True)
        self.project.toolChangedSign.emit()
