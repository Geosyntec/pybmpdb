import json
from pkg_resources import resource_filename

from ._parameters import parameters
from ._units import units


__all__ = ["getUnits", "getTexParam", "getTexUnit", "getNormalization", "getConversion"]


def _find_by_name(value_string, list_of_dicts, key="name"):
    # get the parameter's entry in the lookup list of dicts
    _entry = list(
        filter(
            lambda x: x[key].strip().lower() == value_string.strip().lower(),
            list_of_dicts,
        )
    )

    if len(_entry) != 1:
        msg = "Found ({}) entries found for {}. Expected 1."
        raise ValueError(msg.format(len(_entry), value_string))

    return _entry[0]


def getUnitsFromParam(paramname, attr="name"):
    """
    Returns the standard units for a given parameter
    """
    p = _find_by_name(paramname, parameters)
    u = _find_by_name(p["units"], units)
    return u[attr]


def getUnits(unitname, attr="name"):
    """
    Returns the standard units for a given parameter
    """
    u = _find_by_name(unitname, units)
    return u[attr]


def getParam(paramname, attr="name"):
    p = _find_by_name(paramname, parameters)
    return p[attr]


def getNormalization(unit):
    """
    Returns the factor by which you should multiply a result
    to normalize the given units to the base units for that
    quantity (e.g., ng/L -> g/L)
    """
    if unit is None:
        _factor = 1
    else:
        # get the unit's entry
        u = _find_by_name(unit, units)
        _factor = u["factor"]

    return _factor


def getConversion(param):
    """
    Returns the factor by which you should divide a *normalized*
    result to convert to the standard units for that parameter
    (e.g., g/L -> ug/L for Dissolved Lead)
    """

    # get the parameter's entry in the lookup list of dicts
    p = _find_by_name(param, parameters)

    return getNormalization(p["units"])
