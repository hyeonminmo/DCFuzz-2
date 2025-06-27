import atexit
import copy
import datetime
import json
import logging
import math
import os
import pathlib
import random
import signal
import subprocess
import sys
import threading
import time
import traceback
from abc import abstractmethod
from collections import deque
from pathlib import Path
from typing import Deque, Dict, List, Optional

if __package__ is None:
    sys.path.append(
        os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    __package__ = "dcfuzz"

from cgroupspy import trees

#from . import cgroup_utils, cli
from . import config as Config
#from . import coverage, fuzzer_driver, fuzzing, policy, sync, utils
#from .common import IS_DEBUG, IS_PROFILE, nested_dict
#from .datatype import Bitmap
#from .mytype import BitmapContribution, Coverage, Fuzzer, Fuzzers
#from .singleton import SingletonABCMeta




config: Dict = Config.CONFIG


logger = logging.getLogger('dcfuzz.main')


LOG = nested_dict()

OUTPUT: Path
INPUT : Optional[Path]
LOG_DATETIME: str
LOG_FILE_NAME: str

TARGET: str
FUZZERS: Fuzzers = []
CPU_ASSIGN: Dict[Fuzzer, float] = {}

ARGS: cli.ArgsParser


START_TIME: float = 0.0

SLEEP_GRANULARITY: int = 60

RUNNING: bool = False



def cleanup(exit_code=0):
    global ARGS
    logger.info('cleanup')
    LOG['end_time'] = time.time()
    write_log()
    for fuzzer in FUZZERS:
        stop(fuzzer)
    if exit_code == 0 and ARGS.tar:
        save_tar()
    os._exit(exit_code)


def cleanup_exception(etype, value, tb):
    traceback.print_exception(etype, value, tb)
    cleanup(1)

# An initialization function that prepares the execution environment before fuzzing by setting up termination and exception handling, creating a health check file, and initializing the logging structure.
def init():
    global START_TIME, LOG
    signal.signal(signal.SIGTERM, lambda x, frame: sys.exit(0))
    signal.signal(signal.SIGINT, lambda x, frame: sys.exit(0))
    atexit.register(cleanup)
    sys.excepthook = cleanup_exception
    health_check_path = os.path.realpath(os.path.join(ARGS.output, 'health'))
    pathlib.Path(health_cehck_path).touch(mode=0o666, exist_ok=True)
    LOG['log'] = []
    LOG['round'] = []





def start(fuzzer: Fuzzer,
          output_dir,
          timeout,
          input_dir=None,
          empty_seed=False):
    '''
    call Fuzzer API to start fuzzer
    '''

    global  FUZZERS, ARGS
    fuzzer_config = config['fuzzer'][fuzzer]
    create_output_dir = fuzzer_config.get('create_output_dir', True)

    # NOTE: some fuzzers like angora will check whether outptu directory
    #       is non-exsitent and reports error otherwise.
    if create_output_dir:
        host_output_dir = f'{output_dir}/{ARGS.target}/{fuzzer}'
        os.makedirs(host_output_dir, exist_ok=True)
    else:
        host_output_dir = f'{output_dir}/{ARGS.target}'
        if os.path.exists(f'{output_dir}/{ARGS.target}/{fuzzer}'):
            logger.error(f'Please remove {output_dir}/{ARGS.target}/{fuzzer}')
            terminate_dcfuzz()
        os.makedirs(host_output_dir, exist_ok=True)
    
    kw = gen_fuzzer_driver_args(fuzzer=fuzzer,
                                input_dir=input_dir,
                                empty_seed=empty_seed)
    kw['command'] = 'start'

    fuzzer_driver.main(**kw)

    scale(fuzzer=fuzzer,
          scale_num=1,
          input_dir=input_dir,
          empty_seed=empty_seed)



def init_cgroup():
    '''
    cgroup /dcfuzz is created by /init.sh, the command is the following:

    cgcreate -t yufu -a yufu -g cpu:/autofz
    '''
    global FUZZERS, CGROUP_ROOT
    cgroup_path = cgroup_utils.get_cgroup_path()
    container_id = os.path.basename(cgroup_path)
    cgroup_path_fs = os.path.join('/sys/fs/cgroup/cpu', cgroup_path[1:])
    dcfuzz_cgroup_path_fs = os.path.join(cgroup_path_fs, 'dcfuzz')

    if not os.path.exists(dcfuzz_cgroup_path_fs):
        logger.critical(
            'dcfuzz cgroup not exists. make sure to run /init.sh first')
        terminate_autofz()

    t = trees.Tree()
    p = os.path.join('/cpu', cgroup_path[1:], 'dcfuzz')
    CGROUP_ROOT = os.path.join(cgroup_path, 'dcfuzz')

    cpu_node = t.get_node_by_path(p)

    for fuzzer in FUZZERS:
        fuzzer_cpu_node = t.get_node_by_path(os.path.join(p, fuzzer))

        if not fuzzer_cpu_node:
            fuzzer_cpu_node = cpu_node.create_cgroup(fuzzer)

        cfs_period_us = fuzzer_cpu_node.controller.cfs_period_us
        quota = int(cfs_period_us * (JOBS))
        fuzzer_cpu_node.controller.cfs_quota_us = quota

    return True









def main():
    global ARGS, FUZZERS, TARGET

    ARGS = cli.ArgsParser().parse_args()
    TARGET = ARGS.target

    unsupported_fuzzers = config['target'][TARGET].get('unsupported',[])
    available_fuzzers = list(config['fuzzer'].keys())

    available_fuzzers = [ 
        fuzzer for fuzzer in available_fuzzers
        if fuzzer not in unsupported_fuzzers
    ]

    FUZZERS = availabe_fuzzers if 'all' in ARGS.fuzzer else ARGS.fuzzer


    for fuzzer in FUZZERS:
        if not fuzzing.check(TARGET, fuzer, OUTPUT):
            exit(1)

    try:
        os.makedirs(OUTPUT, exist_ok=False)
    except FileExistsError:
        logger.error(f'remove {OUTPUT{')
        exit(1)

    with open(os.path.join(OUTPUT, 'cmdline', 'w')) as f:
        cmdline = " ".join(sys.argv)
        LOG['cmd'] = cmdline
        f.write(f"{cmdline}\n")

    init()
    current_time = time.time()

    # set the run-time for each phase
    SYNC_TIME = ARGS.sync


    timeout = ARGS.timeout


    # evaluate fuzzer
    # ?

    START_TIME = time.time()

    init_cgroup()

    # setup fuzzer

    for fuzzer in FUZZERS :
        logger.info(f'warm up {fuzzer}')
        CPU_ASSIGN[fuzzer] = 0
        start(fuzzer=fuzzer,
                output_dir=OUTPUT,
                timeout=timeout,
                input_dir=INPUT,
                empty_seed=ARGS.empty_seed)























if __name__ == '__main__':
    main()
