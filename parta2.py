import pandas as pd
import argparse
import matplotlib.pyplot as plt
import numpy as np
import sys

a=sys.argv[1]

b=sys.argv[2]

#commands = sys.argv[1:3]

# 读取csv文件
df_owid_covid = pd.read_csv('owid-covid-data-2020-monthly.csv', encoding = 'ISO-8859-1')

# 查列出所有不同地区的名字
locations_name = []

for x in df_owid_covid['location']:
    jud = 0
    for y in range(len(locations_name)):
        if x == locations_name[y]:
            jud = 1
    if jud == 0:
        locations_name.append(x)
        
# filter/locate the data required
ratedict = {}

for location in range(len(locations_name)):
    loc = df_owid_covid.loc[df_owid_covid['location'] == locations_name[location]]
    name = loc['location'].values[0]
    if loc['total_cases'].max() == 0:
        ratedict[name] = 0
    else:
        ratedict[name] = loc['total_deaths'].max()/loc['total_cases'].max()

    plt.scatter(loc['total_cases'].max(), ratedict[name], label=name)

# set arguments for overall plot
plt.ylabel("case_fatality_rate")
plt.xlabel("new_cases")
plt.title("scatter-a")
plt.xlim(-1e6,9e6)
plt.grid(True)
plt.savefig(a)
plt.close()

# the log-scale x-axis plot
owid_covid_logscale = [np.log(number+(1e-5)) if (int(number)>0) else number for number in df_owid_covid['total_cases']]
#display(owid_covid_logscale)
df_owid_covid_logscale = df_owid_covid
df_owid_covid_logscale['total_cases'] = owid_covid_logscale

# filter/locate the data required
for location in range(len(locations_name)):

    loc = df_owid_covid_logscale.loc[df_owid_covid_logscale['location'] == locations_name[location]]
    name = loc['location'].values[0]
    print(loc['total_cases'].max())
    plt.scatter(loc['total_cases'].max(), ratedict[name], label=name)

# et arguments for overall plot
plt.ylabel("case_fatality_rate")
plt.xlabel("new_cases(log-scale)")
plt.title("scatter-b")
#plt.xlim(-0.5,50)
plt.grid(True)
plt.savefig(b)
plt.close()