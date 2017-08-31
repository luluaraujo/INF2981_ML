#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 31 22:10:56 2017

@author: Luciane Araujo
"""
import os
import codecs
from os import walk
from shutil import copyfile
import collections

"""
Proportions: 
blow_down: 101 - 0.25% - 25
conventional_mine: 100 - 0.25% 
slash_burn: 209 - 0.52%%
blooming: 332 - 0.82%
artisinal_mine: 339 - 0.84%
selective_logging: 340 - 0.84%
cloudy: 2303 - 6%
bare_ground: 859 - 2%
haze: 2695 - 7%
habitation: 3662 - 9%
cultivation: 4547 - 11%
water: 7262 - 17%
partly_cloudy: 7251 - 18%
road: 8076 - 20%
agriculture: 12338 - 30%
clear: 28203 - 70%
primary: 37840 - 93%
    
"""

PATH_DATASET = '/Users/user/Documents/Mestrado/INF2981_ML_II/projeto/dataset'
arquivo_labels = PATH_DATASET + '/train_v2.csv'
FOLDER_TRAIN_20 = PATH_DATASET + '/train-20-ndvi'
number_of_images = 40479
number_of_training_images = int(round(40479*0.2, 0))
separador = ' '


def copyFirstXFilesToFolder(files_number, folder, file_label_dict, labels_qtd, selected_files):
    src = PATH_DATASET + '/train-tif-v2-separados/'+folder
    #dest = FOLDER_TRAIN_20 + '/'+folder
    dest = FOLDER_TRAIN_20

    if not os.path.exists(dest):
        os.makedirs(dest)
        
    for (dirpath, dirnames, filenames) in walk(src):   
        counter = 0;
        added_files = 0;
        while(counter <= len(filenames)-1 and added_files < files_number):
            filename = filenames[counter]
            if(filename in selected_files):
                counter = counter + 1
                continue
            else:
                selected_files.add(filename)
    
            file = '/'+filename
            copyfile(src+file, dest+file)
            counter = counter + 1
            added_files = added_files + 1
            labels = file_label_dict[filename.replace(".tif","")]
            for label in labels:
                labels_qtd[label] = labels_qtd[label] + 1   
        break

"""
Step 1. Load labels
"""

labels_dictionary = {}
selected_labels_qtd = {
        'blow_down':0, 
        'conventional_mine': 0,
        'slash_burn':0,
        'blooming':0,
        'artisinal_mine':0,
        'selective_logging':0,
        'cloudy':0,
        'bare_ground':0,
        'haze':0,
        'habitation':0,
        'cultivation':0,
        'water':0,
        'partly_cloudy':0,
        'road':0,
        'agriculture':0,
        'clear':0,
        'primary':0
        }
selected_files = set()

with codecs.open(arquivo_labels,'r') as arquivo:
    linhas=arquivo.readlines()
    for linha in linhas:
        tokens=linha[:-1].split(separador) #[:-1] eliminar o "/n" do fim da linha
        dict_tokens = {tokens[0] : set(tokens[1:len(tokens)])}
        labels_dictionary.update(dict_tokens)


""" 
Step 2: select rare images to keep proportion

"""
label_percent_dict = [
        ('blow_down',0.0025), 
        ('conventional_mine', 0.0025),
        ('slash_burn',0.0052),
        ('blooming',0.0082),
        ('artisinal_mine',0.0084),
        ('selective_logging',0.0084),
        ('bare_ground',0.02),
        ('cloudy',0.06),
        ('haze',0.07),
        ('habitation',0.09),
        ('cultivation',0.11),
        ('water',0.17),
        ('partly_cloudy',0.18),
        ('road',0.20),
        ('agriculture',0.30),
        ('clear',0.70),
        ('primary',0.93)
        ]
label_percent_dict = collections.OrderedDict(label_percent_dict)
total_selected = 0

for key, value in label_percent_dict.items():
    to_be_selected = int(round(number_of_training_images*value, 0))
    selected = to_be_selected - selected_labels_qtd[key]
    total_selected = total_selected + selected
    print(key + ':' + str(to_be_selected))
    print(key + ':' + str(selected_labels_qtd[key]))
    print(key + ':' + str(selected))

    
    if(selected<=0):
        continue
    copyFirstXFilesToFolder(selected, key, labels_dictionary, selected_labels_qtd, selected_files)
    
print('Number of training images: ' + str(number_of_training_images))
print('Selected files: ' + str(len(selected_files)))
print('Total specified for selection: ' + str(total_selected))
print(selected_labels_qtd)


