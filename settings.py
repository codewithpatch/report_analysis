import logging
import os
from datetime import date, timedelta

logging.basicConfig(
    format='%(asctime)s %(levelname)-6s %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S',
    level=logging.DEBUG,
)

# To change date to specific date
# Use this format -> date(2012, 8, 20)
# DATE = date.today()
DATE = date(2020, 10, 19)


def prev_weekday(adate: date) -> date:
    adate -= timedelta(days=1)
    while adate.weekday() > 4:  # Mon-Fri are 0-4
        adate -= timedelta(days=1)

    # Format date 2020-10-16 or date(2020, 10, 16)
    return adate


DATE_TO_PROCESS = prev_weekday(DATE)

# TOGGLE WHICH REPORTS TO RUN
'''
RUN_ALL
    1. If True, It will run all reports in the REPORTS dict regardless of the toggle
    2. If False, Check which reports to run in REPORTS dict:
        1. If toggle is 1 -> Run report analysis
        2. If toggle is 0 -> Skip running report analysis
'''
RUN_ALL = False
REPORTS = {
    'ExceptionRecords': 1,
    'Matched': 0,
    'MISMATCH': 0,
    'MissingInMX': 0,
    'MissingInSAA': 0,
    'UnclassifiedException': 0
}

ROOT_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.join(ROOT_DIR, 'src')

# TEAMS DIRECTORY
BONDS_DIR = os.path.join(SRC_DIR, 'BONDS')
EQD_STRUCT_DIR = os.path.join(SRC_DIR, 'EQD STRUCT')
FXMM_DIR = os.path.join(SRC_DIR, 'FXMM')
MASTER_DIR = os.path.join(SRC_DIR, 'MASTER')

TEAMS = ['BONDS', 'EQD STRUCT', 'FXMM']

# OUTPUT DIRECTORY
OUT_DIR = os.path.join(ROOT_DIR, 'output')