# Adds shared parameters from a shared parameter textfile to a family document.
# Only Works in Revit2025 and later because of API changes of GroupTypeId.

import clr

clr.AddReference("RevitServices")
clr.AddReference("RevitAPI")

from RevitServices.Persistence import DocumentManager
from Autodesk.Revit.DB import Transaction, GroupTypeId

# Inputs
param_names = [str(p) for p in IN[0]]           # List of parameter names
group_name = str(IN[1])                         # Shared parameter group name
shared_param_file_path = str(IN[2])             # Full path to .txt file
is_instance = bool(IN[3])                       # True = instance, False = type

doc = DocumentManager.Instance.CurrentDBDocument
app = DocumentManager.Instance.CurrentUIApplication.Application

results = []

if not doc.IsFamilyDocument:
    OUT = "❌ This script must be run in a family document."
else:
    try:
        app.SharedParametersFilename = shared_param_file_path
        shared_param_file = app.OpenSharedParameterFile()

        if not shared_param_file:
            raise Exception("Failed to open shared parameter file.")

        group = shared_param_file.Groups.get_Item(group_name)
        if not group:
            raise Exception(f"Group '{group_name}' not found.")

        # You can change this group as needed
        param_group = GroupTypeId.Geometry   # ← change to .IdentityData, .Text, etc. if desired

        t = Transaction(doc, "Add Shared Parameters")
        t.Start()

        # Quick lookup of existing parameter names
        existing_params = {p.Definition.Name for p in doc.FamilyManager.GetParameters()}

        for name in param_names:
            definition = group.Definitions.get_Item(name)
            if not definition:
                results.append(f"❌ Parameter '{name}' not found in group '{group_name}'")
                continue

            if name in existing_params:
                results.append(f"⚠️ Parameter '{name}' already exists")
                continue

            try:
                doc.FamilyManager.AddParameter(definition, param_group, is_instance)
                results.append(f"✅ Parameter '{name}' added successfully")
                existing_params.add(name)  # keep lookup up-to-date
            except Exception as e:
                err = str(e).lower()
                if "already in use" in err or "already exists" in err:
                    results.append(f"⚠️ Parameter '{name}' is already in use in this family")
                else:
                    results.append(f"❌ Error adding '{name}': {str(e)}")

        t.Commit()
        OUT = results

    except Exception as e:
        if 't' in locals() and t.HasStarted() and not t.HasEnded():
            t.RollBack()
        OUT = f"❌ Script error: {str(e)}"
