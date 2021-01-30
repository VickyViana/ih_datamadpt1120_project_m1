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
from p_wrangling.m_wrangling import table_pos
from p_analysis.m_analysis import group_mean

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
    parser.add_argument("-co", "--country", help="country to get results from", default='all', type=str)
    parser.add_argument("-b1", "--bonus1", help="activates bonus1 analysis", type=str)
    args = parser.parse_args()
    return args


def init_text_country(argument):
    if argument in COUNTRY_LST:
        print(f'Processing data for {argument}')
    elif argument == None or argument == 'all':
        print('Processing data for all countries')
    else:
        print('No data for this country')
        exit()


def main(argument, argument2):
    init_text_country(argument)
    print('Starting process')
    tables_dict = get_data()
    scraped_countries = get_web_scrap()
    list_job_codes = unique_values(tables_dict['db_career_info'], "normalized_job_code")
    jobs_api_dict = create_api_dict(list_job_codes)
    print('Raw Data obtained')
    print('Cleaning data...')
    clean_gender(tables_dict['db_personal_info'])
    tables_dict['db_country_info'] = df_country_updating(scraped_countries, tables_dict['db_country_info'], 'country_code')
    tables_dict['db_career_info'] = replace_from_dict(tables_dict['db_career_info'] , 'normalized_job_code', jobs_api_dict)
    complete_table = join_tables(tables_dict)
    complete_table = rename_col(complete_table, NAME_DICT)
    print('Data cleaned')
    print('Analysing data...')
    if argument in COUNTRY_LST:
        complete_table = country_selector(complete_table, argument)
    table_reduced1 = column_agg_count(complete_table, COLUMN_LIST, 'uuid', 'Quantity')
    table_reduced1 = column_percentage(table_reduced1, 'Quantity', 'Percentage')
    table_reduced1.to_csv(f'./Results/Table_{argument}.csv')
    print(table_reduced1)
    print(f'Results obtained --> See Table_{argument}.csv in folder "Results"')
    if argument2 == 'y':
        print(f'Calculating Bonus 1 for {argument}')
        print('Cleaning data...')
        table_position = table_pos(complete_table)
        print('Analysing data...')
        table_b1 = group_mean(table_position)
        table_b1.to_csv(f'./Results/Table_b1_{argument}.csv')
        print(table_b1)
        print(f'Results obtained --> See Table_b1_{argument}.csv in folder "Results"')
        print('Process completed')
    else:
        print(f'No results for bonus1 = {argument2}')
        print('Process completed')


if __name__ == '__main__':
    main(argument_parser().country, argument_parser().bonus1)


