#   Based on an early version of pyramidenstumpf.FCMacro
#   Added: real pyramids (with a point on top/bottom)
#   Added: an input form to enter the data of the pyramid

#*****#**********************************************************************
#*                                                                         *
#*   Copyright (c) 2014                                                    *  
#*   Thomas Gundermann <thomas@freecadbuch.de>                             * 
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)    *
#*   as published by the Free Software Foundation; either version 2 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   This program is distributed in the hope that it will be useful,       *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Library General Public License for more details.                  *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with this program; if not, write to the Free Software   *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *
#*                                                                         *
#***************************************************************************



import math
from math import sqrt, pi, sin, cos, asin

import sys
from PySide import QtGui, QtCore


def say(s):
	#FreeCAD.Console.PrintMessage(str(s)+"\n")
	msg = QtGui.QMessageBox()

	msg.setIcon(QtGui.QMessageBox.Information)
	
	msg.setText(s)
	msg.setInformativeText("This is additional information")
	msg.setWindowTitle("Message")
	msg.setDetailedText("The details are as follows:")
	msg.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
	#msg.buttonClicked.connect(msgbtn)
	
	retval = msg.exec_()


def vieleck(anz,size,hoehe): # regelmaesiges vieleck berechnen
	list1=[]
	for p in range(anz):
		if size != 0 :
			punkt=( size*cos(2*math.pi *p/anz),size*sin(2*math.pi*p/anz),hoehe)
		else:
			punkt= (0,0,hoehe)
		list1.append(punkt)
		#say(punkt)
	
	p=0
	if size != 0 :
		punkt=( size*cos(2*math.pi *p/anz),size*sin(2*math.pi*p/anz),hoehe)
	else:
		punkt= (0,hoehe)
	list1.append(punkt)
	#say(list1)
	return list1


def gen_pyramidenstumpf(count=8,size_bottom = 60, size_top=20, height=60):
	if size_bottom != 0 or size_top !=0 : 
		list1=vieleck(count,size_bottom,0)
		list2=vieleck(count,size_top,height)
		
		if size_bottom != 0 and size_top != 0:
			poly1 = Part.makePolygon( list1)
			face1 = Part.Face(poly1)
			poly2 = Part.makePolygon( list2)
			face2 = Part.Face(poly2)
			faceListe=[face1,face2]
		elif size_top != 0:
			poly2 = Part.makePolygon( list2)
			face2 = Part.Face(poly2)
			faceListe=[face2]
		else:    
			poly1 = Part.makePolygon( list1)
			face1 = Part.Face(poly1)
			faceListe=[face1]
		
		for i in range(len(list1)-1):
			if size_top == 0:
				liste3=[list1[i],list1[i+1],list2[i],list1[i]]
			elif size_bottom == 0:
				liste3=[list1[i],list2[i+1],list2[i],list1[i]]
			else:
				liste3=[list1[i],list1[i+1],list2[i+1],list2[i],list1[i]]

			poly=Part.makePolygon(liste3)
			face = Part.Face(poly)
			faceListe.append(face)
			#say(i);say(poly);say(faceListe)
		
		myShell = Part.makeShell(faceListe)   
		mySolid = Part.makeSolid(myShell)

		obj=App.ActiveDocument.addObject("Part::Feature","Pymf")
		obj.Shape = mySolid

#gen_pyramidenstumpf(5,50,25,20)   #testexample




class PyramidDialog(QtGui.QWidget):

	def __init__(self):
		super(PyramidDialog, self).__init__()
        
		self.initUI()
        
	def initUI(self): 
		grid = QtGui.QGridLayout()

		button = QtGui.QPushButton('Cancel')
		grid.addWidget(button, 10, 3)
		button.clicked.connect(self.cancel_method)
		button2 = QtGui.QPushButton('OK')
		grid.addWidget(button2, 10, 5)
		button2.clicked.connect(self.slot_method)

		grid.addWidget(QtGui.QLabel('sides count :'), 0, 2)
		self.count = QtGui.QLineEdit()
		self.count.setMinimumWidth(50)
		self.count.setMaximumWidth(50)
		grid.addWidget(self.count, 0,3)

		grid.addWidget(QtGui.QLabel('height :'), 1, 2)
		self.height = QtGui.QLineEdit()
		grid.addWidget(self.height,1,3)


		grid.addWidget(QtGui.QLabel('Bottom :'), 2, 2)

		grid.addWidget(QtGui.QLabel('radius :'), 3, 2)
		self.radiusb = QtGui.QLineEdit()
		grid.addWidget(self.radiusb,3,3)

		grid.addWidget(QtGui.QLabel('or sidelength:'), 3, 4)
		self.sideb = QtGui.QLineEdit()
		grid.addWidget(self.sideb, 3,5)

		grid.addWidget(QtGui.QLabel('Top :'),4, 2)

		grid.addWidget(QtGui.QLabel('radius :'), 5, 2)
		self.radiust = QtGui.QLineEdit()
		grid.addWidget(self.radiust, 5,3)

		grid.addWidget(QtGui.QLabel('or sidelength:'), 5, 4)
		self.sidet = QtGui.QLineEdit()
		grid.addWidget(self.sidet, 5,5)
		
		self.warninglabel = QtGui.QLabel('')
		grid.addWidget(self.warninglabel, 6, 2)


		self.setLayout(grid)   
		#self.setMinimumSize(300, 285)
		self.move(500, 350)
		self.setWindowTitle('Pyramid as FreeCad-Part')    
		self.show()


	def slot_method(self):
		if (str(self.count.text()))== "":
			n = 0
		else:
			n = int(float(str(self.count.text())))
		if (str(self.height.text()))== "":
			height = 0
		else:
			height = float(str(self.height.text()))
		if (str(self.radiusb.text()))== "":
			radiusb = 0
		else:
			radiusb = float(str(self.radiusb.text()))
		if (str(self.radiust.text()))== "":
			radiust = 0
		else:
			radiust = float(str(self.radiust.text()))
		if (str(self.sideb.text()))== "":
			sideb = 0
		else:
			sideb = float(str(self.sideb.text()))
		if (str(self.sidet.text()))== "":
			sidet = 0
		else:
			sidet = float(str(self.sidet.text()))

		if (n < 3) or ( radiusb == 0 and radiust == 0 and sideb == 0 and sidet == 0):
			say("INPUT ERROR!")

		else :
			angle_center = 2 * math.pi / n
			if sideb != 0 :
				radiusb = (sideb/2) / cos ((math.pi - angle_center) / 2)
			if sidet != 0 :
				radiust = (sidet/2) / cos ((math.pi - angle_center) / 2)
	
			#say(str(n) + "---" + str(height) + "---" + str(diamb) + "---" + str(diamt) + "---" + str(sideb) + "---"  + str(sidet))		
			gen_pyramidenstumpf(n,radiusb,radiust,height)
			self.close()

	def cancel_method(self):
		self.close()


        

mainaction = PyramidDialog()

