import os
from typing import Any

import numpy as np
import pandas as pd
from pandas import DataFrame

from settings import OUT_DIR
from utils import ReportReader


def write_to_excel(df, path):
    try:
        df.to_excel(path, index=False, header=True)
    except FileNotFoundError:
        dir_name = os.path.dirname(path)
        os.mkdir(dir_name)
        df.to_excel(path, index=False, header=True)


def generate_comment(df: DataFrame, key: str, value: Any):
    comment_df = df.loc[df[key] == value, 'Comments']
    try:
        comment = comment_df.iloc[0]
        return comment
    except IndexError:
        return np.nan


def generate_team(df: DataFrame, key: str, value: Any):
    team_df = df.loc[df[key] == value, 'Team']
    try:
        team = team_df.iloc[0]
        return team
    except IndexError:
        return np.nan


class ExceptionRecordsPipeline(ReportReader):
    report = 'ExceptionRecords'

    def __init__(self):
        super(ExceptionRecordsPipeline, self).__init__(report=self.report)
        self.master_df = self.master_report

        self.master_df['Team'] = np.nan
        self.master_df['Comments'] = np.nan

    def process_df(self):
        # Apply first comment
        self.master_df = self.master_df.apply(self.add_comment, axis=1)
        self.master_df = self.master_df.apply(self.add_team, axis=1)

        print()

    @property
    def no_comment_df(self):
        df = self.master_df.loc[self.master_df['Comments'].isnull()]
        return df

    def end_process(self):
        consolidated_fn = 'consolidated.xlsx'
        conso_filepath = os.path.join(OUT_DIR, self.report, consolidated_fn)

        no_comment_fn = 'no_comments.xlsx'
        no_comment_filepath = os.path.join(OUT_DIR, self.report, no_comment_fn)

        write_to_excel(df=self.master_df, path=conso_filepath)
        write_to_excel(df=self.no_comment_df, path=no_comment_filepath)

    def add_comment(self, df):
        trade_id = df['Trade ID']

        # Check if EQD STRUCT REVERSAL
        try:
            if df['Pro Cat'].lower() == 'eqd struct' and df['Remarks'].lower() == 'reversal':
                df['Comments'] = 'reversal'
                return df
        except AttributeError as e:
            pass

        comment = generate_comment(df=self.consolidated_report, key='Trade ID', value=trade_id)

        # Check if SI is empty
        if str(df['SI']) == 'nan':
            index = df.name
            prev_trade_id = self.master_df.iloc[index-1]['Trade ID']
            comment = generate_comment(df=self.consolidated_report, key='Trade ID', value=prev_trade_id)

        # CHECK IF trade id is empty
        try:
            if trade_id.isnull():
                return df
        except AttributeError:
            pass

        df['Comments'] = comment
        return df

    def add_team(self, df):
        trade_id = df['Trade ID']
        try:
            if trade_id.isnull():
                return df

        except AttributeError:
            pass

        team = generate_team(df=self.consolidated_report, key='Trade ID', value=trade_id)
        try:
            df['Team'] = team
            comment = df['Comments']
            if str(comment).lower().startswith('belongs to'):
                df['Team'] = comment.split(" ")[2]

        except IndexError:
            return df

        return df


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
        # result_df = df.loc[(df['SI'].notnull()) & (df['Comments'].isnull())]
        # result_df = df.apply(self.combine_block, axis=1)
        result_df = pd.DataFrame()
        for block_df in self.df_block(df):
            with_si_no_comment = block_df.loc[(block_df.SI.notnull()) & (block_df.Comments.isnull())]
            if with_si_no_comment.empty:
                continue

            result_df = pd.concat([result_df, block_df])
        return result_df

    def df_block(self, df: DataFrame):
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
        self.master_df = self.master_df.apply(self.add_comment, axis=1)
        self.master_df = self.master_df.apply(self.add_team, axis=1)

    def end_process(self):
        consolidated_fn = 'consolidated.xlsx'
        conso_filepath = os.path.join(OUT_DIR, self.report, consolidated_fn)

        no_comment_fn = 'no_comments.xlsx'
        no_comment_filepath = os.path.join(OUT_DIR, self.report, no_comment_fn)

        write_to_excel(df=self.master_df, path=conso_filepath)
        write_to_excel(df=self.no_comment_df, path=no_comment_filepath)

    def add_comment(self, df):
        if str(df['SI']) == 'nan':
            return df

        trade_id = df['Trade ID']
        df['Comments'] = generate_comment(df=self.consolidated_report, key='Trade ID', value=trade_id)
        return df

    def add_team(self, df):
        if str(df['SI']) == 'nan':
            return df

        trade_id = df['Trade ID']
        df['Team'] = generate_team(df=self.consolidated_report, key='Trade ID', value=trade_id)

        return df


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
        self.master_df = self.master_df.apply(self.add_comment, axis=1)
        self.master_df = self.master_df.apply(self.add_team, axis=1)
        print()

    def end_process(self):
        consolidated_fn = 'consolidated.xlsx'
        conso_filepath = os.path.join(OUT_DIR, self.report, consolidated_fn)

        no_comment_fn = 'no_comments.xlsx'
        no_comment_filepath = os.path.join(OUT_DIR, self.report, no_comment_fn)

        write_to_excel(df=self.master_df, path=conso_filepath)
        write_to_excel(df=self.no_comment_df, path=no_comment_filepath)

    def add_comment(self, df):
        if 'COL' in str(df['Strategy']):
            df['Comments'] = f'Strategy: {df["Strategy"]}'
            return df

        trade_id = df['Trade Id']
        df['Comments'] = generate_comment(df=self.consolidated_report, key='Trade Id', value=trade_id)
        return df

    def add_team(self, df):
        trade_id = df['Trade Id']
        df['Team'] = generate_team(df=self.consolidated_report, key='Trade Id', value=trade_id)
        return df


if __name__ == '__main__':
    pipeline = MismatchPipeline()
    pipeline.process_df()
    pipeline.end_process()
