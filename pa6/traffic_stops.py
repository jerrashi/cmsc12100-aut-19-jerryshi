'''
Analyzing traffic stop data.

Jerry Shi
'''

import numpy as np
import pandas as pd

# Defined constants for column names
ARREST_CITATION = 'arrest_or_citation'
IS_ARRESTED = 'is_arrested'
YEAR_COL = 'stop_year'
MONTH_COL = 'stop_month'
DATE_COL = 'stop_date'
STOP_SEASON = 'stop_season'
STOP_OUTCOME = 'stop_outcome'
SEARCH_TYPE = 'search_type'
SEARCH_CONDUCTED = 'search_conducted'
AGE_CAT = 'age_category'
OFFICER_ID = 'officer_id'
STOP_ID = 'stop_id'
DRIVER_AGE = 'driver_age'
DRIVER_RACE = 'driver_race'
DRIVER_GENDER = 'driver_gender'
VIOLATION = "violation"

SEASONS_MONTHS = {
    "winter": [12, 1, 2],
    "spring": [3, 4, 5],
    "summer": [6, 7, 8],
    "fall": [9, 10, 11]}

NA_DICT = {
    'drugs_related_stop': False,
    'search_basis': "UNKNOWN"
    }

AGE_BINS = [0, 21, 36, 50, 65, 100]
AGE_LABELS = ['juvenile', 'young_adult', 'adult', 'middle_aged', 'senior']

SUCCESS_STOPS = ['Arrest', 'Citation']

CATEGORICAL_COLS = [AGE_CAT, DRIVER_GENDER, DRIVER_RACE,
                    STOP_SEASON, STOP_OUTCOME, VIOLATION]


def read_and_process_allstops(csv_file):
    '''
    Purpose: read in csv and process it according to the assignment
      requirements.

    Inputs:
        csv_file (string): path to the csv file to open

    Returns: (dataframe): a processed dataframe,
      or None if the file does not exist
    '''
    try:
        df = pd.read_csv(csv_file, dtype = {OFFICER_ID: str})
        df[DATE_COL] = pd.to_datetime(df[DATE_COL])
        df[YEAR_COL] = df[DATE_COL].dt.year
        df[MONTH_COL] = df[DATE_COL].dt.month

        #add stop_season variable
        for season, months in SEASONS_MONTHS.items():
            in_season = df[MONTH_COL].isin(months)
            df.loc[in_season, STOP_SEASON] = season
        df[AGE_CAT] = pd.cut(df[DRIVER_AGE], bins = AGE_BINS, labels = 
            AGE_LABELS)
        df.loc[df[STOP_OUTCOME].isin(SUCCESS_STOPS), ARREST_CITATION] = True
        df[ARREST_CITATION] = df[ARREST_CITATION].replace({None: False})
        df[OFFICER_ID] = df[OFFICER_ID].replace({None: "UNKNOWN"})
        df[CATEGORICAL_COLS] = df[CATEGORICAL_COLS].astype('category')
        return df

    except FileNotFoundError:
        return None
    

def read_and_process_searches(csv_file, fill_na_dict=None):
    '''
    Purpose: read in csv and process it according to the assignment
        requirements.

    Inputs:
        csv_file (string): path to the csv file to open
        fill_na_dict (dict): of the form {colname: fill value}

    Returns: (dataframe): a processed dataframe,
      or None if the file does not exist
    '''
    try: 
        df = pd.read_csv(csv_file)
        if fill_na_dict is None:
            return df
        else:
            for col, replacement_value in fill_na_dict.items():
                df[col] = df[col].replace({None: replacement_value})
            return df

    except FileNotFoundError:
        return None


def apply_val_filters(df, filter_info):
    '''
    Purpose: apply a value filter to a dataframe

    Inputs:
        df (dataframe)
        filter_info (dict): of the form {'column_name':
            ['value1', 'value2', ...]}

    Returns: (dataframe) filtered dataframe,
      or None if a specified column does not exist
    '''
    try:
        for col, filter_values in filter_info.items():
            df = df[df[col].isin(filter_values)]
        return df

    except KeyError:
        return None


def apply_range_filters(df, filter_info):
    '''
    Purpose: apply a range filter to a dataframe

    Inputs:
        df (dataframe)
        filter_info (dict): of the form {'column_name': ['value1', 'value2']}

    Returns: (dataframe) filtered dataframe,
      or None if a specified column does not exist
    '''
    try:
        for col, filter_range in filter_info.items():
            min_value, max_value = filter_range
            filter = (df[col] >= min_value) & (df[col] <= max_value)
            df = df[filter]
        return df

    except KeyError:
        return None


def get_summary_statistics(df, group_col_list, summary_col=DRIVER_AGE):
    '''
    Purpose: produce a dataframe of aggregations

    Inputs:
        df (dataframe): the dataframe to get aggregations from
        group_col_list (list of str colnames): a list of columns to group by
        summary_col (str colname): a numeric column to aggregate

    Returns: (dataframe) a dataframe constructed from aggregations
    '''
    try:
        global_mean = df[summary_col].mean()
        def mean_diff(series):
            return series.mean() - global_mean
        summary_df = df.groupby(group_col_list)[summary_col].agg([np.median, 
            np.mean, mean_diff])
        return summary_df

    except KeyError:
        return None

    except ValueError:
        return None


def get_rates(df, cat_col, outcome_col):
    '''
    Purpose: returns dataframe of rates given in outcome column

    Inputs:
        df (dataframe)
        cat_col (list) of the column names to group by
        outcome_col (str) column name of outcome column

    Returns: (dataframe) dataframe with the rates for each outcome.
    '''
    try:
        outcome_totals = df.groupby(cat_col)[outcome_col].size()
        outcome_shares = df.groupby(cat_col + [outcome_col]).size() / \
            outcome_totals

        return outcome_shares.unstack(level = len(cat_col)).replace({None: 0})

    except KeyError:
        return None


def compute_search_share(
        stops_df, searches_df, cat_col, M_stops=25):
    '''
    Purpose: return a sorted dataframe of cat_cols by share of search
        conducted
    Inputs:
        stops_df (dataframe)
        searches_df (dataframe)
        cat_cols (list) of the column names to group by
        M_stops (int) minimum number of stops to retain

    Returns (dataframe): dataframe of search rates given by cat_col,
      or None if no officers meet M_stops criterion
    '''
    df = stops_df.merge(searches_df, how = 'left', on = STOP_ID)
    df.loc[df['search_basis'].notnull(), SEARCH_CONDUCTED] = True
    df[SEARCH_CONDUCTED] = df[SEARCH_CONDUCTED].replace({None: False})
    
    series = df.groupby(OFFICER_ID).size() >= M_stops
    series = series[series != False]
    df = df[df[OFFICER_ID].isin(series.index.values)]

    if len(df) == 0:
        return None

    df = get_rates(df, cat_col, SEARCH_CONDUCTED)
    
    shape = df.shape
    if shape[1] == 1:
        df[True] = 0

    return df.sort_values(by=False, ascending = True)