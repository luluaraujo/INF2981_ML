#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 19:50:00 2017

@author: Luciane Calixto de Araujo
"""

def from_code_to_label(code):
    if code == str(-1):
        return "" 
    if code == str(0):
        return "cloudy "
    if code == str(1):
        return "haze "
    if code == str(2):
        return "partly_cloudy "
    if code == str(3):
        return "clear "
    if code == str(4):
        return "agriculture "
    if code == str(5):
        return "cultivation "
    if code == str(6):
        return ""
    if code == str(7):
        return "habitation "
    if code == str(8):
        return "water "
    if code == str(9):
        return "road "
    if code == str(10):
        return "blow_down "
    if code == str(11):
        return "slash_burn "
    if code == str(12):
        return "blooming "
    if code == str(13):
        return "conventional_mine "
    if code == str(14):
        return "artisinal_mine "
    if code == str(15):
        return "selective_logging "
    if code == str(16):
        return "bare_ground "
    return code + ","
    
    


PATH_DATASET = '/Users/user/Documents/Mestrado/INF2981_ML_II/projeto/dataset/'
files = {"result_1.csv","result_2.csv"}
output_file_name = "compiled_results.csv"
output_file_baseline_name = "compiled_results_baseline.csv"
filename_mapping = "test_v2_file_mapping.csv"

output_file = open(PATH_DATASET + output_file_name, 'w')
output_file_baseline = open(PATH_DATASET + output_file_baseline_name, 'w')

output_file.write("image_name,tags\n")
output_file_baseline.write("image_name,tags\n")
line_count = 0;

for filename in files:
    
    file = open(PATH_DATASET + filename)
    lines = file.readlines()

    for line in lines:
        
       tokens = line.split(",")
       new_line = ""
       for token in tokens:
           new_line = new_line + from_code_to_label(token.strip())
       output_file.write(new_line+" primary\n")
       output_file_baseline.write(tokens[0].strip() + ", primary clear agriculture road water \n"  )
       line_count = line_count + 1
    file.close()
    
    
output_file.close()
output_file_baseline.close()

print(line_count)

        
    