#!/usr/bin/env python

__author__    = "Vivek <vivek.balasubramanian@rutgers.edu>"
__copyright__ = "Copyright 2016, http://radical.rutgers.edu"
__license__   = "MIT"

from copy import deepcopy

from radical.entk import NoKernelConfigurationError
from radical.entk import KernelBase

# ------------------------------------------------------------------------------
# 
_KERNEL_INFO = {
            "name":         "grompp",
            "description":  "Gromacs preprocessing kernel",
            "arguments":   {"--mdp=":     
                        {
                            "mandatory": True,
                            "description": "Parameter file"
                        },
                        "--conf=":     
                        {
                            "mandatory": True,
                            "description": "Configuration file."
                        },
                        "--top=":
                        {
                            "mandatory": True,
                            "description": "Topology file"
                        },
                        "--out=":
                        {
                            "mandatory": True,
                            "description": "Output file"
                        }
                    },
            "machine_configs": 
            {
                "*": {
                    "environment"   : None,
                    "pre_exec"      : None,
                    "executable"    : "grompp",
                    "uses_mpi"      : False
                },
                "xsede.stampede":{
                    "environment"   : None,
                    "pre_exec"      : ['. /opt/apps/lmod/lmod/init/sh','module restore','module load boost','module load gromacs/5.1.2'],
                    "executable"    : "gmx grompp",
                    "uses_mpi"      : False
                },
                "local.localhost":{
                    "environment"   : None,
                    "pre_exec"      : ['export PATH=$PATH:/home/vivek91/modules/gromacs-5.1.3/build/bin'],
                    "executable"    : "gmx grompp",
                    "uses_mpi"      : False
                },
                "xsede.comet":{
                    "environment"   : None,
                    "pre_exec"      : ['. /usr/share/Modules/init/sh','module load gromacs'],
                    "executable"    : "gmx grompp",
                    "uses_mpi"      : False
                }
            }
    }


# ------------------------------------------------------------------------------
# 
class grompp_kernel(KernelBase):

    # --------------------------------------------------------------------------
    #
    def __init__(self):
        """Le constructor.
        """
        super(grompp_kernel, self).__init__(_KERNEL_INFO)


    # --------------------------------------------------------------------------
    #
    def _bind_to_resource(self, resource_key):
        """(PRIVATE) Implements parent class method. 
        """
        if resource_key not in _KERNEL_INFO["machine_configs"]:
            if "*" in _KERNEL_INFO["machine_configs"]:
                # Fall-back to generic resource key
                resource_key = "*"
            else:
                raise NoKernelConfigurationError(kernel_name=_KERNEL_INFO["name"], resource_key=resource_key)

        cfg = _KERNEL_INFO["machine_configs"][resource_key]

        executable = cfg['executable']
        arguments  = [  '-f', self.get_arg("--mdp="), 
                        '-c', self.get_arg("--conf="), 
                        '-p', self.get_arg("--top="), 
                        '-o', self.get_arg("--out="), 
                    ]

        self._executable  = executable
        self._arguments   = arguments
        self._environment = cfg["environment"]
        self._uses_mpi    = cfg["uses_mpi"]
        self._pre_exec    = cfg["pre_exec"]

