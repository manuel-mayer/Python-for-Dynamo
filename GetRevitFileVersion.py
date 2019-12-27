import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import *
clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager

#get the current document path as a list
doc = DocumentManager.Instance.CurrentDBDocument
path = [doc.PathName]

#extract the Revit file version from the path
for p in path:
		info = BasicFileInfo.Extract(p)
		version = info.Format

OUT = "Revit "+version
