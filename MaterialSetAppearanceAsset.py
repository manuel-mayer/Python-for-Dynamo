# script to set the appearance-asset of a revit material
# inputs: [0] for revit materials, [1] for revit material assets

import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

def toList(obj):
    if obj is None:
        return []
    if isinstance(obj, (list, tuple)):
        return obj
    else:
        return [obj]

# unwrap inputs
mats = toList(UnwrapElement(IN[0]))
assetElements = toList(UnwrapElement(IN[1]))

# safety check
if not mats or not assetElements:
    OUT = "No valid inputs"
else:
    doc = DocumentManager.Instance.CurrentDBDocument
    TransactionManager.Instance.EnsureInTransaction(doc)
    
    for mat, assetElement in zip(mats, assetElements):
        if mat and assetElement:
            mat.AppearanceAssetId = assetElement.Id
    
    TransactionManager.Instance.TransactionTaskDone()
    
    OUT = mats if isinstance(IN[0], list) else mats[0]
