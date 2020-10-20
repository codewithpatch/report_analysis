import logging
import os
from datetime import date

logging.basicConfig(
    format='%(asctime)s %(levelname)-6s %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S',
    level=logging.DEBUG,
)

# To change date to specific date
# Use this format -> date(2012, 8, 20)
# DATE = date.today()
DATE = date(2020, 10, 19)

ROOT_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.join(ROOT_DIR, 'src')

# TEAMS DIRECTORY
BONDS_DIR = os.path.join(SRC_DIR, 'BONDS')
EQD_STRUCT_DIR = os.path.join(SRC_DIR, 'EQD STRUCT')
FXMM_DIR = os.path.join(SRC_DIR, 'FXMM')
MASTER_DIR = os.path.join(SRC_DIR, 'MASTER')

TEAMS = ['BONDS', 'EQD STRUCT', 'FXMM']
REPORTS = ['ExceptionRecords', 'MISMATCH', 'UnclassifiedException']

# OUTPUT DIRECTORY
OUT_DIR = os.path.join(ROOT_DIR, 'output')