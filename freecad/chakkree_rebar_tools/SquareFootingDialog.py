"""
  SquareFooting.py
  Updated 17 Aug 2017
  
"""
import os
import FreeCAD
import FreeCADGui
import Draft
import Arch

from FreeCAD import Vector
from PySide import QtGui,QtCore

import  UShapeRebar , Stirrup

def getFaceNameFromVector(structure , axis):
    for i in range(6):
        face = structure.Shape.Faces[i]
        if face.normalAt(0,0) == axis:
            return "Face%d"%(i+1)


class SquareFootingTaskPanel:
    def __init__(self):
        self.form = [self.getWidget1(),
                     self.getWidget2(),
                     self.getWidget3()]
    
    def getWidget1(self):
        widget1 = QtGui.QWidget()
        widget1.setFixedHeight(250)
        widget1.setWindowTitle("Square Footing")
        
        self.imageLabel = QtGui.QLabel(u"image")
        self.imageLabel.setParent(widget1)
        self.imageLabel.setPixmap(QtGui.QPixmap(os.path.split(os.path.abspath(__file__))[0] + "/ui/SquareFooting01.svg"))
        
        self.lengthLabel = QtGui.QLabel(u"Length")
        self.lengthLabel.setParent(widget1)
        self.lengthLabel.setGeometry(200-20,150,120,25)
        self.Length = FreeCADGui.UiLoader().createWidget("Gui::InputField")
        self.Length.setText(FreeCAD.Units.Quantity(1000,FreeCAD.Units.Length).UserString)
        self.Length.setParent(widget1)
        self.Length.setGeometry(200-20,175,150,25)
        
        
        self.heightLabel = QtGui.QLabel(u"Height")
        self.heightLabel.setParent(widget1)
        self.heightLabel.setGeometry(200-20,50,120,25)
        self.Height = FreeCADGui.UiLoader().createWidget("Gui::InputField")
        self.Height.setText(FreeCAD.Units.Quantity(300,FreeCAD.Units.Length).UserString)
        self.Height.setParent(widget1)
        self.Height.setGeometry(200-20,75,150,25)
        return widget1
    
    def getWidget2(self):
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
        
        self.covering = FreeCADGui.UiLoader().createWidget("Gui::InputField")
        self.covering.setText(FreeCAD.Units.Quantity(50,FreeCAD.Units.Length).UserString)
        grid2.addWidget(self.covering, 3, 1)
        
        widget2.setLayout(grid2)
        return widget2
    
    def getWidget3(self):
        widget3 = QtGui.QWidget()
        widget3.setWindowTitle("Position")
        grid3 = QtGui.QGridLayout()
        grid3.columnMinimumWidth (0)
        grid3.setColumnStretch (0, 1)
        grid3.setColumnStretch (1, 5)
        grid3.setColumnStretch (2, 3)
        self.xLabel = QtGui.QLabel(u"x")
        self.yLabel = QtGui.QLabel(u"y")
        self.zLabel = QtGui.QLabel(u"z")
        self.xLabel.setFixedWidth(20)
        self.yLabel.setFixedWidth(20)
        self.zLabel.setFixedWidth(20)


        grid3.addWidget(self.xLabel, 1, 0)
        grid3.addWidget(self.yLabel, 2, 0, QtCore.Qt.AlignRight)
        grid3.addWidget(self.zLabel, 3, 0, QtCore.Qt.AlignRight)
        self.dummyLabel = QtGui.QLabel(u"")
        grid3.addWidget(self.dummyLabel, 1, 2)
        
        self.x = FreeCADGui.UiLoader().createWidget("Gui::InputField")
        self.x.setText(FreeCAD.Units.Quantity(0,FreeCAD.Units.Length).UserString)
        grid3.addWidget(self.x, 1, 1)
        self.y = FreeCADGui.UiLoader().createWidget("Gui::InputField")
        self.y.setText(FreeCAD.Units.Quantity(0,FreeCAD.Units.Length).UserString)
        grid3.addWidget(self.y, 2, 1)
        self.z = FreeCADGui.UiLoader().createWidget("Gui::InputField")
        self.z.setText(FreeCAD.Units.Quantity(0,FreeCAD.Units.Length).UserString)
        grid3.addWidget(self.z, 3, 1)
        
        widget3.setLayout(grid3)
        return widget3
    
    def accept(self):
        length = FreeCAD.Units.Quantity(self.Length.text()).Value
        height = FreeCAD.Units.Quantity(self.Height.text()).Value    #self.Height.value()
        L,B,t = length,length,height
        num = self.numRebar.value()
        covering = FreeCAD.Units.Quantity(self.covering.text()).Value 
        dia = self.dia.value()
        x = FreeCAD.Units.Quantity(self.x.text()).Value
        y = FreeCAD.Units.Quantity(self.y.text()).Value
        z = FreeCAD.Units.Quantity(self.z.text()).Value
        pos = ( x,y,z )
        makeSquareFooting(L,t,num,dia,covering,pos)
        return True

def makeSquareFooting(L,t,num,dia,covering,position):

    concrete = FreeCAD.ActiveDocument.addObject("Part::Box","concrete")
    concrete.Length = L
    concrete.Width = L
    concrete.Height = t
    concrete.Placement.Base = Vector(-L/2,-L/2,0)
    footing1 = Arch.makeStructure(concrete)

    footing1.ViewObject.Transparency = 80
    FreeCAD.ActiveDocument.recompute()
    

    roundFactor = 2
    R = roundFactor*dia
    face1 = getFaceNameFromVector(footing1 , Vector(1,0,0) )
    face2 = getFaceNameFromVector(footing1 , Vector(0,1,0) )
    face3 = getFaceNameFromVector(footing1 , Vector(0,0,1) )
    rebar1 = UShapeRebar.makeUShapeRebar(f_cover=covering+dia/2.+R, \
          b_cover=covering+dia/2.,  t_cover=covering, \
          r_cover=covering+dia/2., l_cover=covering+dia/2., diameter=dia,  \
          rounding=2, amount_spacing_check=True, amount_spacing_value=num, \
          orientation = "Bottom", structure = footing1, facename = face1)
    rebar2 = UShapeRebar.makeUShapeRebar(f_cover=covering+dia/2.+R, \
          b_cover=covering+dia/2.+dia,  t_cover=covering, \
          r_cover=covering+dia/2., l_cover=covering+dia/2., diameter=dia,  \
          rounding=roundFactor, amount_spacing_check=True, amount_spacing_value=num, \
          orientation = "Bottom", structure = footing1, facename = face2)
    covering1 = covering+dia+9/2.
    stirrup = Stirrup.makeStirrup(l_cover=covering1, \
               r_cover=covering1, t_cover=50+20, \
               b_cover=covering1, f_cover=covering1, \
               bentAngle=90, bentFactor=6, diameter=9, rounding=2,\
        amount_spacing_check=True, amount_spacing_value=1, structure = footing1, facename = face3)
    FreeCAD.ActiveDocument.recompute()

if __name__=='__main__':
    FreeCADGui.Control.closeDialog()
    FreeCADGui.Control.showDialog(SquareFootingTaskPanel())
