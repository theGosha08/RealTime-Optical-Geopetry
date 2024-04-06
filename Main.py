
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QSlider, QHBoxLayout, QVBoxLayout, QAbstractButton, QRadioButton, QGroupBox, QPushButton
from PyQt5.QtCore import Qt, QTimer, QPoint, QLineF, QLine
from PyQt5 import QtGui
from PyQt5.QtGui import QPainter, QBrush, QPen
import sys
import math

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.setWindowTitle("Optica")
        self.wide = 800
        self.heigh = 500
        self.setFixedSize(self.wide,self.heigh)

        self.dw = QWidget()
        self.ui = QWidget()


        self.x_slider = QSlider(Qt.Horizontal)
        self.x_slider.setTickPosition(QSlider.TicksBelow)

        self.numberOfPositions = 13
        self.x_slider.setTickInterval(61)
        self.x_slider.setMinimum(30)
        self.x_slider.setMaximum(770)
        self.x_slider.valueChanged.connect(self.changedValue)

        self.y_slider = QSlider()
        self.y_slider.setMinimum(75)
        self.y_slider.setMaximum(int(self.heigh/2)-75)
        self.y_slider.valueChanged.connect(self.changedValueY)

        self.y_offset = QSlider()
        self.y_offset.setMinimum(-75)
        self.y_offset.setMaximum(75)
        self.y_offset.valueChanged.connect(self.changedValueOff)

        self.BackButton = QPushButton("Сбросить")
        self.BackButton.clicked.connect(self.resetButton)

        self.R1 = QRadioButton("Собирающая")
        self.R1.toggled.connect(self.RButton)
        self.R1.setChecked(True)
        self.R2 = QRadioButton("Рассеевающая")
        self.R2.toggled.connect(self.RButton)
        self.label1 = QLabel('1.')
        self.label2 = QLabel('2.')
        self.label3 = QLabel('3.')
        self.label4 = QLabel('4.')

        self.resultBox = QGroupBox('Характеристика')
        self.interBox = QGroupBox('Параметры')
        self.drawBox = QGroupBox('Изображение')

        self.buttonLayout = QHBoxLayout()
        self.leftVLayout = QVBoxLayout()
        self.interHLayout = QHBoxLayout()
        self.mainHLayout = QHBoxLayout()
        self.mainVLayout = QVBoxLayout()
        self.labelsVLayout = QVBoxLayout()

        self.leftVLayout.addWidget(self.x_slider)
        self.buttonLayout.addWidget(self.R1)
        self.buttonLayout.addWidget(self.R2)
        self.buttonLayout.addWidget(self.BackButton)

        self.labelsVLayout.addWidget(self.label1)
        self.labelsVLayout.addWidget(self.label2)
        self.labelsVLayout.addWidget(self.label3)
        self.labelsVLayout.addWidget(self.label4)

        self.resultBox.setLayout(self.labelsVLayout)

        self.interHLayout.addLayout(self.leftVLayout)

        self.interHLayout.addWidget(self.y_offset)
        self.interHLayout.addWidget(self.y_slider)
        
        self.interBox.setLayout(self.interHLayout)

        self.mainHLayout.addWidget(self.interBox)
        self.mainHLayout.addWidget(self.resultBox)

        self.leftVLayout.addLayout(self.buttonLayout) 
        self.mainVLayout.addLayout(self.mainHLayout)


        self.ui.setLayout(self.mainVLayout)

        self.ui.setParent(self)
        self.dw.setParent(self)

        self.dw.setFixedSize(800,250)

        self.ui.setFixedSize(800,250)
        self.ui.move(0,250)


        p = self.dw.palette()
        p.setColor(self.dw.backgroundRole(), Qt.red)
        self.dw.setPalette(p)
        p = self.ui.palette()
        p.setColor(self.ui.backgroundRole(), Qt.black)
        self.ui.setPalette(p)

        self.Is_Minmoe = False

        self.OPoint = QPoint(int(self.wide/2),int(self.heigh/4))

        self.LenseType = "O" # O I

        self.objX = 60
        self.objHigh = -30
        self.objY = int(self.heigh/4)

        self.APoint = QPoint(int(self.objX),int(self.objY+self.objHigh))
        self.BPoint = QPoint(int(self.objX),int(self.objY))

        self.A1Point = QPoint()
        self.B1Point = QPoint()

        self.FA1Line = QLineF()
        self.AA1Line = QLineF()
        self.FB1Line = QLineF()
        self.BB1Line = QLineF()

        self.listOfSIgns = ["2F", "F", "F","2F"]
        self.listOfDots = [QPoint(153,int(self.heigh/4)),QPoint(277,int(self.heigh/4)),QPoint(525,int(self.heigh/4)),QPoint(676,int(self.heigh/4))]
        self.listOfLittleDots = [QPoint(92,int(self.heigh/4)),QPoint(215,int(self.heigh/4)),QPoint(337,int(self.heigh/4)),QPoint(462,int(self.heigh/4)),QPoint(616,int(self.heigh/4)),QPoint(738,int(self.heigh/4))]


    def paintEvent(self,event):
        self.painter = QPainter(self)
        self.painter.setPen(QPen(Qt.black, 3, Qt.SolidLine))
        self.DrawGui()
        self.DrawLogic()
        self.painter.end()
        self.update()


    def DrawLogic(self):

        #Рисуем объект ОСЬ Y ИДЕТ СВЕРХУ ВНИЗ!!!!!!!!!!!
        self.painter.setPen(QPen(Qt.black, 3, Qt.SolidLine))
        self.APoint = QPoint(int(self.objX),int(self.objY-self.objHigh))
        self.BPoint = QPoint(int(self.objX),int(self.objY))

        self.painter.drawLine(self.APoint,self.BPoint)

        if self.objHigh < 0:
            self.painter.drawLine(int(self.objX-5),int(self.objY-self.objHigh-5),int(self.objX),int(self.objY-self.objHigh))
            self.painter.drawLine(int(self.objX),int(self.objY-self.objHigh),int(self.objX+5),int(self.objY-self.objHigh-5))
        elif self.objHigh > 0:
            self.painter.drawLine(int(self.objX-5),int(self.objY-self.objHigh+5),int(self.objX),int(self.objY-self.objHigh))
            self.painter.drawLine(int(self.objX),int(self.objY-self.objHigh),int(self.objX+5),int(self.objY-self.objHigh+5))

        self.painter.drawLine(int(self.objX-5),int(self.objY),int(self.objX+5),int(self.objY))
        self.painter.setPen(QPen(Qt.gray, 3, Qt.SolidLine))

        if self.LenseType == "O":
        # Изображение точки А

            if self.APoint.x() < self.wide/2 and  self.APoint.y() < self.heigh/4: #2 четверть
                x = (((self.wide/2)-self.APoint.x())*(self.heigh/2-self.heigh/4))/(self.heigh/4 -self.APoint.y())
                x += self.wide/2
                self.painter.drawLine(self.APoint.x(),self.APoint.y(),int(x),int(self.heigh/2))# Рисуем луч от А через О

                self.AA1Line = QLineF(self.APoint.x(),self.APoint.y(),int(x),int(self.heigh/2))

                self.painter.drawLine(self.APoint.x(),self.APoint.y(),int(self.wide/2),int(self.APoint.y()))
                a1 = (self.listOfDots[2].x() - self.wide/2)*(self.heigh/2-self.heigh/4)/(self.heigh/4 - self.APoint.y())
                a1 += self.listOfDots[2].x()
                self.painter.drawLine(int(self.wide/2),int(self.APoint.y()),int(a1),int(self.heigh/2))# Рисуем отрезок от А до линзы и оттуда луч через F

                self.FA1Line = QLineF(int(self.wide/2),int(self.APoint.y()),int(a1),int(self.heigh/2))

                self.painter.setPen(QPen(Qt.black, 7, Qt.SolidLine))

                if self.FA1Line.intersects(self.AA1Line)[0] == QLineF.BoundedIntersection:
                    self.painter.drawPoint(self.FA1Line.intersects(self.AA1Line)[1]) # Находим пересечение
                    self.A1Point = self.FA1Line.intersects(self.AA1Line)[1] 
                    self.Is_Minmoe = False
                elif self.FA1Line.intersects(self.AA1Line)[0] == QLineF.UnboundedIntersection:
                    self.Is_Minmoe = True
                    col = self.FA1Line.intersects(self.AA1Line)[1]
                    self.painter.drawPoint(col)
                    self.painter.drawPoint(self.FA1Line.intersects(self.AA1Line)[1])
                    self.A1Point = self.FA1Line.intersects(self.AA1Line)[1] 
                    self.painter.setPen(QPen(Qt.gray, 3, Qt.DashLine))
                    self.AA1Line.setP1(col)
                    self.FA1Line.setP1(col)
                    self.painter.drawLines([self.AA1Line,self.FA1Line])


            elif self.APoint.x() < self.wide/2 and  self.APoint.y() > self.heigh/4:#3 четверть
                x = (((self.wide/2)-self.APoint.x()) * self.heigh/4)/(self.APoint.y() - self.heigh/4)
                x += self.wide/2
                self.painter.drawLine(self.APoint.x(),self.APoint.y(),int(x),int(1)) 

                self.AA1Line = QLineF(self.APoint.x(),self.APoint.y(),int(x),int(1))

                self.painter.drawLine(self.APoint.x(),self.APoint.y(),int(self.wide/2),int(self.APoint.y()))
                a1 = (self.listOfDots[2].x() - (self.wide/2))*(self.heigh/2-self.heigh/4)/(self.APoint.y() - self.heigh/4)
                a1 += self.listOfDots[2].x()
                self.painter.drawLine(int(self.wide/2),int(self.APoint.y()),int(a1),1)

                self.FA1Line = QLineF(int(self.wide/2),int(self.APoint.y()),int(a1),1)

                self.painter.setPen(QPen(Qt.black, 7, Qt.SolidLine))

                if self.FA1Line.intersects(self.AA1Line)[0] == QLineF.BoundedIntersection:
                    self.painter.drawPoint(self.FA1Line.intersects(self.AA1Line)[1]) # Находим пересечение
                    self.A1Point = self.FA1Line.intersects(self.AA1Line)[1] 
                    self.Is_Minmoe = False
                elif self.FA1Line.intersects(self.AA1Line)[0] == QLineF.UnboundedIntersection:
                    self.Is_Minmoe = True
                    col = self.FA1Line.intersects(self.AA1Line)[1]
                    self.painter.drawPoint(col)
                    self.painter.drawPoint(self.FA1Line.intersects(self.AA1Line)[1])
                    self.A1Point = self.FA1Line.intersects(self.AA1Line)[1] 
                    self.painter.setPen(QPen(Qt.gray, 3, Qt.DashLine))
                    self.AA1Line.setP1(col)
                    self.FA1Line.setP1(col)
                    self.painter.drawLines([self.AA1Line,self.FA1Line])

            elif self.APoint.x() > self.wide/2 and  self.APoint.y() < self.heigh/4:  # 1 четверть
                x = ((self.APoint.x() - (self.wide/2))*(self.heigh/2-self.heigh/4))/(self.heigh/4 -self.APoint.y())
                x = self.wide/2 - x
                self.painter.drawLine(self.APoint.x(),self.APoint.y(),int(x),int(self.heigh/2))

                self.AA1Line = QLineF(self.APoint.x(),self.APoint.y(),int(x),int(self.heigh/2))

                self.painter.drawLine(self.APoint.x(),self.APoint.y(),int(self.wide/2),int(self.APoint.y()))
                a1 = (self.wide/2 - self.listOfDots[1].x())*(self.heigh/2-self.heigh/4)/(self.heigh/4 - self.APoint.y())
                a1 = self.wide/2 - (self.wide/2 - self.listOfDots[1].x()) - a1
                self.painter.drawLine(int(self.wide/2),int(self.APoint.y()),int(a1),int(self.heigh/2))

                self.FA1Line = QLineF(int(self.wide/2),int(self.APoint.y()),int(a1),int(self.heigh/2))

                self.painter.setPen(QPen(Qt.black, 7, Qt.SolidLine))

                if self.FA1Line.intersects(self.AA1Line)[0] == QLineF.BoundedIntersection:
                    self.painter.drawPoint(self.FA1Line.intersects(self.AA1Line)[1]) # Находим пересечение
                    self.A1Point = self.FA1Line.intersects(self.AA1Line)[1] 
                    self.Is_Minmoe = False
                elif self.FA1Line.intersects(self.AA1Line)[0] == QLineF.UnboundedIntersection:
                    self.Is_Minmoe = True
                    col = self.FA1Line.intersects(self.AA1Line)[1]
                    self.painter.drawPoint(col)
                    self.painter.drawPoint(self.FA1Line.intersects(self.AA1Line)[1])
                    self.A1Point = self.FA1Line.intersects(self.AA1Line)[1] 
                    self.painter.setPen(QPen(Qt.gray, 3, Qt.DashLine))
                    self.AA1Line.setP1(col)
                    self.FA1Line.setP1(col)
                    self.painter.drawLines([self.AA1Line,self.FA1Line])

            elif self.APoint.x() > self.wide/2 and  self.APoint.y() > self.heigh/4:  # 4 четверть
                x = ((self.APoint.x() - (self.wide/2)) * self.heigh/4)/(self.APoint.y() - self.heigh/4)
                x = self.wide/2 - x
                self.painter.drawLine(self.APoint.x(),self.APoint.y(),int(x),int(1))

                self.AA1Line = QLineF(self.APoint.x(),self.APoint.y(),int(x),int(1))

                self.painter.drawLine(self.APoint.x(),self.APoint.y(),int(self.wide/2),int(self.APoint.y()))
                a1 = (self.wide/2 - self.listOfDots[1].x())*(self.heigh/2-self.heigh/4)/(self.APoint.y() - self.heigh/4)
                a1 = self.wide/2 - (self.wide/2 - self.listOfDots[1].x()) - a1
                self.painter.drawLine(int(self.wide/2),int(self.APoint.y()),int(a1),0)

                self.FA1Line = QLineF(int(self.wide/2),int(self.APoint.y()),int(a1),0)

                self.painter.setPen(QPen(Qt.black, 7, Qt.SolidLine))

                if self.FA1Line.intersects(self.AA1Line)[0] == QLineF.BoundedIntersection:
                    self.painter.drawPoint(self.FA1Line.intersects(self.AA1Line)[1]) # Находим пересечение
                    self.A1Point = self.FA1Line.intersects(self.AA1Line)[1] 
                    self.Is_Minmoe = False
                elif self.FA1Line.intersects(self.AA1Line)[0] == QLineF.UnboundedIntersection:
                    self.Is_Minmoe = True
                    col = self.FA1Line.intersects(self.AA1Line)[1]
                    self.painter.drawPoint(col)
                    self.painter.drawPoint(self.FA1Line.intersects(self.AA1Line)[1])
                    self.A1Point = self.FA1Line.intersects(self.AA1Line)[1] 
                    self.painter.setPen(QPen(Qt.gray, 3, Qt.DashLine))
                    self.AA1Line.setP1(col)
                    self.FA1Line.setP1(col)
                    self.painter.drawLines([self.AA1Line,self.FA1Line])

            # Изображение точки В
            self.painter.setPen(QPen(Qt.gray, 3, Qt.SolidLine))

            if self.BPoint.x() < self.wide/2 and  self.BPoint.y() > self.heigh/4:
                x = (((self.wide/2)-self.BPoint.x()) * self.heigh/4)/(self.BPoint.y() - self.heigh/4) # B в 3 четверти
                x += self.wide/2
                self.painter.drawLine(self.BPoint.x(),self.BPoint.y(),int(x),int(1)) 

                self.BB1Line = QLineF(self.BPoint.x(),self.BPoint.y(),int(x),int(1))

                self.painter.drawLine(self.BPoint.x(),self.BPoint.y(),int(self.wide/2),int(self.BPoint.y()))
                b1 = (self.listOfDots[2].x() - (self.wide/2))*(self.heigh/2-self.heigh/4)/(self.BPoint.y() - self.heigh/4)
                b1 += self.listOfDots[2].x()
                self.painter.drawLine(int(self.wide/2),int(self.BPoint.y()),int(b1),1)

                self.FB1Line = QLineF(int(self.wide/2),int(self.BPoint.y()),int(b1),1)

                self.painter.setPen(QPen(Qt.black, 7, Qt.SolidLine))

                if self.FB1Line.intersects(self.BB1Line)[0] == QLineF.BoundedIntersection:
                    self.B1Point = self.FB1Line.intersects(self.BB1Line)[1] 
                    self.painter.drawPoint(self.B1Point) # Находим пересечение
                    self.Is_Minmoe = False
                elif self.FB1Line.intersects(self.BB1Line)[0] == QLineF.UnboundedIntersection:
                    self.Is_Minmoe = True
                    col = self.FB1Line.intersects(self.BB1Line)[1]
                    self.painter.drawPoint(col)
                    self.B1Point = col
                    self.painter.setPen(QPen(Qt.gray, 3, Qt.DashLine))
                    self.BB1Line.setP1(col)
                    self.FB1Line.setP1(col)
                    self.painter.drawLines([self.BB1Line,self.FB1Line])

            elif self.BPoint.x() < self.wide/2 and  self.BPoint.y() < self.heigh/4:# В во 2 четтверти
                x = (((self.wide/2)-self.BPoint.x())*(self.heigh/2-self.heigh/4))/(self.heigh/4 -self.BPoint.y())
                x += self.wide/2
                self.painter.drawLine(self.BPoint.x(),self.BPoint.y(),int(x),int(self.heigh/2))# Рисуем луч от А через О

                self.BB1Line = QLineF(self.BPoint.x(),self.BPoint.y(),int(x),int(self.heigh/2))

                self.painter.drawLine(self.BPoint.x(),self.BPoint.y(),int(self.wide/2),int(self.BPoint.y()))
                b1 = (self.listOfDots[2].x() - self.wide/2)*(self.heigh/2-self.heigh/4)/(self.heigh/4 - self.BPoint.y())
                b1 += self.listOfDots[2].x()
                self.painter.drawLine(int(self.wide/2),int(self.BPoint.y()),int(b1),int(self.heigh/2))# Рисуем отрезок от А до линзы и оттуда луч через F

                self.FB1Line = QLineF(int(self.wide/2),int(self.BPoint.y()),int(b1),int(self.heigh/2))

                self.painter.setPen(QPen(Qt.black, 7, Qt.SolidLine))

                if self.FB1Line.intersects(self.BB1Line)[0] == QLineF.BoundedIntersection:
                    self.painter.drawPoint(self.FB1Line.intersects(self.BB1Line)[1]) # Находим пересечение
                    self.B1Point = self.FB1Line.intersects(self.BB1Line)[1] 
                    self.Is_Minmoe = False
                elif self.FB1Line.intersects(self.BB1Line)[0] == QLineF.UnboundedIntersection:
                    self.Is_Minmoe = True
                    col = self.FB1Line.intersects(self.BB1Line)[1]
                    self.painter.drawPoint(col)
                    self.B1Point = self.FB1Line.intersects(self.BB1Line)[1] 
                    self.painter.setPen(QPen(Qt.gray, 3, Qt.DashLine))
                    self.BB1Line.setP1(col)
                    self.FB1Line.setP1(col)
                    self.painter.drawLines([self.BB1Line,self.FB1Line]) 

            elif self.BPoint.x() > self.wide/2 and  self.BPoint.y() < self.heigh/4:  # В в 1 четверти
                x = ((self.BPoint.x() - (self.wide/2))*(self.heigh/2-self.heigh/4))/(self.heigh/4 -self.BPoint.y())
                x = self.wide/2 - x
                self.painter.drawLine(self.BPoint.x(),self.BPoint.y(),int(x),int(self.heigh/2))

                self.BB1Line = QLineF(self.BPoint.x(),self.BPoint.y(),int(x),int(self.heigh/2))

                self.painter.drawLine(self.BPoint.x(),self.BPoint.y(),int(self.wide/2),int(self.BPoint.y()))
                b1 = (self.wide/2 - self.listOfDots[1].x())*(self.heigh/2-self.heigh/4)/(self.heigh/4 - self.BPoint.y())
                b1 = self.wide/2 - (self.wide/2 - self.listOfDots[1].x()) - b1
                self.painter.drawLine(int(self.wide/2),int(self.BPoint.y()),int(b1),int(self.heigh/2))

                self.FB1Line = QLineF(int(self.wide/2),int(self.BPoint.y()),int(b1),int(self.heigh/2))

                self.painter.setPen(QPen(Qt.black, 7, Qt.SolidLine))

                if self.FB1Line.intersects(self.BB1Line)[0] == QLineF.BoundedIntersection:
                    self.painter.drawPoint(self.FB1Line.intersects(self.BB1Line)[1]) # Находим пересечение
                    self.B1Point = self.FB1Line.intersects(self.BB1Line)[1] 
                    self.Is_Minmoe = False
                elif self.FB1Line.intersects(self.BB1Line)[0] == QLineF.UnboundedIntersection:
                    self.Is_Minmoe = True
                    col = self.FB1Line.intersects(self.BB1Line)[1]
                    self.painter.drawPoint(col)
                    self.B1Point = self.FB1Line.intersects(self.BB1Line)[1] 
                    self.painter.setPen(QPen(Qt.gray, 3, Qt.DashLine))
                    self.BB1Line.setP1(col)
                    self.FB1Line.setP1(col)
                    self.painter.drawLines([self.BB1Line,self.FB1Line])

            elif self.BPoint.x() > self.wide/2 and  self.BPoint.y() > self.heigh/4:  # B в 4 четверти
                x = ((self.BPoint.x() - (self.wide/2)) * self.heigh/4)/(self.BPoint.y() - self.heigh/4)
                x = self.wide/2 - x
                self.painter.drawLine(self.BPoint.x(),self.BPoint.y(),int(x),int(1))

                self.BB1Line = QLineF(self.BPoint.x(),self.BPoint.y(),int(x),int(1))

                self.painter.drawLine(self.BPoint.x(),self.BPoint.y(),int(self.wide/2),int(self.BPoint.y()))
                b1 = (self.wide/2 - self.listOfDots[1].x())*(self.heigh/2-self.heigh/4)/(self.BPoint.y() - self.heigh/4)
                b1 = self.wide/2 - (self.wide/2 - self.listOfDots[1].x()) - b1
                self.painter.drawLine(int(self.wide/2),int(self.BPoint.y()),int(b1),0)

                self.FB1Line = QLineF(int(self.wide/2),int(self.BPoint.y()),int(b1),0)

                self.painter.setPen(QPen(Qt.black, 7, Qt.SolidLine))

                if self.FB1Line.intersects(self.BB1Line)[0] == QLineF.BoundedIntersection:
                    self.painter.drawPoint(self.FB1Line.intersects(self.BB1Line)[1]) # Находим пересечение
                    self.B1Point = self.FB1Line.intersects(self.BB1Line)[1] 
                    self.Is_Minmoe = False
                elif self.FB1Line.intersects(self.BB1Line)[0] == QLineF.UnboundedIntersection:
                    self.Is_Minmoe = True
                    col = self.FB1Line.intersects(self.BB1Line)[1]
                    self.painter.drawPoint(col)
                    self.B1Point = self.FB1Line.intersects(self.BB1Line)[1] 
                    self.painter.setPen(QPen(Qt.gray, 3, Qt.DashLine))
                    self.BB1Line.setP1(col)
                    self.FB1Line.setP1(col)
                    self.painter.drawLines([self.BB1Line,self.FB1Line])

            if self.BPoint.y() == self.heigh/4 :
                self.B1Point = QPoint(int(self.A1Point.x()),int(self.heigh/4))

        elif self.LenseType == "I":
            # Изображение точки А
            if self.APoint.x() < self.wide/2 and  self.APoint.y() < self.heigh/4: #2 четверть
                x = (((self.wide/2)-self.APoint.x())*(self.heigh/2-self.heigh/4))/(self.heigh/4 -self.APoint.y())
                x += self.wide/2
                self.painter.drawLine(self.APoint.x(),self.APoint.y(),int(x),int(self.heigh/2))# Рисуем луч от А через О

                self.AA1Line = QLineF(self.APoint.x(),self.APoint.y(),int(x),int(self.heigh/2))

                self.painter.drawLine(self.APoint.x(),self.APoint.y(),int(self.wide/2),int(self.APoint.y()))
                a1 = (self.listOfDots[1].x() - (self.wide/2))*(self.heigh/2-self.heigh/4)/(self.APoint.y() - self.heigh/4)
                a1 += self.listOfDots[1].x()
                self.painter.setPen(QPen(Qt.gray, 3, Qt.DashLine))
                self.painter.drawLine(int(self.wide/2),int(self.APoint.y()),int(a1),1)

                self.FA1Line = QLineF(int(self.wide/2),int(self.APoint.y()),int(a1),1)

                self.painter.setPen(QPen(Qt.black, 7, Qt.SolidLine))


                if self.FA1Line.intersects(self.AA1Line)[0] == QLineF.BoundedIntersection:
                    self.painter.drawPoint(self.FA1Line.intersects(self.AA1Line)[1]) # Находим пересечение
                    self.A1Point = self.FA1Line.intersects(self.AA1Line)[1] 
                    self.Is_Minmoe = False
                elif self.FA1Line.intersects(self.AA1Line)[0] == QLineF.UnboundedIntersection:
                    self.Is_Minmoe = True
                    col = self.FA1Line.intersects(self.AA1Line)[1]
                    self.painter.drawPoint(col)
                    self.painter.drawPoint(self.FA1Line.intersects(self.AA1Line)[1])
                    self.A1Point = self.FA1Line.intersects(self.AA1Line)[1] 
                    self.painter.setPen(QPen(Qt.gray, 3, Qt.DashLine))
                    self.AA1Line.setP1(col)
                    self.FA1Line.setP1(col)
                    self.painter.drawLines([self.AA1Line,self.FA1Line])


            elif self.APoint.x() < self.wide/2 and  self.APoint.y() > self.heigh/4:#3 четверть
                x = (((self.wide/2)-self.APoint.x()) * self.heigh/4)/(self.APoint.y() - self.heigh/4)
                x += self.wide/2
                self.painter.drawLine(self.APoint.x(),self.APoint.y(),int(x),int(1)) 

                self.AA1Line = QLineF(self.APoint.x(),self.APoint.y(),int(x),int(1))

                self.painter.drawLine(self.APoint.x(),self.APoint.y(),int(self.wide/2),int(self.APoint.y()))
                a1 = (self.listOfDots[1].x() - self.wide/2)*(self.heigh/2-self.heigh/4)/(self.heigh/4 - self.APoint.y())
                a1 += self.listOfDots[1].x()
                self.painter.setPen(QPen(Qt.gray, 3, Qt.DashLine))
                self.painter.drawLine(int(self.wide/2),int(self.APoint.y()),int(a1),int(self.heigh/2))# Рисуем отрезок от А до линзы и оттуда луч через F

                self.FA1Line = QLineF(int(self.wide/2),int(self.APoint.y()),int(a1),int(self.heigh/2))

                self.painter.setPen(QPen(Qt.black, 7, Qt.SolidLine))

                if self.FA1Line.intersects(self.AA1Line)[0] == QLineF.BoundedIntersection:
                    self.painter.drawPoint(self.FA1Line.intersects(self.AA1Line)[1]) # Находим пересечение
                    self.A1Point = self.FA1Line.intersects(self.AA1Line)[1] 
                    self.Is_Minmoe = False
                elif self.FA1Line.intersects(self.AA1Line)[0] == QLineF.UnboundedIntersection:
                    self.Is_Minmoe = True
                    col = self.FA1Line.intersects(self.AA1Line)[1]
                    self.painter.drawPoint(col)
                    self.painter.drawPoint(self.FA1Line.intersects(self.AA1Line)[1])
                    self.A1Point = self.FA1Line.intersects(self.AA1Line)[1] 
                    self.painter.setPen(QPen(Qt.gray, 3, Qt.DashLine))
                    self.AA1Line.setP1(col)
                    self.FA1Line.setP1(col)
                    self.painter.drawLines([self.AA1Line,self.FA1Line])

            elif self.APoint.x() > self.wide/2 and  self.APoint.y() < self.heigh/4:  # 1 четверть
                x = ((self.APoint.x() - (self.wide/2))*(self.heigh/2-self.heigh/4))/(self.heigh/4 -self.APoint.y())
                x = self.wide/2 - x
                self.painter.drawLine(self.APoint.x(),self.APoint.y(),int(x),int(self.heigh/2))

                self.AA1Line = QLineF(self.APoint.x(),self.APoint.y(),int(x),int(self.heigh/2))

                self.painter.drawLine(self.APoint.x(),self.APoint.y(),int(self.wide/2),int(self.APoint.y()))
                a1 = (self.wide/2 - self.listOfDots[2].x())*(self.heigh/2-self.heigh/4)/(self.APoint.y() - self.heigh/4)
                a1 = self.wide/2 - (self.wide/2 - self.listOfDots[2].x()) - a1
                self.painter.drawLine(int(self.wide/2),int(self.APoint.y()),int(a1),0)

                self.FA1Line = QLineF(int(self.wide/2),int(self.APoint.y()),int(a1),0)

                self.painter.setPen(QPen(Qt.black, 7, Qt.SolidLine))

                if self.FA1Line.intersects(self.AA1Line)[0] == QLineF.BoundedIntersection:
                    self.painter.drawPoint(self.FA1Line.intersects(self.AA1Line)[1]) # Находим пересечение
                    self.A1Point = self.FA1Line.intersects(self.AA1Line)[1] 
                    self.Is_Minmoe = False
                elif self.FA1Line.intersects(self.AA1Line)[0] == QLineF.UnboundedIntersection:
                    self.Is_Minmoe = True
                    col = self.FA1Line.intersects(self.AA1Line)[1]
                    self.painter.drawPoint(col)
                    self.painter.drawPoint(self.FA1Line.intersects(self.AA1Line)[1])
                    self.A1Point = self.FA1Line.intersects(self.AA1Line)[1] 
                    self.painter.setPen(QPen(Qt.gray, 3, Qt.DashLine))
                    self.AA1Line.setP1(col)
                    self.FA1Line.setP1(col)
                    self.painter.drawLines([self.AA1Line,self.FA1Line])

            elif self.APoint.x() > self.wide/2 and  self.APoint.y() > self.heigh/4:  # 4 четверть
                x = ((self.APoint.x() - (self.wide/2)) * self.heigh/4)/(self.APoint.y() - self.heigh/4)
                x = self.wide/2 - x
                self.painter.drawLine(self.APoint.x(),self.APoint.y(),int(x),int(1))

                self.AA1Line = QLineF(self.APoint.x(),self.APoint.y(),int(x),int(1))

                self.painter.drawLine(self.APoint.x(),self.APoint.y(),int(self.wide/2),int(self.APoint.y()))
                a1 = (self.wide/2 - self.listOfDots[2].x())*(self.heigh/2-self.heigh/4)/(self.heigh/4 - self.APoint.y())
                a1 = self.wide/2 - (self.wide/2 - self.listOfDots[2].x()) - a1
                self.painter.drawLine(int(self.wide/2),int(self.APoint.y()),int(a1),int(self.heigh/2))

                self.FA1Line = QLineF(int(self.wide/2),int(self.APoint.y()),int(a1),int(self.heigh/2))

                self.painter.setPen(QPen(Qt.black, 7, Qt.SolidLine))

                if self.FA1Line.intersects(self.AA1Line)[0] == QLineF.BoundedIntersection:
                    self.painter.drawPoint(self.FA1Line.intersects(self.AA1Line)[1]) # Находим пересечение
                    self.A1Point = self.FA1Line.intersects(self.AA1Line)[1] 
                    self.Is_Minmoe = False
                elif self.FA1Line.intersects(self.AA1Line)[0] == QLineF.UnboundedIntersection:
                    self.Is_Minmoe = True
                    col = self.FA1Line.intersects(self.AA1Line)[1]
                    self.painter.drawPoint(col)
                    self.painter.drawPoint(self.FA1Line.intersects(self.AA1Line)[1])
                    self.A1Point = self.FA1Line.intersects(self.AA1Line)[1] 
                    self.painter.setPen(QPen(Qt.gray, 3, Qt.DashLine))
                    self.AA1Line.setP1(col)
                    self.FA1Line.setP1(col)
                    self.painter.drawLines([self.AA1Line,self.FA1Line])

            # Изображение точки В
            self.painter.setPen(QPen(Qt.gray, 3, Qt.SolidLine))

            if self.BPoint.x() < self.wide/2 and  self.BPoint.y() > self.heigh/4:
                x = (((self.wide/2)-self.BPoint.x()) * self.heigh/4)/(self.BPoint.y() - self.heigh/4) # B в 3 четверти
                x += self.wide/2
                self.painter.drawLine(self.BPoint.x(),self.BPoint.y(),int(x),int(1)) 

                self.BB1Line = QLineF(self.BPoint.x(),self.BPoint.y(),int(x),int(1))

                self.painter.drawLine(self.BPoint.x(),self.BPoint.y(),int(self.wide/2),int(self.BPoint.y()))
                b1 = (self.listOfDots[1].x() - self.wide/2)*(self.heigh/2-self.heigh/4)/(self.heigh/4 - self.BPoint.y())
                b1 += self.listOfDots[1].x()
                self.painter.drawLine(int(self.wide/2),int(self.BPoint.y()),int(b1),int(self.heigh/2))# Рисуем отрезок от А до линзы и оттуда луч через F

                self.FB1Line = QLineF(int(self.wide/2),int(self.BPoint.y()),int(b1),int(self.heigh/2))

                self.painter.setPen(QPen(Qt.black, 7, Qt.SolidLine))

                if self.FB1Line.intersects(self.BB1Line)[0] == QLineF.BoundedIntersection:
                    self.B1Point = self.FB1Line.intersects(self.BB1Line)[1] 
                    self.painter.drawPoint(self.B1Point) # Находим пересечение
                    self.Is_Minmoe = False
                elif self.FB1Line.intersects(self.BB1Line)[0] == QLineF.UnboundedIntersection:
                    self.Is_Minmoe = True
                    col = self.FB1Line.intersects(self.BB1Line)[1]
                    self.painter.drawPoint(col)
                    self.B1Point = col
                    self.painter.setPen(QPen(Qt.gray, 3, Qt.DashLine))
                    self.BB1Line.setP1(col)
                    self.FB1Line.setP1(col)
                    self.painter.drawLines([self.BB1Line,self.FB1Line])

            elif self.BPoint.x() < self.wide/2 and  self.BPoint.y() < self.heigh/4:# В во 2 четтверти
                x = (((self.wide/2)-self.BPoint.x())*(self.heigh/2-self.heigh/4))/(self.heigh/4 -self.BPoint.y())
                x += self.wide/2
                self.painter.drawLine(self.BPoint.x(),self.BPoint.y(),int(x),int(self.heigh/2))# Рисуем луч от А через О

                self.BB1Line = QLineF(self.BPoint.x(),self.BPoint.y(),int(x),int(self.heigh/2))

                self.painter.drawLine(self.BPoint.x(),self.BPoint.y(),int(self.wide/2),int(self.BPoint.y()))
                b1 = (self.listOfDots[1].x() - (self.wide/2))*(self.heigh/2-self.heigh/4)/(self.BPoint.y() - self.heigh/4)
                b1 += self.listOfDots[1].x()
                self.painter.drawLine(int(self.wide/2),int(self.BPoint.y()),int(b1),1)

                self.FB1Line = QLineF(int(self.wide/2),int(self.BPoint.y()),int(b1),1)

                self.painter.setPen(QPen(Qt.black, 7, Qt.SolidLine))

                if self.FB1Line.intersects(self.BB1Line)[0] == QLineF.BoundedIntersection:
                    self.painter.drawPoint(self.FB1Line.intersects(self.BB1Line)[1]) # Находим пересечение
                    self.B1Point = self.FB1Line.intersects(self.BB1Line)[1] 
                    self.Is_Minmoe = False
                elif self.FB1Line.intersects(self.BB1Line)[0] == QLineF.UnboundedIntersection:
                    self.Is_Minmoe = True
                    col = self.FB1Line.intersects(self.BB1Line)[1]
                    self.painter.drawPoint(col)
                    self.B1Point = self.FB1Line.intersects(self.BB1Line)[1] 
                    self.painter.setPen(QPen(Qt.gray, 3, Qt.DashLine))
                    self.BB1Line.setP1(col)
                    self.FB1Line.setP1(col)
                    self.painter.drawLines([self.BB1Line,self.FB1Line]) 

            elif self.BPoint.x() > self.wide/2 and  self.BPoint.y() < self.heigh/4:  # В в 1 четверти
                x = ((self.BPoint.x() - (self.wide/2))*(self.heigh/2-self.heigh/4))/(self.heigh/4 -self.BPoint.y())
                x = self.wide/2 - x
                self.painter.drawLine(self.BPoint.x(),self.BPoint.y(),int(x),int(self.heigh/2))

                self.BB1Line = QLineF(self.BPoint.x(),self.BPoint.y(),int(x),int(self.heigh/2))

                self.painter.drawLine(self.BPoint.x(),self.BPoint.y(),int(self.wide/2),int(self.BPoint.y()))
                b1 = (self.wide/2 - self.listOfDots[2].x())*(self.heigh/2-self.heigh/4)/(self.BPoint.y() - self.heigh/4)
                b1 = self.wide/2 - (self.wide/2 - self.listOfDots[2].x()) - b1
                self.painter.drawLine(int(self.wide/2),int(self.BPoint.y()),int(b1),0)

                self.FB1Line = QLineF(int(self.wide/2),int(self.BPoint.y()),int(b1),0)

                self.painter.setPen(QPen(Qt.black, 7, Qt.SolidLine))

                if self.FB1Line.intersects(self.BB1Line)[0] == QLineF.BoundedIntersection:
                    self.painter.drawPoint(self.FB1Line.intersects(self.BB1Line)[1]) # Находим пересечение
                    self.B1Point = self.FB1Line.intersects(self.BB1Line)[1] 
                    self.Is_Minmoe = False
                elif self.FB1Line.intersects(self.BB1Line)[0] == QLineF.UnboundedIntersection:
                    self.Is_Minmoe = True
                    col = self.FB1Line.intersects(self.BB1Line)[1]
                    self.painter.drawPoint(col)
                    self.B1Point = self.FB1Line.intersects(self.BB1Line)[1] 
                    self.painter.setPen(QPen(Qt.gray, 3, Qt.DashLine))
                    self.BB1Line.setP1(col)
                    self.FB1Line.setP1(col)
                    self.painter.drawLines([self.BB1Line,self.FB1Line])

            elif self.BPoint.x() > self.wide/2 and  self.BPoint.y() > self.heigh/4:  # B в 4 четверти
                x = ((self.BPoint.x() - (self.wide/2)) * self.heigh/4)/(self.BPoint.y() - self.heigh/4)
                x = self.wide/2 - x
                self.painter.drawLine(self.BPoint.x(),self.BPoint.y(),int(x),int(1))

                self.BB1Line = QLineF(self.BPoint.x(),self.BPoint.y(),int(x),int(1))

                self.painter.drawLine(self.BPoint.x(),self.BPoint.y(),int(self.wide/2),int(self.BPoint.y()))
                b1 = (self.wide/2 - self.listOfDots[2].x())*(self.heigh/2-self.heigh/4)/(self.heigh/4 - self.BPoint.y())
                b1 = self.wide/2 - (self.wide/2 - self.listOfDots[2].x()) - b1
                self.painter.drawLine(int(self.wide/2),int(self.BPoint.y()),int(b1),int(self.heigh/2))

                self.FB1Line = QLineF(int(self.wide/2),int(self.BPoint.y()),int(b1),int(self.heigh/2))

                self.painter.setPen(QPen(Qt.black, 7, Qt.SolidLine))

                if self.FB1Line.intersects(self.BB1Line)[0] == QLineF.BoundedIntersection:
                    self.painter.drawPoint(self.FB1Line.intersects(self.BB1Line)[1]) # Находим пересечение
                    self.B1Point = self.FB1Line.intersects(self.BB1Line)[1] 
                    self.Is_Minmoe = False
                elif self.FB1Line.intersects(self.BB1Line)[0] == QLineF.UnboundedIntersection:
                    self.Is_Minmoe = True
                    col = self.FB1Line.intersects(self.BB1Line)[1]
                    self.painter.drawPoint(col)
                    self.B1Point = self.FB1Line.intersects(self.BB1Line)[1] 
                    self.painter.setPen(QPen(Qt.gray, 3, Qt.DashLine))
                    self.BB1Line.setP1(col)
                    self.FB1Line.setP1(col)
                    self.painter.drawLines([self.BB1Line,self.FB1Line])

            if self.BPoint.y() == self.heigh/4 :
                self.B1Point = QPoint(int(self.A1Point.x()),int(self.heigh/4))

        # Рисуем линии
        

        self.painter.setPen(QPen(Qt.black, 3, Qt.SolidLine))
        if int(self.BPoint.y()) == int(self.heigh/4):
            self.painter.drawLine(int(self.A1Point.x()),int(self.A1Point.y()),int(self.A1Point.x()),int(self.heigh/4))
            if self.A1Point.y() < self.heigh/4:
                self.painter.drawLine(int(self.A1Point.x()-5),int(self.A1Point.y()+5),int(self.A1Point.x()),int(self.A1Point.y()))
                self.painter.drawLine(int(self.A1Point.x()),int(self.A1Point.y()),int(self.A1Point.x()+5),int(self.A1Point.y()+5))
            elif self.A1Point.y() > self.heigh/4:
                self.painter.drawLine(int(self.A1Point.x()+5),int(self.A1Point.y()-5),int(self.A1Point.x()),int(self.A1Point.y()))
                self.painter.drawLine(int(self.A1Point.x()),int(self.A1Point.y()),int(self.A1Point.x()-5),int(self.A1Point.y()-5))
        else:
            self.painter.drawLine(int(self.B1Point.x()-10),int(self.B1Point.y()), int(self.B1Point.x()+10),int(self.B1Point.y()))
            self.painter.drawLine(self.A1Point,self.B1Point)
            if self.A1Point.y() - self.B1Point.y() < 0:
                self.painter.drawLine(int(self.A1Point.x()-5),int(self.A1Point.y()+5),int(self.A1Point.x()),int(self.A1Point.y()))
                self.painter.drawLine(int(self.A1Point.x()),int(self.A1Point.y()),int(self.A1Point.x()+5),int(self.A1Point.y()+5))
            elif self.A1Point.y() - self.B1Point.y() > 0:
                self.painter.drawLine(int(self.A1Point.x()+5),int(self.A1Point.y()-5),int(self.A1Point.x()),int(self.A1Point.y()))
                self.painter.drawLine(int(self.A1Point.x()),int(self.A1Point.y()),int(self.A1Point.x()-5),int(self.A1Point.y()-5))


            # Характеристика 1. Прямое/Перевёрнутое 2. Уменьш/Увелич 3. Действ/Мнимое 4. По одну/Разные стороны

        half = int(self.heigh/4)
            

        if (self.APoint.y() > half and self.A1Point.y() > half) or (self.APoint.y() < half and self.A1Point.y() < half):
            self.label1.setText("1. Прямое")
        else: self.label1.setText("1. Перевёрнутое")

        if QLineF(self.APoint,self.BPoint).length() > QLineF(self.A1Point,self.B1Point).length():
            self.label2.setText("2. Уменьш.")
        else: self.label2.setText("2. Увелич.")

        if self.Is_Minmoe:
            self.label3.setText("3. Мнимое")
        else: self.label3.setText("3. Действ.")

        if (self.APoint.x() < self.wide/2 and self.A1Point.x() < self.wide/2) or (self.APoint.x() > self.wide/2 and self.A1Point.x() > self.wide/2):
            self.label4.setText("4. По одну сторону")
        else: self.label4.setText("4. По разные стороны")




    def DrawGui(self):
        self.painter.drawLine(30,int(self.heigh/4),self.wide-30,int(self.heigh/4))
        self.painter.drawLine(int(self.wide/2),int(self.heigh/4)-50,int(self.wide/2),int(self.heigh/4)+50)

        # Стрелочки
        if self.LenseType == "O":
            self.painter.drawLine(int(self.wide/2)-10,int(self.heigh/4)+40,int(self.wide/2),int(self.heigh/4)+50)
            self.painter.drawLine(int(self.wide/2),int(self.heigh/4)+50,int(self.wide/2)+10,int(self.heigh/4)+40)

            self.painter.drawLine(int(self.wide/2)-10,int(self.heigh/4)-40,int(self.wide/2),int(self.heigh/4)-50)
            self.painter.drawLine(int(self.wide/2),int(self.heigh/4)-50,int(self.wide/2)+10,int(self.heigh/4)-40)
        elif self.LenseType == "I":
            self.painter.drawLine(int(self.wide/2)-10,int(self.heigh/4)+60,int(self.wide/2),int(self.heigh/4)+50)
            self.painter.drawLine(int(self.wide/2),int(self.heigh/4)+50,int(self.wide/2)+10,int(self.heigh/4)+60)

            self.painter.drawLine(int(self.wide/2)-10,int(self.heigh/4)-60,int(self.wide/2),int(self.heigh/4)-50)
            self.painter.drawLine(int(self.wide/2),int(self.heigh/4)-50,int(self.wide/2)+10,int(self.heigh/4)-60)
            


        self.painter.setPen(QPen(Qt.black, 7, Qt.SolidLine))
        self.painter.drawPoint(self.OPoint)
        for i in self.listOfDots:
            self.painter.drawPoint(i)
        self.painter.setPen(QPen(Qt.gray, 3, Qt.SolidLine))
        for i in self.listOfLittleDots:
            self.painter.drawPoint(i)
        for i in self.listOfDots:
            self.painter.setPen(QPen(Qt.black, 5, Qt.SolidLine))
            self.painter.drawText(QPoint(i.x()-5,i.y()+20),self.listOfSIgns[self.listOfDots.index(i)])
            #self.listOfSIgns[self.listOfDots.index(i)].move(i.x(),i.y()+10)
        self.painter.setPen(QPen(Qt.gray, 3, Qt.SolidLine))


    def resetButton(self):
        self.objX = 400
        self.objY = int(self.heigh/4)
        self.objX = 35
        self.x_slider.setValue(400)
        self.y_slider.setValue(int(self.heigh/4))
        self.y_offset.setValue(35)
    def RButton(self):
        RB = self.sender()
        if RB.text() == "Собирающая": 
            self.LenseType = "O"
        elif RB.text() == "Рассеевающая": 
            self.LenseType = "I"
    def changedValue(self):
        self.objX = self.x_slider.value()
    def changedValueY(self):
        self.objY = int(self.heigh/2 - self.y_slider.value())
    def changedValueOff(self):
        self.objHigh = self.y_offset.value()












def application():
    app = QApplication(sys.argv)
    window = Window()
    window.ui.show()
    window.dw.show()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    application()


    class Test:
