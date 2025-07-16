import os
import pathlib
import sys
import time

import peewee
import psutil

from dcfuzz import config as Config
from .db import AFLGoModel, ControllerModel, db_proxy
from .fuzzer import FuzzerDriverException, PSFuzzer


class AFLGoBase(PSFuzzer):
    def __init__(self,
                 seed,
                 output,
                 group,
                 program,
                 argument,
                 master=True,
                 cgroup_path='',
                 fuzzer_id=0,
                 pid=None):

        super().__init__(pid)

