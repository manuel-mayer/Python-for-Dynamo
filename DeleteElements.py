#deletes Elements from the Revit file

import clr

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

# get the current Revit document 
doc = DocumentManager.Instance.CurrentDBDocument

elements = UnwrapElement(IN[0])

# start Revit transaction 
TransactionManager.Instance.EnsureInTransaction(doc)

# loop over each element to delete
for e in elements:
    doc.Delete(e.Id)

# finish transcation in Revit
TransactionManager.Instance.TransactionTaskDone()

OUT = "done"
