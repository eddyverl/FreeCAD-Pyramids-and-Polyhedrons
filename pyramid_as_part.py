"""
author: Eddy Verlinden, Genk Belgium
licence : MIT
"""

import math
import sys
from PySide import QtGui, QtCore



def horizontal_regular_polygon_vertexes(sidescount,radius,z):

    vertexes = []
    if radius != 0 :
        for i in range(0,sidescount+1):
            angle = 2 * math.pi * i / sidescount + math.pi/2
            vertex = (radius * math.cos(angle), radius * math.sin(angle), z)
            vertexes.append(vertex)
    else:
        vertex = (0,0,z)
        vertexes.append(vertex)

    return vertexes

        
def build_pyramid(sidescount,radius_bottom, radius_top, height):
    
    faces = []
    if radius_bottom != 0 or radius_top != 0:

        vertexes_bottom = horizontal_regular_polygon_vertexes(sidescount,radius_bottom,0)
        vertexes_top = horizontal_regular_polygon_vertexes(sidescount,radius_top,height)

        if radius_bottom != 0:
            polygon_bottom = Part.makePolygon(vertexes_bottom)
            face_bottom = Part.Face(polygon_bottom)
            faces.append(face_bottom)
        if radius_top != 0:    
            polygon_top = Part.makePolygon(vertexes_top)
            face_top = Part.Face(polygon_top)
            faces.append(face_top)

        for i in range(sidescount):            
            if radius_top == 0:
                vertexes_side=[vertexes_bottom[i],vertexes_bottom[i+1],vertexes_top[0],vertexes_bottom[i]]
            elif radius_bottom == 0:
                vertexes_side=[vertexes_bottom[0],vertexes_top[i+1],vertexes_top[i],vertexes_bottom[0]]
            else:
                vertexes_side=[vertexes_bottom[i],vertexes_bottom[i+1],vertexes_top[i+1],vertexes_top[i],vertexes_bottom[i]]
            polygon_side=Part.makePolygon(vertexes_side)
            faces.append(Part.Face(polygon_side))

        shell = Part.makeShell(faces)   
        solid = Part.makeSolid(shell)
        obj=App.ActiveDocument.addObject("Part::Feature","Pyramid")
        obj.Shape = solid

def msgbox(s):
	msg = QtGui.QMessageBox()
	msg.setIcon(QtGui.QMessageBox.Information)
	msg.setText(s)
	msg.setWindowTitle("Message")
	msg.setStandardButtons(QtGui.QMessageBox.Ok )	
	retval = msg.exec_()



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
			msgbox("INPUT ERROR!")

		else :
			angle_center = 2 * math.pi / n
			if sideb != 0 :
				radiusb = (sideb/2) / math.cos ((math.pi - angle_center) / 2)
			if sidet != 0 :
				radiust = (sidet/2) / math.cos ((math.pi - angle_center) / 2)
	
			build_pyramid(n,radiusb,radiust,height)
			self.close()

	def cancel_method(self):
		self.close()
        

mainaction = PyramidDialog()

