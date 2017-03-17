#!/usr/bin/env python3
""" Module that convert a pdf to a text file using Tesseract OCR.

	The pdf file is first converted to a png file using ghostscript,
	then the png file if processed by Tesseract.

"""
import os
import subprocess
import glob
import pickle


def png_to_txt(pngpath,short_name,txtpath,log_file,file_data):
	""" Extract the text from a set of png files.

	The png files associated to a single pdf file are numbered according to the page,
	they share the same short_name.

	"""
	png_in = os.path.join(pngpath,short_name)
	# Each page of the document is a different png file
	list_of_pages = glob.glob(png_in+'*')
	file_data[short_name]['nb_pages'] = len(list_of_pages)
	# Extract the text in all the pages
	for pngfile in list_of_pages:
		path,filename = os.path.split(pngfile)
		txtfile = filename[0:-4] #+'.txt'
		txt_out = os.path.join(txtpath,txtfile)
		# Check if the file has already been processed
		if os.path.isfile(txt_out+'.txt'):
			print('Text file {} exists. Skipping the extraction.'.format(txt_out))
			continue
		try:
			cmd_png2txt = (['tesseract', pngfile, 
				txt_out, '-l fra+eng'])
			proc_results = subprocess.run(cmd_png2txt, stdout=subprocess.PIPE,timeout=60)
			if proc_results.returncode:
				report_and_log(short_name,log_file,file_data,'pngerror')
			else:
				print('Text extracted form file: {}'.format(filename))
		except:
			report_and_log(short_name,log_file,file_data,'pngexcepterror')
	return file_data

def pdf_to_png(pdf_file,short_name,png_path,page_limit=4):
	import re
	""" Convert the pdf to png, each page of the pdf gives a different png file."""
	out_name = short_name+'.%d.png'
	out_file = os.path.join(png_path,out_name)
	#Check if the file has already been processed
	out_file1 =os.path.join(png_path,short_name+'.1.png')
	if os.path.isfile(out_file1):
		print(' {} already computed'.format(out_file1))
		return 0
	inputstr = pdf_file
	outputstr = '-sOutputFile=' +out_file
	cmd_pdf2png = (["gs","-dSAFER","-dNOPAUSE", "-q", "-r300x300", "-sDEVICE=pnggray", "-dBATCH",
		"-dLastPage=" + str(page_limit), 
		outputstr.encode('unicode-escape'),
		inputstr.encode('unicode-escape')])
	proc_results = subprocess.run(cmd_pdf2png, stdout=subprocess.PIPE,timeout=60)
	return proc_results.returncode

def pdf2txt(PDF_PATH,PNG_PATH,TXT_PATH,LOGS_PATH,EX_TXT_PICKLE):
	""" Convert pdfs in the PDF_PATH to txt files"""
	# Init
	# initiate log file to report errors
	LOG_FILE1 = os.path.join(LOGS_PATH,'logfile_pdf2png.txt')
	LOG_FILE2 = os.path.join(LOGS_PATH,'logfile_png2txt.txt')

	with open(LOG_FILE1, 'a') as logfile:
					logfile.write('Logfile produced by pdf2txt.py\n')  
	with open(LOG_FILE2, 'a') as logfile:
					logfile.write('Logfile produced by pdf2txt.py\n') 

	# Loop over all the files in the PDF_PATH folder and subfolders
	print('Listing all the pdf files...')
	pdf_files_list = list(glob.glob(os.path.join(PDF_PATH,'**/*.pdf'), recursive=True))
	nb_files = len(pdf_files_list)
	print('{} pdf files found in the given directory and subdirectories.'.format(nb_files))
	nb_errors = 0
	nb_timeout = 0
	file_data = {} # info on files	
	for idx,pdf_file in enumerate(pdf_files_list):
		pdf_path,filename = os.path.split(pdf_file)
		# keeping the relative path
		rel_path =os.path.relpath(pdf_path,PDF_PATH)
		print('processing {}. File {}/{}.'.format(filename,idx+1,nb_files))
		short_name = filename[0:-4]
		file_data[short_name] = {}
		file_data[short_name]['path'] = rel_path
		file_data[short_name]['error'] = 0
		try:
			proc_results = pdf_to_png(pdf_file,short_name,PNG_PATH,page_limit=4)
			if proc_results:
				report_and_log(short_name,LOG_FILE1,file_data,'error')
				nb_errors+=1
			else:
				file_data = png_to_txt(PNG_PATH,short_name,TXT_PATH,LOG_FILE2,file_data)
		except subprocess.TimeoutExpired:
			report_and_log(short_name,LOG_FILE1,file_data,'timeout')
			nb_timeout += 1
	# Save infos on files in a pickle file
	save(file_data,EX_TXT_PICKLE)
	message = ' Total: {} files processed. Nb of errors : {} and Timeouts : {}.'.format(nb_files,nb_errors,nb_timeout)
	return message

def save(data,path):
	with open(path, 'wb') as handle:
		pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)


def report_and_log(filename,log_file,file_data,error_code):
	if error_code is 'timeout': # report time out
		print('!!!!!! Timed out for file {} !!!!!!'.format(filename))
		file_data[filename]['error'] = 1
		with open(log_file, 'a') as logfile:
			logfile.write('Timed out with file: {}\n'.format(filename))

	elif error_code is 'pngerror': # report png errors
		print('Error encountered with file: {}\n'.format(filename))
		file_data[filename]['error'] = 2
		with open(log_file, 'a') as logfile:
			logfile.write('Error with png file : {}\n'.format(filename)) 

	elif error_code is 'pngexcepterror': # report exception errors
		print('Error encountered with png file: {}\n'.format(filename))
		file_data[filename]['error'] = 3
		with open(log_file, 'a') as logfile:
			logfile.write('Error with file (exception raised): {}\n'.format(filename))

	else: # report other errors
		print('Error encountered with file: {}\n'.format(filename))
		file_data[filename]['error'] = 4
		with open(log_file, 'a') as logfile:
			logfile.write('Error with file: {}\n'.format(filename)) 