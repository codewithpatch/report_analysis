from pipelines import generate_output, generate, generate_no_comment_df
from utils import ReportReader
import pandas as pd
import numpy as np


class TemplatePipeline(ReportReader):
    report = 'Enter Report Name Here'

    def __init__(self):
        super().__init__(report=self.report)
        self.master_df = self.master_report

        self.master_df['Team'] = np.nan
        self.master_df['Comments'] = np.nan

    @property
    def no_comment_df(self):
        return generate_no_comment_df(self.master_df)

    def process_df(self):
        self.master_df = self.master_df.apply(self.__add_comment, axis=1)
        self.master_df = self.master_df.apply(self.__add_team, axis=1)

    def end_process(self):
        generate_output(
            report_name=self.report,
            conso_df=self.master_df,
            no_comment_df=self.no_comment_df
        )

    def __add_comment(self, df):
        criteria = {
            'ColumnName1': df['ColumnName1'],
            'ColumnName2': df['ColumnName2']
        }
        df['Comments'] = generate(df=self.consolidated_report, column='Comments', **criteria)

        return df

    def __add_team(self, df):
        criteria = {
            'ColumnName1': df['ColumnName1'],
            'ColumnName2': df['ColumnName2']
        }
        df['Team'] = generate(df=self.consolidated_report, column='Team', **criteria)

        return df
