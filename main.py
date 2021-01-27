# IMPORTS

import argparse
from p_acquisition.m_acquisition import get_data
from p_wrangling.m_wrangling import clean_gender
from p_acquisition.m_acquisition import get_web_scrap
from p_wrangling.m_wrangling import unique_values
from p_acquisition.m_acquisition import create_api_dict
from p_wrangling.m_wrangling import df_country_updating
from p_wrangling.m_wrangling import replace_from_dict
from p_wrangling.m_wrangling import join_tables
from p_wrangling.m_wrangling import rename_col
from p_analysis.m_analysis import column_agg_count
from p_analysis.m_analysis import column_percentage
from p_analysis.m_analysis import country_selector

# CONSTANTS

COUNTRY_LST = ['Belgium', 'Greece', 'Lithuania', 'Portugal', 'Bulgaria', 'Spain', 'Luxembourg', 'Romania', 'Czechia',
               'France', 'Hungary', 'Slovenia', 'Denmark', 'Croatia', 'Malta', 'Slovakia', 'Germany', 'Italy',
               'Netherlands', 'Finland', 'Estonia', 'Cyprus', 'Austria', 'Sweden', 'Ireland', 'Latvia', 'Poland',
               'Great Britain']
NAME_DICT = {'country_code': 'Country', 'normalized_job_code': 'Job Title', 'gender': 'Gender'}
COLUMN_LIST = ['Country', 'Job Title', 'Gender']


# FUNCTIONS

def argument_parser():
    # Parse arguments to this script
    parser = argparse.ArgumentParser(description='pass to the script the country you want to get results from')
    parser.add_argument("-co", "--country", help="country to get results from", type=str)
    args = parser.parse_args()
    return args

def init_text(argument):
    if argument in COUNTRY_LST:
        print(f'Processing data for {argument}')
    elif argument == None:
        print('Processing data for all countries')
    else:
        print('No data for this country')
        exit()

def main(argument):
    init_text(argument)
    print('Starting process')
    tables_dict = get_data()
    scraped_countries = get_web_scrap()
    list_job_codes = unique_values(tables_dict['db_career_info'], "normalized_job_code")
    jobs_api_dict = create_api_dict(list_job_codes)
    print('Raw Data obtained')
    print('Cleaning data...')
    clean_gender(tables_dict['db_personal_info'], "gender")
    tables_dict['db_country_info'] = df_country_updating(scraped_countries, tables_dict['db_country_info'], 'country_code')
    tables_dict['db_career_info'] = replace_from_dict(tables_dict['db_career_info'] , 'normalized_job_code', jobs_api_dict)
    complete_table = join_tables(tables_dict)
    complete_table = rename_col(complete_table, NAME_DICT)
    print('Data cleaned')
    print('Analysing data...')
    # table_reduced = column_selector(complete_table, COLUMN_LIST)
    if argument in COUNTRY_LST:
        print(argument)
        complete_table = country_selector(complete_table, argument)
    table_reduced1 = column_agg_count(complete_table, COLUMN_LIST, 'uuid', 'Quantity')
    table_reduced1 = column_percentage(table_reduced1, 'Quantity', 'Percentage')
    table_reduced1.to_csv('./Results/Table.csv')
    print(table_reduced1)
    print('Results obtained --> See folder "Results"')
    print('Process completed')


if __name__ == '__main__':

    main(argument_parser().country)

