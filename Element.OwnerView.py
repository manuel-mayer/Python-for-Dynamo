import clr

clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import ViewSheet

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

doc = DocumentManager.Instance.CurrentDBDocument

annotations = UnwrapElement(IN[0])

sheets = []
sheet_numbers = []
sheet_names = []
errors = []

for annotation in annotations:
    try:
        # Get the view or sheet that owns this annotation
        owner = doc.GetElement(annotation.OwnerViewId)

        if isinstance(owner, ViewSheet):
            sheets.append(owner.ToDSType(True))
            sheet_numbers.append(owner.SheetNumber)
            sheet_names.append(owner.Name)
            errors.append(None)
        else:
            sheets.append(None)
            sheet_numbers.append(None)
            sheet_names.append(None)
            errors.append("Owner is not a ViewSheet")

    except Exception as e:
        sheets.append(None)
        sheet_numbers.append(None)
        sheet_names.append(None)
        errors.append(str(e))

OUT = sheets, sheet_numbers, sheet_names, errors
