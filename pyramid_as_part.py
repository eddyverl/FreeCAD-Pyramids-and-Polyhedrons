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

def say(s):
		FreeCAD.Console.PrintMessage(str(s)+"\n")

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


gen_pyramidenstumpf(5,0,25,30)
