#!/usr/bin/env python
""" Extract the texts from files in the specified path and save them in pickle file (dataframe).
"""
import textbox
import argparse
import os

parser = argparse.ArgumentParser(description='Extract the texts from files in the specified path and save them in pickle file (dataframe).')
parser.add_argument('folder',
                   help='folder where the pdf files are stored')

args = parser.parse_args()
input_dic = vars(args)
print(input_dic)
TXT_PATH = os.path.join(input_dic['folder'],'txt')
#TXT_PATH = '/media/benjamin/Elements/pdfs/txt'
PICKLE_PATH = os.path.join(input_dic['folder'],'pickle')
if not os.path.exists(PICKLE_PATH):
    os.makedirs(PICKLE_PATH)
PICKLE_FILE = os.path.join(PICKLE_PATH,'texts3.pkl')
textbox.auto_extract(TXT_PATH,PICKLE_FILE)
