#!/usr/bin/env python
import os
import glob
import pickle


def extract_text(path):
	""" Extract the text of all txt files in the path,
		and store it in a dictionary.
		Return the dic with the structure:
		key : 'filename' (without .txt extension and without the page number) 
		value : 'text'
	"""
	from tqdm import tqdm
	files_to_search = os.path.join(path,'*.txt')
	data_dic = {}# key:filename',value:'text'
	data_index = {}
	# progress bar to display
	nb_of_texts = len([item for item in glob.glob(files_to_search)])
	pbar = tqdm(total=nb_of_texts)
	for idx,file in enumerate(glob.glob(files_to_search)):
		pbar.update(1)
		path,txtfile = os.path.split(file)
		fname = txtfile[0:-6] # this assumes a one digit page number appended to the name like this: file.1.txt
		#print(txtfile)
		#print(file)
		with open(file,'r', encoding='utf-8', errors='replace') as text_file:
			try:
				text_block = text_file.read()
			except:
				raise ValueError('Failed to read {}'.format(file))
		if fname in data_dic.keys():
			data_dic[fname]['text'] = data_dic[fname]['text'] + ' ' + text_block
		else:
			data_dic[fname] = {}
			data_dic[fname]['text'] = text_block
			data_dic[fname]['id'] = idx
			data_index[idx] = fname
	pbar.close()
	return data_dic,data_index


def text_split(text):
	""" Split a string of text.
	"""
	import re
	text_list = re.split('; |, | |\n+',text)
	return [word for word in text_list if word]

def remove_empty_files(data_dic,threshold=5):
	""" Remove the empty files from dict.
		An empty file is a file where the number of chars is
		below the threshold.
		return a dict and a list of removed files
	"""
	removed_files_list = [file for file in data_dic.keys() if len(data_dic[file]['text'])<=threshold ]
	for file in removed_files_list:
		del data_dic[file]
	return data_dic,removed_files_list

def save(data,path):
	with open(path, 'wb') as handle:
		pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

def auto_extract(texts_path,pickle_file,log_path):
	""" Automatically extract the texts from the text files in 'texts_path'
		filter out the empty files
		save the dict of data and index in the pickle file 'pickle_file' 
	"""
	print('Extracting the texts from {}'.format(texts_path))
	data_dic,data_index = extract_text(texts_path)
	print('Extraction done.')
	print('Processing the text...')
	data_dic,removed_files_list = remove_empty_files(data_dic,threshold=5)
	# Write removed file to logfile
	logfile = os.path.join(log_path,'text_extraction_log.csv')
	with open(logfile,'w') as log_f:
		log_f.write('List of empty files (no text found).')
		for item in removed_files_list:
			log_f.write('%s\n' % item)
	print('list of empty files written in {}'.format(logfile))
	print('Saving to file {}'.format(pickle_file))
	save([data_dic,data_index],pickle_file)
	print('Saving done.')