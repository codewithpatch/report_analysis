import logging
import os

from pandas import DataFrame

from pipelines import generate_output, generate, generate_no_comment_df, write_to_excel
from pipelines.exception_records import ExceptionRecordsPipeline
from settings import OUT_DIR
from utils import ReportReader
import pandas as pd
import numpy as np


def generate_exception_records() -> DataFrame:
    logging.info("Generating exception report for MissinginSAA lookup...")
    pipeline = ExceptionRecordsPipeline()
    pipeline.process_df()

    return pipeline.master_df.copy()


class MissingInSaaPipeline(ReportReader):
    report = 'MissingInSAA'

    def __init__(self):
        super(MissingInSaaPipeline, self).__init__(report=self.report)
        self.master_df = self.master_report

        self.master_df['Team'] = np.nan
        self.master_df['Comments'] = np.nan

        self.exception_report = generate_exception_records()

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
            'Trade ID': df['Trade ID'],
            'CCY': df['CCY'],
            'Amount': df['Amount'],
            'Msg Type': df['Msg Type']
        }
        df['Comments'] = generate(df=self.consolidated_report, column='Comments', **criteria)

        is_reversal = self.__lookup_exception_report(df['Trade ID'])
        if is_reversal:
            df['Comments'] = 'reversal'

        return df

    def __add_team(self, df):
        criteria = {
            'Trade ID': df['Trade ID'],
            'CCY': df['CCY'],
            'Amount': df['Amount'],
            'Msg Type': df['Msg Type']
        }
        df['Team'] = generate(df=self.consolidated_report, column='Team', **criteria)

        return df

    def __lookup_exception_report(self, trade_id):
        df = self.exception_report
        result_df = df.loc[df['Trade ID'] == trade_id, 'Comments']

        if result_df.empty:
            return False

        if result_df.item().lower() == 'reversal':
            return True

        return False
