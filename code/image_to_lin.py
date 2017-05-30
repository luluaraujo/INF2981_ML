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
    linha_stat = b1stat + b2stat + b3stat + b4stat
    
    metadado=str(metadados).translate(None," []")
    linha_pixel=str(linha_pixel).translate(None," []")
    linha_stat=str(linha_stat).translate(None," []")
        
    
    return metadado, linha_pixel, linha_stat

#=================INICIO da BAGAÇA========================================


pasta_tif = 'G://test-tif-v2//' #pasta onde estão as imagens, deve terminar com //

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
