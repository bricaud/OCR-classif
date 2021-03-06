#!/usr/bin/env python3
""" Program that convert a pdf to a text file using Tesseract OCR.

	The pdf file is first converted to a png file using ghostscript,
	then the png file if processed by Tesseract.

"""
import os
import subprocess
import glob
import platform
import argparse

parser = argparse.ArgumentParser(description='Convert pdf files to txt files in the given folder.')
parser.add_argument('folder',
                   help='folder where the pdf files are stored')

args = parser.parse_args()
input_dic = vars(args)
print('Selected pdf folder: ',input_dic['folder'])
PDF_PATH = input_dic['folder'] 
#PDF_PATH = '/media/benjamin/Elements/pdfs/'

def png_to_txt(pngpath,short_name,txtpath,log_file):
	""" Extract the text from a set of png files.

	The png files associated to a single pdf file are numbered according to the page,
	they share the same short_name.

	"""
	png_in = os.path.join(pngpath,short_name)
	# Iterate over the pages of the document (different png files)
	for pngfile in glob.glob(png_in+'*'):
		path,filename = os.path.split(pngfile)
		txtfile = filename[0:-4] #+'.txt'
		txt_out = os.path.join(txtpath,txtfile)
		try:
			cmd_png2txt = 'tesseract '+ pngfile +' '+txt_out+ ' -l fra+eng'
			proc_results = subprocess.run(cmd_png2txt.split(), stdout=subprocess.PIPE,timeout=60)
			if proc_results.returncode:
				print('Error encountered with file: {}\n'.format(filename))
				with open(log_file, 'a') as logfile:
					logfile.write('Error with file: {}\n'.format(filename))  # report errors
			else:
				print('Text extracted form file: {}'.format(filename))
		except:
			print('error extracting text with file {}'.format(filename))
			with open(log_file, 'a') as logfile:
				logfile.write('Error with file (exception raised): {}\n'.format(filename))  # report errors


def pdf_to_png(pdf_file,short_name,png_path,page_limit=4):
	""" Convert the pdf to png, each page of the pdf gives a different png file."""
	out_name = short_name+'.%d.png'
	out_file = os.path.join(png_path,out_name)
	if platform.system() == 'Windows':
		cmd_pdf2png = ('gswin32c -dSAFER -dNOPAUSE -q -r300x300 -sDEVICE=pnggray -dBATCH -dLastPage=' + str(page_limit) + 
		' -sOutputFile=' + out_file + ' ' + pdf_file)
	else:
		cmd_pdf2png = ('gs -dSAFER -dNOPAUSE -q -r300x300 -sDEVICE=pnggray -dBATCH -dLastPage=' + str(page_limit) + 
		' -sOutputFile=' + out_file + ' ' + pdf_file)
	proc_results = subprocess.run(cmd_pdf2png.split(), stdout=subprocess.PIPE,timeout=60)
	return proc_results

#PDF_PATH = '/media/benjamin/Elements/pdfs/'
LOG_FILE1 = 'logfile_pdf2png.txt'
LOG_FILE2 = 'logfile_png2txt.txt'

# initiate log file to report errors
with open(LOG_FILE1, 'a') as logfile:
				logfile.write('Logfile produced by pdf2txt.py\n')  
with open(LOG_FILE2, 'a') as logfile:
				logfile.write('Logfile produced by pdf2txt.py\n') 

# init paths
png_path = os.path.join(PDF_PATH,'png')
txt_path = os.path.join(PDF_PATH,'txt')
if not os.path.exists(png_path):
    os.makedirs(png_path)
if not os.path.exists(txt_path):
    os.makedirs(txt_path)   

# Loop over all the file in the pdf folder
nb_files = len(list(glob.glob(os.path.join(PDF_PATH,'*.pdf'))))		
for idx,pdf_file in enumerate(glob.glob(os.path.join(PDF_PATH,'*.pdf'))):
	pdf_path,filename = os.path.split(pdf_file)
	print('processing {}. File {}/{}.'.format(filename,idx+1,nb_files))
	short_name = filename[0:-4]
	
	try:
		proc_results = pdf_to_png(pdf_file,short_name,png_path,page_limit=4)
		if proc_results.returncode:
			print('Error encountered with file: {}\n'.format(filename))
			with open(LOG_FILE1, 'a') as logfile:
				logfile.write('Error with file: {}\n'.format(filename))  # report errors
		else:
			png_to_txt(png_path,short_name,txt_path,LOG_FILE2)
	except subprocess.TimeoutExpired:
		print('!!!!!! Timed out for file {} !!!!!!'.format(filename))
		with open(LOG_FILE1, 'a') as logfile:
				logfile.write('Timed out with file: {}\n'.format(filename))  # report time out
