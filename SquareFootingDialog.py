"""
  SquareFooting.py
  10 Aug 2017
  
"""
import os
import FreeCAD
import Draft
import Arch

from FreeCAD import Vector
from PySide import QtGui,QtCore

import  UShapeRebar , Stirrup


class SquareFootingTaskPanel:
    def __init__(self):
        #dir_path = os.path.dirname(os.path.realpath(__file__))
        #Msg("%s\n"%dir_path)
        widget1 = QtGui.QWidget()
        widget1.setFixedHeight(250)
        widget1.setWindowTitle("Square Footing")
        
        self.imageLabel = QtGui.QLabel(u"image")
        self.imageLabel.setParent(widget1)
        self.imageLabel.setPixmap(QtGui.QPixmap(os.path.split(os.path.abspath(__file__))[0] + "/ui/SquareFooting01.svg"))
        
        self.lengthLabel = QtGui.QLabel(u"Lenght")
        self.lengthLabel.setParent(widget1)
        self.lengthLabel.setGeometry(200-20,150,120,25)
        self.Length = QtGui.QDoubleSpinBox()
        self.Length.setRange(1, 10000000.00)
        self.Length.setValue(1000)
        self.Length.setDecimals(0)
        self.Length.setSuffix(' mm')
        self.Length.setSingleStep(25)
        self.Length.setParent(widget1)
        self.Length.setGeometry(200-20,175,120,25)
        
        
        self.heightLabel = QtGui.QLabel(u"Height")
        self.heightLabel.setParent(widget1)
        self.heightLabel.setGeometry(200-20,50,120,25)
        self.Height = QtGui.QDoubleSpinBox()
        self.Height.setRange(1, 10000000.00)
        self.Height.setValue(300)
        self.Height.setDecimals(0)
        self.Height.setSuffix(' mm')
        self.Height.setSingleStep(25)
        self.Height.setParent(widget1)
        self.Height.setGeometry(200-20,75,120,25)
        
        #grid = QtGui.QGridLayout()
        #grid.addWidget(self.imageLabel, 0, 0) 
        #grid.addWidget(self.lengthLabel, 1, 0) 
        #grid.addWidget(self.Length, 1, 1)
        
        #grid.addWidget(self.widthLabel, 2, 0) 
        #grid.addWidget(self.Width, 2, 1)
        #grid.addWidget(self.heightLabel, 3, 0) 
        #grid.addWidget(self.Height, 3, 1)
        #widget1.setLayout(grid)
        
        widget2 = QtGui.QWidget()
        widget2.setWindowTitle("Reinforcement")
        grid2 = QtGui.QGridLayout()
        
        self.numRebarLabel = QtGui.QLabel(u"Number of Rebars")
        self.diaLabel = QtGui.QLabel(u"Diameter")
        self.coveringLabel = QtGui.QLabel(u"Covering")
        grid2.addWidget(self.numRebarLabel, 1, 0)
        grid2.addWidget(self.diaLabel, 2, 0)
        grid2.addWidget(self.coveringLabel, 3, 0)
        
        self.numRebar = QtGui.QSpinBox()
        self.numRebar.setRange(1, 1000)
        self.numRebar.setValue(5)
        grid2.addWidget(self.numRebar, 1, 1)
        
        self.dia = QtGui.QDoubleSpinBox()
        self.dia.setRange(1, 100)
        self.dia.setValue(12)
        self.dia.setDecimals(1)
        self.dia.setSuffix(' mm')
        grid2.addWidget(self.dia, 2, 1)
        
        self.covering = QtGui.QDoubleSpinBox()
        self.covering.setRange(0, 300)
        self.covering.setValue(50)
        self.covering.setDecimals(1)
        self.covering.setSuffix(' mm')
        self.covering.setSingleStep(5)
        grid2.addWidget(self.covering, 3, 1)
        
        widget2.setLayout(grid2)
        
        
        widget3 = QtGui.QWidget()
        widget3.setWindowTitle("Position")
        grid3 = QtGui.QGridLayout()
        self.xLabel = QtGui.QLabel(u"x")
        self.yLabel = QtGui.QLabel(u"y")
        self.zLabel = QtGui.QLabel(u"z")
        grid3.addWidget(self.xLabel, 1, 0)
        grid3.addWidget(self.yLabel, 2, 0)
        grid3.addWidget(self.zLabel, 3, 0)
        
        self.x = QtGui.QDoubleSpinBox()
        self.x.setValue(0)
        self.x.setDecimals(1)
        self.x.setSuffix(' mm')
        self.x.setSingleStep(25)
        grid3.addWidget(self.x, 1, 1)
        self.y = QtGui.QDoubleSpinBox()
        self.y.setValue(0)
        self.y.setDecimals(1)
        self.y.setSuffix(' mm')
        self.y.setSingleStep(25)
        grid3.addWidget(self.y, 2, 1)
        self.z = QtGui.QDoubleSpinBox()
        self.z.setValue(0)
        self.z.setDecimals(1)
        self.z.setSuffix(' mm')
        self.z.setSingleStep(25)
        grid3.addWidget(self.z, 3, 1)
        widget3.setLayout(grid3)
        
        self.form = [widget1,widget2,widget3]
    
    def accept(self):
        length = self.Length.value()
        height = self.Height.value()
        L,B,t = length,length,height
        num = self.numRebar.value()
        covering = self.covering.value()
        dia = self.dia.value()
        makeSquareFooting(L,t,num,dia,covering)
        return True

def makeSquareFooting(L,t,num,dia,covering):
    footing1 = Arch.makeStructure(length=L,width=L,height=t,name='Footing1')
    footing1.Placement.Base=Vector(+L/2., 0 , +t/2.)
    footing1.ViewObject.Transparency = 80
    FreeCAD.ActiveDocument.recompute()
    

    roundFactor = 2
    R = roundFactor*dia
    rebar1 = UShapeRebar.makeUShapeRebar(f_cover=covering+dia/2.+R, \
          b_cover=covering+dia/2.,  t_cover=covering, \
          r_cover=covering+dia/2., l_cover=covering+dia/2., diameter=dia,  \
          rounding=2, amount_spacing_check=True, amount_spacing_value=num, \
          orientation = "Bottom", structure = footing1, facename = 'Face1')
    rebar2 = UShapeRebar.makeUShapeRebar(f_cover=covering+dia/2.+R, \
          b_cover=covering+dia/2.+dia,  t_cover=covering, \
          r_cover=covering+dia/2., l_cover=covering+dia/2., diameter=dia,  \
          rounding=roundFactor, amount_spacing_check=True, amount_spacing_value=num, \
          orientation = "Bottom", structure = footing1, facename = 'Face6')
    FreeCAD.ActiveDocument.recompute()

if __name__=='__main__':
    FreeCADGui.Control.closeDialog()
    FreeCADGui.Control.showDialog(SquareFootingTaskPanel())
