import pandas as pd
import numpy as np
import seaborn as sns
import json
import warnings
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")

lego_file = open('result_Lego.json', 'r')
cache_lego_contents = lego_file.read()
lego_cache = json.loads(cache_lego_contents)

df_1 = pd.DataFrame(list(lego_cache.values())[0])
df_1['Age_Range'] = '1.5+'
df_4 = pd.DataFrame(list(lego_cache.values())[1])
df_4['Age_Range'] = '4+'
df_6 = pd.DataFrame(list(lego_cache.values())[2])
df_6['Age_Range'] = '6+'
df_9 = pd.DataFrame(list(lego_cache.values())[3])
df_9['Age_Range'] = '9+'
df_13 = pd.DataFrame(list(lego_cache.values())[4])
df_13['Age_Range'] = '13+'
df_18 = pd.DataFrame(list(lego_cache.values())[5])
df_18['Age_Range'] = '18+'


df_combo = pd.concat([df_1, df_4, df_6, df_9, df_13, df_18])
df_combo['Price'] = df_combo.Price.str.replace('$','')
df_combo_filtered = df_combo[(df_combo['Price'] != 'Please call the shopping assistant for getting the price') & (df_combo['Pieces'] != 'Not Available')]
df_combo_filtered['Price'] = df_combo_filtered.Price.astype(float)
df_combo_filtered['Pieces'] = df_combo_filtered.Pieces.astype(int)
df_combo_filtered = df_combo_filtered.reset_index()
del df_combo_filtered['index']

df_combo_filtered_2 = df_combo_filtered[(df_combo_filtered['Price']<300) & (df_combo_filtered['Pieces']<5000)]


sns.relplot(x='Pieces', y="Price",hue="Age_Range",
            sizes=(40, 400), alpha=1, height=6, data=df_combo_filtered)
plt.show()

sns.jointplot(x='Pieces', y="Price",kind="kde",data=df_combo_filtered_2)
plt.show()

age_range = df_combo_filtered.groupby('Age_Range').size()
age_range.plot(kind='pie', title='Distribution of Lego toys under different Age Range', ylabel='')
plt.show()

sns.pairplot(df_combo_filtered,vars=['Price','Pieces','Age_Range'])
plt.show()
