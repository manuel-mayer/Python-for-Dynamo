import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *
import Autodesk

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager

doc = DocumentManager.Instance.CurrentDBDocument

collector = FilteredWorksetCollector(doc)
worksetnames = []
for c in collector:
	worksetnames.append(c.Name)
worksetkind = []
for c in collector:	
	worksetkind.append(c.Kind)

OUT = collector, worksetnames, worksetkind
