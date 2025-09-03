# Collects all DirectShape objects in the current revit model

import clr
clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import FilteredElementCollector, DirectShape

# Access the current Revit document
doc = DocumentManager.Instance.CurrentDBDocument

# Collect all DirectShape elements directly from the Revit API
direct_shapes = FilteredElementCollector(doc).OfClass(DirectShape).ToElements()

# Return objects
OUT = direct_shapes
