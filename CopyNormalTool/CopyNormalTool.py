import maya.cmds as cmds

import sys
import maya.cmds as cmds
qtVersion = cmds.about(qtVersion=True)


if qtVersion.startswith("4") or type(qtVersion) not in [str, unicode]:
    from PySide import QtGui
    from PySide import QtCore
    #from PySide import QtWidgets
    from PySide import QtUiTools
    
else:
    from PySide2 import QtGui
    from PySide2 import QtCore
    from PySide2 import QtWidgets
    from PySide2 import QtUiTools


import maya.OpenMayaUI as omui
import os; 

copyNormal_X = 0
copyNormal_Y = 0
copyNormal_Z = 0

scriptPath = os.environ['MAYA_SCRIPT_PATH']; 
path = scriptPath.split(';');
uifile_path = path[2]+"/CopyNormalTool/CopyNormalTool.ui"

def loadui(uifile_path):
    uifile = QtCore.QFile(uifile_path)
    uifile.open(QtCore.QFile.ReadOnly)
    uiWindow = QtUiTools.QUiLoader().load(uifile)
    uifile.close()
    return uiWindow 
    
def RamapValue (Value,Low1Val,High1Val,Low2Val,High2Val): 
    re = (Value - Low1Val)*(High2Val - Low2Val)/(High1Val-Low1Val)+Low2Val
    return re

def displayOrHideNormal(sel,status):
    for i in sel:
        if cmds.toggle(i,q = True,normal = True) != status:
            cmds.toggle(i,normal = True)
        
   
class MainWindows():
    def __init__(self,parent = None):
        self.ui = loadui(uifile_path)
        self.ui.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.ui.show()
        
        self.ui.DisplayButton.clicked.connect(self.DisplayNormal)
        self.ui.HideButton.clicked.connect(self.HideNormal)
        self.ui.CopyButton.clicked.connect(self.CopyNormal)
        self.ui.PasteButton.clicked.connect(self.PatseNormal)
        self.ui.RevertButton.clicked.connect(self.RevertNormal) 
        self.ui.RevertButton.clicked.connect(self.RevertNormal)      
        self.ui.NormalizeCheckBox.stateChanged.connect(self.NormalizeNormal)
        
    def DisplayNormal(self):
        sel = cmds.ls(sl=True)
        displayOrHideNormal(sel,True)
              
    def HideNormal(self):
        sel = cmds.ls(sl=True)
        displayOrHideNormal(sel,False)
            
    def CopyNormal(self):
        global copyNormal_X
        global copyNormal_Y
        global copyNormal_Z
        sel = cmds.ls(sl=True)
        onlyVertices = cmds.filterExpand(sel, sm=31)
        narmalValue = cmds.polyNormalPerVertex( query=True, xyz=True )
        
        copyNormal_X = 0
        copyNormal_Y = 0
        copyNormal_Z = 0
        normallizeStr = ""
        
        if self.ui.NormalizeCheckBox.isChecked():
            copyNormal_X = narmalValue[0]
            copyNormal_Y = narmalValue[1]
            copyNormal_Z = narmalValue[2]
            normallizeStr = "(normallize)"
        else:
            copyNormal_X = RamapValue(narmalValue[0],-0.5774,0.5774,-1,1)
            copyNormal_Y = RamapValue(narmalValue[1],-0.5774,0.5774,-1,1)
            copyNormal_Z = RamapValue(narmalValue[2],-0.5774,0.5774,-1,1)
            
        strX = "Normal X:  "+str(round(copyNormal_X,5))
        strY = "Normal Y:  "+str(round(copyNormal_Y,5))
        strZ = "Normal Z:  "+str(round(copyNormal_Z,5))
        
        self.ui.label.setText(strX+"\n"+strY+"\n"+strZ +"\n"+ normallizeStr)
        
    def PatseNormal(self):
        cmds.polyNormalPerVertex(xyz=(copyNormal_X,copyNormal_Y,copyNormal_Z))
    
    def RevertNormal(self):
        sel = cmds.ls(sl=True)
        onlyVertices = cmds.filterExpand(sel, sm=31)
        cmds.polySetToFaceNormal(onlyVertices)
        cmds.polySoftEdge( a=180 )
        cmds.select( clear = True ) 
        cmds.select(onlyVertices,tgl = True)  
        
    def NormalizeNormal(self):
        print(self.ui.NormalizeCheckBox.isChecked())
        
mainWindows = MainWindows()