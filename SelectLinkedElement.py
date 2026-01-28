// Lets the user select an element from a linked model

import clr
clr.AddReference('RevitAPI')
import Autodesk
from Autodesk.Revit.DB import RevitLinkInstance

clr.AddReference('RevitAPIUI')
from Autodesk.Revit.UI import *
from Autodesk.Revit.UI.Selection import *

clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager
doc = DocumentManager.Instance.CurrentDBDocument
uidoc = DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.GeometryConversion)

elemInLinks=[]

TaskDialog.Show("Selection", "Select the linked elements and press Finish")
reflnk = uidoc.Selection.PickObjects(ObjectType.LinkedElement, "Select linked elements")
for ref in reflnk :
        lnkinst=doc.GetElement(ref)
        tfLnk = lnkinst.GetTotalTransform().ToCoordinateSystem(1)
        doclnk =  lnkinst.GetLinkDocument()
        elemInLink = doclnk.GetElement(ref.LinkedElementId)
        elemInLinks.append(elemInLink)

if len(elemInLinks)>1: OUT = elemInLinks, lnkinst, tfLnk
else:OUT = elemInLinks[0], lnkinst, tfLnk
