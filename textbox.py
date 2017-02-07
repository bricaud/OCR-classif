#!/usr/bin/env python
import os
import glob
import pandas as pd


def extract_text(path):
	""" Extract the text of all txt files in the path,
		and store it in a pandas dataframe.
		Return the dataframe with 2 columns : 
		'filename' (without .txt extension and without the page number) 
		'text'
	"""
	from tqdm import tqdm
	files_to_search = os.path.join(path,'*.txt')
	df = pd.DataFrame()#columns=['index','filename','text'])
	# progress bar to display
	nb_of_texts = len([item for item in glob.glob(files_to_search)])
	pbar = tqdm(total=nb_of_texts)
	for idx,file in enumerate(glob.glob(files_to_search)):
		pbar.update(1)
		path,txtfile = os.path.split(file)
		fname = txtfile[0:-6] # this assumes a one digit page number appended to the name like this: file.1.txt
		with open(file,'r') as text_file:
			text_block = text_file.read()
		df.loc[idx,'filename'] = fname
		df.loc[idx,'text'] = text_block
	pbar.close()
	return df

def merge_pages(df):
	""" Group the texts that belongs to the same pdf file,
		but on different pages.
	"""
	df2 = pd.DataFrame(df.groupby('filename')['text'].apply(lambda x: ' '.join(x)))
	df2['filename']=df2.index
	df2 = df2.reset_index(drop=True)
	return df2

def text_properties(df):
	""" Compute the len of the text in char and in words.
		Split the text into a list of words.
		return the dataframe with the properties recorded
	"""
	df['text_length'] = df['text'].apply(len)
	df = df.sort_values('text_length',ascending=False)
	df['text_list'] = df['text'].apply(text_split)
	df['nb_words'] = df['text_list'].apply(len)
	return df


def text_split(text):
	""" Split a string of text.
	"""
	import re
	text_list = re.split('; |, | |\n+',text)
	return [word for word in text_list if word]

def remove_empty_files(df,threshold=5):
	""" Remove the empty files from the dataframe.
		An empty file is a file where the number of words is
		below the threshold.
		return a dataframe and a list of removed files
	"""
	df_filtered = df[df['nb_words']>threshold]
	removed_files_list = list(df[df['nb_words']<=threshold].index)
	return df_filtered,removed_files_list

def save(df,path):
	df.to_pickle(path)


def auto_extract(texts_path,pickle_file):
	""" Automatically extract the texts from the text files in 'texts_path'
		filter out the empty files
		save the dataframe in the pickle file 'pickle_file' 
	"""
	print('Extracting the texts from {}'.format(texts_path))
	df = extract_text(texts_path)
	print('Extraction done.')
	print('Processing the text...')
	df = merge_pages(df)
	df = text_properties(df)
	df,removed_files_list = remove_empty_files(df,threshold=5)
	# Write removed file to logfile
	logfile = 'extract_log.csv'
	with open(logfile,'w') as log_f:
		log_f.write('List of empty files (no text found).')
		for item in removed_files_list:
  			log_f.write('%s\n' % item)
	print('list of empty files written in {}'.format(logfile))
	print('Saving to file {}'.format(pickle_file))
	save(df,pickle_file)
	print('Saving done.')