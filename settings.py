import os

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