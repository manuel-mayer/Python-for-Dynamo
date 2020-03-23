#Gets all unused filters from the revit document and outputs them as a list.
#Input as Bool. Acts as a refresh toggle.

import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

clr.AddReference("System.Core")
import System.Linq
clr.ImportExtensions(System.Linq)

clr.AddReference("RevitAPI")
import Autodesk.Revit
from Autodesk.Revit.Exceptions import InvalidOperationException
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB import ElementId
from System.Collections.Generic import *

# Import ToDSType(bool) extension method
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

# Import DocumentManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
from RevitServices.Persistence import DocumentManager

def GetFilterIds(view):
  filterIds = None
  try:
    filterIds = view.GetFilters()
  except InvalidOperationException, e:
    filterIds = None
  return filterIds

def GetUsedFilterIds(doc):
  views = FilteredElementCollector(doc).OfClass(View).ToElements()
  usedFilterIds = []
  for view in views:
    viewFilterIds = []
    try:
      viewFilterIds = view.GetFilters()
    except InvalidOperationException, e:
      pass # this exception happens when a view doesn't support filters
    usedFilterIds.extend(viewFilterIds)
  return usedFilterIds

def GetUnusedFilters(doc):
  usedFilterIds = GetUsedFilterIds(doc).ToList[ElementId]()
  unusedFilters = FilteredElementCollector(doc).OfClass(ParameterFilterElement).Excluding(usedFilterIds).ToElements()
  return list(f.ToDSType(True) for f in unusedFilters)

#The inputs to this node will be stored as a list in the IN variables.

bool = IN[0]
output = ""

doc = DocumentManager.Instance.CurrentDBDocument

filters = GetUnusedFilters(doc)
filters2 = UnwrapElement(filters)
filtersID = []
filtersNames = []

if bool == True:
	for f in filters2:
		filtersID.append(f.Id)

	for f in filtersID:
		filtersNames.append(doc.GetElement(f).Name)

#Assign your output to the OUT variable.
OUT = filtersNames
