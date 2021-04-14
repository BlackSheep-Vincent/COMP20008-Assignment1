import pandas as pd
import argparse
import numpy as np

OWcovid = pd.read_csv("owid-covid-data.csv", encoding='ISO-8859-1')

OWcovid = OWcovid.loc[:,['location','date','total_cases','new_cases','total_deaths','new_deaths']]

# 制作掩码抓取2020年数据
OWcovid['date'] = pd.to_datetime(OWcovid['date'])

mask = (OWcovid['date']>'2019') & (OWcovid['date']<'2021')
OWcovid_2020 = OWcovid.loc[mask]

# 建两个series
Date = pd.Series(OWcovid['date'])

listmonths = ['2020-1-1','2020-2-1','2020-3-1','2020-4-1','2020-5-1','2020-6-1','2020-7-1','2020-8-1','2020-9-1','2020-10-1','2020-11-1','2020-12-1','2021-1-1']
Months = pd.Series(listmonths)
Months = pd.to_datetime(Months)

# reset the index
OWcovid_2020 = OWcovid_2020.reset_index()

# 添加单独一列记录每行数据所处的月份
MonthsDic = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sept', 10:'Oct', 11:'Nov', 12:'Dec'}

OWcovid_2020['month'] = '1'

datamonths = []
for x in OWcovid_2020['date']:  
    for y in range(12):
        if (x>=Months.loc[y]) & (x<Months.loc[y+1]):
            datamonths.append(MonthsDic[y+1])
datamonths = pd.Series(datamonths)

OWcovid_2020['month'] = datamonths

# group by 两个条件
groupby2020 = OWcovid_2020.loc[:,['location','month','total_cases','new_cases','total_deaths','new_deaths']].groupby(['location','month']).agg({'total_cases':'max','new_cases':'sum','total_deaths':'max','new_deaths':'sum'})

# compute the fataility rate and sorting values
fatalityrate = []
new_cases = pd.Series(groupby2020['new_cases'])
new_deaths = pd.Series(groupby2020['new_deaths'])

fatalityrate = (new_deaths/new_cases).replace([np.inf, -np.inf, "", np.nan],0)

groupby2020['case_fatality_rate'] = fatalityrate
groupby2020 = groupby2020[['case_fatality_rate','total_cases','new_cases','total_deaths','new_deaths']]
groupby2020 = groupby2020.sort_values(by=['location','month'], ascending = [True, True])
groupby2020 = groupby2020.replace([np.inf, -np.inf, "", np.nan],0)

# print前五行
groupby2020_first5 = groupby2020.head()
print(groupby2020_first5)

parser = argparse.ArgumentParser()
parser.add_argument('owid-covid-data-2020-monthly.csv')
args = parser.parse_args()
args = groupby2020
args.to_csv('owid-covid-data-2020-monthly.csv')