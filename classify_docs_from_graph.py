#!/usr/bin/env python
""" Classify the documents using the graph and the texts in pickle file (dataframe).
"""
import txt2graph
import argparse
import os
import sys

parser = argparse.ArgumentParser(description='Create the graph from the texts in pickle file (dataframe).')
parser.add_argument('folder',
                   help='folder where the pdf files are stored')
parser.add_argument('csv_file',
                   help='csv file to store the classification results')

args = parser.parse_args()
input_dic = vars(args)
PDF_PATH = input_dic['folder']
PICKLE_PATH = os.path.join(PDF_PATH,'pickle')
CSV_FILE = input_dic['csv_file']
print('Pickle path: ',PICKLE_PATH)

#PICKLE_PATH = os.path.join(input_dic['folder'],'pickle')
PICKLE_FILE = os.path.join(PICKLE_PATH,'texts2.pkl')
GRAPH_NAME = os.path.join(PICKLE_PATH,'graph.pkl')


CSV_PATH = os.path.join(PDF_PATH,'csv')
if not os.path.exists(CSV_PATH):
    os.makedirs(CSV_PATH)
csv_filename = os.path.join(CSV_PATH,CSV_FILE)
txt2graph.doc_classif(GRAPH_NAME,PICKLE_FILE,csv_filename)
print('CSV file saved in {}'.format(csv_filename))
