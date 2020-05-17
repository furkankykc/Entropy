from __future__ import division

import math

import numpy as np
import pandas as pd
from graphviz import Digraph


class Tree:

    def __init__(self, data=""):
        self.arr = []
        self.next = None
        self.data = data
        self.label = None
        self.id = None

    def __str__(self):
        return ('-->' + self.yazdir(1))

    # varsayılan ağaç yazdırma fonksiyonunun özyinelemeli kısmıdır.
    def yazdir(self, a=1):
        text = str(self.data)
        if (len(self.arr) > 0):
            for i in self.arr:
                text += '\n' + '\t-' * a * 2 + '>' + str(i.data) + '[' + i.next.yazdir(a + 1) + ']'
        return text

    # ağacı yazdırmak için kullanılacak fonksiyon
    def yaz(self):
        print('-->' + self.yazdir(1))

    def new_edge(self, root_id, dot):
        dot.node(str(self.id), str(self.data), color='red')
        dot.edge(str(root_id), str(self.id))
        if (len(self.arr) > 0):
            for i in self.arr:
                dot.node(str(i.id), str(i.data))
                dot.edge(str(self.id), str(i.id))
                i.next.new_edge(i.id, dot)
        else:
            dot.node(str(self.id), str(self.data), color='red')
            dot.edge(str(root_id), str(self.id))

    # ağacı çizdirmek için kenarlarının bağlantılarının özyinelemeli olarak belirlendiği fonksiyon
    def edgege(self, root_id, dot):
        ld = ""

        # karar dügümnlerinin renk listesi
        last_node_color = ['white', 'red']

        # tüm düğümlerin renklerinin listesi
        colors = ['red', 'green', 'blue', 'cyan', 'ping', 'purple', 'orange', 'brown', 'gray']
        # ağacın cocukları varmı
        if (len(self.arr) > 0):
            # ağacın tüm çocukları için
            for i in self.arr:
                # çizdirilecek obje olan dot'a düğümün tanımlanması
                dot.node(str(i.id), i.data)  # ,color=colors[i.id%len(colors)])
                # eklenen düğümün kök dügümüne bağlantısının kenar tanımlanması
                dot.edge(str(root_id), str(i.id))
                # düğümün çocukları için aynı fonksiyonun özyinelemeli olarak çağırılması
                i.next.edgege(i.id, dot)
        else:
            # eğer bir dügümün çocugu yoksa bu sonuç düğügümüdür.
            # sonuç dügümünün tanımlamalarının yapılması
            dot.node(str(self.id), str(self.data), color=last_node_color[1])
            dot.edge(str(root_id), str(self.id))

    def enumerate(self):
        # kullanılacak listenin tanımlanması
        myl = []
        # id değerinin tanımlanması
        id = 0
        # geçişler için  olarak kullanılacak geçici ağacın oluşturulması
        temp = self
        while temp != None:
            # ağacın id lerinin atanması
            temp.id = id
            id += 1
            # ağacın her cocuğu için
            for i in temp.arr:
                i.id = id
                id += 1
                # eğer boş değilse sonradan bakmak üzere listeye at
                if i != None:
                    myl.append(i)
            # eğer liste boş değilse listenin ilk elemanını seç ve sil
            if myl:
                temp = myl.pop(0).next
            else:
                temp = None

    def draw(self):
        # ağacın numaralandırılması (breath first)
        self.enumerate()
        # çizilecek yapının tanımlanması
        dot = Digraph(comment='Entropy')
        # ağacın kökünün yapıya aktarılması
        dot.node(str(self.id), str(self.data))
        # kenar tanımlama algoritmasına yolla
        self.new_edge(0, dot)
        # ağaç style'si için tanımlamalar
        styles = {
            'graph': {
                'label': 'Entropy',
                'fontsize': '16',
                'fontcolor': 'white',
                'bgcolor': 'white',

            },
            'nodes': {
                'fontname': 'Helvetica',
                'shape': 'hexagon',
                'fontcolor': 'white',
                'color': 'white',
                'style': 'filled',
                'fillcolor': '#006699',
            },
            'edges': {
                'style': 'dashed',
                'color': '#E0F2F2',
                'arrowhead': 'open',
                'fontname': 'Courier',
                'fontsize': '12',
                'fontcolor': 'white',
            }
        }
        # ağaç yapısına style uygulanması
        dot = self.apply_styles(dot, styles)
        # ağaçın çizdirilip gösterilmesi
        dot.render('test-output/round-table.gv', view=True)  # doctest: +SKIP

    # style'ı uygulayan fonksiyon
    def apply_styles(self, graph, styles):
        graph.graph_attr.update(
            ('graph' in styles and styles['graph']) or {}
        )
        graph.node_attr.update(
            ('nodes' in styles and styles['nodes']) or {}
        )
        graph.edge_attr.update(
            ('edges' in styles and styles['edges']) or {}
        )
        return graph


# entropy hesaplanarak karar ağacının oluşturulması
def entropyHesapla(df, tree, f=0, alfa=0.04):
    # f değeri 0 için karcı
    # f değeri 1 için shannon
    # f değeri diğerleri için deng
    dict = {}
    for col in range(0, len(df.columns) - 1):
        entropy = 0
        # print('\rData Loading {:.2f}%'.format(col / (len(df.columns) - 1) * 100), end='', flush=True)
        for idx, i in enumerate(df[df.columns[col]].unique()):

            for j in df[df.columns[-1]].unique():
                new = df[df[df.columns[col]] == i]
                new2 = new[new[new.columns[-1]] == j]
                # print (df[new.columns[1]]);
                # print('olasilik: ',len(new2),'/',len(new),i,j,len(df),len(new),'/',len(df[df.columns[col]]))
                if (len(new) == 0 or len(new2) == 0):
                    continue
                # entropy-=(len(new)/len(df[df.columns[col]]))*(len(new2)/len(new)*math.log(len(new2)/len(new),2))
                if (f == 0):
                    entropy += karci(len(new), len(df[df.columns[col]]), len(new2), len(new), alfa)
                elif (f == 1):
                    entropy += shannon(len(new), len(df[df.columns[col]]), len(new2), len(new))
                else:
                    entropy += deng(len(new), len(df[df.columns[col]]), len(new2), len(new))

        # print('entropy = ',entropy)

        dict[df.columns[col]] = entropy
    if len(dict) > 0:
        minimum = min(dict, key=dict.get)
    else:
        tree.data = df[df.columns[-1]].unique()[0]
        return
    # todo bura
    tree.data = minimum
    # print(df[min])
    mindf = df[minimum].unique()
    # print(dict)
    for m in mindf:

        temp = Tree()
        temp.data = m
        tree.arr.append(temp)
        budf = (df[df[minimum] == m])
        if (len(budf[df.columns[-1]].unique()) > 0):
            temp.next = Tree()
            entropyHesapla(budf.drop(minimum, 1), temp.next)


# karcı entropisi
def karci(payToplam, paydaToplam, payOlma, paydaOlma, alfa=0.04):
    a = abs(-math.pow((payToplam / paydaToplam), alfa) * math.log(payOlma / paydaOlma, 2))
    # print a
    # print((payToplam), '/', (paydaToplam), '\t', (payOlma), '/', (paydaOlma), '*', math.log(payOlma / paydaOlma, 2),
    #     '\t=',a)

    return a


# shannon (varsayılan) entropi
def shannon(payToplam, paydaToplam, payOlma, paydaOlma):
    # print ((payToplam),'/',(paydaToplam),'\t',(payOlma),'/',(paydaOlma),'*',math.log(payOlma/paydaOlma,2),'\t=', (-(payToplam/paydaToplam)*(payOlma/paydaOlma)*math.log(payOlma/paydaOlma,2)))
    return -(payToplam / paydaToplam) * (payOlma / paydaOlma) * math.log(payOlma / paydaOlma, 2)


# deng entropisi
def deng(payToplam, paydaToplam, payOlma, paydaOlma):
    entropy = -(payToplam / paydaToplam) * (payOlma / paydaOlma) * math.log(
        (payOlma / paydaOlma) / (math.pow(2, paydaToplam) - 1), 2)
    # print((payToplam), '/', (paydaToplam), '\t', (payOlma), '/', (paydaOlma), '*', math.log((payOlma/paydaOlma)/(math.pow(2,paydaToplam)-1),2),
    #      '\t=',entropy)

    return entropy


#
# def yazdir(tt):
#     str = tt.data
#     if (len(tt.arr) > 0):
#         for i in tt.arr:
#             str += '=>' + (i.data) + '[' + yazdir(i.next) + ']'
#
#     return str


class entropy:
    func_list = ['karci', 'deng', 'shannon']
    func_id = 0

    df = None

    def __init__(self, data, func_name, column_list=None, resultCol=''):

        if column_list is None:
            column_list = []

        if func_name in self.func_list:
            self.func_id = self.func_list.index(func_name)
        else:
            raise ValueError(func_name, " is not valid func_names ", self.func_list)

        if type(data) == type(pd.get_dummies('data')):
            self.df = data
        elif type(data) == str:
            if len(column_list) > 0:
                self.df = pd.DataFrame(np.array(pd.read_csv(data)),
                                       columns=column_list)
            else:
                np_data = pd.read_csv(data)
                # column_list = np.array(np_data[0])
                # print(pd.read_csv(data,index_col=0,nrows=0).columns.to_list())
                self.df = pd.DataFrame(np_data)
            if resultCol != '':
                self.prepare(resultCol)
        else:
            raise EnvironmentError("not valid data_set, data_set type must be pandas dataframe")

    def calc(self):
        tree = Tree()
        entropyHesapla(self.df, tree, self.func_id)
        tree.draw()
        tree.yaz()

    def prepare(self, colName: str):
        blueWins = self.df[[colName]]
        self.df.drop(columns=[colName], inplace=True)
        self.df.insert(len(self.df.columns), colName, blueWins)

# deneme datası
# text dosyasından datanın okunması
# a = pd.read_csv('Qualitative_Bankruptcy.data.csv')
# data'nın dataframe yapısına atılması ve stun isimlerinin tanımlanması
# df = pd.DataFrame(np.array(a),columns=['Industrial Risk','Management Risk','Financial Flexibility','Credibility','Competitiveness','Operating Risk','Class'])
# df = pd.DataFrame(a,columns=['EGITIM','YAS','CINSIYET','KABUL'])
# columns =['Industrial Risk','Management Risk','Financial Flexibility','Credibility','Competitiveness','Operating Risk','Class']
# entropy('Qualitative_Bankruptcy.data.csv','karci',columns).calc()
# root = Tree()


# entropyHesapla(df,root,1,1)

# root.yaz()
# root.draw()
