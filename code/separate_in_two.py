# -*- coding: utf-8 -*-
import os
import numpy as np
from osgeo import gdal
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
        print(image_id)
        
    return cloud_label.pop()
        

def image_to_lin(image_file, export_as_ndvi):
    
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
        b1=(np.array(b1.ReadAsArray()))  #bandas em 16 bits tipo numpy array
        b2=(np.array(b2.ReadAsArray()))
        b3=(np.array(b3.ReadAsArray()))
        b4=(np.array(b4.ReadAsArray()))
        
        b1=(b1).astype('uint8') #bandas em 8 bits tipo numpy array
        b2=(b2).astype('uint8')
        b3=(b3).astype('uint8')
        b4=(b4).astype('uint8')
        
        b1_lin=(b1.reshape(256*256)).tolist() #gera vetor 1D para cada banda
        b2_lin=(b2.reshape(256*256)).tolist()
        b3_lin=(b3.reshape(256*256)).tolist()
        b4_lin=(b4.reshape(256*256)).tolist()
        
        linha_pixel=b1_lin + b2_lin + b3_lin + b4_lin #gera vetor 1D para cada imagem
        
        #linha_pixel=b4_lin
    else:
        b3=(np.array(b3.ReadAsArray())).astype(np.int) 
        b4=(np.array(b4.ReadAsArray())).astype(np.int) 
    
        a=(b4-b3)*255 #calcula o NDVI, o scalar é usado para ter valores de pixel adequados
        b=(b4+b3)
        ndvi=(a/b)
        neg = np.min(ndvi) #aplica offset para não haver valores negativos
        ndvi = ndvi-neg
        
        ndvi=(ndvi).astype('uint8')
        
        ndvi_lin=(ndvi.reshape(256*256)).tolist()
                
        linha_pixel=ndvi_lin
        
    linha_stat = b1stat + b2stat + b3stat + b4stat
    
    metadados=str(metadados).replace(" ","").replace("[", "").replace("]","")
    linha_pixel=str(linha_pixel).replace(" ","").replace("[", "").replace("]","")
    linha_stat=str(linha_stat).replace(" ","").replace("[", "").replace("]","")
        
    
    return metadados, linha_pixel, linha_stat

#=================INICIO da BAGAÇA========================================

PATH_DATASET = '/Users/user/Documents/Mestrado/INF2981_ML_II/projeto/dataset'
pasta_tif = PATH_DATASET + '/test-tif-v2/' #pasta onde estão as imagens, deve terminar com //
pasta_tif1 = PATH_DATASET + '/test-tif-v2/1/' #pasta onde estão as imagens, deve terminar com //
pasta_tif2 = PATH_DATASET + '/test-tif-v2/2/' #pasta onde estão as imagens, deve terminar com //


if not os.path.exists(pasta_tif1):
    os.makedirs(pasta_tif1)

if not os.path.exists(pasta_tif2):
    os.makedirs(pasta_tif2)

lista_tif = [f for f in os.listdir(pasta_tif) if f.endswith('.tif')]



counter = 0
for file in lista_tif:
    path=pasta_tif+file
    try:
        if counter % 2 == 0:
            os.rename(pasta_tif+file, pasta_tif1+file)
        else:
            os.rename(pasta_tif+file, pasta_tif2+file)
    except Exception as e: 
        print(file+'\n')
        
    counter = counter + 1
        
