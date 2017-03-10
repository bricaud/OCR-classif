#!/usr/bin/env python
""" Create a series of folders and store a copy of the classified files in them.
The folders are created from the csv file.
"""
import argparse
import os
import shutil
import csv

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

# losding the CSV file into a dict of clusters
cluster_dic ={}
print('Loading: ',CSV_FILE)
with open(CSV_FILE, 'r') as csvfile:
	clusters_table = csv.DictReader(csvfile, delimiter=',')
	for row in clusters_table:
		for key in row.keys():
			if key in cluster_dic.keys():
				cluster_dic[key].append(row[key])
			else:
				cluster_dic[key]=[row[key]]
# Remove the cluster id given in the first row:
del cluster_dic['']

for key in cluster_dic.keys():
	c_folder = 'cluster'+str(key)
	c_path = os.path.join(CLASSIF_PATH,c_folder)
	print('Writing folder {}'.format(c_path))
	if not os.path.exists(c_path):
			os.makedirs(c_path)
	for file in cluster_dic[key]:
		if '/' in file: # stop condition in the list (data other than filenames are stored after the string containing '/')
			break
		if len(file)>0:
			filename = os.path.join(PDF_PATH,file+'.pdf')
			new_filename = os.path.join(c_path,file+'.pdf')
			shutil.copy2(filename,new_filename)
print('Classification done.')