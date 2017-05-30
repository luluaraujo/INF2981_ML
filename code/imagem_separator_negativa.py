# -*- coding: utf-8 -*-
"""
Created on Sat May 27 18:19:58 2017

@author: willian
"""
import codecs
from shutil import copyfile

tema_alvo = 'agriculture'
quantidade_alvo = 450
pasta_entrada= 'G:\\coord_reader\\
pasta_saida= 'G:\\coord_reader\\
arquivo_entrada = 'G:\\coord_reader\\ilhs_bolivia-Brasil_gms.txt'
tabulador = ' '

nao_tema_alvo='NAO_'+ tema_alvo

diretorio = pasta_saida + nao_tema_alvo

if not os.path.exists(diretorio):
    os.makedirs(diretorio)

lista_negativos=[]

with codecs.open(arquivo_entrada,'r') as arquivo:
    linhas=arquivo.readlines()
    for linha in linhas:
        linha=linha.split(tabulador)
        if tema_alvo not in linha:
            lista_negativos.append(item[0])
                    
lista_negativos_sort=sorted(lista_negativos)

total = len(lista_negativos_sort)
if total<quantidade_alvo:
    quantidade_alvo = total

quantidade = 0

while quantidade <= quantidade_alvo:
    try:              
        item = lista_negativos_sort[quantidade]
        scr = pasta_entrada + item + '.tif'
        dst = diretorio + '//' + item + '.tif'
        try:
            copyfile(scr, dst)
        except:
            print item + '- Falhou na Copia ou nao existe'
    except:
        print 'quantidade nao disponivel'
    quantidade = quantidade + 1
            
