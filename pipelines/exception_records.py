import os

import numpy as np

from pipelines import generate, generate_team, write_to_excel, generate_no_comment_df, generate_output
from settings import OUT_DIR
from utils import ReportReader


class ExceptionRecordsPipeline(ReportReader):
    report = 'ExceptionRecords'

    def __init__(self):
        super(ExceptionRecordsPipeline, self).__init__(report=self.report)
        self.master_df = self.master_report

        self.master_df['Team'] = np.nan
        self.master_df['Comments'] = np.nan

    def process_df(self):
        # Apply first comment
        self.master_df = self.master_df.apply(self.__add_comment, axis=1)
        self.master_df = self.master_df.apply(self.__add_team, axis=1)

    @property
    def no_comment_df(self):
        return generate_no_comment_df(self.master_df)

    def end_process(self):
        generate_output(
            report_name=self.report,
            conso_df=self.master_df,
            no_comment_df=self.no_comment_df
        )

    def __add_comment(self, df):
        index = df.name
        trade_id = df['Trade ID']

        criteria_df = df

        # If SI is empty, use the previous row as criteria
        if str(df['SI']) == 'nan':
            criteria_df = self.master_df.iloc[index-1]

        # If Trade ID is empty, use the next row as criteria
        if str(trade_id) == 'nan':
            criteria_df = self.master_df.iloc[index+1]

        criteria = {
            'Trade ID': criteria_df['Trade ID'],
            'CCY': criteria_df['CCY'],
            'Amount': criteria_df['Amount'],
            'Msg Type': criteria_df['Msg Type']
        }

        # Check if EQD STRUCT REVERSAL
        try:
            if criteria_df['Pro Cat'].lower() == 'eqd struct' and criteria_df['Remarks'].lower() == 'reversal':
                df['Comments'] = 'reversal'
                return df
        except AttributeError:
            if str(df['Pro Cat']).lower() == 'eqd struct' and str(df['Remarks']).lower() == 'reversal':
                df['Comments'] = 'reversal'
                return df

        df['Comments'] = generate(df=self.consolidated_report, column='Comments', **criteria)
        return df

    def __add_team(self, df):
        index = df.name
        trade_id = df['Trade ID']

        team = generate_team(df=self.consolidated_report, key='Trade ID', value=trade_id)
        if str(team) == 'nan':
            trade_id = self.master_df.iloc[index+1]['Trade ID']
            team = generate_team(df=self.consolidated_report, key='Trade ID', value=trade_id)

        df['Team'] = team

        return df
