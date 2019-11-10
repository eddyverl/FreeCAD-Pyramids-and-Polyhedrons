# ***************************************************************************
# *   Copyright (c) 2019  Eddy Verlinden                                    *   
# *                                                                         *
# *   This file is part of the FreeCAD CAx development system.              *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# *   FreeCAD is distributed in the hope that it will be useful,            *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU Lesser General Public License for more details.                   *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with FreeCAD; if not, write to the Free Software        *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# *                                                                         *
# ***************************************************************************

import FreeCAD,FreeCADGui
import Part
import math
import sys


def horizontal_regular_polygon_vertexes(sidescount,radius,z, startangle = 0):
    vertexes = []
    if radius != 0 :
        for i in range(0,sidescount+1):
            angle = 2 * math.pi * i / sidescount + math.pi + startangle
            vertex = (radius * math.cos(angle), radius * math.sin(angle), z)
            vertexes.append(vertex)
    else:
        vertex = (0,0,z)
        vertexes.append(vertex)
    return vertexes



class Pyramid:
    
    radius1value = 0
    radius2value = 0
    sidescountvalue = 0
    side1value = 0
    side2value = 0
    
    def __init__(self, obj, sidescount = 5,radius_bottom = 2 , radius_top = 4, height = 10):
        obj.addProperty("App::PropertyLength","Radius1","Pyramid","Radius of the pyramid").Radius1=radius_bottom
        obj.addProperty("App::PropertyLength","Radius2","Pyramid","Radius of the pyramid").Radius2=radius_top
        obj.addProperty("App::PropertyLength","Height","Pyramid","Height of the pyramid").Height = height
        obj.addProperty("App::PropertyInteger","Sidescount","Pyramid","Sidescount of the pyramid").Sidescount = sidescount
        obj.addProperty("App::PropertyLength","Sidelength1","Pyramid","Sidelength1 of the pyramid")
        obj.addProperty("App::PropertyLength","Sidelength2","Pyramid","Sidelength2 of the pyramid")
        obj.Proxy = self

        
    def execute (self,obj):
              
        sidescount = obj.Sidescount
        angle = 2 * math.pi / sidescount
        radius_bottom = obj.Radius1
        radius_top = obj.Radius2
        height = obj.Height
        
        
        if radius_bottom != self.radius1value: # or sidescount != self.sidescountvalue
            obj.Sidelength1 = radius_bottom * math.sin(angle/2) * 2
            self.radius1value = radius_bottom
            self.side1value = obj.Sidelength1
        elif obj.Sidelength1 != self.side1value:
            self.radius1value = (obj.Sidelength1 / 2) / math.sin(angle/2) 
            obj.Radius1 = self.radius1value
            radius_bottom = self.radius1value
            side1value = obj.Sidelength1

        if radius_top != self.radius2value :  #or sidescount != self.sidescountvalue
            obj.Sidelength2 = radius_top * math.sin(angle/2) * 2
            self.radius2value = radius_top
            self.side2value = obj.Sidelength2
        elif obj.Sidelength2 != self.side2value:
            self.radius2value = (obj.Sidelength2 / 2) / math.sin(angle/2) 
            obj.Radius2 = self.radius2value
            radius_top = self.radius2value
            side2value = obj.Sidelength2

        faces = []
        if radius_bottom == 0 and radius_top == 0:
            FreeCAD.Console.PrintMessage("Both radiuses are zero" + "\n")
        else:
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
            obj.Shape = solid
        
            

# ===========================================================================    

class ViewProviderBox:
    def __init__(self, obj):
        obj.Proxy = self

    def attach(self, obj):
        return

    def updateData(self, fp, prop):
        return

    def getDisplayModes(self,obj):
        return "As Is"
        
    def getDefaultDisplayMode(self):
        return "As Is"

    def setDisplayMode(self,mode):
        return "As Is"

    def onChanged(self, vobj, prop):
        pass

    def getIcon(self):
        return str(FreeCAD.getUserAppDataDir())+'Mod' + '/polyhedrons/resources/icons/pyramid.svg'

# ===========================================================================    

obj=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","Pyramid")   # see https://www.freecadweb.org/wiki/Creating_a_FeaturePython_Box,_Part_II
Pyramid(obj)
ViewProviderBox(obj.ViewObject)  
FreeCAD.ActiveDocument.recompute()
