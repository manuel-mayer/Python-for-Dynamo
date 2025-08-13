# Finds empty entries in a list and returns their index. Works with nested lists.

inputList = IN[0]

# Define what counts as empty
def is_empty(item):
    return item is None or item == "" or (isinstance(item, list) and len(item) == 0)

# Recursive function to find empty indexes
def find_empty_indexes(lst, path=[]):
    empty_paths = []
    if isinstance(lst, list):
        for i, item in enumerate(lst):
            new_path = path + [i]
            if isinstance(item, list):
                empty_paths.extend(find_empty_indexes(item, new_path))
            elif is_empty(item):
                empty_paths.append(new_path)
    elif is_empty(lst):
        empty_paths.append(path)
    return empty_paths

# Output: List of index paths
OUT = find_empty_indexes(inputList)
