# Importing the 'Common Language Runtime' library
import clr
# Adding specific references: The Revit API
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *
clr.AddReference('RevitNodes')
import Revit
# Importing specific extension methods that allow us to gain
# information such as 'Coord' data
clr.ImportExtensions(Revit.GeometryConversion)
clr.ImportExtensions(Revit.Elements)
# Creating an empty list that we populate later
OUT = []
# Running a 'for loop' over everything inside our input list
# by Unwrapping them (Which is requried between Revit and Dynamo
# objects
for item in UnwrapElement(IN[0]):
    # For our 'for loop' to work, we need to indent as Python is 
    # very particular about indentation. We simply then 'nest' in
    # our line of code an appendation of each 'looped' item into
    # our previously created empty list. We then 'cast' the data
    # to a Point (Which dynamo can read)
    OUT.append(item.Coord.ToPoint())
    # Natively, Dynamo understands that the OUT is our output, so
    # pushes this data through the node out port
