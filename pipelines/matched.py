import numpy as np

from pipelines import generate_no_comment_df, generate, generate_output
from utils import ReportReader


class MatchedPipeline(ReportReader):
    report = 'Matched'

    def __init__(self):
        super(MatchedPipeline, self).__init__(report=self.report)
        self.master_df = self.master_report
        self.master_df['Team'] = np.nan
        self.master_df['Comments'] = np.nan

    @property
    def no_comment_df(self):
        df = self.master_df
        return df.loc[
            (df['Team'] == 'FXMM') &
            (df['Comments'].isnull()) & (
                (df['Trade Id'] == 0) |
                (df['Trade Id'].isnull())
            )
        ]

    def process_df(self):
        self.master_df = self.master_df.apply(self.__add_team, axis=1)
        self.master_df = self.master_df.apply(self.__add_comment, axis=1)

    def end_process(self):
        generate_output(
            report_name=self.report,
            conso_df=self.master_df,
            no_comment_df=self.no_comment_df
        )

    def __add_comment(self, df):
        criteria = {
            'SI': df['SI'],
            'Trade Id': df['Trade Id'],
            'Netted Id': df['Netted Id'],
            'SAA Ref': df['SAA Ref']
        }
        if df['Team'] == 'FXMM':
            df['Comments'] = generate(df=self.consolidated_report, column='Comments', **criteria)
        else:
            df['Comments'] = 'MATCHED'

        return df

    def __add_team(self, df):
        df['Team'] = df['Product Category']

        return df
