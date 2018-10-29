import pandas as pd
import time
from Entropy import entropy
import numpy as np




testDataManual= pd.np.array([['ORTA', 'YASLI', 'ERKEK', 'EVET'],
                             ['ILK',    'GENC', 'ERKEK','HAYIR'],
                             ['YUKSEK', 'ORTA', 'KADIN','HAYIR'],
                             ['ORTA',   'ORTA', 'ERKEK','EVET'],
                             ['ILK',    'ORTA', 'ERKEK','EVET'],
                             ['YUKSEK', 'YASLI','KADIN','EVET'],
                             ['ILK',    'GENC', 'KADIN','HAYIR']])

columns2=['EGITIM', 'YAS', 'CINSIYET', 'KABUL']
testDataManual = pd.DataFrame(testDataManual,columns=columns2)
data = 'Qualitative_Bankruptcy.data.txt'
df = pd.DataFrame(np.array(pd.read_csv(data)))
columns =['Industrial Risk','Management Risk','Financial Flexibility','Credibility','Competitiveness','Operating Risk','Class']

entropy(testDataManual,'karci',columns2).calc()