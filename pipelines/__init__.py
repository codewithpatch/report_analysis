import logging
import os
from typing import Any

import numpy as np
import pandas as pd
from pandas import DataFrame

from settings import OUT_DIR, DATE, DATE_TO_PROCESS


def write_to_excel(df, path):
    try:
        df.to_excel(path, index=False, header=True)
    except FileNotFoundError:
        dir_name = os.path.dirname(path)
        os.mkdir(dir_name)
        df.to_excel(path, index=False, header=True)


def generate(df: DataFrame, column: str, **kwargs):
    logging.debug(f"Generating '{column}' for criteria {kwargs}")
    condition = pd.Series(True, index=df.index)
    for k, v in kwargs.items():
        condition = condition & (df[k] == v)

    result_df = df.loc[condition]
    try:
        result = result_df[column].iloc[0]
        return result
    except IndexError:
        return np.nan


def generate_team(df: DataFrame, key: str, value: Any):
    team_df = df.loc[df[key] == value, 'Team']
    try:
        team = team_df.iloc[0]
        return team
    except IndexError:
        return np.nan


def generate_no_comment_df(df: DataFrame):
    return df.loc[
        (df['Comments'].isnull()) |
        (df['Comments'].str.lower().str.startswith('belongs to')) |
        (df['Comments'].str.lower().str.startswith('not ours'))
    ]


def generate_output(report_name: str, conso_df: DataFrame, no_comment_df: DataFrame):
    file_date = DATE_TO_PROCESS.strftime('%d%b%Y')
    outfile_prefix = f'{report_name}_{file_date}'

    consolidated_fn = f'{outfile_prefix}_consolidated.xlsx'
    conso_filepath = os.path.join(OUT_DIR, report_name, consolidated_fn)

    no_comment_fn = f'{outfile_prefix}_no_comments.xlsx'
    no_comment_filepath = os.path.join(OUT_DIR, report_name, no_comment_fn)

    write_to_excel(df=conso_df, path=conso_filepath)
    write_to_excel(df=no_comment_df, path=no_comment_filepath)