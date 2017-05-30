# -*- coding: utf-8 -*-
"""
Created on Sat May 27 18:19:58 2017

@author: willian
"""
import codecs
from shutil import copyfile
import os

#tema_alvo = 'agriculture'
#quantidade_alvo = 450
pasta_entrada= 'E://pessoal//Lu//train-tif-v2//'
pasta_saida= 'E://pessoal//Lu//separados//'
arquivo_entrada = 'E://pessoal//Lu//label//train_v2csv//train_v2.txt'
tabulador = ' '
arquivo_erro='E://pessoal//Lu//separados//erro.txt'

#diretorio_saida = pasta_saida + tema_alvo

#if not os.path.exists(diretorio_saida):
#    os.makedirs(diretorio_saida)
erro_file = open(arquivo_erro,"w")

with codecs.open(arquivo_entrada,'r') as arquivo:
    linhas=arquivo.readlines()
    for linha in linhas:
        linha=linha[:-1].split(tabulador) #[:-1] eliminar o "/n" do fim da linha
        i=0
        for item in linha:
            if i==0:
                imagem_nome = item + '.tif'
            else:
                diretorio_saida = pasta_saida + item + '//'
                if not os.path.exists(diretorio_saida):
                    os.makedirs(diretorio_saida)
                dst = diretorio_saida + imagem_nome
                scr = pasta_entrada + imagem_nome
                try:
                    copyfile(scr, dst)
                except:
                    #print(imagem_nome + ' do tipo ' + item + ' - Falhou na Copia ou nao existe')
                    erro_file.write(imagem_nome + ' do tipo ' + item + ' - Falhou na Copia ou nao existe'+'\n')
            i=i+1
            
erro_file.close()
