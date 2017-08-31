# -*- coding: utf-8 -*-

from osgeo import gdal
import sys
import numpy as np
import os

def image_to_lin(image_file):
    
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
     
    metadado=str(metadados).translate(None," []")
    linha_pixel=str(linha_pixel).translate(None," []")
    linha_stat=str(linha_stat).translate(None," []")       
    
    return metadado, linha_pixel, linha_stat

#=================INICIO da BAGAÇA========================================


pasta_tif = 'D://train//toy//' #pasta onde estão as imagens, deve terminar com //

saida_pixel = pasta_tif + 'pixels.txt'
saida_metadado = pasta_tif + 'metadados.txt'
saida_stat = pasta_tif + 'estatisticas.txt'
saida_erro = pasta_tif + 'erro.txt'

pixel_file = open(saida_pixel, "w")
metadado_file = open(saida_metadado, "w")
stat_file = open(saida_stat, "w")
erro_file = open(saida_erro,"w")

lista_tif = [f for f in os.listdir(pasta_tif) if f.endswith('.tif')]

for file in lista_tif:
    path=pasta_tif+file
    print path
    try:
        metadados, linha_pixel, linha_stat = image_to_lin(path)
        pixel_file.write(file+','+linha_pixel+'\n')
        metadado_file.write(file+','+metadados+'\n')
        stat_file.write(file+','+linha_stat+'\n')
    except:
        erro_file.write(file+'\n')
    

pixel_file.close()
metadado_file.close()
stat_file.close()
erro_file.close()
