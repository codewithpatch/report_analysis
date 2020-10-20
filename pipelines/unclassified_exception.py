import os

import numpy as np

from pipelines import generate, generate_team, write_to_excel, generate_no_comment_df, generate_output
from settings import OUT_DIR
from utils import ReportReader


class UnclassifiedExceptionPipeline(ReportReader):
    report = 'UnclassifiedException'

    def __init__(self):
        super(UnclassifiedExceptionPipeline, self).__init__(report=self.report)
        self.master_df = self.master_report

        self.master_df['Team'] = np.nan
        self.master_df['Comments'] = np.nan

    @property
    def no_comment_df(self):
        df = self.master_df.loc[self.master_df['Comments'].isnull()]
        return df

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
        if 'COL' in str(df['Strategy']):
            df['Comments'] = f'Strategy: {df["Strategy"]}'
            return df

        criteria = {
            'Trade Id': df['Trade Id'],
            'Pay/Receive': df['Pay/Receive'],
            'Amount': df['Amount']
        }
        df['Comments'] = generate(df=self.consolidated_report, column='Comments', **criteria)
        return df

    def __add_team(self, df):
        criteria = {
            'Trade Id': df['Trade Id'],
            'Pay/Receive': df['Pay/Receive'],
            'Amount': df['Amount']
        }
        df['Team'] = generate(df=self.consolidated_report, column='Team', **criteria)

        return df
