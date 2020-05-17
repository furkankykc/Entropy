import numpy as np
import pandas as pd

from Entropy import entropy

testDataManual = pd.np.array([['ORTA', 'YASLI', 'ERKEK', 'EVET'],
                              ['ILK', 'GENC', 'ERKEK', 'HAYIR'],
                              ['YUKSEK', 'ORTA', 'KADIN', 'HAYIR'],
                              ['ORTA', 'ORTA', 'ERKEK', 'EVET'],
                              ['ILK', 'ORTA', 'ERKEK', 'EVET'],
                              ['YUKSEK', 'YASLI', 'KADIN', 'EVET'],
                              ['ILK', 'GENC', 'KADIN', 'HAYIR']])

testManual = pd.np.array([['ORTA', 'YASLI', 'ERKEK'],['ILK', 'GENC', 'KADIN'],
                              ])
testCol = ['EGITIM', 'YAS', 'CINSIYET']
testtData = pd.DataFrame(testManual, columns=testCol)


columns2 = ['EGITIM', 'YAS', 'CINSIYET', 'KABUL']
testDataManual = pd.DataFrame(testDataManual, columns=columns2)
# data = 'Qualitative_Bankruptcy.data.csv'
# cov19 = 'TimeAge.csv'
# df = pd.DataFrame(np.array(pd.read_csv(data)))
# columns = ['Industrial Risk', 'Management Risk', 'Financial Flexibility', 'Credibility', 'Competitiveness',
#            'Operating Risk', 'Class']
#

data = 'Qualitative_Bankruptcy.data.csv'
# # df = pd.DataFrame(pd.read_csv(data))
# # blueWins = df[['blueWins']]
# # df.drop(columns=['blueWins'],inplace=True)
# # df.insert(len(df.columns), 'blueWins', blueWins)
# # print(df.head())
e = entropy(testDataManual, 'karci',resultCol='KABUL',column_list=columns2)
e.calc()
e.result(testtData)
# for index, row in testtData.iterrows():
#
#     print(row['YAS'])
# rangei =100
# rangej = 1
# for i in range(0,rangei):
#     for j in range(0,rangej):
#         print('\rData Loading {:.5f}% {} {}'.format((i+j/(rangej-1 if rangej != 1 else rangej))/(rangei)*100,i,j), end='\n', flush=False)
