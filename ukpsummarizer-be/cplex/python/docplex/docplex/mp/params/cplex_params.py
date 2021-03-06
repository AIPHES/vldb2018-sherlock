# --------------------------------------------------------------------------
# Source file provided under Apache License, Version 2.0, January 2004,
# http://www.apache.org/licenses/
# (c) Copyright IBM Corp. 2015, 2016
# --------------------------------------------------------------------------

# gendoc: ignore
from docplex.mp.params.parameter_hierarchy_12620 import make_root_params_12620
from docplex.mp.params.parameter_hierarchy_12630 import make_root_params_12630
from docplex.mp.params.parameter_hierarchy_12700 import make_root_params_12700
from docplex.mp.params.parameter_hierarchy_12710 import make_root_params_12710
from docplex.mp.params.parameter_hierarchy_12800 import make_root_params_12800

def _make_default_parameters():
    # when cloudcplex switches to 12.7.1 use this.
    return make_root_params_12700()


def get_params_from_cplex_version(cpx_version):
    # INTERNAL
    # returns a parameter tree depending on the cplex version, if any.
    # if none is found, returns a default version.
    if cpx_version is None:
        # this can happen, protect from startswith failure
        return _make_default_parameters()
    if cpx_version.startswith("12.6.2."):
        return make_root_params_12620()
    elif cpx_version.startswith("12.6.3."):
        return make_root_params_12630()
    elif cpx_version.startswith("12.7.0"):
        return make_root_params_12700()
    elif cpx_version.startswith("12.7.1"):
        return make_root_params_12710()
    elif cpx_version.startswith("12.8.0"):
        return make_root_params_12800()
    else:
        return _make_default_parameters()
