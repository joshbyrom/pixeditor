#!/usr/bin/env python
#-*- coding: utf-8 -*-

from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import Qt
import os
import xml.etree.ElementTree as ET

def open_pix(url=None):
    if not url:
        url = QtGui.QFileDialog.getOpenFileName(None, "open pix file", "", "Pix files (*.pix );;All files (*)")
    if url:
        try:
            save = open(url, "r")
            size, colors, frames = return_canvas(save)
            save.close()
            return size, colors, frames
        except IOError:
            print "Can't open file"
            return False, False, False
        return False, False, False
        
def return_canvas(save):
    pix = ET.parse(save).getroot()
    xSize = pix.find("size").attrib
    size = (int(xSize["width"]), int(xSize["height"]))
    print size
    xColors = pix.find("colors").text
    colors = [int(n) for n in xColors.split(',')]
    print colors
    xFrames = pix.find("frames")
    frames = []
    for i in xFrames.itertext():
        if i == "0":
            frames.append(False)
        else:
            frames.append([int(n) for n in i.split(',')])
    print frames
    return size, colors, frames
    
def open_old_pix(url=None):
    if not url:
        url = QtGui.QFileDialog.getOpenFileName(None, "open pix file", "", "Pix files (*.pix );;All files (*)")
    if url:
        try:
            save = open(url, "r")
            size, colors, frames = return_old_canvas(save)
            save.close()
            return size, colors, frames
        except IOError:
            print "Can't open file"
            return False, False, False
        return False, False, False
    
def return_old_canvas(save):
    frames = []
    for line in save.readlines():
        if line[0:5] == "COLOR":
            colors = [int(n) for n in line[6:-2].split(',')]
        elif line[0:5] == "SIZE ":
            size = [int(n) for n in line[6:-2].split(',')]
        elif line[0:5] == "PIXEL":
            frames.append([int(n) for n in line[6:-2].split(',')])
        elif line[0:5] == "STILL":
            frames.append(None)
    return size, colors, frames
    
def save_pix(size, color, frames, pixurl=None):
    if not pixurl:
        directory = ""
        repeat = True
        while repeat:
            url = QtGui.QFileDialog.getSaveFileName(None, "save pix file", directory, "Pix files (*.pix )")
            if url:
                directory = os.path.dirname(str(url))
                ext = os.path.splitext(str(url))[1]
                if ext == ".pix":
                    pixurl = url
                    repeat = False
                else:
                    pixurl = os.path.join(os.path.splitext(str(url))[0], ".pix")
                    if os.path.isfile(pixurl):
                        message = """It seems that you try to save as %s, unfortunaly, I can't do that.
I can save your animation as :
%s
but this file allready exit.
Should I overwrite it ?""" %(ext, pixurl)
                        okButton = "Overwrite"
                    else:
                        message = """It seems that you try to save as %s, unfortunaly, I can't do that.
Should I save your animation as :
%s ?""" %(ext, pixurl)
                        okButton = "Save"

                    messageBox = QtGui.QMessageBox()
                    messageBox.setWindowTitle("Oups !")
                    messageBox.setText(message);
                    messageBox.setIcon(QtGui.QMessageBox.Warning)
                    messageBox.addButton("Cancel", QtGui.QMessageBox.RejectRole)
                    messageBox.addButton(okButton, QtGui.QMessageBox.AcceptRole)
                    ret = messageBox.exec_();
                    if ret:
                        repeat = False
            else:
                return False
    try:
        save = open(str(pixurl), "w")
        save.write(return_pix(size, color, frames))
        save.close()
        return True
    except IOError:
        print "Can't open file"
        return False
        
def return_pix(size, color, frames):
    saveElem = ET.Element("pix", version="0,1")
    sizeElem = ET.SubElement(saveElem, "size")
    sizeElem.attrib["width"] = str(size[0])
    sizeElem.attrib["height"] = str(size[1])
    colorElem = ET.SubElement(saveElem, "colors", lenght=str(len(color)))
    colorElem.text = ','.join(str(n) for n in color)
    framesElem = ET.SubElement(saveElem, "frames", lenght=str(len(frames)))
    for n, frame in enumerate(frames):
        f = ET.SubElement(framesElem, "f%s" %(n))
        if not frame:
            f.text = "0"
        else:
            l = []
            for y in xrange(frame.height()):
                for x in xrange(frame.width()):
                    l.append(frame.pixelIndex(x, y))
            f.text = ','.join(str(p) for p in l)
    return ET.tostring(saveElem)
    
def return_old_pix(size, color, frames):
    pix = ""
    col = [int(i) for i in color]
    pix = "%sCOLOR%s\n" %(pix, col)
    pix = "%sSIZE (%s, %s)\n" %(pix, size[0], size[0])
    for im in frames:
        if im:
            l = []
            for y in xrange(im.height()):
                for x in xrange(im.width()):
                    l.append(im.pixelIndex(x, y))
            s = ','.join(str(n) for n in l)
            pix = "%sPIXEL(%s)\n" %(pix, s)
        else:
            pix = "%sSTILL\n" %(pix,)
    return pix
            
            
def export_png(frames, url=None):
    url = QtGui.QFileDialog.getSaveFileName(None, "Export animation as png", "", "Png files (*.png )")
    if url:
        url = os.path.splitext(str(url))[0]
        files = []
        fnexist = False
        for n, im in enumerate(frames, 1):
            fn = "%s%s.png" %(url, n)
            if os.path.isfile(fn):
                fnexist = True
            if im:
                files.append((fn, im))
                sim = im
            else:
#                sim.save(fn)
                files.append((fn, sim))
        if fnexist:
            message = QtGui.QMessageBox()
            message.setWindowTitle("Overwrite?")
            message.setText("Some filename allready exist.\nDo you want to overwrite them?");
            message.setIcon(QtGui.QMessageBox.Warning)
            message.addButton("Cancel", QtGui.QMessageBox.RejectRole)
            message.addButton("Overwrite", QtGui.QMessageBox.AcceptRole)
            ret = message.exec_();
            if ret:
                for i in files:
                    i[1].save(i[0])
        else:
            for i in files:
                i[1].save(i[0])

def export(frames, url=None):
    url = QtGui.QFileDialog.getSaveFileName(None, "export (.png or .nanim)", "", "Png files (*.png);;Nanim files (*.nanim)")
    if url:
        if url.endsWith("png"):
            export_png(frames, url)
        elif url.endsWith("nanim"):
            export_nanim(frames, url)

def export_png(frames, url):
    url = os.path.splitext(str(url))[0]
    files = []
    fnexist = False
    for n, im in enumerate(frames, 1):
        fn = "%s%s.png" %(url, n)
        if os.path.isfile(fn):
            fnexist = True
        if im:
            files.append((fn, im))
            sim = im
        else:
#                sim.save(fn)
            files.append((fn, sim))
    if fnexist:
        message = QtGui.QMessageBox()
        message.setWindowTitle("Overwrite?")
        message.setText("Some filename allready exist.\nDo you want to overwrite them?");
        message.setIcon(QtGui.QMessageBox.Warning)
        message.addButton("Cancel", QtGui.QMessageBox.RejectRole)
        message.addButton("Overwrite", QtGui.QMessageBox.AcceptRole)
        ret = message.exec_();
        if ret:
            for i in files:
                i[1].save(i[0])
    else:
        for i in files:
            i[1].save(i[0])

def export_nanim(frames, url):
    try:
        import google.protobuf
    except ImportError:
        message = QtGui.QMessageBox()
        message.setWindowTitle("Import error")
        message.setText("You need google protobuf to export as nanim.\nYou can download it at :\nhttps://code.google.com/p/protobuf/downloads/list");
        message.setIcon(QtGui.QMessageBox.Warning)
        message.addButton("Ok", QtGui.QMessageBox.AcceptRole)
        message.exec_();
        return

    import nanim_pb2
    nanim = nanim_pb2.Nanim()
    animation = nanim.animations.add()
    animation.name = "default"
    i = 0
    for im in frames:
        if not im:
            im = exim
        exim = im
        nimage = nanim.images.add()
        nimage.width = im.width()
        nimage.height = im.height()
        nimage.format = nanim_pb2.RGBA_8888
        nimage.name = "img_%d" % i
        i = i + 1
        pixels = bytearray()
        for y in xrange(im.height()):
            for x in xrange(im.width()):
                colors = QtGui.QColor(im.pixel(x,y))
                pixels.append(colors.red())
                pixels.append(colors.green())
                pixels.append(colors.blue())
                pixels.append(colors.alpha())
        nimage.pixels = str(pixels)

        frame = animation.frames.add()
        frame.imageName = nimage.name
        frame.duration = 100
        frame.u1 = 0
        frame.v1 = 0
        frame.u2 = 1
        frame.v2 = 1
    f = open(url, "wb")
    f.write(nanim.SerializeToString())
    f.close()

if __name__ == '__main__':
    #~ ouverturexml
    open_pix("/media/donnees/programation/pixeditor/master/test.pix")
