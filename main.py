import logging
import os
from pathlib import Path

import pandas as pd
from pandas import DataFrame

from settings import TEAMS, SRC_DIR, REPORTS
from utils import ReportReader


if __name__ == '__main__':
    reader = ReportReader('ExceptionRecords')
