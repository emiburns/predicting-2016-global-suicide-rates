#importing libraries
import os
import pandas as pd
import numpy as np
import functools 
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

#reading in previously scraped wikipedia data
scraped_df = pd.read_csv('/Users/emilyburns/Documents/Data_Science/projects/web_scraping_wiki/data/raw_data/scraped_data_clean.csv')

#reading in and cleaning mental disorders csv
disorders_df = pd.read_csv('/Users/emilyburns/Documents/Data_Science/projects/web_scraping_wiki/data/raw_data/share-with-mental-and-substance-disorders.csv')
disorders_df.head()

disorders_df = disorders_df.loc[disorders_df['Year'] == 2015]
disorders_df = disorders_df.drop(['Year', 'Code'], axis =1)
disorders_df = disorders_df.rename(columns = {'Entity': 'Country',
                                                  'Prevalence - Mental and substance use disorders - Sex: Both - Age: Age-standardized (Percent)': '2015_Disorder_Prevalence'})

disorders_df = disorders_df[~disorders_df['Country'].isin(["Micronesia (country)", "Middle SDI", 
                                                           "Australasia", "Central Asia", "Central Europe",
                                                           "Central Europe, Eastern Europe, and Central Asia", 
                                                           "Central Latin America", "Central Sub-Saharan Africa",
                                                           "East Asia", "Eastern Europe", "Eastern Sub-Saharan Africa", 
                                                           "High-income", "High-income Asia Pacific", "High-middle SDI", 
                                                           "Latin America and Caribbean", "Low SDI", "Low-middle SDI", 
                                                           "North Africa and Middle East", "North America", 
                                                           "Southeast Asia", "Southeast Asia, East Asia, and Oceania", 
                                                           "Southern Latin America", "Southern Sub-Saharan Africa", 
                                                           "Sub-Saharan Africa", "Tropical Latin America", 
                                                           "Western Europe", "Western Sub-Saharan Africa"])]

disorders_df.head(10)

#reading in and cleaning unemployment rate csv
unemployment_df = pd.read_csv('/Users/emilyburns/Documents/Data_Science/projects/web_scraping_wiki/data/raw_data/unemployment-rate.csv')
unemployment_df.head()

unemployment_df = unemployment_df.loc[unemployment_df['Year'] == 2015]
unemployment_df = unemployment_df.drop(['Year', 'Code'], axis =1)

unemployment_df.columns = unemployment_df.columns.str.replace(' ', '_').str.replace('[()]', '').str.replace('[%]', '')
unemployment_df = unemployment_df.rename(columns = {'Entity': 'Country',
                                                    'Unemployment,_total__of_total_labor_force_modeled_ILO_estimate': 
                                                    '2015_Unemployment'})
unemployment_df = unemployment_df[~unemployment_df['Country'].isin(["Arab World", "Caribbean small states", 
                                                                    "Central Europe and the Baltics", 
                                                                    "Early-demographic dividend", "East Asia & Pacific", 
                                                                    "South Asia", "Small states", "Euro area",
                                                                    "Europe & Central Asia", "Post-demographic dividend",
                                                                    "European Union", "Fragile and conflict affected situations",
                                                                    "High income", "IBRD only", "IDA & IBRD total",
                                                                    "IDA blend", "IDA only", "IDA total", 
                                                                    "Late-demographic dividend","Latin America & Caribbean", 
                                                                    "Pre-demographic dividend",
                                                                    "Low & middle income", "Low income", "Lower middle income",
                                                                    "Middle East & North Africa", "Pacific island small states",
                                                                    "Other small states","Middle income", "Sub-Saharan Africa",
                                                                    "Syrian Arab Republic", "Upper middle income"])]

unemployment_df.head(10)

#reading in and cleaning gender ratio csv
gender_df = pd.read_csv('/Users/emilyburns/Documents/Data_Science/projects/web_scraping_wiki/data/raw_data/share-population-female.csv')
gender_df.head()

gender_df = gender_df.loc[gender_df['Year'] == 2015]
gender_df = gender_df.drop(['Year'], axis =1)
gender_df = gender_df.rename(columns = {'Entity': 'Country', 'Population, female (% of total)': '2015_Gender_Ratio'})
gender_df = gender_df[~gender_df['Country'].isin(["Arab World", "Caribbean small states", "Central Europe and the Baltics",
                                                  "Early-demographic dividend", "East Asia & Pacific", "South Asia", 
                                                  "Small states", "Euro area", "Europe & Central Asia", 
                                                  "Post-demographic dividend", "European Union", 
                                                  "Fragile and conflict affected situations", "High income", "IBRD only", 
                                                  "IDA & IBRD total","IDA blend", "IDA only", "IDA total", 
                                                  "Late-demographic dividend", "Latin America & Caribbean", 
                                                  "Pre-demographic dividend", "Low & middle income", "Low income", 
                                                  "Lower middle income","Middle East & North Africa", 
                                                  "Pacific island small states","Other small states","Middle income", 
                                                  "Sub-Saharan Africa","Syrian Arab Republic", "Upper middle income"])]
gender_df.head(10)

#merging cleaned dataframes
frames = [disorders_df, unemployment_df, scraped_df, gender_df]
df_final = functools.reduce(lambda left,right: pd.merge(left,right, on=['Country'], how='outer'), frames)
df_final.head(25)

df_final.info()

#cleaning data types
df_final['2015_Healthcare_Expenditure'] = df_final['2015_Healthcare_Expenditure'].str.replace(',', '')
df_final['2015_Healthcare_Expenditure'] = df_final['2015_Healthcare_Expenditure'].astype(np.float64)
df_final.info()

#function for checking for variable irregularities 
def CheckRates(column, n):
    return df_final[df_final[column] > n].sum()

CheckRates("2015_Disorder_Prevalence", 70)
CheckRates("2015_Unemployment", 80)
CheckRates("2016_Suicide_Rate", 60)
CheckRates("2015_Gender_Ratio", 70)

#percent missing values per column
percent_missing = df_final.isnull().sum() * 100 / len(df_final)
missing_value_df = pd.DataFrame({'column_name': df_final.columns,
                                 'percent_missing': percent_missing})
missing_value_df

df_final = df_final.drop('2015_Literacy_Rates', 1) #dropping literacy (over 40% NaN values)
df_final.apply(lambda x: sum(x.isnull().values), axis = 1)

#identifying rows with missing values over 70% per row
sum(df_final.apply(lambda x: sum(x.isnull().values), axis = 1) > 4) #54

df_final = df_final.dropna(thresh=4, axis=0)
sum(df_final.apply(lambda x: sum(x.isnull().values), axis = 1) > 4)
df_final.info()

#checking percent missing values per column again
percent_missing = df_final.isnull().sum() * 100 / len(df_final)
missing_value_df = pd.DataFrame({'percent_missing': percent_missing})

missing_value_df #no column missing over 20% of values

#imputing remaining missing values
df_final = df_final[['Country', 'Code', '2016_Suicide_Rate', '2015_Disorder_Prevalence', '2015_Unemployment', 
                    '2015_Healthcare_Expenditure', '2015_Gender_Ratio']]

df_impute = df_final.iloc[:, 2:7]

imputer = IterativeImputer(max_iter=10, random_state=101)
imputer.fit(df_impute)
df_impute_final = imputer.transform(df_impute)
df_impute_final = pd.DataFrame(df_impute_final, columns=df_impute.columns)
df_impute_final.head(15)

#merging dataframes back
df_impute_final["Country"] = df_final["Country"].values
df_impute_final["Code"] = df_final["Code"].values
df_impute_final.head(15)

#rechecking for NaN values
percent_missing = df_impute_final.isnull().sum() * 100 / len(df_impute_final)
missing_value_df = pd.DataFrame({'percent_missing': percent_missing})
missing_value_df.head()

#feature engineering classification outcome variable 
df_impute_final['2016_Suicide_Rate'].mean() #9.50

def ClassifyRate(row):
   if row['2016_Suicide_Rate'] > 9.50:
      return 1
   if row['2016_Suicide_Rate'] <= 9.50:
      return 0
    
df_impute_final['Suicide_Classification'] = df_impute_final.apply(lambda row: ClassifyRate(row), axis=1)
df_impute_final.info()

df_impute_final['Suicide_Classification'] = df_impute_final['Suicide_Classification'].astype('category')
df_impute_final['Suicide_Classification'] = df_impute_final['Suicide_Classification'].cat.rename_categories({0:'Below', 1:'Above'})
df_impute_final['Suicide_Classification']

#writing clean data to csv file
path = '/Users/emilyburns/Documents/Data_Science/projects/web_scraping_wiki/data/processed_data'
output_file = os.path.join(path, 'all_project_data_clean.csv')

df_impute_final.to_csv(output_file, index = False)