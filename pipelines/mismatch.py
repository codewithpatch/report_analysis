import os

import numpy as np

import pandas as pd
from pandas import DataFrame

from pipelines import generate, generate_team, write_to_excel, generate_no_comment_df, generate_output
from settings import OUT_DIR
from utils import ReportReader


class MismatchPipeline(ReportReader):
    report = 'MISMATCH'

    def __init__(self):
        super(MismatchPipeline, self).__init__(report=self.report)
        self.master_df = self.master_report
        self.master_df['Team'] = np.nan
        self.master_df['Comments'] = np.nan

    @property
    def no_comment_df(self):
        df = self.master_df
        result_df = pd.DataFrame()
        for block_df in self.__df_block(df):
            with_si_no_comment = block_df.loc[
                (block_df.SI.notnull()) & (
                    (block_df['Comments'].str.lower().str.startswith('belongs to')) |
                    (block_df['Comments'].str.lower().str.startswith('not ours')) |
                    (block_df.Comments.isnull())
                )
            ]
            if with_si_no_comment.empty:
                continue

            result_df = pd.concat([result_df, block_df])
        return result_df

    @staticmethod
    def __df_block(df: DataFrame):
        with_si = df.loc[(df['SI'].notnull())]
        i = 0
        for row in df.iterrows():
            if str(row[1].SI) == 'nan':
                continue

            index = row[1].name
            try:
                next_index = with_si.iloc[i+1].name
            except IndexError:
                yield df[index::]
                break

            block_df = df[index:next_index]
            yield block_df

            i += 1

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
        if str(df['SI']) == 'nan':
            return df

        criteria = {
            'MSG Type': df['MSG Type'],
            'SAA Ref': df['SAA Ref'],
            'MX Amt': df['MX Amt']
        }
        df['Comments'] = generate(df=self.consolidated_report, column='Comments', **criteria)
        return df

    def __add_team(self, df):
        if str(df['SI']) == 'nan':
            return df

        criteria = {
            'MSG Type': df['MSG Type'],
            'SAA Ref': df['SAA Ref'],
            'MX Amt': df['MX Amt']
        }

        df['Team'] = generate(df=self.consolidated_report, column='Team', **criteria)

        return df
