# IMPORTS

import pandas as pd
from functools import reduce


# FUNCTIONS

def gender_unify(column_g):  # Function to unify the gender results in only two: Female and Male
    if column_g.startswith('F' or 'f'):  # Function to unify the gender results in only two: Female and Male
        return 'Female'
    else:
        return 'Male'


def clean_gender(table, gender):  # Function to clean column "gender" in df_personal_info
    table['gender'] = table.apply(lambda x: gender_unify(x['gender']), axis=1)
    return table


def unique_values(dataframe, column):
    # Function that gets the unique values of a df column and introduce them in a list (removing 'None')
    uniques = dataframe[column].unique()
    list_uniques = uniques.tolist()
    list_uniques = [x for x in list_uniques if x is not None]
    return list_uniques


def countries_raw(table):  # Function that finds elements starting with td, and put them on a list
    countries_list_raw = [x.text for x in table.find_all('td')]
    return countries_list_raw


def get_countries_code_list(table_raw):  # Function to get a list with countries codes
    code_country_list = [x for x in table_raw if x.startswith("(")]
    return code_country_list


def get_countries_list(table_raw, code_country_list):  # Function to get a list with countries names
    countries_list = [x for x in table_raw if x not in code_country_list]
    return countries_list


def clean_n(list_name):  # Function to clean data in a list, removing \n
    new_list = [x.replace('\n', '') for x in list_name]
    return new_list


def no_brackets(list_name):  # Function to remove parentheses
    list_clean = [x.replace('(','').replace(')','') for x in list_name]
    return list_clean


def dict_country_creation(table):  # Function to get a dictionary with countries codes clean
    countries_list_raw = countries_raw(table)
    code_country_list = get_countries_code_list(countries_list_raw)
    countries_list = get_countries_list(countries_list_raw, code_country_list)
    code_country_list = clean_n(code_country_list)
    countries_list = clean_n(countries_list)
    code_country_list = no_brackets(code_country_list)
    dict_countries = dict(zip(code_country_list, countries_list))
    dict_countries['GR'] = 'Greece'
    dict_countries['GB'] = 'Great Britain'
    return dict_countries


def replace_from_dict(dataframe, column, dictionary):
    #  Function that replace the info in a column of a dataframe for the respective data in a dictionary
    df_replaced = dataframe.replace({column: dictionary})
    return df_replaced


def df_country_updating(table, dataframe, column):
    print('Updating db_county_info table...')
    dict_countries = dict_country_creation(table)
    df_replaced = replace_from_dict(dataframe, column, dict_countries)
    return df_replaced


def rename_col(df, name_dict):  # Function that changes the name of a column in a dataframe
    df = df.rename(columns=name_dict)
    return df


def join_tables(tables_dic):
    table_complete = reduce(lambda left, right: pd.merge(left, right, on='uuid'), tables_dic.values())
    return table_complete

