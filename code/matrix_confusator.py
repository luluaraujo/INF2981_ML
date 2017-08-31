# -*- coding: utf-8 -*-
"""
Created on Sat May 27 18:19:58 2017

@author: willian
"""
import codecs
#from shutil import copyfile
#import os

arquivo_entrada = 'D://train//dataset//train_v2.csv//train_v2.txt'
tabulador = ' '

lista=[]
features = []
texto=[]

with codecs.open(arquivo_entrada,'r') as arquivo:
    linhas=arquivo.readlines()
    for linha in linhas:
        linha=linha.split(tabulador)
        linha[-1]=linha[-1][:-1]
        linha=linha[1:]
        texto.append(linha)
        i=0
        for item in linha:
            features.append(item) #registra todos os valores que aperecem

import collections
import itertools

counter=collections.Counter(features)
soma=(counter)
tipos=(counter.keys())

combinacoes = list(itertools.combinations(tipos, 2))

labels_dict={}            
for item in combinacoes:
    dict_tokens={item:0}
    labels_dict.update(dict_tokens)

for linha in texto:
    for item in combinacoes:
        test=0
        for i in item:
            if i in linha:
                test=test+1
        if test==len(item):
            labels_dict[item]=labels_dict[item]+1

relat = sorted(labels_dict.items(), key=lambda x:x[1])
'''            
i=0
conta = collections.Counter([])
         
for lin in texto:
    for item2 in comb2:
        if all(x in lin for x in item2):
            i=i+1
            print('la')
            nome = item2[0]+&+item[1]
            #contap=collections.Counter(item2)
            print contap
            conta=conta+contap
            print conta
            

#counter=collections.Counter(comb2)
#soma=(counter)
#tipos=(counter.keys())  

'''