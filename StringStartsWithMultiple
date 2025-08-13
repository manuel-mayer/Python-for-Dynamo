# Expands the funtionality of the dynamo String.StartsWith node. 
# Multiple filter inputs are supported and the script returns all elements if filter is empty.

# Inputs:
# IN[0] = inputList: List[List[str]]
# IN[1] = filterString: str (comma-separated)

inputList = IN[0]
filterString = IN[1]

# Parse filter string into list of prefixes
filterNames = [f.strip() for f in filterString.split(",") if f.strip()] if filterString else []

def should_include(s):
    # Return True if string does NOT start with any filter name
    return not any(s.startswith(f) for f in filterNames)

# Apply filtering to each sublist
filteredList = []
for sublist in inputList:
    filteredSublist = [s for s in sublist if should_include(s)]
    filteredList.append(filteredSublist)

# Output
OUT = filteredList
