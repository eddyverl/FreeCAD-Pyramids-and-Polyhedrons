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

# Version 01.04

# Version 01.02  (2020-01-15)
# added geodesic sphere

# version 01.03   (2020-01-23)
# added hexahedron  (cube)

# version 01.04  (2020-01-30)
# renamed Mod to Pyramids-and-Polyhedrons

# version 01.05  (2020-12-26)
# additional namechanges, no functional changes

# version 01.07a  (2020-12-30)
# flexibility for installation folder


class PolyhydronsWorkbench (Workbench):

    MenuText = "Pyramids-and-Polyhedrons"
    ToolTip = "A workbench for generating pyramids, polyhedrons and geodesic spheres"
    #Icon = """paste here the contents of a 16x16 xpm icon"""
    
    
    def getWorkbenchFolder(self):

         
        import os.path
        from os import path
        
        import workbenchfolders
        
        print (workbenchfolders.recommended_folders)
        
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
        
        
    

    def __init__(self):
        resourcespath = self.getWorkbenchFolder() + "/Resources/"
        
        self.__class__.Icon = resourcespath + "Icons/Pyramids-and-Polyhedrons_workbench_icon.svg"

    def Initialize(self):
        """This function is executed when FreeCAD starts"""
        import polyhedrons # import here all the needed files that create your FreeCAD commands
        self.list = ["Pyramid","Tetrahedron","Hexahedron","Octahedron","Dodecahedron","Icosahedron","Icosahedron_truncated","Geodesic_sphere"] # A list of command names created in the line above
        self.appendToolbar("Pyramids-and-Polyhedrons",self.list) # creates a new toolbar with your commands
        self.appendMenu("Pyramids-and-Polyhedrons",self.list) # creates a new menu
        #self.appendMenu(["An existing Menu","My submenu"],self.list) # appends a submenu to an existing menu

    def Activated(self):
        """This function is executed when the workbench is activated"""
        return

    def Deactivated(self):
        """This function is executed when the workbench is deactivated"""
        return

    def ContextMenu(self, recipient):
        """This is executed whenever the user right-clicks on screen"""
        # "recipient" will be either "view" or "tree"
        self.appendContextMenu("Pyramids-and-Polyhedrons",self.list) # add commands to the context menu

    def GetClassName(self): 
        # this function is mandatory if this is a full python workbench
        return "Gui::PythonWorkbench"
       
Gui.addWorkbench(PolyhydronsWorkbench())
