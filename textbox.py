#!/usr/bin/env python
import os
import glob
import pickle


def remove_extensions(text_file):
	""" Remove the extensions on 'file.nb.txt' and return 'file'."""
	without_txt_extension,ext = os.path.splitext(text_file)
	without_nb_extension,ext = os.path.splitext(without_txt_extension)
	return without_nb_extension

def find_nb_of_pages(txt_short_filename):
	files_pages = txt_short_filename + '.*.txt'
	print(files_pages)
	return len(glob.glob(files_pages))

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
	# Assuming the file to be made of one digit page number appended to the name like this: file.1.txt:
	set_of_text_files = set([remove_extensions(item) for item in glob.glob(files_to_search)])
	nb_of_texts = len(set_of_text_files)
	# progress bar to display
	pbar = tqdm(total=nb_of_texts)
	for idx,file in enumerate(set_of_text_files):
		pbar.update(1)
		nb_of_pages = find_nb_of_pages(file)
		full_text,error_code = singlepdf_extract_text(file,nb_of_pages)
		
		path,fname = os.path.split(file)
		data_dic[fname] = {}
		data_dic[fname]['text'] = full_text
		data_dic[fname]['error'] = error_code
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

################################################
### New version using database

def singlepdf_extract_text(txt_short_filename,nb_of_pages):
	""" Extract the text of all txt files (one per page) associated to a pdf file,
		and return a string containing the text. It also return an error code (0 if no error in the process).

		>> full_text,error_code = singlepdf_extract_text(txt_short_filename,nb_of_pages)

	"""
	full_text = ''
	error_code = 0	
	for idx in range(nb_of_pages):
		# name of the text file for each page
		page_nb = idx+1
		file = txt_short_filename + '.' + str(page_nb) + '.' + 'txt'
		with open(file,'r', encoding='utf-8', errors='replace') as text_file:
			try:
				text_block = text_file.read()
			except:
				error_code = 1
				text_block = ''
				raise ValueError('Failed to read {}'.format(file))
		full_text = full_text + ' ' + text_block
	return full_text,error_code

def flag_empty_text(text,min_nb_of_chars=5):
	""" detect the empty text
		An empty file is a file where the number of chars is
		below the threshold (default=5).
		return a boolean
	"""
	empty = False
	if len(text)<min_nb_of_chars:
		empty = True
	return empty
