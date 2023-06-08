import clr

clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

#Import the Revit API
clr.AddReference('RevitAPI')
import Autodesk
from Autodesk.Revit.DB import *

#Import DocumentManager and TransactionManager
clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

#Import ToDSType(bool) extensions method
clr.AddReference('RevitNodes')
import Revit
clr.ImportExtensions(Revit.Elements)

#Reference the active Document and application
doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

#Start scripting here:

bool = IN[0]

if bool == True:
        col = FilteredElementCollector(doc).OfClass(ImportInstance).ToElements()
        impinst = []
        impname = []

        for i in col:
                if i.IsLinked != True:
                        impinst.append(i)

        for j in impinst:
                impname.append(j.Category.Name)

        OUT = impinst, impname

else:
        OUT = "Set bool to True"
