#!/usr/bin/env python
""" Create the graph from the texts in pickle file (dataframe).
"""
import txt2graph
import argparse
import os
import sys
import textbox

parser = argparse.ArgumentParser(description='Create the graph from the texts in pickle file (dataframe).')
parser.add_argument('folder',
                   help='folder where the pdf files are stored')
parser.add_argument('csv_file',
                   help='csv file to store the classification results')

args = parser.parse_args()
input_dic = vars(args)
PDF_PATH = input_dic['folder']
TXT_PATH = os.path.join(PDF_PATH,'txt')
PICKLE_PATH = os.path.join(PDF_PATH,'pickle')
if not os.path.exists(PICKLE_PATH):
    os.makedirs(PICKLE_PATH)
CSV_FILE = input_dic['csv_file']
print('Pickle path: ',PICKLE_PATH)

#PICKLE_PATH = os.path.join(input_dic['folder'],'pickle')
PICKLE_FILE = os.path.join(PICKLE_PATH,'texts.pkl')
GRAPH_NAME = os.path.join(PICKLE_PATH,'graph.pkl')

# Extract the text from the txt files and save them in a pickle file
textbox.auto_extract(TXT_PATH,PICKLE_FILE)


# Create the graph from the pickle file
txt2graph.run(PICKLE_FILE,GRAPH_NAME,min_weight=10,max_iter=20000)
print('Graph saved in file {}'.format(GRAPH_NAME))
