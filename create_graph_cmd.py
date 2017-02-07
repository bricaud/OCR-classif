#!/usr/bin/env python
""" Create the graph from the texts in pickle file (dataframe).
"""
import txt2graph
import argparse
import os
import sys

parser = argparse.ArgumentParser(description='Create the graph from the texts in pickle file (dataframe).')
parser.add_argument('folder',
                   help='folder where the pdf files are stored')
parser.add_argument('grevia_folder',
                   help='folder where the Grevia module is stored')

args = parser.parse_args()
input_dic = vars(args)
PICKLE_PATH = os.path.join(input_dic['folder'],'pickle')
print('Pickle path: ',PICKLE_PATH)
print('Grevia module path: ',input_dic['grevia_folder'])

#PICKLE_PATH = os.path.join(input_dic['folder'],'pickle')
PICKLE_FILE = os.path.join(PICKLE_PATH,'texts3.pkl')
GRAPH_NAME = os.path.join(PICKLE_PATH,'graph.pkl')
GREVIA_PATH = input_dic['grevia_folder']
#GREVIA_PATH = '/home/benjamin/Documents/eviacybernetics/Projets/Grevia'
sys.path.append(GREVIA_PATH)
txt2graph.run(PICKLE_FILE,GRAPH_NAME,GREVIA_PATH)
txt2graph.doc_classif(GRAPH_NAME,PICKLE_FILE,GREVIA_PATH,'filename_table.csv')
