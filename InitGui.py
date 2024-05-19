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

# Version 01.08

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

# version 01.08   (2023-08-21)
# no printing of the workbenchfolders  (issue bij Alex Neufeld)

import os

import FreeCAD
import FreeCADGui

import pyramids_utils

# Add translations path
FreeCADGui.addLanguagePath(
    os.path.join(pyramids_utils.getWorkbenchFolder(), "Resources", "Translations")
)
FreeCADGui.updateLocale()


class PolyhydronsWorkbench(Workbench):
    translate = FreeCAD.Qt.translate

    MenuText = translate("Workbench", "Pyramids-and-Polyhedrons")
    ToolTip = translate(
        "Workbench", "A workbench for generating pyramids, polyhedrons and geodesic spheres"
    )

    def __init__(self):
        resourcespath = self.getWorkbenchFolder() + "/Resources/"

        self.__class__.Icon = resourcespath + "Icons/Pyramids-and-Polyhedrons_workbench_icon.svg"

    def Initialize(self):
        """This function is executed when FreeCAD starts"""
        import polyhedrons # import here all the needed files that create your FreeCAD commands
        self.list = ["Pyramid","Tetrahedron","Hexahedron","Octahedron","Dodecahedron","Icosahedron","Icosahedron_truncated",
                     "Geodesic_sphere","RegularSolid"] # A list of command names created in the line above
        #self.appendMenu(["An existing Menu","My submenu"],self.list) # appends a submenu to an existing menu
        QT_TRANSLATE_NOOP = FreeCAD.Qt.QT_TRANSLATE_NOOP
        self.appendToolbar(
            QT_TRANSLATE_NOOP("Workbench", "Pyramids-and-Polyhedrons"), self.list
        )  # creates a new toolbar with your commands
        self.appendMenu(
            QT_TRANSLATE_NOOP("Workbench", "Pyramids-and-Polyhedrons"), self.list
        )  # creates a new menu

    def Activated(self):
        """This function is executed when the workbench is activated"""
        return

    def Deactivated(self):
        """This function is executed when the workbench is deactivated"""
        return

    def ContextMenu(self, recipient):
        """This is executed whenever the user right-clicks on screen"""
        # "recipient" will be either "view" or "tree"
        QT_TRANSLATE_NOOP = FreeCAD.Qt.QT_TRANSLATE_NOOP
        self.appendContextMenu(
            QT_TRANSLATE_NOOP("Workbench", "Pyramids-and-Polyhedrons"), self.list
        )  # add commands to the context menu

    def GetClassName(self):
        # this function is mandatory if this is a full python workbench
        return "Gui::PythonWorkbench"


Gui.addWorkbench(PolyhydronsWorkbench())
