# -*- coding: utf-8 -*-
import os
import numpy as np
from osgeo import gdal
import scipy.stats as sc
import matplotlib.pyplot as plt

def histograma(image):
    vetor=[]
    b = sc.histogram(image,25,(0,256))[0]
    for item in b:
        vetor.append(item)
    
    return vetor

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
        print(image_id)
        
    return cloud_label.pop()
        

def image_to_lin(image_file, export_as_ndvi):
    
    #print(image_file)
    
    gtif = gdal.Open(image_file)
    
    metadados = gtif.GetMetadata()
    
    b1 = gtif.GetRasterBand(1)  #bandas em 16 bits tipo gdal
    b2 = gtif.GetRasterBand(2)
    b3 = gtif.GetRasterBand(3)
    b4 = gtif.GetRasterBand(4)
      
   
    
    b1stat = b1.GetStatistics( True, True ) #estatisticas media, despad, min e max
    b2stat = b2.GetStatistics( True, True )
    b3stat = b3.GetStatistics( True, True )
    b4stat = b4.GetStatistics( True, True )
    
    if(not export_as_ndvi):
        #b1=(np.array(b1.ReadAsArray()))  #bandas em 16 bits tipo numpy array
        #b2=(np.array(b2.ReadAsArray()))
        #b3=(np.array(b3.ReadAsArray()))
        #b4=(np.array(b4.ReadAsArray()))
        
        b1=(np.array(b1.ReadAsArray())).astype(np.int32) 
        b2=(np.array(b2.ReadAsArray())).astype(np.int32)    
        b3=(np.array(b3.ReadAsArray())).astype(np.int32) 
        b4=(np.array(b4.ReadAsArray())).astype(np.int32) 
        
        b1=(b1).astype('uint8') #bandas em 8 bits tipo numpy array
        b2=(b2).astype('uint8')
        b3=(b3).astype('uint8')
        b4=(b4).astype('uint8')
        
        b1_lin=(b1.reshape(256*256)).tolist() #gera vetor 1D para cada banda
        b2_lin=(b2.reshape(256*256)).tolist()
        b3_lin=(b3.reshape(256*256)).tolist()
        b4_lin=(b4.reshape(256*256)).tolist()
        
        linha_pixel=b1_lin + b2_lin + b3_lin + b4_lin #gera vetor 1D para cada imagem
        
        linha_stat = b1stat + b2stat + b3stat + b4stat
        
        linha_stat=str(linha_stat).replace(" ","").replace("[", "").replace("]","")
        
        #linha_pixel=b4_lin
    else:
        #b3=(np.array(b3.ReadAsArray())).astype(np.int) 
        #b4=(np.array(b4.ReadAsArray())).astype(np.int) 
        b1=(np.array(b1.ReadAsArray())).astype(np.int32) 
        b2=(np.array(b2.ReadAsArray())).astype(np.int32)    
        b3=(np.array(b3.ReadAsArray())).astype(np.int32) 
        b4=(np.array(b4.ReadAsArray())).astype(np.int32)
        
        np.seterr(invalid='ignore')
    
        ndvi = (b4 - b3)/(b4 + b3)
        ndvi = (ndvi + 1) * (2**7 - 1)
        ndvi = ndvi.astype(np.uint8)
        
        b1=(b1).astype(np.uint8) 
        b2=(b2).astype(np.uint8)
        b3=(b3).astype(np.uint8)
        b4=(b4).astype(np.uint8)
        ndvi=(ndvi).astype(np.uint8)
    
        #h1 = histograma(b1)
        #h2 = histograma(b2)
        #h3 = histograma(b3)
        #h4 = histograma(b4)
        
        #hndvi = histograma(ndvi)
        
        #histograma_lin = h1+h2+h3+h4+hndvi
        
        ndvi_lin=(ndvi.reshape(256*256)).tolist()
        
        linha_pixel=ndvi_lin
        
        #linha_stat=str(histograma_lin).replace(" ","").replace("[", "").replace("]","")
        
    
    
    metadados=str(metadados).replace(" ","").replace("[", "").replace("]","")
    linha_pixel=str(linha_pixel).replace(" ","").replace("[", "").replace("]","")
    
        
    
    return metadados, linha_pixel #, linha_stat

#=================INICIO da BAGAÇA========================================

PATH_DATASET = '/Users/user/Documents/Mestrado/INF2981_ML_II/projeto/dataset'
pasta_tif = PATH_DATASET + '/train-tif-v2/' #pasta onde estão as imagens, deve terminar com //
pasta_result = PATH_DATASET + '/train-tif-v2/result/'
#arquivo_labels = PATH_DATASET + '/test_v2.csv'
separador = ' '

saida_pixel = pasta_result + 'pixels.txt'
saida_metadado = pasta_result + 'metadados.txt'
saida_stat = pasta_result + 'estatisticas.txt'
saida_erro = pasta_result + 'erro.txt'

if not os.path.exists(pasta_result): 
    os.makedirs(pasta_result)

pixel_file = open(saida_pixel, "w")
metadado_file = open(saida_metadado, "w")
stat_file = open(saida_stat, "w")
erro_file = open(saida_erro,"w")

lista_tif = [f for f in os.listdir(pasta_tif) if f.endswith('.tif')]

labels_dictionary = {}
#with codecs.open(arquivo_labels,'r') as arquivo:
#    linhas=arquivo.readlines()
#    for linha in linhas:
#        tokens=linha[:-1].split(separador) #[:-1] eliminar o "/n" do fim da linha
#        dict_tokens = {tokens[0] : set(tokens[1:len(tokens)])}
#        labels_dictionary.update(dict_tokens)


for file in lista_tif:
    path=pasta_tif+file
    try:
        filename_no_extension = file.replace(".tif","")
        #labels = set_to_cloud_classification(filename_no_extension, labels_dictionary[filename_no_extension])
        #metadados, linha_pixel, linha_stat = image_to_lin(path, True)
        metadados, linha_pixel = image_to_lin(path, True)
        pixel_file.write(filename_no_extension+','+linha_pixel+'\n')
        metadado_file.write(file+','+metadados+'\n')
        #stat_file.write(file+','+linha_stat+'\n')
    except Exception as e: 
        erro_file.write(file+'\n')
        
pixel_file.close()
metadado_file.close()
stat_file.close()
erro_file.close()
