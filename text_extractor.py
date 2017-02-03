#!/usr/bin/env python
""" Extract the texts from files in the specified path and save them in pickle file (dataframe).
"""
import textbox
TXT_PATH = '/media/benjamin/Elements/pdfs/txt'
PICKLE_FILE = './texts3.pkl'
textbox.auto_extract(TXT_PATH,PICKLE_FILE)
