# Changes the value of a very simple revit viewfilter.
# Example: Parameter is not A -> Parameter is not B
# Inputs: [0] = ID of viewfilter, [1] = new paramter value as string

import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import *
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument
pfe = UnwrapElement(IN[0])     # ParameterFilterElement
new_x = str(IN[1])             # new "not equal" value

TransactionManager.Instance.EnsureInTransaction(doc)

try:
    filter_obj = pfe.GetElementFilter()
    
    # Unwrap to get the ElementParameterFilter
    if isinstance(filter_obj, LogicalAndFilter):
        subfilters = filter_obj.GetFilters()
        if len(subfilters) != 1:
            raise Exception("AND has {} subfilters (expected 1)".format(len(subfilters)))
        eparam_filter = subfilters[0]
    else:
        eparam_filter = filter_obj
    
    if not isinstance(eparam_filter, ElementParameterFilter):
        raise Exception("Not an ElementParameterFilter")
    
    rules = eparam_filter.GetRules()
    if len(rules) != 1:
        raise Exception("Expected 1 rule, found {}".format(len(rules)))
    
    old_rule = rules[0]
    
    # Handle possible FilterInverseRule
    if isinstance(old_rule, FilterInverseRule):
        inner_rule = old_rule.GetInnerRule()
        param_id = old_rule.GetRuleParameter()   # works on inverse
        is_inverted = True
    else:
        inner_rule = old_rule
        param_id = old_rule.GetRuleParameter()
        is_inverted = False
    
    # Create new NOT EQUALS rule (same param, new value)
    new_inner_rule = ParameterFilterRuleFactory.CreateNotEqualsRule(
        param_id,
        new_x,
        True   # case sensitive
    )
    
    # Re-apply inverse if original was inverted
    final_rule = FilterInverseRule(new_inner_rule) if is_inverted else new_inner_rule
    
    new_eparam = ElementParameterFilter(final_rule)
    
    # Re-apply AND wrapper if original had it
    if isinstance(filter_obj, LogicalAndFilter):
        pfe.SetElementFilter(LogicalAndFilter([new_eparam]))
    else:
        pfe.SetElementFilter(new_eparam)
    
    OUT = "Filter updated"

except Exception as e:
    OUT = str(e)

TransactionManager.Instance.TransactionTaskDone()
