#Gets all unused filters from the revit document and outputs them as a list.
#Input as Bool. Acts as a refresh toggle.

import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *
import Autodesk

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
from RevitServices.Persistence import DocumentManager

#The inputs to this node will be stored as a list in the IN variables.

bool = IN[0]
output = ""

doc = DocumentManager.Instance.CurrentDBDocument
collector = FilteredElementCollector(doc)
allviews = collector.OfClass(View).ToElements()
viewlist = []

for v in allviews:
	if v.ViewType == ViewType.ThreeD:
		if not(v.IsTemplate):
			viewlist.append(v)
	else:
		viewlist.append(v)

views = UnwrapElement(viewlist)

viewTemplates = []
for v in views:
	if v.IsTemplate:
		viewTemplates.append(v)

usedTemplates = []
for v in views:
	if v.ViewTemplateId.IntegerValue != -1:
		usedTemplates.append(v.Document.GetElement(v.ViewTemplateId))

uniqueUsedTemplates = []

if len(usedTemplates) != 0:
	uniqueUsedTemplates.append(usedTemplates[0])
	for used in usedTemplates:
		buffer = False
		for unique in uniqueUsedTemplates:
			if used.Name == unique.Name:
				buffer = False
				break
			else:
				buffer = True
		if buffer:
			uniqueUsedTemplates.append(used)

indexes = []
i = 0
for v in viewTemplates:
	for u in usedTemplates:
		if u.Name == v.Name:
			indexes.append(i)
			break
	i = i + 1

indexes.reverse()

for i in indexes:
	viewTemplates.pop(i)

viewTemplatesID = []
viewTempNames = []

if bool == True:
	for v in viewTemplates:
		viewTemplatesID.append(v.Id)

	for v in viewTemplatesID:
		viewTempNames.append(doc.GetElement(v).Name)

OUT = viewTempNames
