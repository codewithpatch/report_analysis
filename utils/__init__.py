import glob
import logging
import os
from datetime import timedelta, date
from pathlib import Path

import pandas as pd
from pandas import DataFrame

from settings import SRC_DIR, TEAMS, DATE


class ReportReader:
    teams = TEAMS

    def __init__(self, report: str):
        self.report = report
        self.consolidated_report = self.__consolidate_report()

    @property
    def master_report(self):
        return self.read_report('MASTER')

    def __consolidate_report(self) -> DataFrame:
        logging.info(f"Consolidating '{self.report}' report for {self.teams}.")
        consolidated_df = pd.DataFrame()
        for team in self.teams:
            logging.info(f"Reading '{self.report}' for '{team}'...")
            report_df = self.read_report(team)

            if self.report != 'MISMATCH':
                report_df['Team'] = team
            else:
                report_df.loc[report_df['SI'].notnull(), 'Team'] = team

            consolidated_df = pd.concat([consolidated_df, report_df])

        return consolidated_df

    def read_report(self, team) -> DataFrame:
        report = ReportPath(report=self.report, team=team)
        report_df = pd.read_excel(report.filepath)

        return report_df


class ReportPath:
    def __init__(self, report, team):
        self.report = report
        self.team = team

        # date format ex: 16 Oct 2020
        self.process_date = prev_weekday(DATE).strftime('%d %b %Y')

        self.dir = os.path.join(SRC_DIR, self.team)
        self.glob_path = os.path.join(self.dir, self.glob_filename)
        self.filepath = os.path.join(self.dir, self.filename)

    @property
    def filename(self):
        files = glob.glob(self.glob_path)
        if len(files) > 1:
            raise FileExistsError(f"Two files found for Report '{self.report}' - Team '{self.team}'. "
                                  f"Check '{self.dir}' for duplicate files.'")

        if not files:
            raise FileNotFoundError(f"No file found for Globpath: '{self.glob_path}' - Report '{self.report}'"
                                    f" - Team '{self.team}'. "
                                    f"Check Directory: '{self.dir}'.")

        return files[0]

    @property
    def glob_filename(self):
        report_split = list(self.report)
        report_glob = map(lambda e: f"[{e.upper()}{e.lower()}]", report_split)
        report_glob = str().join(report_glob)
        if self.team == 'MASTER':
            return f'{report_glob}-{self.process_date}*.xlsx'
        else:
            return f'{report_glob}*.xlsx'


def prev_weekday(adate: date) -> date:
    adate -= timedelta(days=1)
    while adate.weekday() > 4:  # Mon-Fri are 0-4
        adate -= timedelta(days=1)
    return adate


