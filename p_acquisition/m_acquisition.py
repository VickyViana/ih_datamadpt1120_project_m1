# IMPORTS

import pandas as pd
from sqlalchemy import create_engine
import quandl
import requests
from bs4 import BeautifulSoup

# FUNCTIONS

def db_connect(data_path='./data/raw_data_project_m1.db'):  # Function that creates engine to connect to DB
    connection = f'sqlite:///{data_path}'
    engine = create_engine(connection)
    return engine


def df_info(table_name, engine):  # Function that returns a dataframe from a DB
    df_from_db = pd.read_sql_query(f"select * from {table_name}", engine)
    return df_from_db


def get_db_list():  # Function to create a list with the names of tables in DB
    engine_connect = db_connect()
    db_raw = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table'", engine_connect)
    db_raw_list = db_raw.name.tolist()
    return db_raw_list


def db_dic(db_raw_list, engine):
    # Function that reads tables in DB and introduce them in dictionary, to access them easily
    df_dic = {}
    for name in db_raw_list:
        df_dic[f'db_{name}'] = pd.read_sql_query("select * FROM {name}".format(name=name), engine)
    return df_dic


def get_data():  # Function to get DB tables data in a dictionary
    print('Getting DataBase raw data...')
    engine = db_connect(data_path='./data/raw_data_project_m1.db')
    db_raw_list = get_db_list()
    tables_dic = db_dic(db_raw_list, engine)
    return tables_dic


def get_eurostat(url='https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Glossary:Country_codes'):
    html = requests.get(url).content
    return html


def get_web_scrap():
    # Function to get data from Eurostat
    print("Getting countries data from web scraping...")
    html = get_eurostat(url='https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Glossary:Country_codes')
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table')
    return table


def create_api_list(list_job):  # Function to make a call to the API with every job in list_job, and store it in a list
    api_list = []
    for x in list_job:
        base_url = f'http://api.dataatwork.org/v1/jobs/{x}'
        response = requests.get(base_url)
        results = response.json()
        api_list.append(results)
    return api_list


def create_api_dict(list_job_codes):
    # Function to create a dictionary with job codes and job titles from list_job_codes
    print('Getting jobs data from API...')
    api_list = create_api_list(list_job_codes)
    api_df = pd.DataFrame(api_list)
    jobs_dict = api_df.set_index('uuid').to_dict()['title']
    return jobs_dict


