# ih_datamadpt1120_project_m1
Ironhack Madrid - Data Analytics Part Time - November 2020 - Project Module 1

The purpose of this project is to archive a resumed information about employed people in European countries that have jobs related with Data analysis. The results obtained are presented in a dataframe, and consist of percentages of how many people work in each different job position, separated by gender and country. These results can be calculated for a particular country or for all at a time. 
An extra bonus information can be obtained, related to the opinion of each worker about basic income. An average of pro arguments and cons arguments will be shown for people y position in favour or against it. This outcome will be with regard of the country chosen in the begining (or all countries). 


<p align="center">
<img src="https://1.cms.s81c.com/sites/default/files/2019-01-30/1_Cloud-EU-data-responsibility.jpg">
</p>


## **How it works**
Clone this repository to your local folders. 

:warning: Please be aware of the python version you are using and the libraries you need to have installed. See "Technology stack" section.

In console write down --> python main.py  --> You will get the result for all countries

In console write down --> python main.py -co "Country name" --> You will get the result for the country you wrote. 
Other way coud be --> python main.py --country "Country name"

Yo can choose any of the following countries: 'Belgium', 'Greece', 'Lithuania', 'Portugal', 'Bulgaria', 'Spain', 'Luxembourg', 'Romania', 'Czechia', 'France', 'Hungary', 'Slovenia', 'Denmark', 'Croatia', 'Malta', 'Slovakia', 'Germany', 'Italy', 'Netherlands', 'Finland', 'Estonia', 'Cyprus', 'Austria', 'Sweden', 'Ireland', 'Latvia', 'Poland'and 'Great Britain'. Don't forget 

The results would be printed in console as well as in a Table.csv file in Results folder, in order to use them for later analyses. The table obtained will be similar to this:

| Country | Job Title | Gender | Quantity | Percentage |
|---|---|---|---|---|
| Austria | Data Administrator| Male | 4 | 6% |
| Austria | Data Administrator| Female | 3 | 4% |
| ... | ... | ... | ... | ... |




## **Technology stack**

- **Programming Language**: Python 3.8
- **Libraries in Use: pandas**, numpy, argparse, sqlalchemy, requests, bs4, functools.



## **Folder structure**
```
└── ih_datamadpt1120_project_m1
    ├── __trash__
    ├── .gitignore
    ├── requirements.txt
    ├── README.md
    ├── main.py
    ├── p_acquisition
    │   ├── __init__.py
    │   └── m_acquisition.py
    ├── p_analysis
    │   ├── __init__.py
    │   └── m_analysis.py
    ├── p_wrangling
    │   ├── __init__.py
    │   └── m_wrangling.py
    ├── Results
    │   └── Table.csv
    └── data
        └── raw_data_project_m1.db
```     
   
     
## **Next steps**
 - It would be a good upgrade to improve the loop of acquisition API data to get the information faster.
 

 
