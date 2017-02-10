#!/usr/bin/env python
""" Create a series of folders and store a copy of the classified files in them.
The folders are created from the csv file.
"""
import argparse
import os
import shutil
import pandas as pd

parser = argparse.ArgumentParser(description='From the csv file, create a series of folders and store a copy of the classified files in them.')
parser.add_argument('pdf_folder',
                   help='Folder containing the pdfs')
parser.add_argument('csv_file',
                   help='csv file where the pdfs are classified')
parser.add_argument('target_folder',
                   help='Target folder where to classify the pdfs')

args = parser.parse_args()
input_dic = vars(args)

PDF_PATH = input_dic['pdf_folder']
CSV_FILE = input_dic['csv_file']
CLASSIF_PATH = input_dic['target_folder']

print('Loading: ',CSV_FILE)
clusters_table = pd.read_csv(CSV_FILE, index_col=0)


#file_path = '/media/benjamin/FAT32/pdfs'
#classif_path = '/media/benjamin/FAT32/pdfs/classif'
for name,column in clusters_table.iteritems():
    c_folder = 'cluster'+str(name)
    c_path = os.path.join(CLASSIF_PATH,c_folder)
    print('Writing folder {}'.format(c_path))
    if not os.path.exists(c_path):
            os.makedirs(c_path)
    for file in column:
    	if '/' in file:
    		break
        if pd.notnull(file):
            filename = os.path.join(PDF_PATH,file+'.pdf')
            new_filename = os.path.join(c_path,file+'.pdf')
            shutil.copy2(filename,new_filename)
print('Classification done.')