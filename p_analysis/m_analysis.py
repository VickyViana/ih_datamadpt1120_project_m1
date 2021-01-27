# IMPORTS

import numpy as np

# FUNCTIONS


def column_selector(df, column_list):
    # Function to select in a df a certain number of columns (in a list) in certain order
    df_reduced = df[column_list]
    return df_reduced


def column_agg_count(table, column, column_count, new_name_col):
    table_reduced = table.groupby(column).agg({column_count: 'count'}).rename(columns={column_count: new_name_col})
    return table_reduced


def agg_custom_function(col):
    return (col / np.sum(col)) * 100


def column_percentage(df, column_to_count, new_col_name):
    df[new_col_name] = (100 * (df[column_to_count] / df[column_to_count].sum())).round(3).astype(str) + '%'
    return df


def country_selector(table, country):
    filter_country = table['Country'] == country
    table = table[filter_country]
    return table
