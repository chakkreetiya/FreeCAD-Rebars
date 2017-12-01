# -*- coding=utf8 -*-
# **************************************************
# *  rebar in beam
# *   Copyright (c) 2017 - chakkree tiyawongsuwan  *
# **************************************************
import os
import FreeCAD ,FreeCADGui
import Arch
from FreeCAD import Vector , Units

from StraightRebar import makeStraightRebar
from UShapeRebar import makeUShapeRebar
from LShapeRebar import makeLShapeRebar
from Stirrup import makeStirrup

from PySide import QtGui,QtCore

class BeamRebarTaskPanel:
    def __init__(self):
        self.form = [self.getWidgetGeometry(), 
                     self.getWidget1(),self.getWidget2(),
                     self.getWidget3(), self.getWidget5(),
                     self.getWidget6() ]
    
    def getWidgetGeometry(self):
        widgetGeometry = QtGui.QWidget()
        widgetGeometry.setFixedHeight(100)
        widgetGeometry.setWindowTitle("Beam Geometry")
        
        self.L_Label = QtGui.QLabel(u"L = ")
        self.L_Label.setParent(widgetGeometry)
        self.L_Label.setGeometry(30,0,120,25) # x,y ,w, h
        
        self.b_Label = QtGui.QLabel(u"b = ")
        self.b_Label.setParent(widgetGeometry)
        self.b_Label.setGeometry(30,20,120,25) # x,y ,w, h
        
        self.h_Label = QtGui.QLabel(u"h = ")
        self.h_Label.setParent(widgetGeometry)
        self.h_Label.setGeometry(30,40,120,25) # x,y ,w, h
        
        self.dir_Label = QtGui.QLabel(u"Direction = ")
        self.dir_Label.setParent(widgetGeometry)
        self.dir_Label.setGeometry(30,60,130,25) # x,y ,w, h
        return widgetGeometry
        
    def getWidget1(self):
        widget1 = QtGui.QWidget()
        widget1.setFixedHeight(200)
        widget1.setWindowTitle("Top Main Rebar")

        self.image1Label = QtGui.QLabel(u"image1")
        self.image1Label.setParent(widget1)
        self.image1Label.setPixmap(QtGui.QPixmap(os.path.split(os.path.abspath(__file__))[0] + "/ui/Beam/TopMainRebarU.svg"))
        
        self.Type1Label = QtGui.QLabel(u"Type")
        self.Type1Label.setParent(widget1)
        self.Type1Label.setGeometry(30,20,120,25) # x,y ,w, h
        
        self.TypeMain = QtGui.QComboBox( widget1)
        self.TypeMain.addItem("Straight")
        self.TypeMain.addItem("U Shape")
        self.TypeMain.addItem("L Shape Left")
        self.TypeMain.addItem("L Shape Right")
        self.TypeMain.setCurrentIndex(1)
        self.TypeMain.setGeometry(70,20,120,25)


        self.NumTopMainLabel = QtGui.QLabel(u"Num =")
        self.NumTopMainLabel.setParent(widget1)
        self.NumTopMainLabel.setGeometry(170+50,60,40,25) # x,y ,w, h
        self.NumTopMain = QtGui.QComboBox( widget1)
        self.NumTopMain.addItem("2")
        self.NumTopMain.addItem("3")
        self.NumTopMain.setCurrentIndex(0)
        self.NumTopMain.setGeometry(170+100,60,40,25)

        self.DiaTopMainLabel = QtGui.QLabel(u"Dia =")
        self.DiaTopMainLabel.setParent(widget1)
        self.DiaTopMainLabel.setGeometry(170+50,90,40,25) # x,y ,w, h
        self.DiaTopMain = QtGui.QComboBox( widget1)
        self.DiaTopMain.addItem("12")
        self.DiaTopMain.addItem("15")
        self.DiaTopMain.addItem("16")
        self.DiaTopMain.addItem("19")
        self.DiaTopMain.addItem("20")
        self.DiaTopMain.addItem("22")
        self.DiaTopMain.addItem("25")
        self.DiaTopMain.addItem("32")
        self.DiaTopMain.setCurrentIndex(0)
        self.DiaTopMain.setGeometry(170+100,90,40,25)

        self.LCoverTopMainLabel = QtGui.QLabel(u"Left Cover:")
        self.LCoverTopMainLabel.setParent(widget1)
        self.LCoverTopMainLabel.setGeometry(10,135,80,25) # x,y ,w, h

        self.LCoverTopMain = FreeCADGui.UiLoader().createWidget("Gui::InputField")
        self.LCoverTopMain.setText(FreeCAD.Units.Quantity(-100,FreeCAD.Units.Length).UserString)
        self.LCoverTopMain.setParent(widget1)
        self.LCoverTopMain.setGeometry(10,160,120,25)
        
        self.RCoverTopMainLabel = QtGui.QLabel(u"Right Cover:")
        self.RCoverTopMainLabel.setParent(widget1)
        self.RCoverTopMainLabel.setGeometry(170,135,80,25) # x,y ,w, h
        
        self.RCoverTopMain = FreeCADGui.UiLoader().createWidget("Gui::InputField")
        self.RCoverTopMain.setText(FreeCAD.Units.Quantity(-100,FreeCAD.Units.Length).UserString)
        self.RCoverTopMain.setParent(widget1)
        self.RCoverTopMain.setGeometry(170,160,120,25)
        
        self.TypeMain.currentIndexChanged.connect(self.changeImageTopMain)
        self.NumTopMain.currentIndexChanged.connect(self.changeNumTopAddR)
        return widget1

    def changeImageTopMain(self):
        #Msg(self.TypeMain.currentIndex())
        #Msg('\n')
        if self.TypeMain.currentIndex() ==0:
            self.image1Label.setPixmap(QtGui.QPixmap(os.path.split(os.path.abspath(__file__))[0] + "/ui/Beam/TopMainRebarS.svg"))
        elif self.TypeMain.currentIndex() ==1:
            self.image1Label.setPixmap(QtGui.QPixmap(os.path.split(os.path.abspath(__file__))[0] + "/ui/Beam/TopMainRebarU.svg"))
        elif self.TypeMain.currentIndex() ==2:
            self.image1Label.setPixmap(QtGui.QPixmap(os.path.split(os.path.abspath(__file__))[0] + "/ui/Beam/TopMainRebarLL.svg"))
        if self.TypeMain.currentIndex() ==3:
            self.image1Label.setPixmap(QtGui.QPixmap(os.path.split(os.path.abspath(__file__))[0] + "/ui/Beam/TopMainRebarLR.svg"))

    def changeNumTopAddR(self):
        if self.NumTopMain.currentIndex() ==0:
            self.NumTopR.model().item(4).setEnabled(True)
        if self.NumTopMain.currentIndex() ==1:
            self.NumTopR.model().item(4).setEnabled(False)
    
    def getWidget2(self):
        widget2 = QtGui.QWidget()
        widget2.setWindowTitle("Bottom Main Rebar")
        widget2.setFixedHeight(200)
        
        self.image2Label = QtGui.QLabel(u"image2")
        self.image2Label.setParent(widget2)
        self.image2Label.setPixmap(QtGui.QPixmap(os.path.split(os.path.abspath(__file__))[0] + "/ui/Beam/BottomMainRebarS.svg"))
        
        self.Type2Label = QtGui.QLabel(u"Type")
        self.Type2Label.setParent(widget2)
        self.Type2Label.setGeometry(30,20,120,25) # x,y ,w, h
        self.BottomMain = QtGui.QComboBox( widget2)
        self.BottomMain.addItem("Straight")
        self.BottomMain.addItem("U Shape")
        self.BottomMain.addItem("L Shape Left")
        self.BottomMain.addItem("L Shape Right")
        self.BottomMain.setCurrentIndex(0)
        self.BottomMain.setGeometry(70,20,120,25)
        
        self.NumBottomMainLabel = QtGui.QLabel(u"Num =")
        self.NumBottomMainLabel.setParent(widget2)
        self.NumBottomMainLabel.setGeometry(170+50,60,40,25) # x,y ,w, h
        self.NumBottomMain = QtGui.QComboBox( widget2)
        self.NumBottomMain.addItem("2")
        self.NumBottomMain.addItem("3")
        self.NumBottomMain.setCurrentIndex(0)
        self.NumBottomMain.setGeometry(170+100,60,40,25)
        
        self.DiaBottomMainLabel = QtGui.QLabel(u"Dia =")
        self.DiaBottomMainLabel.setParent(widget2)
        self.DiaBottomMainLabel.setGeometry(170+50,90,40,25) # x,y ,w, h
        self.DiaBottomMain = QtGui.QComboBox( widget2)
        self.DiaBottomMain.addItem("12")
        self.DiaBottomMain.addItem("15")
        self.DiaBottomMain.addItem("16")
        self.DiaBottomMain.addItem("19")
        self.DiaBottomMain.addItem("20")
        self.DiaBottomMain.addItem("22")
        self.DiaBottomMain.addItem("25")
        self.DiaBottomMain.addItem("32")
        self.DiaBottomMain.setCurrentIndex(0)
        self.DiaBottomMain.setGeometry(170+100,90,40,25)

        self.LCoverBottomMainLabel = QtGui.QLabel(u"Left Cover:")
        self.LCoverBottomMainLabel.setParent(widget2)
        self.LCoverBottomMainLabel.setGeometry(10,135,80,25) # x,y ,w, h

        self.LCoverBottomMain = FreeCADGui.UiLoader().createWidget("Gui::InputField")
        self.LCoverBottomMain.setText(FreeCAD.Units.Quantity(-100,FreeCAD.Units.Length).UserString)
        self.LCoverBottomMain.setParent(widget2)
        self.LCoverBottomMain.setGeometry(10,160,120,25)
        
        self.RCoverBottomMainLabel = QtGui.QLabel(u"Right Cover:")
        self.RCoverBottomMainLabel.setParent(widget2)
        self.RCoverBottomMainLabel.setGeometry(170,135,80,25) # x,y ,w, h
        
        self.RCoverBottomMain = FreeCADGui.UiLoader().createWidget("Gui::InputField")
        self.RCoverBottomMain.setText(FreeCAD.Units.Quantity(-100,FreeCAD.Units.Length).UserString)
        self.RCoverBottomMain.setParent(widget2)
        self.RCoverBottomMain.setGeometry(170,160,120,25)
        
        self.BottomMain.currentIndexChanged.connect(self.changeImageBottomMain)
        self.NumBottomMain.currentIndexChanged.connect(self.changeNumAddMid)
        return widget2

    def changeImageBottomMain(self):
        
        if self.BottomMain.currentIndex() ==0:
            self.image2Label.setPixmap(QtGui.QPixmap(os.path.split(os.path.abspath(__file__))[0] + "/ui/Beam/BottomMainRebarS.svg"))
        elif self.BottomMain.currentIndex() ==1:
            self.image2Label.setPixmap(QtGui.QPixmap(os.path.split(os.path.abspath(__file__))[0] + "/ui/Beam/BottomMainRebarU.svg"))
        elif self.BottomMain.currentIndex() ==2:
            self.image2Label.setPixmap(QtGui.QPixmap(os.path.split(os.path.abspath(__file__))[0] + "/ui/Beam/BottomMainRebarLL.svg"))
        if self.BottomMain.currentIndex() ==3:
            self.image2Label.setPixmap(QtGui.QPixmap(os.path.split(os.path.abspath(__file__))[0] + "/ui/Beam/BottomMainRebarLR.svg"))

    def changeNumAddMid(self):
        #Msg("changeNumAddMid\n")
        if self.NumBottomMain.currentIndex() ==0:
            self.NumAddMid.model().item(4).setEnabled(True)
        if self.NumBottomMain.currentIndex() ==1:
            self.NumAddMid.model().item(4).setEnabled(False)
#
   
    def getWidget3(self):
        widget3 = QtGui.QWidget()
        widget3.setWindowTitle("Add Middle Rebar")
        widget3.setFixedHeight(150)
        self.image3Label = QtGui.QLabel(u"image3")
        self.image3Label.setParent(widget3)
        self.image3Label.setPixmap(QtGui.QPixmap(os.path.split(os.path.abspath(__file__))[0] + "/ui/Beam/AddMidRebar.svg"))
        self.LengthAddMid = QtGui.QComboBox( widget3)
        self.LengthAddMid.addItem("L/7")
        self.LengthAddMid.addItem("L/8")
        self.LengthAddMid.setCurrentIndex(0)
        self.LengthAddMid.setGeometry(20,90,55,25)
        
        self.NumAddMidLabel = QtGui.QLabel(u"Num =")
        self.NumAddMidLabel.setParent(widget3)
        self.NumAddMidLabel.setGeometry(170+50,20,40,25) # x,y ,w, h
        self.NumAddMid = QtGui.QComboBox( widget3)
        self.NumAddMid.addItem("0")
        self.NumAddMid.addItem("1")
        self.NumAddMid.addItem("2")
        self.NumAddMid.addItem("3")
        self.NumAddMid.addItem("4")
        self.NumAddMid.setCurrentIndex(1)
        self.NumAddMid.setGeometry(170+100,20,40,25)
        
        self.DiaAddMidLabel = QtGui.QLabel(u"Dia =")
        self.DiaAddMidLabel.setParent(widget3)
        self.DiaAddMidLabel.setGeometry(170+50,50,40,25) # x,y ,w, h
        self.DiaAddMid = QtGui.QComboBox( widget3)
        self.DiaAddMid.addItem("12")
        self.DiaAddMid.addItem("15")
        self.DiaAddMid.addItem("16")
        self.DiaAddMid.addItem("19")
        self.DiaAddMid.addItem("20")
        self.DiaAddMid.addItem("22")
        self.DiaAddMid.addItem("25")
        self.DiaAddMid.addItem("32")
        self.DiaAddMid.setCurrentIndex(0)
        self.DiaAddMid.setGeometry(170+100,50,40,25)


        return widget3
    


    def getWidget5(self):
        widget5 = QtGui.QWidget()
        widget5.setWindowTitle("Add Top-Right Rebar")
        widget5.setFixedHeight(200)
        self.image3Label = QtGui.QLabel(u"image5")
        self.image3Label.setParent(widget5)
        self.image3Label.setPixmap(QtGui.QPixmap(os.path.split(os.path.abspath(__file__))[0] + "/ui/Beam/AddTopRightRebarType1.svg"))
        
        self.TypeTopR = QtGui.QComboBox( widget5)
        self.TypeTopR.addItem("Type1")
        self.TypeTopR.addItem("Type2")
        self.TypeTopR.setCurrentIndex(0)
        self.TypeTopR.setGeometry(10,10,70,25)
        self.TypeTopR.setVisible(False)
        

        self.LengthTopR = QtGui.QComboBox( widget5)
        self.LengthTopR.addItem("L/3")
        self.LengthTopR.addItem("L/4")
        self.LengthTopR.setCurrentIndex(0)
        self.LengthTopR.setGeometry(140,10,50,25)
        
        self.LengthTopNear = QtGui.QComboBox( widget5)
        self.LengthTopNear.addItem("L/3")
        self.LengthTopNear.addItem("L/4")
        self.LengthTopNear.setCurrentIndex(0)
        self.LengthTopNear.setGeometry(210,10,50,25)
        
        
        self.NumTopRLabel = QtGui.QLabel(u"Num =")
        self.NumTopRLabel.setParent(widget5)
        self.NumTopRLabel.setGeometry(170+105,10,40,25) # x,y ,w, h
        self.NumTopR = QtGui.QComboBox( widget5)
        self.NumTopR.addItem("0")
        self.NumTopR.addItem("1")
        self.NumTopR.addItem("2")
        self.NumTopR.addItem("3")
        self.NumTopR.addItem("4")
        self.NumTopR.setCurrentIndex(1)
        self.NumTopR.setGeometry(170+155,10,40,25)
        
        self.DiaTopRLabel = QtGui.QLabel(u"Dia =")
        self.DiaTopRLabel.setParent(widget5)
        self.DiaTopRLabel.setGeometry(170+105,40,40,25) # x,y ,w, h
        self.DiaTopR = QtGui.QComboBox( widget5)
        self.DiaTopR.addItem("12")
        self.DiaTopR.addItem("15")
        self.DiaTopR.addItem("16")
        self.DiaTopR.addItem("19")
        self.DiaTopR.addItem("20")
        self.DiaTopR.addItem("22")
        self.DiaTopR.addItem("25")
        self.DiaTopR.addItem("32")
        self.DiaTopR.setCurrentIndex(0)
        self.DiaTopR.setGeometry(170+155,40,40,25)
        
        self.Col_WidthLabel = QtGui.QLabel(u"Column Width:")
        self.Col_WidthLabel.setParent(widget5)
        self.Col_WidthLabel.setGeometry(115,135,90,25) # x,y ,w, h
        
        self.Col_Width = FreeCADGui.UiLoader().createWidget("Gui::InputField")
        self.Col_Width.setText(FreeCAD.Units.Quantity(200,FreeCAD.Units.Length).UserString)
        self.Col_Width.setParent(widget5)
        self.Col_Width.setGeometry(80,160,120,25)

        self.L2_Label = QtGui.QLabel(u"Beam Adjacent Length:")
        self.L2_Label.setParent(widget5)
        self.L2_Label.setGeometry(220,135,150,25) # x,y ,w, h
        
        self.L2 = FreeCADGui.UiLoader().createWidget("Gui::InputField")
        self.L2.setText(FreeCAD.Units.Quantity(1000,FreeCAD.Units.Length).UserString)
        self.L2.setParent(widget5)
        self.L2.setGeometry(220,160,120,25)

        self.TypeTopR.currentIndexChanged.connect(self.changeFormTopR)
        
        return widget5
    
    def changeFormTopR(self):
        if self.TypeTopR.currentIndex() ==0:
            self.image3Label.setPixmap(QtGui.QPixmap(os.path.split(os.path.abspath(__file__))[0] + "/ui/Beam/AddTopRightRebarType1.svg"))
            self.L2_Label.setVisible(True)
            self.L2.setVisible(True)
            self.LengthTopNear.setVisible(True)
            self.Col_WidthLabel.setText('Column Width:')
        elif self.TypeTopR.currentIndex() ==1:
            self.image3Label.setPixmap(QtGui.QPixmap(os.path.split(os.path.abspath(__file__))[0] + "/ui/Beam/AddTopRightRebarType2.svg"))
            self.L2_Label.setVisible(False)
            self.L2.setVisible(False)
            self.LengthTopNear.setVisible(False)
            self.Col_WidthLabel.setText('Right Cover:')
    
    def getWidget6(self):
        widget6 = QtGui.QWidget()
        widget6.setWindowTitle("Stirrup")
        widget6.setFixedHeight(150)
        
        self.image6Label = QtGui.QLabel(u"image6")
        self.image6Label.setParent(widget6)
        self.image6Label.setPixmap(QtGui.QPixmap(os.path.split(os.path.abspath(__file__))[0] + "/ui/Beam/StirrupRebar.svg"))
        
        self.DiaStirrupLabel = QtGui.QLabel(u"Dia =")
        self.DiaStirrupLabel.setParent(widget6)
        self.DiaStirrupLabel.setGeometry(50,30,40,25) # x,y ,w, h
        self.DiaStirrupLabel2 = QtGui.QLabel(u"@")
        self.DiaStirrupLabel2.setParent(widget6)
        self.DiaStirrupLabel2.setGeometry(140,30,40,25) # x,y ,w, h
        
        self.DiaStirrup = QtGui.QComboBox( widget6)
        self.DiaStirrup.addItem("6")
        self.DiaStirrup.addItem("9")
        self.DiaStirrup.addItem("12")
        self.DiaStirrup.setCurrentIndex(0)
        self.DiaStirrup.setGeometry(90,30,40,25)
        
        self.Spacing = FreeCADGui.UiLoader().createWidget("Gui::InputField")
        self.Spacing.setText(FreeCAD.Units.Quantity(175,FreeCAD.Units.Length).UserString)
        self.Spacing.setParent(widget6)
        self.Spacing.setGeometry(170,30,100,25)
        return widget6

    
    def accept(self):
        direction = self.dir_Label.text().split("'")[1]
        if self.TypeMain.currentIndex() ==0:
            typeTopMain = 'S'
        elif self.TypeMain.currentIndex() ==1:
            typeTopMain = 'U'
        elif self.TypeMain.currentIndex() ==2:
            typeTopMain = 'LL'
        elif self.TypeMain.currentIndex() ==3:
            typeTopMain = 'LR'
        
        numTopMain = self.NumTopMain.currentIndex()+2
        numBottomMain = self.NumBottomMain.currentIndex()+2
        numAddMid = self.NumAddMid.currentIndex()
        #Msg('numAddMid=%d\n'%numAddMid)
        diaTopMain = int( self.DiaTopMain.currentText() )
        diaBottomMain = int( self.DiaBottomMain.currentText() )
        diaAddMid = int( self.DiaAddMid.currentText() )
        diaStirrup = int( self.DiaStirrup.currentText() )
        spacing =  Units.Quantity(self.Spacing.text()).Value
        LCoverTopMain = Units.Quantity(self.LCoverTopMain.text()).Value
        RCoverTopMain = Units.Quantity(self.RCoverTopMain.text()).Value
        LCoverBottomMain = Units.Quantity(self.LCoverBottomMain.text()).Value
        RCoverBottomMain = Units.Quantity(self.RCoverBottomMain.text()).Value


        if self.LengthAddMid.currentIndex()==0:
            L7 = 1/7.0
        elif self.LengthAddMid.currentIndex()==1:
            L7 = 1/8.0

        numAddTopR = self.NumTopR.currentIndex()
        diaAddTopR = int( self.DiaAddMid.currentText() )
        L2 = Units.Quantity(self.L2.text()).Value
        ColWidth = Units.Quantity(self.Col_Width.text()).Value
        if self.LengthTopR.currentIndex()==0:
            L1_3 = 1/3.0
        elif self.LengthTopR.currentIndex()==1:
            L1_3 = 1/4.0 
         
        if self.LengthTopNear.currentIndex()==0:
            L2_3 = 1/3.0
        elif self.LengthTopNear.currentIndex()==1:
            L2_3 = 1/4.0
        #Msg("numTopMain=%d , numBottomMain=%d \n"%(numTopMain,numBottomMain))
        createBeamRebar(
             TopMain={'type':typeTopMain,'num':numTopMain , 'dia':diaTopMain , 
                      'L_Cover':LCoverTopMain , 'R_Cover':RCoverTopMain},
             BottomMain={'type':'S' , 'num':numBottomMain , 'dia':diaBottomMain,
                        'L_Cover':LCoverBottomMain , 'R_Cover':RCoverBottomMain},
             AddMid = {'num':numAddMid , 'dia':diaAddMid , 'L7':L7} ,
             AddTopR = {'num':numAddTopR , 'dia':diaAddTopR ,
                         'LTop3':L1_3 , 'LNear3':L2_3 ,
                         'L2':L2 ,'Col_Width':ColWidth},
             Stirrup={'dia':diaStirrup , 'spacing':float(spacing)} ,
             direction=direction)
        FreeCAD.ActiveDocument.recompute()
        return True

def createBeamRebar(TopMain, BottomMain , AddMid , AddTopR ,
             Stirrup ,  direction='Horizontal' , covering=25  , 
             structure = None):
    if not structure:
        selected_obj = FreeCADGui.Selection.getSelectionEx()[0]
        structure = selected_obj.Object
    
    h = structure.Height
    diaStir = float(  Stirrup['dia'] )
    if direction=='Horizontal':
        face='Face1'
        b = structure.Width
        L = structure.Length
    elif direction=='Vertical':
        face='Face2'
        b = structure.Length
        L = structure.Width
    #Msg("b=%g \nh=%g\nL=%g\n "%(b,h,L))
    
    # topMain ----------------    
    dia = float( TopMain['dia'] )
    coverNet =  covering +  diaStir+ dia/2
    if TopMain['type']=='S':
        rebar1 = makeStraightRebar(f_cover=coverNet, coverAlong=("Top Side", coverNet), 
              rt_cover=TopMain['R_Cover'], lb_cover=TopMain['L_Cover'], 
              diameter=dia, 
              amount_spacing_check=True, amount_spacing_value =int(TopMain['num']) , 
              orientation = "Horizontal", 
              structure = structure, facename =face )
    elif TopMain['type']=='U':
        rebar1 = makeUShapeRebar(f_cover=coverNet, 
               b_cover=float(h)-coverNet-1.5*dia-12*dia, 
               r_cover=TopMain['R_Cover'], l_cover=TopMain['L_Cover'], 
               diameter=dia , t_cover=coverNet, 
               rounding=3, 
               amount_spacing_check=True, amount_spacing_value=int(TopMain['num']), 
               orientation = "Top", 
                structure = structure, facename = face)
    elif TopMain['type']=='LL' or TopMain['type']=='LR':
        if TopMain['type']=='LL':
            orientation = 'Top Left'
        elif TopMain['type']=='LR':
            orientation = 'Top Right'
        rebar1 =makeLShapeRebar(f_cover=coverNet, 
               b_cover=float(h)-coverNet-1.5*dia-12*dia, t_cover=coverNet,
               l_cover=TopMain['L_Cover'], r_cover=TopMain['R_Cover'], 
               diameter=dia,  rounding=3, 
               amount_spacing_check=True, amount_spacing_value=int(TopMain['num']), 
               orientation = orientation, 
               structure = structure, facename = face)
    #rebar1.Label = "เหล็กหลักบน"
    rebar1.Label = "TopMainRebar"

    # bottomMain ----------------    
    dia = float( BottomMain['dia'] )
    coverNet =  covering +  diaStir+ dia/2
    if BottomMain['type']=='S':
        rebar2 = makeStraightRebar(f_cover=coverNet, coverAlong=("Bottom Side", coverNet), 
              rt_cover=BottomMain['R_Cover'], lb_cover=BottomMain['L_Cover'], 
              diameter=dia, 
              amount_spacing_check=True, amount_spacing_value =int(BottomMain['num']) , 
              orientation = "Horizontal", 
              structure = structure, facename =face )
    elif BottomMain['type']=='U':
        rebar2 = makeUShapeRebar(f_cover=coverNet, 
               t_cover=float(h)-coverNet-1.5*dia-12*dia, 
               r_cover=TopMain['R_Cover'], l_cover=TopMain['L_Cover'], 
               diameter=dia , b_cover=coverNet, 
               rounding=3, 
               amount_spacing_check=True, amount_spacing_value=int(TopMain['num']), 
               orientation = "Bottom", 
                structure = structure, facename = face)
    #rebar2.Label = "เหล็กหลักล่าง"
    rebar2.Label = "BottomMainRebar"
    # Add Mid ----------------    
    dia = float( AddMid['dia'] )
    num = int( AddMid['num'] )
    coverNet =  covering +  diaStir+ dia/2
    if BottomMain['num']==2 and  (num==1 or num==3 or num==4):
        rebar3_1 = makeStraightRebar(f_cover=float(b)/2.0, coverAlong=("Bottom Side", coverNet), 
              rt_cover=float(L)*AddMid['L7'], lb_cover=float(L)*AddMid['L7'], 
              diameter=dia, 
              amount_spacing_check=True, amount_spacing_value =1 , 
              orientation = "Horizontal", 
              structure = structure, facename =face )
        #rebar3_1.Label = "เหล็กเสริมพิเศษกลางคาน1"   
        rebar3_1.Label = "AddMidRebar1" 
    if BottomMain['num']==2 and  (num==2 or num==3 ):
        numAdd = 2
        rebar3_2 = makeStraightRebar(f_cover=coverNet, 
              coverAlong=("Bottom Side", coverNet+25+dia), 
              rt_cover=float(L)*AddMid['L7'], lb_cover=float(L)*AddMid['L7'], 
              diameter=dia, 
              amount_spacing_check=True, amount_spacing_value =numAdd , 
              orientation = "Horizontal", 
              structure = structure, facename =face )
        #rebar3_2.Label = "เหล็กเสริมพิเศษกลางคาน2" 
        rebar3_2.Label = "AddMidRebar2"  
    if BottomMain['num']==2 and  (num==4):
        numAdd = 3
        rebar3_2 = makeStraightRebar(f_cover=coverNet, 
              coverAlong=("Bottom Side", coverNet+25+dia), 
              rt_cover=float(L)*AddMid['L7'], lb_cover=float(L)*AddMid['L7'], 
              diameter=dia, 
              amount_spacing_check=True, amount_spacing_value =numAdd , 
              orientation = "Horizontal", 
              structure = structure, facename =face )
        #rebar3_2.Label = "เหล็กเสริมพิเศษกลางคาน2" 
        rebar3_2.Label = "AddMidRebar2" 
    if BottomMain['num']==3 and  (num==1 or num==2 or num==3):
        numAdd = num
        rebar3_2 = makeStraightRebar(f_cover=coverNet, 
              coverAlong=("Bottom Side", coverNet+25+dia), 
              rt_cover=float(L)*AddMid['L7'], lb_cover=float(L)*AddMid['L7'], 
              diameter=dia, 
              amount_spacing_check=True, amount_spacing_value =numAdd , 
              orientation = "Horizontal", 
              structure = structure, facename =face )
        #rebar3_2.Label = "เหล็กเสริมพิเศษกลางคาน2" 
        rebar3_2.Label = "AddMidRebar2" 

    # Add Top Right --------------------------
    dia = float( AddTopR['dia'] )
    num = int( AddTopR['num'] )
    coverNet =  covering +  diaStir+ dia/2
    if TopMain['num']==2 and  (num==1 or num==3 or num==4):
        rebar4_1 = makeStraightRebar(f_cover=float(b)/2.0, coverAlong=("Top Side", coverNet), 
              lb_cover=+float(L)-float(L)*AddTopR['LTop3'],
              rt_cover=-AddTopR['Col_Width']-AddTopR['L2']*AddTopR['LTop3'], 
              diameter=dia,
              amount_spacing_check=True, amount_spacing_value =1 , 
              orientation = "Horizontal", 
              structure = structure, facename =face )
        #rebar4_1.Label = "เหล็กเสริมพิเศษบนขวา1"  
        rebar4_1.Label = "TopAddRightRebar1"  
    if TopMain['num']==2 and (num==2 or num==3 or num==4):
        if num==2 or num ==3:
            numAdd =2
        elif num==4:
            numAdd = 3
        rebar4_2 = makeStraightRebar(f_cover=coverNet, 
              coverAlong=("Top Side", coverNet+25+dia), 
              lb_cover=+float(L)-float(L)*AddTopR['LTop3'],
              rt_cover=-AddTopR['Col_Width']-AddTopR['L2']*AddTopR['LTop3'] ,
              diameter=dia, 
              amount_spacing_check=True, amount_spacing_value =numAdd , 
              orientation = "Horizontal", 
              structure = structure, facename =face )
        #rebar4_2.Label = "เหล็กเสริมพิเศษกลางคาน2"
        rebar4_2.Label = "TopAddRightRebar2"
    if TopMain['num']==3 and  (num==1 or num==2 or num==3):
        numAdd = num
        rebar4_2 = makeStraightRebar(f_cover=coverNet, 
              coverAlong=("Top Side", coverNet+25+dia), 
              lb_cover=+float(L)-float(L)*AddTopR['LTop3'],
              rt_cover=-AddTopR['Col_Width']-AddTopR['L2']*AddTopR['LTop3'] ,
              diameter=dia, 
              amount_spacing_check=True, amount_spacing_value =numAdd , 
              orientation = "Horizontal", 
              structure = structure, facename =face )
        #rebar4_2.Label = "เหล็กเสริมพิเศษกลางคาน2" 
        rebar4_2.Label = "TopAddRightRebar2" 
 
    # stirrup
    if direction=='Horizontal':
        face='Face6'
    elif direction=='Vertical':
        face='Face1'
    coverNet =  covering +  diaStir/2.
    spacing = float(  Stirrup['spacing'] )
    Lnet = float(L) - 200
    num = int (  round(Lnet/ spacing) )
    num += 1
    gap = (float(L)-(num-1)*spacing)/2.0
    stir1 = makeStirrup(l_cover =coverNet , r_cover=coverNet, 
        t_cover=coverNet, b_cover=coverNet, 
        f_cover=gap, bentAngle=135, bentFactor=6, 
        diameter=diaStir, rounding=2,
        amount_spacing_check=True, amount_spacing_value=3, 
        structure = structure, facename = face)
    stir1.CustomSpacing = "%d@%d"%(num ,  int(spacing) )
    stir1.Label = "เหล็กปลอก"

def RunBeamRebarDialog():
    selected_obj = FreeCADGui.Selection.getSelectionEx()[0]
    structure = selected_obj.Object
    
    h = structure.Height 
    b = structure.Width
    L = structure.Length
    #Msg("b=%g \nh=%g\nL=%g\n "%(b,h,L))
    if b<L:
        dir = 'Horizontal'
    else:
        dir = 'Vertical'
        temp = b
        b=L
        L =temp
    form1 = BeamRebarTaskPanel()
    form1.L_Label.setText('L=%g'%L)
    form1.b_Label.setText('b=%g'%b)
    form1.h_Label.setText('h=%g'%h)
    form1.dir_Label.setText("Direction='%s' "%dir)

    FreeCADGui.Control.closeDialog()
    FreeCADGui.Control.showDialog(form1)
    


if __name__=='__main__':
    
    if not True:
        createBeamRebar(
             TopMain={'type':'U','num':2 , 'dia':12 , 
                      'L_Cover':-150 , 'R_Cover':-150},
             BottomMain={'type':'S' , 'num':2 , 'dia':12,
                        'L_Cover':-150 , 'R_Cover':-150},
             AddMid = {'num':4 , 'dia':12} ,             
             Stirrup={'dia':6 , 'spacing':175})

    if not True:
        createBeamRebar(direction='Vertical' , 
            TopMain={'type':'S' , 'num':2 , 'dia':12,
            'L_Cover':-150 , 'R_Cover':-150},
            BottomMain={'type':'U' , 'num':2 , 'dia':12,
            'L_Cover':-150 , 'R_Cover':-150},
             AddMid = {'num':3 , 'dia':12} ,
            Stirrup={'dia':6 , 'spacing':175})

    if not True:
        FreeCADGui.Control.closeDialog()
        FreeCADGui.Control.showDialog(BeamRebarTaskPanel())
    
    if  True:
        RunBeamRebarDialog()
    
    FreeCAD.ActiveDocument.recompute()
    Msg('Done!\n')