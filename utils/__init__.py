import logging
import os
from pathlib import Path

import pandas as pd
from pandas import DataFrame

from settings import SRC_DIR, TEAMS


class ReportReader:
    teams = TEAMS

    def __init__(self, report: str):
        self.report = report

    @property
    def consolidated_report(self) -> DataFrame:
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

    @property
    def master_report(self):
        return self.read_report('MASTER')

    def read_report(self, team) -> DataFrame:
        filename = self.report + '.xlsx'
        if team == 'MASTER':
            filename = f'{self.report}_masterdata.xlsx'

            if self.report == 'UnclassifiedException':
                filename = 'UnclassifiedException.xlsx'

        report_dir = os.path.join(SRC_DIR, team)
        report_path = os.path.join(report_dir, filename)

        if not Path(report_path).is_file():
            raise FileNotFoundError(f"'{filename}' does not exist in {report_path}")

        report = pd.read_excel(report_path)

        return report
