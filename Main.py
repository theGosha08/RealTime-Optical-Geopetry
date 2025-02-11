
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

        self.dwWide = self.wide # draw window Wide
        self.dwHigh = self.heigh/2

        self.dwxCenter = self.dwWide/2 # draw window x center
        self.dwyCenter = self.dwHigh/2 # draw window y center

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
        self.listOfDots = []
        for dot in range(4):
            self.listOfDots.append(QPoint(int(30+ (self.dwWide-(30*2))/4/2   +  (  (self.dwWide-(30*2))/4   )*dot),   int(self.dwyCenter)))

        self.listOfLittleDots = [] #маленькие серые точки нужны для красоты
        for dot in range(12):
            self.listOfLittleDots.append(QPoint(int(30+ (self.dwWide-(30*2))/12/2   +  (  (self.dwWide-(30*2))/12  )*dot),   int(self.dwyCenter)))
        #self.listOfDots = [QPoint(153,int(self.heigh/4)),QPoint(277,int(self.heigh/4)),QPoint(525,int(self.heigh/4)),QPoint(676,int(self.heigh/4))]
        #self.listOfLittleDots = [QPoint(92,int(self.heigh/4)),QPoint(215,int(self.heigh/4)),QPoint(337,int(self.heigh/4)),QPoint(462,int(self.heigh/4)),QPoint(616,int(self.heigh/4)),QPoint(738,int(self.heigh/4))]

        

    def paintEvent(self,event): 
        self.painter = QPainter(self)
        self.painter.setPen(QPen(Qt.black, 3, Qt.SolidLine))
        self.DrawGui()
        self.DrawLogic()
        self.painter.end()
        self.update()


    def DrawLogic(self):

        #Рисуем объект ОСЬ Y ИДЕТ СВЕРХУ ВНИЗ!!!!!!!!!!!
        
        self.APoint = QPoint(int(self.objX),int(self.objY-self.objHigh)) # верхушка объекта
        self.BPoint = QPoint(int(self.objX),int(self.objY)) # основание объекта


        self.DrawObj(self.APoint, self.BPoint) #рисуем объект

        self.painter.setPen(QPen(Qt.gray, 3, Qt.SolidLine))

        if self.LenseType == "O":
        # Изображение точки А1 и линий АА1, А-линза-F-A1
            
            if self.APoint.x() < self.dwxCenter and  self.APoint.y() < self.dwyCenter: #2 четверть
                x2 = ((self.dwxCenter - self.APoint.x()) * (self.dwyCenter))/(self.dwyCenter - self.APoint.y()) # x2 = (x1*y2)/y1
                x2 += self.dwxCenter

                self.AA1Line = QLineF(self.APoint.x(), self.APoint.y(), int(x2), int(self.dwHigh))# Рисуем луч от А через О
                self.painter.drawLine(self.AA1Line)

                self.painter.drawLine(self.APoint.x(), self.APoint.y(), int(self.dwxCenter), int(self.APoint.y())) # Рисуем отрезок от А до линзы
                a1 = ((self.listOfDots[2].x() - self.dwxCenter)*self.dwyCenter)/(self.dwyCenter - self.APoint.y()) # Xa1 = (Xf*Ya1)/Yf
                a1 += self.listOfDots[2].x()

                self.FA1Line = QLineF(int(self.dwxCenter), int(self.APoint.y()), int(a1), int(self.dwHigh))
                self.painter.drawLine(self.FA1Line) # Рисуем отрезок линзы от до a1 через F

                self.painter.setPen(QPen(Qt.black, 7, Qt.SolidLine))
            
                


            elif self.APoint.x() < self.dwxCenter and  self.APoint.y() > self.dwyCenter:#3 четверть

                x2 = ((self.dwxCenter - self.APoint.x()) * (self.dwyCenter))/(self.APoint.y() - self.dwyCenter) # x2 = (x1*y2)/y1
                x2 += self.dwxCenter

                self.AA1Line = QLineF(self.APoint.x(), self.APoint.y(), int(x2), int(1))# Рисуем луч от А через О
                self.painter.drawLine(self.AA1Line)

                self.painter.drawLine(self.APoint.x(), self.APoint.y(), int(self.dwxCenter), int(self.APoint.y())) # Рисуем отрезок от А до линзы
                a1 = ((self.listOfDots[2].x() - self.dwxCenter)*self.dwyCenter)/(self.APoint.y() - self.dwyCenter) # Xa1 = (Xf*Ya1)/Yf
                a1 += self.listOfDots[2].x()

                self.FA1Line = QLineF(int(self.dwxCenter), int(self.APoint.y()), int(a1), int(1))
                self.painter.drawLine(self.FA1Line) # Рисуем отрезок линзы от до a1 через F

                self.painter.setPen(QPen(Qt.black, 7, Qt.SolidLine))



            elif self.APoint.x() > self.wide/2 and  self.APoint.y() < self.heigh/4:  # 1 четверть

                x2 = (self.APoint.x() - self.dwxCenter) * (self.dwyCenter)/(self.dwyCenter - self.APoint.y()) # x2 = (x1*y2)/y1
                x2 = self.dwxCenter - x2

                self.AA1Line = QLineF(self.APoint.x(), self.APoint.y(), int(x2), int(self.dwHigh))# Рисуем луч от А через О
                self.painter.drawLine(self.AA1Line)

                self.painter.drawLine(self.APoint.x(), self.APoint.y(), int(self.dwxCenter), int(self.APoint.y())) # Рисуем отрезок от А до линзы
                a1 = ((self.dwxCenter - self.listOfDots[1].x()) * self.dwyCenter)/(self.dwyCenter - self.APoint.y()) # Xa1 = (Xf*Ya1)/Yf
                a1 = self.listOfDots[1].x() - a1

                self.FA1Line = QLineF(int(self.dwxCenter), int(self.APoint.y()), int(a1), int(self.dwHigh))
                self.painter.drawLine(self.FA1Line) # Рисуем отрезок линзы от до a1 через F

                self.painter.setPen(QPen(Qt.black, 7, Qt.SolidLine))


                

            elif self.APoint.x() > self.wide/2 and  self.APoint.y() > self.heigh/4:  # 4 четверть
                x2 = ((self.APoint.x() - self.dwxCenter) * (self.dwyCenter))/(self.APoint.y() - self.dwyCenter) # x2 = (x1*y2)/y1
                x2 = self.dwxCenter - x2

                self.AA1Line = QLineF(self.APoint.x(), self.APoint.y(), int(x2), int(1))# Рисуем луч от А через О
                self.painter.drawLine(self.AA1Line)

                self.painter.drawLine(self.APoint.x(), self.APoint.y(), int(self.dwxCenter), int(self.APoint.y())) # Рисуем отрезок от А до линзы
                a1 = ((self.dwxCenter - self.listOfDots[1].x()) * self.dwyCenter)/(self.APoint.y() - self.dwyCenter) # Xa1 = (Xf*Ya1)/Yf
                a1 = self.listOfDots[1].x() - a1

                self.FA1Line = QLineF(int(self.dwxCenter), int(self.APoint.y()), int(a1), int(0))
                self.painter.drawLine(self.FA1Line) # Рисуем отрезок линзы от до a1 через F

                self.painter.setPen(QPen(Qt.black, 7, Qt.SolidLine))






            #Определение пересечений и строительство линий если изображение мнимое

            if self.FA1Line.intersects(self.AA1Line)[0] == QLineF.BoundedIntersection: # Если линии пересекаются
                self.Is_Minmoe = False
                self.A1Point = self.FA1Line.intersects(self.AA1Line)[1] # Находим пересечение
                self.painter.drawPoint(self.A1Point)
            elif self.FA1Line.intersects(self.AA1Line)[0] == QLineF.UnboundedIntersection: # Если линии НЕ пересекаются (я не пишу else т.к линии могут быть паралельны!)
                self.Is_Minmoe = True
                self.A1Point = self.FA1Line.intersects(self.AA1Line)[1]
                #col = self.FA1Line.intersects(self.AA1Line)[1]
                self.painter.drawPoint(self.A1Point)
                #self.painter.drawPoint(self.FA1Line.intersects(self.AA1Line)[1])
                     
                self.painter.setPen(QPen(Qt.gray, 3, Qt.DashLine))
                self.AA1Line.setP1(self.A1Point)
                self.FA1Line.setP1(self.A1Point)
                self.painter.drawLines([self.AA1Line,self.FA1Line])

        
           
                    
            # Изображение точки В
            self.painter.setPen(QPen(Qt.gray, 3, Qt.SolidLine))

            if self.BPoint.x() < self.wide/2 and  self.BPoint.y() > self.heigh/4:
              
                x2 = ((self.dwxCenter - self.BPoint.x()) * (self.dwyCenter))/(self.BPoint.y() - self.dwyCenter) # x2 = (x1*y2)/y1
                x2 += self.dwxCenter

                self.BB1Line = QLineF(self.BPoint.x(), self.BPoint.y(), int(x2), int(1))# Рисуем луч от B через О
                self.painter.drawLine(self.BB1Line)

                self.painter.drawLine(self.BPoint.x(), self.BPoint.y(), int(self.dwxCenter), int(self.BPoint.y())) # Рисуем отрезок от B до линзы
                b1 = ((self.listOfDots[2].x() - self.dwxCenter)*self.dwyCenter)/(self.BPoint.y() - self.dwyCenter) # Xb1 = (Xf*Yb1)/Yf
                b1 += self.listOfDots[2].x()

                self.FB1Line = QLineF(int(self.dwxCenter), int(self.BPoint.y()), int(b1), int(1))
                self.painter.drawLine(self.FB1Line) # Рисуем отрезок линзы от до b1 через F

                self.painter.setPen(QPen(Qt.black, 7, Qt.SolidLine))

                

            elif self.BPoint.x() < self.wide/2 and  self.BPoint.y() < self.heigh/4:# В во 2 четтверти
                x2 = ((self.dwxCenter - self.BPoint.x()) * (self.dwyCenter))/(self.dwyCenter - self.BPoint.y()) # x2 = (x1*y2)/y1
                x2 += self.dwxCenter

                self.BB1Line = QLineF(self.BPoint.x(), self.BPoint.y(), int(x2), int(self.dwHigh))# Рисуем луч от B через О
                self.painter.drawLine(self.BB1Line)

                self.painter.drawLine(self.BPoint.x(), self.BPoint.y(), int(self.dwxCenter), int(self.BPoint.y())) # Рисуем отрезок от B до линзы
                b1 = ((self.listOfDots[2].x() - self.dwxCenter)*self.dwyCenter)/(self.dwyCenter - self.BPoint.y()) # Xb1 = (Xf*Yb1)/Yf
                b1 += self.listOfDots[2].x()

                self.FB1Line = QLineF(int(self.dwxCenter), int(self.BPoint.y()), int(b1), int(self.dwHigh))
                self.painter.drawLine(self.FB1Line) # Рисуем отрезок линзы от до b1 через F

                self.painter.setPen(QPen(Qt.black, 7, Qt.SolidLine))

                 



            elif self.BPoint.x() > self.wide/2 and  self.BPoint.y() < self.heigh/4:  # В в 1 четверти
                x2 = ((self.BPoint.x() - self.dwxCenter) * (self.dwyCenter))/(self.dwyCenter - self.BPoint.y()) # x2 = (x1*y2)/y1
                x2 = self.dwxCenter - x2

                self.BB1Line = QLineF(self.BPoint.x(), self.BPoint.y(), int(x2), int(self.dwHigh))# Рисуем луч от B через О
                self.painter.drawLine(self.BB1Line)

                self.painter.drawLine(self.BPoint.x(), self.BPoint.y(), int(self.dwxCenter), int(self.BPoint.y())) # Рисуем отрезок от B до линзы
                b1 = ((self.dwxCenter - self.listOfDots[1].x()) * self.dwyCenter)/(self.dwyCenter - self.BPoint.y()) # Xb1 = (Xf*Yb1)/Yf
                b1 = self.listOfDots[1].x() - b1

                self.FB1Line = QLineF(int(self.dwxCenter), int(self.BPoint.y()), int(b1), int(self.dwHigh))
                self.painter.drawLine(self.FB1Line) # Рисуем отрезок линзы от до b1 через F

                self.painter.setPen(QPen(Qt.black, 7, Qt.SolidLine))

                




            elif self.BPoint.x() > self.wide/2 and  self.BPoint.y() > self.heigh/4:  # B в 4 четверти

                x2 = ((self.BPoint.x() - self.dwxCenter) * (self.dwyCenter))/(self.BPoint.y() - self.dwyCenter) # x2 = (x1*y2)/y1
                x2 = self.dwxCenter - x2

                self.BB1Line = QLineF(self.BPoint.x(), self.BPoint.y(), int(x2), int(1))# Рисуем луч от B через О
                self.painter.drawLine(self.BB1Line)

                self.painter.drawLine(self.BPoint.x(), self.BPoint.y(), int(self.dwxCenter), int(self.BPoint.y())) # Рисуем отрезок от B до линзы
                b1 = ((self.dwxCenter - self.listOfDots[1].x()) * self.dwyCenter)/(self.BPoint.y() - self.dwyCenter) # Xb1 = (Xf*Yb1)/Yf
                b1 = self.listOfDots[1].x() - b1

                self.FB1Line = QLineF(int(self.dwxCenter), int(self.BPoint.y()), int(b1), int(0))
                self.painter.drawLine(self.FB1Line) # Рисуем отрезок линзы от до b1 через F

                self.painter.setPen(QPen(Qt.black, 7, Qt.SolidLine))


                #Определение пересечений и строительство линий если изображение мнимое

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
                x2 = ((self.dwxCenter - self.APoint.x()) * (self.dwyCenter))/(self.dwyCenter - self.APoint.y()) # x2 = (x1*y2)/y1
                x2 += self.dwxCenter

                self.AA1Line = QLineF(self.APoint.x(), self.APoint.y(), int(x2), int(self.dwHigh))# Рисуем луч от А через О
                self.painter.drawLine(self.AA1Line)

                self.painter.drawLine(self.APoint.x(), self.APoint.y(), int(self.dwxCenter), int(self.APoint.y())) # Рисуем отрезок от А до линзы
                a1 = ((self.listOfDots[1].x() - self.dwxCenter) * self.dwyCenter)/(self.APoint.y() - self.dwyCenter) # Xa1 = (Xf*Ya1)/Yf
                a1 += self.listOfDots[1].x()

                self.FA1Line = QLineF(int(self.dwxCenter), int(self.APoint.y()), int(a1), int(1))
                self.painter.drawLine(self.FA1Line) # Рисуем отрезок линзы от до a1 через F

                self.painter.setPen(QPen(Qt.black, 7, Qt.SolidLine))



            elif self.APoint.x() < self.wide/2 and  self.APoint.y() > self.heigh/4:#3 четверть
                x2 = ((self.dwxCenter - self.APoint.x()) * (self.dwyCenter))/(self.APoint.y() - self.dwyCenter) # x2 = (x1*y2)/y1
                x2 += self.dwxCenter

                self.AA1Line = QLineF(self.APoint.x(), self.APoint.y(), int(x2), int(1))# Рисуем луч от А через О
                self.painter.drawLine(self.AA1Line)

                self.painter.drawLine(self.APoint.x(), self.APoint.y(), int(self.dwxCenter), int(self.APoint.y())) # Рисуем отрезок от А до линзы
                a1 = ((self.listOfDots[1].x() - self.dwxCenter) * self.dwyCenter)/(self.dwyCenter - self.APoint.y()) # Xa1 = (Xf*Ya1)/Yf
                a1 += self.listOfDots[1].x()

                self.FA1Line = QLineF(int(self.dwxCenter), int(self.APoint.y()), int(a1), int(self.dwHigh))
                self.painter.drawLine(self.FA1Line) # Рисуем отрезок линзы от до a1 через F

                self.painter.setPen(QPen(Qt.black, 7, Qt.SolidLine))



            elif self.APoint.x() > self.wide/2 and  self.APoint.y() < self.heigh/4:  # 1 четверть
                
                x2 = ((self.APoint.x() - self.dwxCenter) * (self.dwyCenter))/(self.dwyCenter - self.APoint.y())  # x2 = (x1*y2)/y1
                x2 = self.dwxCenter - x2

                self.AA1Line = QLineF(self.APoint.x(), self.APoint.y(), int(x2), int(self.dwHigh))# Рисуем луч от А через О
                self.painter.drawLine(self.AA1Line)

                self.painter.drawLine(self.APoint.x(), self.APoint.y(), int(self.dwxCenter), int(self.APoint.y())) # Рисуем отрезок от А до линзы
                a1 = ((self.dwxCenter - self.listOfDots[2].x()) * self.dwyCenter)/(self.APoint.y() - self.dwyCenter) # Xa1 = (Xf*Ya1)/Yf
                a1 = self.listOfDots[2].x() - a1

                self.FA1Line = QLineF(int(self.dwxCenter), int(self.APoint.y()), int(a1), int(0))
                self.painter.drawLine(self.FA1Line) # Рисуем отрезок линзы от до a1 через F

                self.painter.setPen(QPen(Qt.black, 7, Qt.SolidLine))



            elif self.APoint.x() > self.wide/2 and  self.APoint.y() > self.heigh/4:  # 4 четверть

                x2 = ((self.APoint.x() - self.dwxCenter) * (self.dwyCenter))/(self.APoint.y() - self.dwyCenter)  # x2 = (x1*y2)/y1
                x2 = self.dwxCenter - x2

                self.AA1Line = QLineF(self.APoint.x(), self.APoint.y(), int(x2), int(1))# Рисуем луч от А через О
                self.painter.drawLine(self.AA1Line)

                self.painter.drawLine(self.APoint.x(), self.APoint.y(), int(self.dwxCenter), int(self.APoint.y())) # Рисуем отрезок от А до линзы
                a1 = ((self.dwxCenter - self.listOfDots[2].x()) * self.dwyCenter)/(self.dwyCenter - self.APoint.y()) # Xa1 = (Xf*Ya1)/Yf
                a1 = self.listOfDots[2].x() - a1

                self.FA1Line = QLineF(int(self.dwxCenter), int(self.APoint.y()), int(a1), int(self.dwHigh))
                self.painter.drawLine(self.FA1Line) # Рисуем отрезок линзы от до a1 через F

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

            if self.BPoint.x() < self.wide/2 and  self.BPoint.y() > self.heigh/4:# B в 3 четверти
                x2 = ((self.dwxCenter - self.BPoint.x()) * (self.dwyCenter))/(self.BPoint.y() - self.dwyCenter) # x2 = (x1*y2)/y1
                x2 += self.dwxCenter

                self.BB1Line = QLineF(self.BPoint.x(), self.BPoint.y(), int(x2), int(1))# Рисуем луч от B через О
                self.painter.drawLine(self.BB1Line)

                self.painter.drawLine(self.BPoint.x(), self.BPoint.y(), int(self.dwxCenter), int(self.BPoint.y())) # Рисуем отрезок от B до линзы
                b1 = ((self.listOfDots[1].x() - self.dwxCenter)*self.dwyCenter)/(self.dwyCenter - self.BPoint.y()) # Xb1 = (Xf*Yb1)/Yf
                b1 += self.listOfDots[1].x()

                self.FB1Line = QLineF(int(self.dwxCenter), int(self.BPoint.y()), int(b1), int(self.dwHigh))
                self.painter.drawLine(self.FB1Line) # Рисуем отрезок линзы от до b1 через F

                self.painter.setPen(QPen(Qt.black, 7, Qt.SolidLine))


                

            elif self.BPoint.x() < self.wide/2 and  self.BPoint.y() < self.heigh/4:# В во 2 четтверти
                
                x2 = ((self.dwxCenter - self.BPoint.x()) * (self.dwyCenter))/(self.dwyCenter - self.BPoint.y()) # x2 = (x1*y2)/y1
                x2 += self.dwxCenter

                self.BB1Line = QLineF(self.BPoint.x(), self.BPoint.y(), int(x2), int(self.dwHigh))# Рисуем луч от B через О
                self.painter.drawLine(self.BB1Line)

                self.painter.drawLine(self.BPoint.x(), self.BPoint.y(), int(self.dwxCenter), int(self.BPoint.y())) # Рисуем отрезок от B до линзы
                b1 = ((self.listOfDots[1].x() - self.dwxCenter)*self.dwyCenter)/(self.BPoint.y() - self.dwyCenter) # Xb1 = (Xf*Yb1)/Yf
                b1 += self.listOfDots[1].x()

                self.FB1Line = QLineF(int(self.dwxCenter), int(self.BPoint.y()), int(b1), int(1))
                self.painter.drawLine(self.FB1Line) # Рисуем отрезок линзы от до b1 через F

                self.painter.setPen(QPen(Qt.black, 7, Qt.SolidLine))

                

            elif self.BPoint.x() > self.wide/2 and  self.BPoint.y() < self.heigh/4:  # В в 1 четверти

                x2 = ((self.BPoint.x() - self.dwxCenter) * (self.dwyCenter))/(self.dwyCenter - self.BPoint.y()) # x2 = (x1*y2)/y1
                x2 = self.dwxCenter - x2

                self.BB1Line = QLineF(self.BPoint.x(), self.BPoint.y(), int(x2), int(self.dwHigh))# Рисуем луч от B через О
                self.painter.drawLine(self.BB1Line)

                self.painter.drawLine(self.BPoint.x(), self.BPoint.y(), int(self.dwxCenter), int(self.BPoint.y())) # Рисуем отрезок от B до линзы
                b1 = ((self.dwxCenter - self.listOfDots[2].x()) * self.dwyCenter)/(self.BPoint.y() - self.dwyCenter) # Xb1 = (Xf*Yb1)/Yf
                b1 = self.listOfDots[2].x() - b1

                self.FB1Line = QLineF(int(self.dwxCenter), int(self.BPoint.y()), int(b1), int(0))
                self.painter.drawLine(self.FB1Line) # Рисуем отрезок линзы от до b1 через F

                self.painter.setPen(QPen(Qt.black, 7, Qt.SolidLine))

                

            elif self.BPoint.x() > self.wide/2 and  self.BPoint.y() > self.heigh/4:  # B в 4 четверти
                x2 = ((self.BPoint.x() - self.dwxCenter) * (self.dwyCenter))/(self.BPoint.y() - self.dwyCenter) # x2 = (x1*y2)/y1
                x2 = self.dwxCenter - x2

                self.BB1Line = QLineF(self.BPoint.x(), self.BPoint.y(), int(x2), int(1))# Рисуем луч от B через О
                self.painter.drawLine(self.BB1Line)

                self.painter.drawLine(self.BPoint.x(), self.BPoint.y(), int(self.dwxCenter), int(self.BPoint.y())) # Рисуем отрезок от B до линзы
                b1 = ((self.dwxCenter - self.listOfDots[2].x()) * self.dwyCenter)/(self.dwyCenter - self.BPoint.y()) # Xb1 = (Xf*Yb1)/Yf
                b1 = self.listOfDots[2].x() - b1

                self.FB1Line = QLineF(int(self.dwxCenter), int(self.BPoint.y()), int(b1), int(self.dwHigh))
                self.painter.drawLine(self.FB1Line) # Рисуем отрезок линзы от до b1 через F

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
        
        self.DrawObj(self.A1Point,self.B1Point)

            # Характеристика 1. Прямое/Перевёрнутое 2. Уменьш/Увелич 3. Действ/Мнимое 4. По одну/Разные стороны

        half = int(self.dwyCenter)
            

        if (self.APoint.y() > half and self.A1Point.y() > half) or (self.APoint.y() < half and self.A1Point.y() < half):
            self.label1.setText("1. Прямое")
        else: self.label1.setText("1. Перевёрнутое")

        if QLineF(self.APoint,self.BPoint).length() > QLineF(self.A1Point,self.B1Point).length():
            self.label2.setText("2. Уменьш.")
        else: self.label2.setText("2. Увелич.")

        if self.Is_Minmoe:
            self.label3.setText("3. Мнимое")
        else: self.label3.setText("3. Действ.")

        if (self.APoint.x() < self.dwxCenter and self.A1Point.x() < self.wide/2) or (self.APoint.x() > self.dwxCenter and self.A1Point.x() > self.dwxCenter):
            self.label4.setText("4. По одну сторону")
        else: self.label4.setText("4. По разные стороны")




    def DrawGui(self):
        self.painter.drawLine(30,int(self.dwyCenter),self.wide-30,int(self.dwyCenter))#основная линия
        self.painter.drawLine(int(self.dwxCenter),int(self.dwyCenter)-50,int(self.dwxCenter),int(self.dwyCenter)+50)#Линза

        # Стрелочки у линзы
        if self.LenseType == "O":
            self.painter.drawLine(int(self.dwxCenter)-10,int(self.dwyCenter)+40,int(self.dwxCenter),int(self.dwyCenter)+50)
            self.painter.drawLine(int(self.dwxCenter),int(self.dwyCenter)+50,int(self.dwxCenter)+10,int(self.dwyCenter)+40)

            self.painter.drawLine(int(self.dwxCenter)-10,int(self.dwyCenter)-40,int(self.dwxCenter),int(self.dwyCenter)-50)
            self.painter.drawLine(int(self.dwxCenter),int(self.dwyCenter)-50,int(self.dwxCenter)+10,int(self.dwyCenter)-40)
        elif self.LenseType == "I":
            self.painter.drawLine(int(self.dwxCenter)-10,int(self.dwyCenter)+60,int(self.dwxCenter),int(self.dwyCenter)+50)
            self.painter.drawLine(int(self.dwxCenter),int(self.dwyCenter)+50,int(self.dwxCenter)+10,int(self.dwyCenter)+60)

            self.painter.drawLine(int(self.dwxCenter)-10,int(self.dwyCenter)-60,int(self.dwxCenter),int(self.dwyCenter)-50)
            self.painter.drawLine(int(self.dwxCenter),int(self.dwyCenter)-50,int(self.dwxCenter)+10,int(self.dwyCenter)-60)
            


        self.painter.setPen(QPen(Qt.gray, 3, Qt.SolidLine))
        for i in self.listOfLittleDots:
            self.painter.drawPoint(i)

        self.painter.setPen(QPen(Qt.black, 7, Qt.SolidLine))
        self.painter.drawPoint(self.OPoint)
        for i in self.listOfDots:
            self.painter.drawPoint(i)
        
        for i in self.listOfDots:
            self.painter.setPen(QPen(Qt.black, 5, Qt.SolidLine))
            self.painter.drawText(QPoint(i.x()-5,i.y()+20),self.listOfSIgns[self.listOfDots.index(i)])
            #self.listOfSIgns[self.listOfDots.index(i)].move(i.x(),i.y()+10)
        self.painter.setPen(QPen(Qt.gray, 3, Qt.SolidLine))


    def resetButton(self):
        self.objX = 400
        self.objY = int(self.dwyCenter)
        self.objX = 35
        self.x_slider.setValue(400)
        self.y_slider.setValue(int(self.dwyCenter))
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
        self.objY = int(self.dwHigh - self.y_slider.value())
    def changedValueOff(self):
        self.objHigh = self.y_offset.value()

    def DrawObj(self, A = QPoint(),B = QPoint(), h = None):

        self.painter.setPen(QPen(Qt.black, 3, Qt.SolidLine))
        self.painter.drawLine(A,B)
        x = int(A.x())
        y = int(B.y())
        h = int(B.y() - A.y())
        # стрелочка у объекта
        if h < 0:
            self.painter.drawLine(x-5, y-h-5, x, y-h)
            self.painter.drawLine(x, y-h, x+5, y-h-5)
        elif h > 0:
            self.painter.drawLine(x-5, y-h+5, x, y-h)
            self.painter.drawLine(x, y-h, x+5, y-h+5)

        # дно объекта
        self.painter.drawLine(x-5, y, x+5, y)
        












def application():
    app = QApplication(sys.argv)
    window = Window()
    window.ui.show()
    window.dw.show()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    application()


    #class Test:
