#importing libraries and functions
import sys 
import os
sys.path.append(os.path.abspath("/Users/emilyburns/Documents/Data_Science/projects/web_scraping_wiki/code/script/functions"))
from funs_do_webscraping import *
import requests  
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

################################################
#Scraping: Wiki 2016 Global Suicide Rates
################################################

#pulling wiki page
url_sr = "https://en.wikipedia.org/wiki/List_of_countries_by_suicide_rate"
page = FindTable(url_sr)

#rendering each HTML tag from wiki page on its own line
soup = GetTags(page)

#pulling the correct table from the wiki page
suicide_table = GetTable(soup, 3)

#pulling relevant data from the table
country = []
rate = []

for row in suicide_table.find_all('tr'):
    cells = row.find_all('td')
    if len(cells)==9:
        countries = cells[1]
        country.append(countries.text.strip())
        
        rates = cells[3]
        rate.append(rates.text.strip())

#creating a dataframe with the data from the wiki table
suiciderate_df = pd.DataFrame(country, columns =['Country'])
suiciderate_df["2016_Suicide_Rate"] = rate

#cleaning data and setting index
suiciderate_df["Country"] = suiciderate_df["Country"].str.replace('more info', '').str.replace('(', '').str.replace(')', '')
suiciderate_df['Country'] = suiciderate_df['Country'].map(lambda x: x.rstrip('[b]'))

suiciderate_df['Country'] = list(replaced(suiciderate_df['Country'], 'Antigua and Baruda', 'Antigua and Barbuda'))
suiciderate_df['Country'] = list(replaced(suiciderate_df['Country'], 'Australia ', 'Australia')) 
suiciderate_df['Country'] = list(replaced(suiciderate_df['Country'], 'Afghanista', 'Afghanistan'))
suiciderate_df['Country'] = list(replaced(suiciderate_df['Country'], 'Azerbaija', 'Azerbaijan'))
suiciderate_df['Country'] = list(replaced(suiciderate_df['Country'], 'B', 'Benin'))
suiciderate_df['Country'] = list(replaced(suiciderate_df['Country'], 'Barados', 'Barbados'))
suiciderate_df['Country'] = list(replaced(suiciderate_df['Country'], 'Belgiu', 'Belgium'))
suiciderate_df['Country'] = list(replaced(suiciderate_df['Country'], 'Bhutan ', 'Bhutan'))
suiciderate_df['Country'] = list(replaced(suiciderate_df['Country'], 'Cameroon ', 'Cameroon'))
suiciderate_df['Country'] = list(replaced(suiciderate_df['Country'], 'China ', 'China'))
suiciderate_df['Country'] = list(replaced(suiciderate_df['Country'], 'Canada ', 'Canada'))
suiciderate_df['Country'] = list(replaced(suiciderate_df['Country'], 'Chil', 'Chile'))
suiciderate_df['Country'] = list(replaced(suiciderate_df['Country'], 'Czech Repulic', 'Czech Republic'))
suiciderate_df['Country'] = list(replaced(suiciderate_df['Country'], 'DR Congo', 'Democratic Republic of the Congo'))
suiciderate_df['Country'] = list(replaced(suiciderate_df['Country'], 'Djiouti', 'Djibouti'))
suiciderate_df['Country'] = list(replaced(suiciderate_df['Country'], 'Dominican Repulic', 'Dominican Republic'))
suiciderate_df['Country'] = list(replaced(suiciderate_df['Country'], 'Edcuad', 'Edcuador'))
suiciderate_df['Country'] = list(replaced(suiciderate_df['Country'], 'Finland ', 'Finland'))
suiciderate_df['Country'] = list(replaced(suiciderate_df['Country'], 'France ', 'France'))
suiciderate_df['Country'] = list(replaced(suiciderate_df['Country'], 'Ga', 'Gabon'))
suiciderate_df['Country'] = list(replaced(suiciderate_df['Country'], 'Greec', 'Greece'))
suiciderate_df['Country'] = list(replaced(suiciderate_df['Country'], 'Hait', 'Haiti'))
suiciderate_df['Country'] = list(replaced(suiciderate_df['Country'], 'Ira', 'Iran'))
suiciderate_df['Country'] = list(replaced(suiciderate_df['Country'], 'Ireland ', 'Ireland'))
suiciderate_df['Country'] = list(replaced(suiciderate_df['Country'], 'India ', 'India'))
suiciderate_df['Country'] = list(replaced(suiciderate_df['Country'], 'Japan ', 'Japan'))
suiciderate_df['Country'] = list(replaced(suiciderate_df['Country'], 'Kazakhsta', 'Kazakhstan'))
suiciderate_df['Country'] = list(replaced(suiciderate_df['Country'], 'Kiriati', 'Kiribati'))
suiciderate_df['Country'] = list(replaced(suiciderate_df['Country'], 'Lesoth', 'Lesotho'))
suiciderate_df['Country'] = list(replaced(suiciderate_df['Country'], 'Luxemourg', 'Luxembourg'))
suiciderate_df['Country'] = list(replaced(suiciderate_df['Country'], 'Lithuania ', 'Lithuania'))
suiciderate_df['Country'] = list(replaced(suiciderate_df['Country'], 'Malaw', 'Malawi'))
suiciderate_df['Country'] = list(replaced(suiciderate_df['Country'], 'Mexic', 'Mexico'))
suiciderate_df['Country'] = list(replaced(suiciderate_df['Country'], 'Morocc', 'Morocco'))
suiciderate_df['Country'] = list(replaced(suiciderate_df['Country'], 'Mozambiqu', 'Mozambique'))
suiciderate_df['Country'] = list(replaced(suiciderate_df['Country'], 'Nepal ', 'Nepal'))
suiciderate_df['Country'] = list(replaced(suiciderate_df['Country'], 'Qata', 'Qatar'))
suiciderate_df['Country'] = list(replaced(suiciderate_df['Country'], 'Romania ', 'Romania'))
suiciderate_df['Country'] = list(replaced(suiciderate_df['Country'], 'Russia ', 'Russia'))
suiciderate_df['Country'] = list(replaced(suiciderate_df['Country'], 'Siera L', 'Siera Leone'))
suiciderate_df['Country'] = list(replaced(suiciderate_df['Country'], 'Spa', 'Spain'))
suiciderate_df['Country'] = list(replaced(suiciderate_df['Country'], 'Singapore ', 'Singapore'))
suiciderate_df['Country'] = list(replaced(suiciderate_df['Country'], 'Sweden ', 'Sweden'))
suiciderate_df['Country'] = list(replaced(suiciderate_df['Country'], 'Sri Lanka ', 'Sri Lanka'))
suiciderate_df['Country'] = list(replaced(suiciderate_df['Country'], 'Switzerland  ', 'Switzerland'))
suiciderate_df['Country'] = list(replaced(suiciderate_df['Country'], 'Suda', 'Sudan'))
suiciderate_df['Country'] = list(replaced(suiciderate_df['Country'], 'Tajikista', 'Tajikistan'))
suiciderate_df['Country'] = list(replaced(suiciderate_df['Country'], 'Tanzania, United Republic of', 'Tanzania'))
suiciderate_df['Country'] = list(replaced(suiciderate_df['Country'], 'Tog', 'Togo'))
suiciderate_df['Country'] = list(replaced(suiciderate_df['Country'], 'Turkmenista', 'Turkmenistan'))
suiciderate_df['Country'] = list(replaced(suiciderate_df['Country'], 'Uzbekista', 'Uzbekistan'))
suiciderate_df['Country'] = list(replaced(suiciderate_df['Country'], 'United Kingdom ', 'United Kingdom'))
suiciderate_df['Country'] = list(replaced(suiciderate_df['Country'], 'United States ', 'United States'))
suiciderate_df['Country'] = list(replaced(suiciderate_df['Country'], 'Ukraine ', 'Ukraine'))

suiciderate_df.head(10)

################################################
#Scraping: Wiki 2015 Global Literacy Rates
################################################
url_lit = "https://en.wikipedia.org/wiki/List_of_countries_by_literacy_rate"
page = FindTable(url_lit)
soup = GetTags(page)
lit_table = GetTable(soup, 3)

#pulling relevant data from table
country_lit = []
rate_lit = []

for row in lit_table.find_all('tr'):
    cells = row.find_all('td')
    if len(cells)==6:
        countries_lit = cells[0]
        country_lit.append(countries_lit.text.strip())
        
        rates_lit = cells[1]
        rate_lit.append(rates_lit.text.strip())

#cleaning pulled data from data & creating dataframe with it
rate_lit = [x[0:4] for x in rate_lit]
rate_lit = [x.strip('%') for x in rate_lit]
lit_df = pd.DataFrame(rate_lit, columns =['2015_Literacy_Rates'])
lit_df["Country"] = country_lit

lit_df.head(10)

#pulling additional territories included in separate table
lit_table2 = GetTable(soup, 4)

#pulling relevant data from additional table
lit_territory = []
lit_rate_terr = []
lit_year = []

for row in lit_table2.find_all('tr'):
    cells = row.find_all('td')
    if len(cells)>1:
        lit_territories = cells[0]
        lit_territory.append(lit_territories.text.strip())
        
        lit_rates_terr = cells[1]
        lit_rate_terr.append(lit_rates_terr.text.strip())
        
        years = cells[5]
        lit_year.append(years.text.strip())        
        
#cleaning pulled data from table
Year = [x[0:4] for x in lit_year]
lit_rate_terr = [x.strip('%') for x in lit_rate_terr]

#creating dataframe w/ cleaned data
lit_terr_df = pd.DataFrame(lit_rate_terr, columns =['2015_Literacy_Rates'])
lit_terr_df['Country'] = lit_territory
lit_terr_df['Year'] = Year
lit_terr_df = lit_terr_df.loc[lit_terr_df['Year'] == '2015']
lit_terr_df = lit_terr_df.drop('Year', 1)

lit_terr_df.head(10)

#building single dataframe from the two literacy tables
frames = [lit_df, lit_terr_df]
literacy_df = pd.concat(frames)

literacy_df.head(10)

################################################
#Scraping: Wiki 2015 Health Care Expenditure Rates
################################################       
url_hc = "https://en.wikipedia.org/wiki/List_of_countries_by_total_health_expenditure_per_capita"
page = FindTable(url_hc) 
soup = GetTags(page)
hc_table = GetTable(soup, 6)

#pulling relevant data from table
country_hc = []
hc_rate = []

for row in hc_table.find_all('tr'):
    cells = row.find_all('td')
    if len(cells)==5:
        countries_hc = cells[0]
        country_hc.append(countries_hc.text.strip())
        
        hc_rates = cells[4]
        hc_rate.append(hc_rates.text.strip())
        
#creating dataframe w/ cleaned data
healthcare_df = pd.DataFrame(hc_rate, columns =['2015_Healthcare_Expenditure'])
healthcare_df['Country'] = country_hc
healthcare_df["Country"] = healthcare_df["Country"].str.replace("United States of America", "United States")
healthcare_df['Country'] = list(replaced(healthcare_df['Country'], 'Brunei Darussalam', 'Brunei'))
healthcare_df['Country'] = list(replaced(healthcare_df['Country'], 'Dominica', 'Dominican Republic'))
healthcare_df['Country'] = list(replaced(healthcare_df['Country'], 'Iran (Islamic Republic of)', 'Iran'))
healthcare_df['Country'] = list(replaced(healthcare_df['Country'], 'Republic of Moldova', 'Moldova'))
healthcare_df['Country'] = list(replaced(healthcare_df['Country'], 'Russian Federation', 'Russia'))
healthcare_df['Country'] = list(replaced(healthcare_df['Country'], 'United Republic of Tanzania United States', 'Tanzania'))
healthcare_df['Country'] = list(replaced(healthcare_df['Country'], 'Venezuela (Bolivarian Republic of)', 'Venezuela'))
healthcare_df['Country'] = list(replaced(healthcare_df['Country'], 'Viet Nam', 'Vietnam'))

healthcare_df.head(10)

################################################
#Merging scraped datasets
################################################
#building combined dataframe
df_final = pd.merge(suiciderate_df, literacy_df, on = "Country", how = "outer")
df_final = pd.merge(df_final, healthcare_df, on = "Country", how = "outer")
df_final.head(25)

df_final.info()

#writing raw data to csv file
path = '/Users/emilyburns/Documents/Data_Science/projects/web_scraping_wiki/data/raw_data'
output_file = os.path.join(path,'scraped_data_clean.csv')

df_final.to_csv(output_file, index = False)