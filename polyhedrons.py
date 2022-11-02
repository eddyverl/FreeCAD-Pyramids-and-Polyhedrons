# ***************************************************************************
# *   Copyright (c) 2019  Eddy Verlinden , Genk Belgium   (eddyverl)        *   
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

# Based on examples at : https://www.freecadweb.org/wiki/Workbench_creation

# Version 01.07




# Version 01.02  (2020-01-15)
# added geodesic sphere

# version 01.03   (2020-01-23)
# added hexahedron  (cube)

# version 01.04  (2020-01-30)
# renamed Mod to Pyramids-and-Polyhedrons

# version 01.05  (2020-02-24)
# Side of icosahedron_truncated was side of icosahedron -> corrected

# version 01.06  (2020-12-21)
# Pyramids are rotatable around the z-axis and start parallel to the x-axis

# version 01.07  (2020-12-26)
# Some namechanges

# version 01.07a (2020-12-30)
# flexibility for installation folder

# version 01.07b (2020-01-02)
# icosahedron_truncated : now radius of the result, not of the base icosahedron



import FreeCAD,FreeCADGui
import Part
import math
import sys
from FreeCAD import Base

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



def horizontal_regular_pyramid_vertexes(sidescount,radius,z, anglez = 0): # anglez in degrees
    vertexes = []
    odd = 0
    if (sidescount % 2) == 0:
        odd = 1
    if radius != 0 :
        for i in range(0,sidescount+1):
            angle = 2 * math.pi * i / sidescount + (math.pi * (odd/sidescount + 1/2)) + anglez * math.pi / 180
            vertex = (radius * math.cos(angle), radius * math.sin(angle), z)
            vertexes.append(vertex)
    else:
        vertex = (0,0,z)
        vertexes.append(vertex)
    return vertexes


def getWorkbenchFolder():

    import os.path
    from os import path
    
    import workbenchfolders
    
    basedir = str(FreeCAD.getUserAppDataDir())
    folder = ""
    
    for tryfolder in workbenchfolders.recommended_folders:
            if path.exists(basedir + tryfolder):
                    folder = basedir + tryfolder
                    return folder
    
    for tryfolder in workbenchfolders.user_chosen_folders:
            if path.exists(basedir + tryfolder):
                    folder = basedir + tryfolder
                    return folder
            if path.exists(tryfolder):
                    folder = tryfolder
                    return folder
                    
    return ""
        
        
 

# ===========================================================================    

class ViewProviderBox:
    
    obj_name = "Dodecahedron"
    
    def __init__(self, obj, obj_name):
        self.obj_name = obj_name
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
        #return str(FreeCAD.getUserAppDataDir()) + 'Mod' + '/Pyramids-and-Polyhedrons/Resources/Icons/' + (self.obj_name).lower() + '.svg'
        return getWorkbenchFolder() + "/Resources/Icons/' + (self.obj_name).lower() + '.svg'"
        
    def __getstate__(self):
        return None

    def __setstate__(self,state):
        return None
       
# ===========================================================================    

class Pyramid:
 
    radius1value = 0
    radius2value = 0
    sidescountvalue = 0
    side1value = 0
    side2value = 0
    anglez = 0

    def __init__(self, obj, sidescount = 5,radius_bottom = 2 , radius_top = 4, height = 10, angz = 0):
        obj.addProperty("App::PropertyLength","Radius1","Pyramid","Radius of the pyramid").Radius1=radius_bottom
        obj.addProperty("App::PropertyLength","Radius2","Pyramid","Radius of the pyramid").Radius2=radius_top
        obj.addProperty("App::PropertyLength","Height","Pyramid","Height of the pyramid").Height = height
        obj.addProperty("App::PropertyInteger","Sidescount","Pyramid","Sidescount of the pyramid").Sidescount = sidescount
        obj.addProperty("App::PropertyLength","Sidelength1","Pyramid","Sidelength1 of the pyramid")
        obj.addProperty("App::PropertyLength","Sidelength2","Pyramid","Sidelength2 of the pyramid")
        obj.addProperty("App::PropertyAngle","Z_rotation","Pyramid","alfa angle around Z").Z_rotation = angz

        obj.Proxy = self

        
    def execute (self,obj):
              
        sidescount = int(obj.Sidescount)
        angle = 2 * math.pi / sidescount
        radius_bottom = float(obj.Radius1)
        radius_top = float(obj.Radius2)
        sidelength_top = float(obj.Sidelength2)
        sidelength_bottom = float(obj.Sidelength1)
        height = float(obj.Height)
        anglez = float(obj.Z_rotation)

        if radius_bottom != self.radius1value or sidescount != self.sidescountvalue:
            obj.Sidelength1 = radius_bottom * math.sin(angle/2) * 2
            self.radius1value = radius_bottom
            self.side1value = float(obj.Sidelength1)
        elif sidelength_bottom != self.side1value:
            self.radius1value = float(obj.Sidelength1 / 2) / math.sin(angle/2) 
            obj.Radius1 = self.radius1value
            radius_bottom = self.radius1value
            self.side1value = float(obj.Sidelength1)

        if radius_top != self.radius2value or sidescount != self.sidescountvalue: 
            obj.Sidelength2 = radius_top * math.sin(angle/2) * 2
            self.radius2value = float(radius_top)
            self.side2value = float(obj.Sidelength2)
        elif sidelength_top != self.side2value:
            self.radius2value = float(obj.Sidelength2 / 2) / math.sin(angle/2) 
            obj.Radius2 = self.radius2value
            radius_top = self.radius2value
            self.side2value = float(obj.Sidelength2)
            
        self.sidescountvalue = sidescount
        faces = []
        if radius_bottom == 0 and radius_top == 0:
            FreeCAD.Console.PrintMessage("Both radiuses are zero" + "\n")
        else:
            vertexes_bottom = horizontal_regular_pyramid_vertexes(sidescount,radius_bottom,0     ,anglez)
            vertexes_top    = horizontal_regular_pyramid_vertexes(sidescount,radius_top   ,height,anglez)

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
        
class PyramidCommand:
    
    def GetResources(self):
        return {'Pixmap'  : getWorkbenchFolder() + '/Resources/Icons/pyramid.svg',
                'Accel' : "Shift+P", 
                'MenuText': "Pyramid",
                'ToolTip' : "Generate a Pyramid with any number of sides"}

    def Activated(self):
        obj=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","Pyramid")   # see https://www.freecadweb.org/wiki/Creating_a_FeaturePython_Box,_Part_II
        Pyramid(obj)
        ViewProviderBox(obj.ViewObject, "Pyramid") 
        #obj.ViewObject.Proxy=0            
        FreeCAD.ActiveDocument.recompute()
        FreeCADGui.SendMsgToActiveView("ViewFit")
        return

        
    def IsActive(self):
        if FreeCAD.ActiveDocument == None:
               return False
        else:
               return True

FreeCADGui.addCommand('Pyramid',PyramidCommand())


# ===========================================================================    
    
class Tetrahedron:
        # == basics ==
        #R = z / 4 * sqrt(6)
        #ro = z / 12 * sqrt(6)    -->   ro = R / 3
        #z = 4 * R / sqrt(6)
        #h = z / 3 * sqrt(6) = 4 * R / sqrt(6) /3 * sqrt(6) = 4 * R / 3  = ro + R 
        #radius at level = z / 2 / cos(30) = (4 * R / sqrt(6)) / 2 / sqrt(3) * 2 = 4 * R / (sqrt(6) * sqrt(3))= 4 * R / (3 * sqrt(2)
        
    radiusvalue = 0    
    def __init__(self, obj, radius=5):
        obj.addProperty("App::PropertyLength","Radius","Tetrahedron","Radius of the tetrahedron").Radius=radius
        obj.addProperty("App::PropertyLength","Side","Tetrahedron","Sidelength of the tetrahedron")
        obj.Proxy = self

        
    def execute (self,obj):

        radius = float(obj.Radius)
        if (radius != self.radiusvalue):
            obj.Side = radius * 4 / math.sqrt(6)
            self.radiusvalue = radius
        else:
            self.radiusvalue = float(obj.Side * math.sqrt(6) / 4)
            obj.Radius = self.radiusvalue
            radius = self.radiusvalue
            
        faces = []        
        vertexes_bottom = horizontal_regular_polygon_vertexes(3,4*radius/3/math.sqrt(2),- radius / 3)
        vertexes_top    = horizontal_regular_polygon_vertexes(1,0,radius)
        
        for i in range(3):
            vertexes_side=[vertexes_bottom[i],vertexes_bottom[i+1],vertexes_top[0],vertexes_bottom[i]]
            polygon_side=Part.makePolygon(vertexes_side)
            faces.append(Part.Face(polygon_side))

        polygon_bottom=Part.makePolygon(vertexes_bottom)
        
        faces.append(Part.Face(polygon_bottom))
        shell = Part.makeShell(faces)
        solid = Part.makeSolid(shell)
        obj.Shape = solid
        

class TetrahedronCommand:
    
    def GetResources(self):
        return {'Pixmap'  : getWorkbenchFolder() + '/Resources/Icons/tetrahedron.svg',
                'Accel' : "Shift+T", 
                'MenuText': "Tetrahedron",
                'ToolTip' : "Generate a Tetrahedron"}

    def Activated(self):
        obj=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","Tetrahedron")
        Tetrahedron(obj)
        #obj.ViewObject.Proxy=0
        ViewProviderBox(obj.ViewObject, "Tetrahedron") 
        FreeCAD.ActiveDocument.recompute()
        FreeCADGui.SendMsgToActiveView("ViewFit")
        return
        
    def IsActive(self):
        if FreeCAD.ActiveDocument == None:
               return False
        else:
               return True
        

FreeCADGui.addCommand('Tetrahedron',TetrahedronCommand())

# ===========================================================================    

class Hexahedron: 
 
    radiusvalue = 0  
    
    def __init__(self, obj, radius=5):
        obj.addProperty("App::PropertyLength","Radius","Hexahedron","Radius of the hexahedron").Radius=radius
        obj.addProperty("App::PropertyLength","Side","Hexahedron","Sidelength of the hexahedron")
        obj.Proxy = self

    def execute(self, obj):
            
        radius = float(obj.Radius) 
        if (radius != self.radiusvalue):
            side = radius * 2 / math.sqrt(3)
            obj.Side = side
            self.radiusvalue = radius
        else:
            self.radiusvalue = obj.Side / 2 * math.sqrt(3)
            obj.Radius = self.radiusvalue
            radius = self.radiusvalue
            side = obj.Side       
             
        faces = []
        vertexes_bottom = horizontal_regular_polygon_vertexes(4,math.sqrt(side ** 2 / 2),- side/2, math.pi/4)
        vertexes_top    = horizontal_regular_polygon_vertexes(4,math.sqrt(side ** 2 / 2), side/2, math.pi/4)

        for i in range(4):
            vertexes_side=[vertexes_bottom[i],vertexes_bottom[i+1],vertexes_top[i+1],vertexes_top[i],vertexes_bottom[i]]
            polygon_side=Part.makePolygon(vertexes_side)
            faces.append(Part.Face(polygon_side))

        polygon_bottom=Part.makePolygon(vertexes_bottom)
        faces.append(Part.Face(polygon_bottom))
        
        polygon_top=Part.makePolygon(vertexes_top)
        faces.append(Part.Face(polygon_top))

        shell = Part.makeShell(faces)
        solid = Part.makeSolid(shell)
        obj.Shape = solid        
        
        
class HexahedronCommand:
    
    def GetResources(self):
        return {'Pixmap'  : getWorkbenchFolder() + '/Resources/Icons/hexahedron.svg',
                'Accel' : "Shift+H", 
                'MenuText': "Hexahedron",
                'ToolTip' : "Generate a Hexahedron"}

    def Activated(self):
        obj=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","Hexahedron")
        Hexahedron(obj)
        #obj.ViewObject.Proxy=0
        ViewProviderBox(obj.ViewObject, "Hexahedron") 
        FreeCAD.ActiveDocument.recompute()
        FreeCADGui.SendMsgToActiveView("ViewFit")
        return
        
    def IsActive(self):
        if FreeCAD.ActiveDocument == None:
               return False
        else:
               return True
        

FreeCADGui.addCommand('Hexahedron',HexahedronCommand())        
# ===========================================================================    

class Octahedron: 
    # Z = R * sqrt(2)   
    radiusvalue = 0  
    
    def __init__(self, obj, radius=5):
        obj.addProperty("App::PropertyLength","Radius","Octahedron","Radius of the octahedron").Radius=radius
        obj.addProperty("App::PropertyLength","Side","Octahedron","Sidelength of the octahedron")
        obj.Proxy = self
  
    def execute (self,obj):

        radius = float(obj.Radius)
        if (radius != self.radiusvalue):
            obj.Side = radius * math.sqrt(2)
            self.radiusvalue = radius
        else:
            self.radiusvalue = float(obj.Side / math.sqrt(2))
            obj.Radius = self.radiusvalue
            radius = self.radiusvalue
            
 

        faces = []
        vertexes_middle = horizontal_regular_polygon_vertexes(4,radius,0)
        vertexes_bottom = horizontal_regular_polygon_vertexes(1,0,-radius)
        vertexes_top    = horizontal_regular_polygon_vertexes(1,0,radius)

        for i in range(4):
            vertexes_side=[vertexes_middle[i],vertexes_middle[i+1],vertexes_top[0],vertexes_middle[i]]
            polygon_side=Part.makePolygon(vertexes_side)
            faces.append(Part.Face(polygon_side))

        for i in range(4):
            vertexes_side=[vertexes_middle[i],vertexes_middle[i+1],vertexes_bottom[0],vertexes_middle[i]]
            polygon_side=Part.makePolygon(vertexes_side)
            faces.append(Part.Face(polygon_side))

        shell = Part.makeShell(faces)
        solid = Part.makeSolid(shell)
        obj.Shape = solid

  
class OctahedronCommand:
        
    def GetResources(self):
        return {'Pixmap'  : getWorkbenchFolder() + '/Resources/Icons/octahedron.svg',
                'Accel' : "Shift+O",
                'MenuText': "Octahedron",
                'ToolTip' : "Generate a Octahedron"}

    def Activated(self):
        obj=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","Octahedron")
        Octahedron(obj)
        #obj.ViewObject.Proxy=0
        ViewProviderBox(obj.ViewObject, "Octahedron") 
        FreeCAD.ActiveDocument.recompute()
        FreeCADGui.SendMsgToActiveView("ViewFit")
        return

        
    def IsActive(self):
        if FreeCAD.ActiveDocument == None:
               return False
        else:
               return True
                
FreeCADGui.addCommand('Octahedron',OctahedronCommand())

# ===========================================================================    
    
class Dodecahedron:
    
    radiusvalue = 0  
   
    def __init__(self, obj, radius=5):
        obj.addProperty("App::PropertyLength","Radius","Dodecahedron","Radius of the dodecahedron").Radius=radius
        obj.addProperty("App::PropertyLength","Side","Dodecahedron","Sidelength of the dodecahedron")
        obj.Proxy = self
    

    def execute (self,obj):
        
        angleribs = 121.717474411
        anglefaces = 116.565051177

        radius = float(obj.Radius)
        if (radius != self.radiusvalue):
            obj.Side = 4 * radius /  (math.sqrt(3) * ( 1 + math.sqrt(5)))
            self.radiusvalue = radius
        else:
            self.radiusvalue = float(obj.Side * (math.sqrt(3) * ( 1 + math.sqrt(5))) / 4)
            obj.Radius = self.radiusvalue
            radius = self.radiusvalue
            
        faces = []
        z = 4 * radius /  (math.sqrt(3) * ( 1 + math.sqrt(5)))
        r = z/2 * math.sqrt((25 + (11 * math.sqrt(5)))/10)
        # int sphere r is height / 2

        h2 = z * math.sin(angleribs/180 * math.pi)

        #height of the side-tips
        radius1 = z / 2 / math.sin(36 * math.pi / 180)
        h5h = (radius1 + radius1 * math.cos(36 * math.pi / 180))   * math.sin(anglefaces * math.pi / 180) #height of the tops

        radius2 = radius1 - z * math.cos(angleribs * math.pi / 180 )

        r=(h2 + h5h)/2  # XXX to make it fit!




        vertexes_bottom = horizontal_regular_polygon_vertexes(5,radius1,-r)
        vertexes_low = horizontal_regular_polygon_vertexes(5,radius2, -r + h2)
        vertexes_high = horizontal_regular_polygon_vertexes(5,radius2, -r + h5h,  math.pi/5)
        vertexes_top = horizontal_regular_polygon_vertexes(5,radius1, r, math.pi/5)

        polygon_bottom = Part.makePolygon(vertexes_bottom)
        face_bottom = Part.Face(polygon_bottom)
        faces.append(face_bottom)

        polygon_top = Part.makePolygon(vertexes_top)
        face_top = Part.Face(polygon_top)
        faces.append(face_top)

        for i in range(5):
            vertexes_side=[vertexes_bottom[i],vertexes_bottom[i+1],vertexes_low[i+1],vertexes_high[i],vertexes_low[i], vertexes_bottom[i] ]
            polygon_side=Part.makePolygon(vertexes_side)
            faces.append(Part.Face(polygon_side))

        for i in range(5):
            #vertexes_side=[vertexes_top[i],vertexes_top[i+1],vertexes_high[i+1],vertexes_high2[i], vertexes_high[i],vertexes_top[i] ]
            vertexes_side=[vertexes_top[i],vertexes_top[i+1],vertexes_high[i+1],vertexes_low[i+1],vertexes_high[i],vertexes_top[i] ]
            polygon_side=Part.makePolygon(vertexes_side)
            faces.append(Part.Face(polygon_side))

        shell = Part.makeShell(faces)
        solid = Part.makeSolid(shell)
        obj.Shape = solid

class DodecahedronCommand:    
    def GetResources(self):
        return {'Pixmap'  : getWorkbenchFolder() + '/Resources/Icons/dodecahedron.svg',
                'Accel' : "Shift+D",
                'MenuText': "Dodecahedron",
                'ToolTip' : "Generate a Dodecahedron"}

    def Activated(self):
        obj=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","Dodecahedron")
        Dodecahedron(obj)
        #obj.ViewObject.Proxy=0
        ViewProviderBox(obj.ViewObject, "Dodecahedron")
        FreeCAD.ActiveDocument.recompute()
        FreeCADGui.SendMsgToActiveView("ViewFit")
        return

        
    def IsActive(self):
        if FreeCAD.ActiveDocument == None:
               return False
        else:
               return True

FreeCADGui.addCommand('Dodecahedron',DodecahedronCommand())

# ===========================================================================    

class Icosahedron:
    
    radiusvalue = 0  

    def __init__(self, obj, radius=5):
        obj.addProperty("App::PropertyLength","Radius","Icosahedron","Radius of the icosahedron").Radius=radius
        obj.addProperty("App::PropertyLength","Side","Icosahedron","Sidelength of the icosahedron")
        obj.Proxy = self


    def execute (self,obj):

        radius = float(obj.Radius)
        if (radius != self.radiusvalue):
            obj.Side = 4*radius / math.sqrt(10 + 2 * math.sqrt(5))
            self.radiusvalue = radius
        else:
            self.radiusvalue = float(obj.Side * math.sqrt(10 + 2 * math.sqrt(5)) / 4)
            obj.Radius = self.radiusvalue
            radius = self.radiusvalue
            

        z = 4*radius / math.sqrt(10 + 2 * math.sqrt(5))
        anglefaces = 138.189685104
        r = z/12 * math.sqrt(3) * (3 + math.sqrt(5))


        #radius of a pentagram with the same side
        radius2 = z / math.sin(36 * math.pi/180)/2
        #height of radius2 in the sphere

        angle = math.acos(radius2/radius)
        height = radius * math.sin(angle)

        faces = []

        vertex_bottom = (0,0,-radius)
        vertexes_low = horizontal_regular_polygon_vertexes(5,radius2, -height)
        vertexes_high = horizontal_regular_polygon_vertexes(5,radius2, height, math.pi/5)
        vertex_top = (0,0,radius)


        for i in range(5):
            vertexes_side=[vertex_bottom,vertexes_low[i],vertexes_low[i+1], vertex_bottom]
            polygon_side=Part.makePolygon(vertexes_side)
            faces.append(Part.Face(polygon_side))

        for i in range(5):
            vertexes_side=[vertexes_low[i],vertexes_low[i+1],vertexes_high[i],vertexes_low[i] ]
            polygon_side=Part.makePolygon(vertexes_side)
            faces.append(Part.Face(polygon_side))
            vertexes_side=[vertexes_high[i],vertexes_high[i+1],vertexes_low[i+1],vertexes_high[i] ]
            polygon_side=Part.makePolygon(vertexes_side)
            faces.append(Part.Face(polygon_side))

        for i in range(5):
            vertexes_side=[vertex_top,vertexes_high[i],vertexes_high[i+1],vertex_top ]
            polygon_side=Part.makePolygon(vertexes_side)
            faces.append(Part.Face(polygon_side))

        shell = Part.makeShell(faces)
        solid = Part.makeSolid(shell)
        obj.Shape = solid
   
class IcosahedronCommand:
    def GetResources(self):
        return {'Pixmap'  : getWorkbenchFolder() + '/Resources/Icons/icosahedron.svg',
                'Accel' : "Shift+I",
                'MenuText': "Icosahedron",
                'ToolTip' : "Generate a Icosahedron"}

    def Activated(self):
        obj=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","Icosahedron")
        Icosahedron(obj)
        #obj.ViewObject.Proxy=0
        ViewProviderBox(obj.ViewObject, "Icosahedron")
        FreeCAD.ActiveDocument.recompute()
        FreeCADGui.SendMsgToActiveView("ViewFit")
        return

        
    def IsActive(self):
        if FreeCAD.ActiveDocument == None:
               return False
        else:
               return True

FreeCADGui.addCommand('Icosahedron',IcosahedronCommand())

# ===========================================================================    

class Icosahedron_truncated:
    
    radiusvalue = 0  

    def __init__(self, obj, radius=5):
        obj.addProperty("App::PropertyLength","Radius","Icosahedron_truncated","Radius").Radius=radius
        obj.addProperty("App::PropertyLength","Side","Icosahedron_truncated","Sidelength")
        obj.Proxy = self

    def execute (self,obj):

        radius = float(obj.Radius) * 1.144  # correction for Icosohedron --> truncated
        if (radius != self.radiusvalue):
            obj.Side = 4*radius / math.sqrt(10 + 2 * math.sqrt(5)) / 3
            self.radiusvalue = radius
        else:
            self.radiusvalue = float(obj.Side * math.sqrt(10 + 2 * math.sqrt(5)) / 4) * 3
            obj.Radius = self.radiusvalue
            radius = self.radiusvalue

        
        z =  float(4*radius)  / math.sqrt(10 + 2 * math.sqrt(5)) # z of base icosahedron 
        anglefaces = 138.189685104
        r = z/12 * math.sqrt(3) * (3 + math.sqrt(5))

        #radius of a pentagram with the same side
        radius2 = z / math.sin(36 * math.pi/180)/2

        #height of radius2 in the sphere
        angle = math.acos(radius2/radius)
        height = radius * math.sin(angle) 

        faces = []
        
        vertex_bottom = (0,0,-radius)
        vertexes_low =  horizontal_regular_polygon_vertexes(5,radius2 , -height)
        vertexes_high = horizontal_regular_polygon_vertexes(5,radius2 , height ,  -math.pi/5)
        vertex_top = (0,0,radius) 

        vertexes_bottom = []
        vertexes_top = []

        for i in range(6):
            new_vertex = ((vertex_bottom[0]+vertexes_low[i][0])/3 , (vertex_bottom[1]+vertexes_low[i][1])/3 , vertex_bottom[2]-(vertex_bottom[2]-vertexes_low[i][2])/3)
            vertexes_bottom.append(new_vertex)
        polygon_side=Part.makePolygon(vertexes_bottom)
        faces.append(Part.Face(polygon_side))

        for i in range(6):
            new_vertex = ((vertex_top[0]+vertexes_high[i][0])/3 , (vertex_top[1]+vertexes_high[i][1])/3 , vertex_top[2]-(vertex_top[2]-vertexes_high[i][2])/3)
            vertexes_top.append(new_vertex)
        polygon_side=Part.makePolygon(vertexes_top)
        faces.append(Part.Face(polygon_side))

        pg6_bottom = []
        for i in range(5):
            vertex1=vertexes_bottom[i]
            vertex2=vertexes_bottom[i+1]
            vertex3=(vertexes_bottom[i+1][0] + (vertexes_low[i+1][0] - vertexes_bottom[i+1][0])/2, vertexes_bottom[i+1][1] + (vertexes_low[i+1][1] - vertexes_bottom[i+1][1])/2, (vertexes_low[i+1][2] + vertexes_bottom[i+1][2])/2)
            vertex4=((vertexes_low[i+1][0]*2 +vertexes_low[i][0])/3, (vertexes_low[i+1][1]*2 +vertexes_low[i][1])/3, -height)
            vertex5=((vertexes_low[i+1][0]+vertexes_low[i][0]*2)/3, (vertexes_low[i+1][1] +vertexes_low[i][1]*2)/3, -height)
            vertex6=(vertexes_bottom[i][0] + (vertexes_low[i][0] - vertexes_bottom[i][0])/2, vertexes_bottom[i][1] + (vertexes_low[i][1] - vertexes_bottom[i][1])/2, (vertexes_low[i][2] + vertexes_bottom[i][2])/2)
            vertexes = [vertex1,vertex2,vertex3,vertex4,vertex5,vertex6,vertex1]
            pg6_bottom.append(vertexes)
            polygon_side=Part.makePolygon(vertexes)
            faces.append(Part.Face(polygon_side))

        pg6_top = []
        for i in range(5):
            vertex1=vertexes_top[i]
            vertex2=vertexes_top[i+1]
            vertex3=(vertexes_top[i+1][0] + (vertexes_high[i+1][0] - vertexes_top[i+1][0])/2, vertexes_top[i+1][1] + (vertexes_high[i+1][1] - vertexes_top[i+1][1])/2, (vertexes_high[i+1][2] + vertexes_top[i+1][2])/2)
            vertex4=((vertexes_high[i+1][0]*2 +vertexes_high[i][0])/3, (vertexes_high[i+1][1]*2 +vertexes_high[i][1])/3, height)
            vertex5=((vertexes_high[i+1][0]+vertexes_high[i][0]*2)/3, (vertexes_high[i+1][1] +vertexes_high[i][1]*2)/3, height)
            vertex6=(vertexes_top[i][0] + (vertexes_high[i][0] - vertexes_top[i][0])/2, vertexes_top[i][1] + (vertexes_high[i][1] - vertexes_top[i][1])/2, (vertexes_high[i][2] + vertexes_top[i][2])/2)
            vertexes = [vertex1,vertex2,vertex3,vertex4, vertex5,vertex6,vertex1]
            pg6_top.append(vertexes)
            polygon_side=Part.makePolygon(vertexes)
            faces.append(Part.Face(polygon_side))

        pg6_low = []
        for i in range(5):
            vertex1 = pg6_bottom[i][3]
            vertex2 = pg6_bottom[i][4]
            vertex3 = ((vertexes_low[i][0]*2 + vertexes_high[i+1][0])/3,(vertexes_low[i][1]*2 + vertexes_high[i+1][1])/3, (vertexes_low[i][2]*2 + vertexes_high[i+1][2])/3)
            vertex4 = ((vertexes_low[i][0] + vertexes_high[i+1][0]*2)/3,(vertexes_low[i][1] + vertexes_high[i+1][1]*2)/3, (vertexes_low[i][2] + vertexes_high[i+1][2]*2)/3)
            vertex5 = ((vertexes_low[i+1][0] + vertexes_high[i+1][0]*2)/3,(vertexes_low[i+1][1] + vertexes_high[i+1][1]*2)/3, (vertexes_low[i+1][2] + vertexes_high[i+1][2]*2)/3)
            vertex6 = ((vertexes_low[i+1][0]*2 + vertexes_high[i+1][0])/3,(vertexes_low[i+1][1]*2 + vertexes_high[i+1][1])/3, (vertexes_low[i+1][2]*2 + vertexes_high[i+1][2])/3)
            vertexes = [vertex1,vertex2,vertex3,vertex4, vertex5,vertex6,vertex1]
            pg6_low.append(vertexes)
            polygon_side=Part.makePolygon(vertexes)
            faces.append(Part.Face(polygon_side))

        pg6_high = []
        for i in range(5):
            vertex1 = pg6_top[i][3]
            vertex2 = pg6_top[i][4]
            vertex3 = pg6_low[i-1][4]
            vertex4 = pg6_low[i-1][5]
            vertex5 = pg6_low[i][2]
            vertex6 = pg6_low[i][3]
            vertexes = [vertex1,vertex2, vertex3, vertex4,vertex5,vertex6 ,vertex1]
            pg6_high.append(vertexes)
            polygon_side=Part.makePolygon(vertexes)
            faces.append(Part.Face(polygon_side))

        for i in range(5):
            vertex1 = pg6_top[i][4]
            vertex2 = pg6_top[i][5]
            vertex3 = pg6_high[i-1][6]
            vertex4 = pg6_high[i-1][5]
            vertex5 = pg6_low[i-1][4]
            vertexes = [vertex1,vertex2, vertex3,vertex4,vertex5,vertex1]
            polygon_side=Part.makePolygon(vertexes)
            faces.append(Part.Face(polygon_side))

        for i in range(5):
            vertex1 = pg6_bottom[i][4]
            vertex2 = pg6_bottom[i][5]
            vertex3 = pg6_low[i-1][6]
            vertex4 = pg6_low[i-1][5]
            vertex5 = pg6_high[i][4]
            vertexes = [vertex1,vertex2, vertex3,vertex4,vertex5, vertex1]
            polygon_side=Part.makePolygon(vertexes)
            faces.append(Part.Face(polygon_side))


        shell = Part.makeShell(faces)
        solid = Part.makeSolid(shell)
        obj.Shape = solid

   
class IcosahedronTrCommand:
    def GetResources(self):
        return {'Pixmap'  : getWorkbenchFolder() + '/Resources/Icons/icosahedron_trunc.svg',
                'Accel' : "Shift+F", 
                'MenuText': "Icosahedron truncated",
                'ToolTip' : "Generate a Truncated Icosahedron (football)"}

    def Activated(self):
        obj=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","Icosahedron_truncated")
        Icosahedron_truncated(obj)
        #obj.ViewObject.Proxy=0
        ViewProviderBox(obj.ViewObject, "Icosahedron_trunc")
        FreeCAD.ActiveDocument.recompute()
        FreeCADGui.SendMsgToActiveView("ViewFit")
        return

        
    def IsActive(self):
        if FreeCAD.ActiveDocument == None:
               return False
        else:
               return True

FreeCADGui.addCommand('Icosahedron_truncated',IcosahedronTrCommand())

# ===========================================================================    

def geodesic_radius2side(radius, div):
    # approximative experience values! Not all sides are equal!
    dictsides = {"2":618.034, "3":412.41, "4":312.87,"5":245.09,"6":205.91,"7":173.53,"8":152.96,"9":135.96,"10":121.55}
    div = int(round(div))
    if div < 0:
        return 0
    if div == 1:
        return radius * 4 / math.sqrt(10 + 2 * math.sqrt(5))
    elif div <= 10:
        factor = dictsides[str(div)]
        return radius * factor / 1000

def geodesic_side2radius(side, div):
    # approximative experience values!  Not all sides are equal!
    dictsides = {"2":618.034, "3":412.41, "4":312.87,"5":245.09,"6":205.91,"7":173.53,"8":152.96,"9":135.96,"10":121.55}
    div = int(round(div))
    if div < 0:
        return 0
    if div == 1:
        return side / 4 * math.sqrt(10 + 2 * math.sqrt(5))
    elif div <= 10:
        factor = dictsides[str(div)]
        return side * 1000 / factor


# =========================================================================== 

class Geodesic_sphere:
    
    radiusvalue = 0  
    divided_by = 2


    def __init__(self, obj, radius=5, div=2):
        obj.addProperty("App::PropertyLength","Radius","Geodesic","Radius of the sphere").Radius=radius
        obj.addProperty("App::PropertyLength","Side","Geodesic","Sidelength of the triangles (approximative!)")
        obj.addProperty("App::PropertyInteger","DividedBy","Geodesic","The sides of the basic polyhedron are divided in ... (value 1 to 10)").DividedBy = div

        obj.Proxy = self

    
    def geodesic_divide_triangles(self,vertex1, vertex2, vertex3, faces):
        
        vector1 = (Base.Vector(vertex2) - Base.Vector(vertex1)) / self.divided_by
        vector2 = (Base.Vector(vertex3) - Base.Vector(vertex2)) / self.divided_by

        icosaPt={}

        
        icosaPt[str(1)] = Base.Vector(vertex1) 
          
        for level in range(self.divided_by):
            l1 = level + 1
            icosaPt[str(l1*10+1)] = icosaPt[str(1)]+ vector1 * (l1)

            for pt in range(level+1):
                icosaPt[str(l1*10+2+pt)] = icosaPt[str(l1*10+1)] + vector2 *(pt+1)
                    
        
        for level in range(self.divided_by):

            for point in range(level+1):
                vertex1x = icosaPt[str(level*10+1+point)].normalize().multiply(self.radiusvalue)
                vertex2x = icosaPt[str(level*10+11+point)].normalize().multiply(self.radiusvalue)
                vertex3x = icosaPt[str(level*10+12+point)].normalize().multiply(self.radiusvalue)
                polygon = Part.makePolygon([vertex1x,vertex2x,vertex3x, vertex1x])
                faces.append(Part.Face(polygon))

            for point in range(level):
                vertex1x = icosaPt[str(level*10+1+point)].normalize().multiply(self.radiusvalue)
                vertex2x = icosaPt[str(level*10+2+point)].normalize().multiply(self.radiusvalue)
                vertex3x = icosaPt[str(level*10+12+point)].normalize().multiply(self.radiusvalue)
                polygon = Part.makePolygon([vertex1x,vertex2x,vertex3x, vertex1x])
                faces.append(Part.Face(polygon))
      
        return faces

         

    def execute (self,obj):

        obj.DividedBy = int(round(obj.DividedBy))
        if obj.DividedBy <= 0:
            obj.DividedBy = 1
        if obj.DividedBy > 10:
            obj.DividedBy = 10
                    
            
        radius = float(obj.Radius)
        if radius != self.radiusvalue or obj.DividedBy != self.divided_by:
            self.divided_by = obj.DividedBy
            obj.Side = geodesic_radius2side(radius, self.divided_by)
            self.radiusvalue = radius
        else:
            self.radiusvalue = geodesic_side2radius(obj.Side,self.divided_by)
            obj.Radius = self.radiusvalue
            radius = self.radiusvalue
            
        self.divided_by = obj.DividedBy   

        z = 4*radius / math.sqrt(10 + 2 * math.sqrt(5))
        anglefaces = 138.189685104
        r = z/12 * math.sqrt(3) * (3 + math.sqrt(5))


        #radius of a pentagram with the same side
        radius2 = z / math.sin(36 * math.pi/180)/2
        
        #height of radius2 in the sphere
        angle = math.acos(radius2/radius)
        height = radius * math.sin(angle)

        faces = []

        vertex_bottom = (0,0,-radius)
        vertexes_low = horizontal_regular_polygon_vertexes(5,radius2, -height)
        vertexes_high = horizontal_regular_polygon_vertexes(5,radius2, height, math.pi/5)
        vertex_top = (0,0,radius)
        
        for i in range(5):
            faces = self.geodesic_divide_triangles(vertex_bottom,vertexes_low[i+1],vertexes_low[i],faces)

       
        for i in range(5):
            faces = self.geodesic_divide_triangles(vertexes_high[i],vertexes_low[i+1],vertexes_low[i],faces)
            faces = self.geodesic_divide_triangles(vertexes_low[i+1],vertexes_high[i+1],vertexes_high[i],faces)

        for i in range(5):
            faces = self.geodesic_divide_triangles(vertex_top,vertexes_high[i],vertexes_high[i+1],faces)
    
        
        shell = Part.makeShell(faces)
        solid = Part.makeSolid(shell)
        obj.Shape = solid        
 
   
class GeodesicSphereCommand:
    def GetResources(self):
        return {'Pixmap'  : getWorkbenchFolder() + '/Resources/Icons/geodesic_sphere.svg',
                'Accel' : "Shift+G", 
                'MenuText': "Geodesic sphere",
                'ToolTip' : "Generate Geodesic Spheres"}

    def Activated(self):
        obj=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","Geodesic sphere")
        Geodesic_sphere(obj)
        #obj.ViewObject.Proxy=0
        ViewProviderBox(obj.ViewObject, "Geodesic sphere")
        FreeCAD.ActiveDocument.recompute()
        FreeCADGui.SendMsgToActiveView("ViewFit")
        return

        
    def IsActive(self):
        if FreeCAD.ActiveDocument == None:
               return False
        else:
               return True

FreeCADGui.addCommand('Geodesic_sphere',GeodesicSphereCommand())


# The following code section provides an object that can be parameterised to produce any of the platonic, archimedean and catalan
# solids, and more, by starting with one of the five platonic solids and then truncating vertices respectively edges.

from FreeCAD import Vector
from math import sqrt
from functools import reduce

# The python code of the following three functions "vSum", "source" and "createSolid" is taken from Blenders add_mesh_solid.py
# from the "Add Mesh Extra Objects" addon, authored by Dreampainter, licensed as SPDX-License-Identifier GPL-2.0-or-later,
# refer https://github.com/blender/blender-addons/blob/master/add_mesh_extra_objects/add_mesh_solid.py. 

# function to make the reduce function work as a workaround to sum a list of vectors

def vSum(list):
    return reduce(lambda a, b: a.add(b), list)


# creates the 5 platonic solids as a base for the rest
#  plato: should be one of {"4","6","8","12","20"}. decides what solid the
#         outcome will be.
#  returns a list of vertices and faces

def source(plato):
    verts = []
    faces = []

    # Tetrahedron
    if plato == "4":
        # Calculate the necessary constants
        s = sqrt(2) / 3.0
        t = -1 / 3
        u = sqrt(6) / 3

        # create the vertices and faces
        v = [(0, 0, 1), (2 * s, 0, t), (-s, u, t), (-s, -u, t)]
        faces = [[0, 1, 2], [0, 2, 3], [0, 3, 1], [1, 3, 2]]

    # Hexahedron (cube)
    elif plato == "6":
        # Calculate the necessary constants
        s = 1 / sqrt(3)

        # create the vertices and faces
        v = [(-s, -s, -s), (s, -s, -s), (s, s, -s), (-s, s, -s), (-s, -s, s), (s, -s, s), (s, s, s), (-s, s, s)]
        faces = [[0, 3, 2, 1], [0, 1, 5, 4], [0, 4, 7, 3], [6, 5, 1, 2], [6, 2, 3, 7], [6, 7, 4, 5]]

    # Octahedron
    elif plato == "8":
        # create the vertices and faces
        v = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
        faces = [[4, 0, 2], [4, 2, 1], [4, 1, 3], [4, 3, 0], [5, 2, 0], [5, 1, 2], [5, 3, 1], [5, 0, 3]]

    # Dodecahedron
    elif plato == "12":
        # Calculate the necessary constants
        s = 1 / sqrt(3)
        t = sqrt((3 - sqrt(5)) / 6)
        u = sqrt((3 + sqrt(5)) / 6)

        # create the vertices and faces
        v = [(s, s, s), (s, s, -s), (s, -s, s), (s, -s, -s), (-s, s, s), (-s, s, -s), (-s, -s, s), (-s, -s, -s),
             (t, u, 0), (-t, u, 0), (t, -u, 0), (-t, -u, 0), (u, 0, t), (u, 0, -t), (-u, 0, t), (-u, 0, -t), (0, t, u),
             (0, -t, u), (0, t, -u), (0, -t, -u)]
        faces = [[0, 8, 9, 4, 16], [0, 12, 13, 1, 8], [0, 16, 17, 2, 12], [8, 1, 18, 5, 9], [12, 2, 10, 3, 13],
                 [16, 4, 14, 6, 17], [9, 5, 15, 14, 4], [6, 11, 10, 2, 17], [3, 19, 18, 1, 13], [7, 15, 5, 18, 19],
                 [7, 11, 6, 14, 15], [7, 19, 3, 10, 11]]

    # Icosahedron
    elif plato == "20":
        # Calculate the necessary constants
        s = (1 + sqrt(5)) / 2
        t = sqrt(1 + s * s)
        s = s / t
        t = 1 / t

        # create the vertices and faces
        v = [(s, t, 0), (-s, t, 0), (s, -t, 0), (-s, -t, 0), (t, 0, s), (t, 0, -s), (-t, 0, s), (-t, 0, -s),
             (0, s, t), (0, -s, t), (0, s, -t), (0, -s, -t)]
        faces = [[0, 8, 4], [0, 5, 10], [2, 4, 9], [2, 11, 5], [1, 6, 8], [1, 10, 7], [3, 9, 6], [3, 7, 11],
                 [0, 10, 8], [1, 8, 10], [2, 9, 11], [3, 11, 9], [4, 2, 0], [5, 0, 2], [6, 1, 3], [7, 3, 1],
                 [8, 6, 4], [9, 4, 6], [10, 5, 7], [11, 7, 5]]

    # convert the tuples to Vectors
    verts = [Vector(i) for i in v]
    
    return verts, faces

def createSolid(plato, vtrunc, etrunc, dual, snub):
    # the duals from each platonic solid
    dualSource = {"4": "4",
                  "6": "8",
                  "8": "6",
                  "12": "20",
                  "20": "12"}

    # constants saving space and readability
    vtrunc *= 0.5
    etrunc *= 0.5
    supposedSize = 0
    noSnub = (snub == "None") or (etrunc == 0.5) or (etrunc == 0)
    lSnub = (snub == "Left") and (0 < etrunc < 0.5)
    rSnub = (snub == "Right") and (0 < etrunc < 0.5)

    # no truncation
    if vtrunc == 0:
        if dual:  # dual is as simple as another, but mirrored platonic solid
            vInput, fInput = source(dualSource[plato])
            supposedSize = vSum(vInput[i] for i in fInput[0]).Length / len(fInput[0])
            vInput = [-i * supposedSize for i in vInput]            # mirror it
            return vInput, fInput
        return source(plato)
    elif 0 < vtrunc <= 0.5:  # simple truncation of the source
        vInput, fInput = source(plato)
    else:
        # truncation is now equal to simple truncation of the dual of the source
        vInput, fInput = source(dualSource[plato])
        supposedSize = vSum(vInput[i] for i in fInput[0]).Length / len(fInput[0])
        vtrunc = 1 - vtrunc  # account for the source being a dual
        if vtrunc == 0:    # no truncation needed
            if dual:
                vInput, fInput = source(plato)
                vInput = [i * supposedSize for i in vInput]
                return vInput, fInput
            vInput = [-i * supposedSize for i in vInput]
            return vInput, fInput

    # generate connection database
    vDict = [{} for i in vInput]
    # for every face, store what vertex comes after and before the current vertex
    for x in range(len(fInput)):
        i = fInput[x]
        for j in range(len(i)):
            vDict[i[j - 1]][i[j]] = [i[j - 2], x]
            if len(vDict[i[j - 1]]) == 1:
                vDict[i[j - 1]][-1] = i[j]

    # the actual connection database: exists out of:
    # [vtrunc pos, etrunc pos, connected vert IDs, connected face IDs]
    vData = [[[], [], [], []] for i in vInput]
    fvOutput = []      # faces created from truncated vertices
    feOutput = []      # faces created from truncated edges
    vOutput = []       # newly created vertices
    for x in range(len(vInput)):
        i = vDict[x]   # lookup the current vertex
        current = i[-1]
        while True:    # follow the chain to get a ccw order of connected verts and faces
            vData[x][2].append(i[current][0])
            vData[x][3].append(i[current][1])
            # create truncated vertices
            vData[x][0].append((1 - vtrunc) * vInput[x] + vtrunc * vInput[vData[x][2][-1]])
            current = i[current][0]
            if current == i[-1]:
                break                   # if we're back at the first: stop the loop
        fvOutput.append([])             # new face from truncated vert
        fOffset = x * (len(i) - 1)      # where to start off counting faceVerts
        # only create one vert where one is needed (v1 todo: done)
        if etrunc == 0.5:
            for j in range(len(i) - 1):
                vOutput.append((vData[x][0][j] + vData[x][0][j - 1]) * etrunc)  # create vert
                fvOutput[x].append(fOffset + j)                                 # add to face
            fvOutput[x] = fvOutput[x][1:] + [fvOutput[x][0]]                    # rotate face for ease later on
            # create faces from truncated edges.
            for j in range(len(i) - 1):
                if x > vData[x][2][j]:     # only create when other vertex has been added
                    index = vData[vData[x][2][j]][2].index(x)
                    feOutput.append([fvOutput[x][j], fvOutput[x][j - 1],
                                     fvOutput[vData[x][2][j]][index],
                                     fvOutput[vData[x][2][j]][index - 1]])
        # edge truncation between none and full
        elif etrunc > 0:
            for j in range(len(i) - 1):
                # create snubs from selecting verts from rectified meshes
                if rSnub:
                    vOutput.append(etrunc * vData[x][0][j] + (1 - etrunc) * vData[x][0][j - 1])
                    fvOutput[x].append(fOffset + j)
                elif lSnub:
                    vOutput.append((1 - etrunc) * vData[x][0][j] + etrunc * vData[x][0][j - 1])
                    fvOutput[x].append(fOffset + j)
                else:   # noSnub,  select both verts from rectified mesh
                    vOutput.append(etrunc * vData[x][0][j] + (1 - etrunc) * vData[x][0][j - 1])
                    vOutput.append((1 - etrunc) * vData[x][0][j] + etrunc * vData[x][0][j - 1])
                    fvOutput[x].append(2 * fOffset + 2 * j)
                    fvOutput[x].append(2 * fOffset + 2 * j + 1)
            # rotate face for ease later on
            if noSnub:
                fvOutput[x] = fvOutput[x][2:] + fvOutput[x][:2]
            else:
                fvOutput[x] = fvOutput[x][1:] + [fvOutput[x][0]]
            # create single face for each edge
            if noSnub:
                for j in range(len(i) - 1):
                    if x > vData[x][2][j]:
                        index = vData[vData[x][2][j]][2].index(x)
                        feOutput.append([fvOutput[x][j * 2], fvOutput[x][2 * j - 1],
                                         fvOutput[vData[x][2][j]][2 * index],
                                         fvOutput[vData[x][2][j]][2 * index - 1]])
            # create 2 tri's for each edge for the snubs
            elif rSnub:
                for j in range(len(i) - 1):
                    if x > vData[x][2][j]:
                        index = vData[vData[x][2][j]][2].index(x)
                        feOutput.append([fvOutput[x][j], fvOutput[x][j - 1],
                                         fvOutput[vData[x][2][j]][index]])
                        feOutput.append([fvOutput[x][j], fvOutput[vData[x][2][j]][index],
                                         fvOutput[vData[x][2][j]][index - 1]])
            elif lSnub:
                for j in range(len(i) - 1):
                    if x > vData[x][2][j]:
                        index = vData[vData[x][2][j]][2].index(x)
                        feOutput.append([fvOutput[x][j], fvOutput[x][j - 1],
                                         fvOutput[vData[x][2][j]][index - 1]])
                        feOutput.append([fvOutput[x][j - 1], fvOutput[vData[x][2][j]][index],
                                         fvOutput[vData[x][2][j]][index - 1]])
        # special rules for birectified mesh (v1 todo: done)
        elif vtrunc == 0.5:
            for j in range(len(i) - 1):
                if x < vData[x][2][j]:  # use current vert,  since other one has not passed yet
                    vOutput.append(vData[x][0][j])
                    fvOutput[x].append(len(vOutput) - 1)
                else:
                    # search for other edge to avoid duplicity
                    connectee = vData[x][2][j]
                    fvOutput[x].append(fvOutput[connectee][vData[connectee][2].index(x)])
        else:   # vert truncation only
            vOutput.extend(vData[x][0])   # use generated verts from way above
            for j in range(len(i) - 1):   # create face from them
                fvOutput[x].append(fOffset + j)

    # calculate supposed vertex length to ensure continuity
    if supposedSize and not dual:                    # this to make the vtrunc > 1 work
        supposedSize *= len(fvOutput[0]) / vSum(vOutput[i] for i in fvOutput[0]).Length
        vOutput = [-i * supposedSize for i in vOutput]

    # create new faces by replacing old vert IDs by newly generated verts
    ffOutput = [[] for i in fInput]
    for x in range(len(fInput)):
        # only one generated vert per vertex,  so choose accordingly
        if etrunc == 0.5 or (etrunc == 0 and vtrunc == 0.5) or lSnub or rSnub:
            ffOutput[x] = [fvOutput[i][vData[i][3].index(x) - 1] for i in fInput[x]]
        # two generated verts per vertex
        elif etrunc > 0:
            for i in fInput[x]:
                ffOutput[x].append(fvOutput[i][2 * vData[i][3].index(x) - 1])
                ffOutput[x].append(fvOutput[i][2 * vData[i][3].index(x) - 2])
        else:   # cutting off corners also makes 2 verts
            for i in fInput[x]:
                ffOutput[x].append(fvOutput[i][vData[i][3].index(x)])
                ffOutput[x].append(fvOutput[i][vData[i][3].index(x) - 1])

    if not dual:
        return vOutput, fvOutput + feOutput + ffOutput
    else:
        # do the same procedure as above,  only now on the generated mesh
        # generate connection database
        vDict = [{} for i in vOutput]
        dvOutput = [0 for i in fvOutput + feOutput + ffOutput]
        dfOutput = []

        for x in range(len(dvOutput)):               # for every face
            i = (fvOutput + feOutput + ffOutput)[x]  # choose face to work with
            # find vertex from face
            normal = (vOutput[i[0]] - vOutput[i[1]]).cross(vOutput[i[2]] - vOutput[i[1]]).normalize()
            dvOutput[x] = normal / (normal.dot(vOutput[i[0]]))
            for j in range(len(i)):  # create vert chain
                vDict[i[j - 1]][i[j]] = [i[j - 2], x]
                if len(vDict[i[j - 1]]) == 1:
                    vDict[i[j - 1]][-1] = i[j]

        # calculate supposed size for continuity
        supposedSize = vSum([vInput[i] for i in fInput[0]]).Length / len(fInput[0])
        supposedSize /= dvOutput[-1].Length
        dvOutput = [i * supposedSize for i in dvOutput]

        # use chains to create faces
        for x in range(len(vOutput)):
            i = vDict[x]
            current = i[-1]
            face = []
            while True:
                face.append(i[current][1])
                current = i[current][0]
                if current == i[-1]:
                    break
            dfOutput.append(face)

        return dvOutput, dfOutput

# The following two classes "RegularSolid" and "RegularSolidCommand" make the abilities of the "createSolid" function above
# available to FreeCAD. They also borrow somewhat on the add_mesh_solid.py referenced above:

class RegularSolid:
    
    enums = {
    "Source": (("4", "Tetrahedron", ""),
            ("6", "Hexahedron", "", True),
            ("8", "Octahedron", ""),
            ("12", "Dodecahedron", ""),
            ("20", "Icosahedron", "")),
    "Snub": (("None", "No Snub", "", True),
            ("Left", "Left Snub", ""),
            ("Right", "Right Snub", "")),
    "Presets": (("0", "Custom", ""),
            ("t4", "Truncated Tetrahedron", ""),
            ("r4", "Cuboctahedron", ""),
            ("t6", "Truncated Cube", ""),
            ("t8", "Truncated Octahedron", ""),
            ("b6", "Rhombicuboctahedron", ""),
            ("c6", "Truncated Cuboctahedron", "", True),
            ("s6", "Snub Cube", ""),
            ("r12", "Icosidodecahedron", ""),
            ("t12", "Truncated Dodecahedron", ""),
            ("t20", "Truncated Icosahedron", ""),
            ("b12", "Rhombicosidodecahedron", ""),
            ("c12", "Truncated Icosidodecahedron", ""),
            ("s12", "Snub Dodecahedron", ""),
            ("dt4", "Triakis Tetrahedron", ""),
            ("dr4", "Rhombic Dodecahedron", ""),
            ("dt6", "Triakis Octahedron", ""),
            ("dt8", "Tetrakis Hexahedron", ""),
            ("db6", "Deltoidal Icositetrahedron", ""),
            ("dc6", "Disdyakis Dodecahedron", ""),
            ("ds6", "Pentagonal Icositetrahedron", ""),
            ("dr12", "Rhombic Triacontahedron", ""),
            ("dt12", "Triakis Icosahedron", ""),
            ("dt20", "Pentakis Dodecahedron", ""),
            ("db12", "Deltoidal Hexecontahedron", ""),
            ("dc12", "Disdyakis Triacontahedron", ""),
            ("ds12", "Pentagonal Hexecontahedron", ""))
    }
    # actual preset values (Source, Vtrunc, Etrunc, Dual, Snub)
    p = {"t4": ["4", 2 / 3, 0, 0, "None"],
         "r4": ["4", 1, 1, 0, "None"],
         "t6": ["6", 2 / 3, 0, 0, "None"],
         "t8": ["8", 2 / 3, 0, 0, "None"],
         "b6": ["6", 1.0938, 1, 0, "None"],
         "c6": ["6", 1.0572, 0.585786, 0, "None"],
         "s6": ["6", 1.0875, 0.704, 0, "Left"],
         "r12": ["12", 1, 0, 0, "None"],
         "t12": ["12", 2 / 3, 0, 0, "None"],
         "t20": ["20", 2 / 3, 0, 0, "None"],
         "b12": ["12", 1.1338, 1, 0, "None"],
         "c12": ["20", 0.921, 0.553, 0, "None"],
         "s12": ["12", 1.1235, 0.68, 0, "Left"],
         "dt4": ["4", 2 / 3, 0, 1, "None"],
         "dr4": ["4", 1, 1, 1, "None"],
         "dt6": ["6", 2 / 3, 0, 1, "None"],
         "dt8": ["8", 2 / 3, 0, 1, "None"],
         "db6": ["6", 1.0938, 1, 1, "None"],
         "dc6": ["6", 1.0572, 0.585786, 1, "None"],
         "ds6": ["6", 1.0875, 0.704, 1, "Left"],
         "dr12": ["12", 1, 0, 1, "None"],
         "dt12": ["12", 2 / 3, 0, 1, "None"],
         "dt20": ["20", 2 / 3, 0, 1, "None"],
         "db12": ["12", 1.1338, 1, 1, "None"],
         "dc12": ["20", 0.921, 0.553, 1, "None"],
         "ds12": ["12", 1.1235, 0.68, 1, "Left"]}
         
    sizenames = ["Midradius", "Inradius", "Circumradius", "LongEdge", "ShortEdge"]
   
    def __init__(self, obj, midradius=10):
        obj.addProperty("App::PropertyLength","Midradius","RegularSolid","Radius of inscribed sphere touching closest edge").Midradius=midradius
        obj.addProperty("App::PropertyLength","Inradius","RegularSolid","Radius of inscribed sphere touching closest face")
        obj.addProperty("App::PropertyLength","Circumradius","RegularSolid","Radius of inscribed sphere touching furthest vertex")
        obj.addProperty("App::PropertyLength","LongEdge","RegularSolid","Length of longest edge")
        obj.addProperty("App::PropertyLength","ShortEdge","RegularSolid","Length of shortest edge")
        obj.addProperty("App::PropertyEnumeration","KeepSize","RegularSolid","What drives solid size when changing construction")
        obj.KeepSize = self.sizenames
        obj.KeepSize = self.sizenames[0]
        obj.addProperty("App::PropertyEnumeration","Source","RegularSolid","Initiating body")
        obj.Source = [e[1] for e in self.enums["Source"]]
        obj.Source = [e[1] for e in self.enums["Source"] if len(e)>=4 and e[3]][0]
        obj.addProperty("App::PropertyFloat","Vtrunc","RegularSolid","Amount of vertex truncation/elongation").Vtrunc = 0.0
        obj.addProperty("App::PropertyFloat","Etrunc","RegularSolid","Amount of edge truncation").Etrunc = 0.0
        obj.addProperty("App::PropertyEnumeration","Snub","RegularSolid","Create the snub version")
        obj.Snub = [e[1] for e in self.enums["Snub"]]
        obj.Snub = [e[1] for e in self.enums["Snub"] if len(e)>=4 and e[3]][0]
        obj.addProperty("App::PropertyBool","Dual","RegularSolid","Create the dual of the current solid").Dual = False
        obj.addProperty("App::PropertyEnumeration","Presets","RegularSolid","Preset parameters for some hard names")
        obj.Presets = [e[1] for e in self.enums["Presets"]]
        obj.Presets = [e[1] for e in self.enums["Presets"] if len(e)>=4 and e[3]][0]
        obj.Proxy = self
        self.prevcode = None
        self.prevsizes = (None,None,None,None,None)

    def execute (self,obj):
        sizes = (obj.Midradius,obj.Inradius,obj.Circumradius,obj.LongEdge,obj.ShortEdge)
        keepsize = obj.KeepSize
        for i in range(len(sizes)):
            if sizes[i]!=self.prevsizes[i] and self.prevsizes[i]!=None:
                keepsize = self.sizenames[i]
                break
        
        presetcode = [e[0] for e in self.enums["Presets"] if e[1]==obj.Presets][0]
        if presetcode!="0" and presetcode!=self.prevcode: # The user has selected a new preset
                source,vtrunc,etrunc,dual,snub = self.p[presetcode]
                obj.Source = [e[1] for e in self.enums["Source"] if e[0]==source][0]
                obj.Vtrunc,obj.Etrunc,obj.Dual = vtrunc,etrunc,dual
                obj.Snub = [e[1] for e in self.enums["Snub"] if e[0]==snub][0]
        else: # The preset is as it was, or it was set to "Custom". Check if the user has changed a parameter affecting the preset
            source = [e[0] for e in self.enums["Source"] if e[1]==obj.Source][0]
            vtrunc,etrunc,dual = obj.Vtrunc,obj.Etrunc,obj.Dual
            snub = [e[0] for e in self.enums["Snub"] if e[1]==obj.Snub][0]
            if presetcode!="0" and self.p[presetcode]!=(source,vtrunc,etrunc,dual,snub):
                presetcode = "0"
                obj.Presets = [e[1] for e in self.enums["Presets"] if e[0]==presetcode][0]
        self.prevcode = presetcode
        
        bpy_verts,bpy_faces = createSolid(source,vtrunc,etrunc,dual,snub)
        
        faces = []
        for face in bpy_faces:
            verts = [bpy_verts[vi] for vi in face]+[bpy_verts[face[0]]]
            polygon=Part.makePolygon(verts)
            faces.append(Part.Face(polygon))
            
        v0 = Vector(0,0,0)
        s0 = Part.Point(v0).toShape()
        origsizes = (
            min(e.distToShape(s0)[0] for f in faces for e in f.Edges), # Midradius
            min(f.distToShape(s0)[0] for f in faces), # Inradius
            max(v.distToShape(s0)[0] for f in faces for v in f.Vertexes), # Circumradius
            max(e.Length for f in faces for e in f.Edges), # LongEdge
            min(e.Length for f in faces for e in f.Edges) # ShortEdge
        )
        
        for i in range(len(self.sizenames)):
            if keepsize==self.sizenames[i]:
                scale = sizes[i]/origsizes[i]
                
        obj.Midradius,obj.Inradius,obj.Circumradius,obj.LongEdge,obj.ShortEdge = self.prevsizes = tuple(os*scale for os in origsizes)
        
        shell = Part.makeShell(faces).scaled(scale,v0)
        solid = Part.makeSolid(shell)
        obj.Shape = solid
        
 
class RegularSolidCommand:    
    def GetResources(self):
        return {'Pixmap'  : getWorkbenchFolder() + '/Resources/Icons/regularsolid.svg',
                'Accel' : "Shift+R",
                'MenuText': "Regular Solid",
                'ToolTip' : "Generate a Regular Solid"}

    def Activated(self):
        obj=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","RegularSolid")
        RegularSolid(obj)
        #obj.ViewObject.Proxy=0
        ViewProviderBox(obj.ViewObject, "RegularSolid")
        FreeCAD.ActiveDocument.recompute()
        FreeCADGui.SendMsgToActiveView("ViewFit")
        return

        
    def IsActive(self):
        return FreeCAD.ActiveDocument!=None

FreeCADGui.addCommand('RegularSolid',RegularSolidCommand())
