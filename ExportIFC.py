#Based on a Nicklas Verdier Østergaard's script, nvo@niras.dk
#Revised by Alban de Chasteigner

import clr
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

def tolist(obj1):
    if hasattr(obj1,"__iter__"): return obj1
    else: return [obj1]

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application
uidoc=DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument

folder=UnwrapElement(IN[0])
view = tolist(UnwrapElement(IN[1]))
name=tolist(UnwrapElement(IN[2]))
fileversion = IN[3]
Projectorigin = IN[4]
userDefinedPset = IN[5]
exportbasequantities = IN[6]

if userDefinedPset != "":
        userDefPsetBool= "true"
else:
        userDefPsetBool= "false"

TransactionManager.Instance.EnsureInTransaction(doc)
result = []

for i,v in enumerate(view):
        options=IFCExportOptions()

        #if fileversion != None:
        #       options.FileVersion = fileversion
        if fileversion == "IFC4":
                options.FileVersion = IFCVersion.IFC4
        if fileversion == "IFC4x3":
                options.FileVersion = IFCVersion.IFC4x3 
        if fileversion == "IFC4RV":
                options.FileVersion = IFCVersion.IFC4RV
        if fileversion == "IFC4DTV":
                options.FileVersion = IFCVersion.IFC4DTV
        if fileversion == "IFC2x2":
                options.FileVersion = IFCVersion.IFC2x2
        if fileversion == "IFC2x3":
                options.FileVersion = IFCVersion.IFC2x3
        if fileversion == "IFC2x3CV2":
                options.FileVersion = IFCVersion.IFC2x3CV2
        if fileversion == "IFC2x3BFM":
                options.FileVersion = IFCVersion.IFC2x3BFM
        if fileversion == "IFC2x3FM":
                options.FileVersion = IFCVersion.IFC2x3FM
        if fileversion == "IFCBCA":
                options.FileVersion = IFCVersion.IFCBCA
        if fileversion == "IFCCOBIE":
                options.FileVersion = IFCVersion.IFCCOBIE
        if fileversion == "":
                options.FileVersion = IFCVersion.Default

        options.AddOption("WallAndColumnSplitting", "false")    # trennt Bauteile an Geschossebenen. Fast immer besser händische Kontrolle zu haben        
               
        options.FilterViewId = v.Id

        options.AddOption("SitePlacement", IN[4])   # Ursprung: 0=Gemeinsam genutzt, 1=Vermessungspkt, 2=Projekt-Basispkt,
                                                    # 3=InternerUrsprung, 4=Projekt-Basispkt genordet, 5=InternerUrsprung genordnet
        options.AddOption("SpaceBoundaries ", "1")  # Raumbegrenzung: 0=Keine, 1=1.Ebene, 2=2.Ebene

        #### Additional Content Tab ####
        options.AddOption("VisibleElementsOfCurrentView ", "true")  # exportiert nur Elemente in der aktiven Ansicht
        options.AddOption("ExportRoomsInView", "false")             # exportiert Räume
        options.AddOption("IncludeSteelElements", "true")           # exportiert Stahlverbindungen, für uns meist nicht relevant
        options.AddOption("Export2DElements", "false")              # exportiert 2D-Elemente, wird aber von Revit kaum unterstützt
        options.AddOption("ExportLinkedFiles", "false")             # exportiert Verlinkungen, funktioniert nicht, Modelle müssten im Hintergrund geöffnet werden

        #### Property Sets Tab ####
        options.ExportBaseQuantities = exportbasequantities             # BaseQuantities: Exportiert die Basismengen, immer einschalten
        options.AddOption("ExportInternalRevitPropertySets", "false")   # exportiert alle Revit-Eigenschaften an jedem Bauteil. Immer ausschalten
        options.AddOption("ExportIFCCommonPropertySets","true")         # exportiert IFC-Standard-Eigenschaften wie WallCommon: IsExternal, LoadBearing
        options.AddOption("ExportSchedulesAsPsets", "false")            # exportiert Parameter über Bauteillisten, nutzen wir nicht
        options.AddOption("ExportSpecificSchedules", "false")           # exportiert Parameter über Bauteillisten, nutzen wir nicht           
        options.AddOption("ExportUserDefinedPsets",userDefPsetBool)     # exportiert Parameter über eine Mappingdatei, Standard für jedes Projekt
        if userDefinedPset != "":
                options.AddOption("ExportUserDefinedPsetsFileName",userDefinedPset)
        else:
                pass

        #### Advanced Tab ####
        options.AddOption("ExportPartsAsBuildingElements", "true")      # Bauteile die in Revit mit Teilelemente unterteilt wurden werden nicht als IfcElementPart
                                                                        # ausgegeben, sondern als die urpsrüngliche Revitkategorie z.B. IfcSlab für Geschossdecken
        options.AddOption("ExportSolidModelRep", "true")                # erlaubt eine Mischung von BREPS und Meshes was zu kleineren Dateigrößen führt
        options.AddOption("UseActiveViewGeometry", "true")              # nutzt den Detaillierungsgrad der Exportansicht
        options.AddOption("UseFamilyAndTypeNameForReference ", "false") # Bezeichnung für "Reference" in den PSets: true= Basiswand:B_W_I_0,3, false= B_W_I_0,3
        options.AddOption("Use2DRoomBoundaryForVolume", "false")        # true= Vereinfacht das Revit-Raumvolumen, false= nimmt die 3D-Raumgeometrie aus Revit
        options.AddOption("IncludeSiteElevation","false")               # bei Georeferenzierten Exporten einschalten, ansonsten ausschalten
        options.AddOption("StoreIFCGUID", "true")                       # schreibt das IfcGuid in einen Revitparameter, hilfreich beim Suchen der Bauteile
        options.AddOption("ExportBoundingBox", "false")                 # erlaubt den Export von Boundingboxen, fast immer irrelevant für uns, also ausschalten
        options.AddOption("UseOnlyTriangulation", "false")              # true= in Revit triangulierte Flächen dürfen vereinfacht werden, false= Triangulation bleibt unverändert
        options.AddOption("UseTypeNameOnlyForIfcType", "true")          # IFC-Typname: true= B_W_I_0,3, false= Basiswand:B_W_I_0,3
        options.AddOption("UseVisibleRevitNameAsEntityName", "true")    # IFC-Name: true= Wände : Basiswand : B_W_I_0,3, false= Basiswand:B_W_I_0,3:123456
        
        #### Level of Detail Tab ####
        options.AddOption("TessellationLevelOfDetail", "0,5")           # Detaillierungsgrad für die Triangulierung beim Export, Wert von 0 (niedrig) bis 1 (hoch)
       
        c=doc.Export(folder, name[i], options)
        result.append(c)

# End Transaction
TransactionManager.Instance.TransactionTaskDone()

if fileversion == "":
        OUT="Default settings used"
else:
        OUT='Success'
