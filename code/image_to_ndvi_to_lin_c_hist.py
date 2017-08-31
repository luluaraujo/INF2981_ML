# -*- coding: utf-8 -*-

from osgeo import gdal
import numpy as np
import os
import codecs

def set_to_string(labels_set):
    label_str = ""
    for label in labels_set:
        if(len(label_str) == 0):
            label_str = label 
        else:
            label_str = label_str + " " + label 
    
    return label_str

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
        print(image_id + ": to many cloud labels")
        return 2
    if len(cloud_label) < 1:
        print(image_id + ": no cloud labels")
        return 2
        
    return cloud_label.pop()

def histograma(image):
    vetor=[]
    b = np.histogram(image,256,(0,256))[0]
    for item in b:
        vetor.append(item)
    
    return vetor

def image_to_lin(image_file):
    
    gtif = gdal.Open(image_file)
    
    metadados = gtif.GetMetadata()
    
    b1 = gtif.GetRasterBand(1)  #bandas em 16 bits tipo gdal
    b2 = gtif.GetRasterBand(2)
    b3 = gtif.GetRasterBand(3)
    b4 = gtif.GetRasterBand(4)
      
    #b1=(np.array(b1.ReadAsArray())).astype(np.int) 
    #b2=(np.array(b2.ReadAsArray())).astype(np.int)    
    b3=(np.array(b3.ReadAsArray())).astype(np.int) 
    b4=(np.array(b4.ReadAsArray())).astype(np.int) 

    a=(b4-b3)*255 #calcula o NDVI, o scalar é usado para ter valores de pixel adequados
    b=(b4+b3)
    ndvi=(a/b)
    neg = np.min(ndvi) #aplica offset para não haver valores negativos
    if neg < 0:
        ndvi = ndvi-neg
    
    b1=(np.array(b1.ReadAsArray())).astype('uint8') 
    b2=(np.array(b2.ReadAsArray())).astype('uint8')
    b3=(b3).astype('uint8')
    b4=(b4).astype('uint8')
    ndvi=(ndvi).astype('uint8')

    h1 = histograma(b1)
    h2 = histograma(b2)
    h3 = histograma(b3)
    h4 = histograma(b4)
    hndvi = histograma(ndvi)
    
    histograma_lin = h1+h2+h3+h4+hndvi
    
   
    ndvi_lin=(ndvi.reshape(256*256)).tolist()
            
    linha_pixel=ndvi_lin
    #linha_stat = b1stat + b2stat + b3stat + b4stat
     
    metadado=str(metadados).replace(" ","").replace("[", "").replace("]","")
    linha_pixel=str(linha_pixel).replace(" ","").replace("[", "").replace("]","")
    linha_stat=str(histograma_lin).replace(" ","").replace("[", "").replace("]","")
    
    return metadado, linha_pixel, linha_stat

#=================INICIO da BAGAÇA========================================

PATH_DATASET = '/Users/user/Documents/Mestrado/INF2981_ML_II/projeto/dataset'
pasta_tif = PATH_DATASET + '/train-tif-v2/'
pasta_resultado = PATH_DATASET + '/train-tif-v2/result/'
arquivo_labels = PATH_DATASET + '/train_v2.csv'
separador = ' '

saida_pixel = pasta_resultado + 'pixels.nh.csv'
saida_metadado = pasta_resultado + 'metadados.nh.csv'
saida_stat = pasta_resultado + 'estatisticas.nh.csv'
saida_erro = pasta_resultado + 'erro.txt'

if not os.path.exists(pasta_resultado):
    os.makedirs(pasta_resultado)

pixel_file = open(saida_pixel, "w")
metadado_file = open(saida_metadado, "w")
stat_file = open(saida_stat, "w")
erro_file = open(saida_erro,"w")

lista_tif = [f for f in os.listdir(pasta_tif) if f.endswith('.tif')]

labels_dictionary = {}
with codecs.open(arquivo_labels,'r') as arquivo:
    linhas=arquivo.readlines()
    for linha in linhas:
        tokens=linha[:-1].split(separador) #[:-1] eliminar o "/n" do fim da linha
        dict_tokens = {tokens[0] : set(tokens[1:len(tokens)])}
        labels_dictionary.update(dict_tokens)

total=len(lista_tif)
total_div = int(total/1)
i=0

for file in lista_tif:
    i=i+1
    path=pasta_tif+file
    if i%total_div == 0:
        print(str((i*100)/total) + '%')
    try:
        nome=file[:-4]
        labels = set_to_cloud_classification(nome, labels_dictionary[nome])
        metadados, linha_pixel, linha_stat = image_to_lin(path)
        pixel_file.write(str(labels)+','+linha_pixel+'\n')
        metadado_file.write(str(labels)+','+metadados+'\n')
        stat_file.write(str(labels)+','+linha_stat+'\n')
    except:
        erro_file.write(nome+'\n')
    

pixel_file.close()
metadado_file.close()
stat_file.close()
erro_file.close()
