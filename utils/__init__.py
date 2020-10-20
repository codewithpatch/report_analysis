import glob
import logging
import os

import pandas as pd
from pandas import DataFrame

from settings import SRC_DIR, TEAMS, DATE_TO_PROCESS


class ReportReader:
    teams = TEAMS

    def __init__(self, report: str):
        self.report = report
        self.consolidated_report = self.__consolidate_report()

    @property
    def master_report(self):
        folder_name = 'MASTER'
        report_df = self.read_report(folder_name)
        report_df['Value Date'] = report_df['Value Date'].apply(datetime_to_date)
        if self.report != 'MISMATCH':
            report_df = report_df.loc[report_df['Value Date'] == DATE_TO_PROCESS]

        return report_df

    def __consolidate_report(self) -> DataFrame:
        logging.info(f"Consolidating '{self.report}' report for {self.teams}.")
        consolidated_df = pd.DataFrame()
        for team in self.teams:
            if team.lower() == 'funding':
                continue

            logging.info(f"Reading '{self.report}' for '{team}'...")
            report_df = self.read_report(team)

            if self.report != 'MISMATCH':
                report_df['Team'] = team
            else:
                report_df.loc[report_df['SI'].notnull(), 'Team'] = team

            consolidated_df = pd.concat([consolidated_df, report_df])

        consolidated_df['Value Date'] = consolidated_df['Value Date'].apply(datetime_to_date)
        if self.report != 'MISMATCH':
            consolidated_df = consolidated_df.loc[consolidated_df['Value Date'] == DATE_TO_PROCESS]

        return consolidated_df

    def read_report(self, team, any_file=None, filename=None) -> DataFrame:
        report = ReportPath(report=self.report, team=team, any_file=any_file, filename=filename)
        report_df = pd.read_excel(report.filepath)

        return report_df
# Usage
# report = ReportReader(report='ReportName')
# report.read_report(team='TEAM1')


class ReportPath:

    def __init__(self, report, team, any_file=False, filename=None):
        self.report = report
        self.team = team
        self.any_file = any_file
        self._filename = filename

        # date format ex: 16 Oct 2020
        self.process_date = DATE_TO_PROCESS.strftime('%d %b %Y')

        self.glob_path = os.path.join(self.dir, self.glob_filename)
        self.filepath = os.path.join(self.dir, self.filename)

    @property
    def filename(self):
        if self._filename:
            return self._filename

        files = glob.glob(self.glob_path)
        if len(files) > 1:
            raise FileExistsError(f"Two files found for Report '{self.report}' - Team '{self.team}'. "
                                  f"Check '{self.dir}' for duplicate files.'")

        if not files:
            raise FileNotFoundError(f"No file found for Globpath: '{self.glob_path}' - Report '{self.report}'"
                                    f" - Team '{self.team}'. "
                                    f"Check Directory: '{self.dir}'.")

        return os.path.basename(files[0])

    @property
    def dir(self):
        folder_date = DATE_TO_PROCESS.strftime('%y%m%d')
        return os.path.join(SRC_DIR, self.team, folder_date)

    @property
    def glob_filename(self):
        if self.any_file:
            return '[!~$]*.xlsx'

        report_split = list(self.report)
        report_glob = map(lambda e: f"[{e.upper()}{e.lower()}]", report_split)
        report_glob = str().join(report_glob)

        # if self.team == 'MASTER':
        #     # return f'{report_glob}-{self.process_date}*.xlsx'
        #     return f'{report_glob}*.xlsx'
        # else:
        #     return f'{report_glob}*.xlsx'

        return f'{report_glob}*.xlsx'
# Usage
# rpath = ReportPath(report='ExceptionRecords', team='BONDS')


def datetime_to_date(value):
    try:
        # format date 2020-10-15 or date(2020, 10, 15)
        return value.date()
    except AttributeError:
        return value
