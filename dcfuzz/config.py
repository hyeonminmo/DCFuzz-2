#!/usr/bin/env python3

'''
config file for dcfuzz
'''

import os
import sys
import tempfile
from typing import Dict

# FIXME
if not __package__:
    sys.path.append(
        os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    __package__ = "dcfuzz"

INPUT_DIR = 'queue'
CRASH_DIR = 'crashes'

# NOTE: you can define your own config
CONFIG: Dict = {
    # these will be default parameters for cli.py
    'scheduler': {
        'prep_time': 300,
        'focus_time': 300,
        'coverage_update_time': 30,
        'sync_time': 300,
        'timeout': '24h'
    },
    # unused now
    'docker': {
        'root_dir': '/work/dcfuzz',
        'network': 'dcfuzz'
    },
    # binary directories for AFL-compiled binaries
    # justafl is used to get AFL bitmap
    # aflasan is used to triage crashes/bugs
    'evaluator': {
        'binary_root': '/d/p/justafl',
        'binary_crash_root': '/d/p/aflasan',
    },
    # only specify basic things
    # how to launch fuzzers with proper arguments is handled by fuzzer driver
    'fuzzer': {
        'aflgo': {
            'input_dir': INPUT_DIR, # queue dir
            'crash_dir': CRASH_DIR,
            'skip_crash_file': ['README.txt'],
            'command': '/fuzzer/aflgo/afl-fuzz', # fuzzer binary path
            'target_root': '/benchmark/bin/AFLGo', # which binary is used to fuzz
            'afl_based': True,
        },
        'windranger': {
            'input_dir': INPUT_DIR,
            'crash_dir': CRASH_DIR,
            'skip_crash_file': ['README.txt'],
            'command': '/fuzzer/windranger/fuzz/afl-fuzz',
            'target_root': '/',
            'afl_based': True
        },
        'fairfuzz': {
            'input_dir': INPUT_DIR,
            'crash_dir': CRASH_DIR,
            'skip_crash_file': ['README.txt'],
            'command': '/fuzzer/afl-rb/afl-fuzz',
            'target_root': '/d/p/justafl',
            'afl_based': True
        }
    }
