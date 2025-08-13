# Finds empty entries in a list and returns their index

inputList = IN[0]

# Define what counts as "empty"
def is_empty(item):
    return item is None or item == "" or (isinstance(item, list) and len(item) == 0)

# Collect indexes of empty items
emptyIndexes = [i for i, item in enumerate(inputList) if is_empty(item)]

# Output: List of indexes
OUT = emptyIndexes
