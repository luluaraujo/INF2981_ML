# -*- coding: utf-8 -*-
import os
import numpy as np
from osgeo import gdal
import codecs

def set_to_cloud_classification(image_id, labels_set):
    
    cloud_label = set()
    
    if "cloudy" in labels_set:
        cloud_label.add(0)
    if "haze" in labels_set:
        cloud_label.add(1)
    if "partly_cloudy" in labels_set:
        cloud_label.add(2)
    if "clear" in labels_set:
        cloud_label.add(3)
        
    if len(cloud_label) > 1:
        print(image_id + ": more then 1 cloud label")
        return -1
    if len(cloud_label) < 1:
        print(image_id + ": no cloud label present")
        return -1
    return cloud_label.pop()

def set_to_primary_classification(image_id, labels_set):
    
    label = set()
    
    if "primary" in labels_set:
        label.add(6)
    else:
        label.add(-1)
    return label.pop()


def set_to_agriculture_classification(image_id, labels_set):
    
    label = set()
    if "agriculture" in labels_set:
        label.add(4)
    else:
        label.add(-1)
    return label.pop()

def set_to_road_classification(image_id, labels_set):
    
    label = set()
    if "road" in labels_set:
        label.add(9)
    else:
        label.add(-1)
    return label.pop()

def set_to_cloudy_classification(image_id, labels_set):
    
    label = set()
    if "cloudy" in labels_set:
        label.add(0)
    else:
        label.add(-1)
    return label.pop()

def set_to_water_classification(image_id, labels_set):
    
    label = set()
    if "water" in labels_set:
        label.add(8)
    else:
        label.add(-1)
    return label.pop()



def set_to_label_classification(image_id, labels_set, label_str, label_index):
    
    label = set()
    if label_str in labels_set:
        label.add(label_index)
    else:
        label.add(-1)
    return label.pop()
        

#=================INICIO da BAGAÇA========================================

PATH_DATASET = '/Users/user/Documents/Mestrado/INF2981_ML_II/projeto/dataset'
pasta_labels = PATH_DATASET + '/labels/' #pasta onde estão as imagens, deve terminar com //
arquivo_labels = PATH_DATASET + '/train_v2.csv'
separador = ' '

saida_labels = pasta_labels + 'labels_bare_ground.nh.csv'

if not os.path.exists(pasta_labels):
    os.makedirs(pasta_labels)

labels_file = open(saida_labels, "w")

labels_dictionary = {}

with codecs.open(arquivo_labels,'r') as arquivo:
    linhas=arquivo.readlines()
    for linha in linhas:
        tokens=linha[:-1].split(separador) #[:-1] eliminar o "/n" do fim da linha
        dict_tokens = {tokens[0] : set(tokens[1:len(tokens)])}
        labels_dictionary.update(dict_tokens)

count = 0
for key, value in labels_dictionary.items(): 
    filename_no_extension = key
    labels = set_to_label_classification(filename_no_extension, labels_dictionary[filename_no_extension], "bare_ground", 16)
    if(labels != -1):
        count = count + 1
    print(count)
    labels_file.write(filename_no_extension+','+str(labels)+"\n")
        
labels_file.close()
