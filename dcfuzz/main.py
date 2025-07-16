#!/usr/bin/env python3 
import sys, os, time, shutil
import os
import time
import shutil
import signal
import subprocess
import logging
import datetime
import copy
import threading


from . import config as Config


# Global variable

config: Dict = Config.CONFIG

logger = logging.getLogger('dcfuzz.main')

logging.basicConfig(level=logging.INFO, filename='testlogging.log', filemode='w', format ='%(asctime)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s')


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






def main():
    global ARGS, FUZZERS, TARGET

    ARGS = cli.ArgsParser().parse_args()

    TARGET = ARGS.target

    FUZZERS = ARGS.fuzzer

    for fuzzer in FUZZERS:
        if fuzzing.check(TARGET, fuzzer, OUTPUT):
            logger.error(f'false {fuzzer}')
            exit(1)

    try:
        os.mkedirs(OUTPUT, exist_ok=False)
    except FileExistsError:
        logger.error(f'remove {OUTPUT}')
        exit(1)







if __name__ == "__main__":
    main()








