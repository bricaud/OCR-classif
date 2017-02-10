#!/usr/bin/env python
import tkinter as tk
import tkinter.filedialog as tkd
import shlex,subprocess
import sys
import platform
import txt2graph
import os

process_handle = None
filepath = None
grevia_path = None
csv_file = 'table_classif.csv'

def ask_path():
	global filepath
	filepath = tkd.askdirectory(title="Directory for pdf files")#,filetypes=[('png files','.png'),('all files','.*')])
	textbox.insert('end','Directory selected: '+filepath+'\n')
	textbox.insert('end','Now: run pdf2txt.\n')
	return filepath

def ask_grevia_path():
	global grevia_path
	grevia_path = tkd.askdirectory(title="Directory for the Grevia module")#,filetypes=[('png files','.png'),('all files','.*')])
	textbox.insert('end','Directory selected: '+grevia_path+'\n')
	textbox.insert('end','Now: build the graph.\n')
	return grevia_path

def run_pdf2txt(filepath):
	textbox.insert('end','Running pdf2txt...\n')
	print('Running pdf2txt..Please wait.')
	if platform.system() == 'Windows':
		cmd_pdf2txt = 'start cmd.exe /K python pdf2txt.py '+filepath
		try:
			proc_results = subprocess.run(shlex.split(cmd_pdf2txt), shell=True, stdout=subprocess.PIPE)
		except:
			print('Error while calling pdf2txt with {}'.format(cmd_pdf2txt))
	else:
		cmd_pdf2txt = 'xterm -e python3 pdf2txt.py '+filepath
		try:
			proc_results = subprocess.run(shlex.split(cmd_pdf2txt), stdout=subprocess.PIPE)
		except:
			print('Error while calling pdf2txt with {}'.format(cmd_pdf2txt))
	textbox.insert('end','pdf2txt: process finished. Please close the window.\n')
	textbox.insert('end','Now: run text_extractor.\n')


def run_text_extractor():
	textbox.insert('end','Running text_extractor...\n')
	print('Running text_extractor...Please wait.')
	if platform.system() == 'Windows':
		cmd_pdf2txt = 'start cmd.exe /K python text_extractor.py '+filepath
		try:
			proc_results = subprocess.run(cmd_pdf2txt, shell=True, stdout=subprocess.PIPE)
		except:
			print('Error while calling text_extractor with {}'.format(cmd_pdf2txt))
	else:
		cmd_pdf2txt = 'xterm -e python3 text_extractor.py '+filepath
		try:
			proc_results = subprocess.run(shlex.split(cmd_pdf2txt), stdout=subprocess.PIPE)
			#proc_results = subprocess.run(cmd_pdf2txt, stdout=subprocess.PIPE)
		except:
			print('Error while calling text_extractor with {}'.format(cmd_pdf2txt))
	print('text_extractor finished.')
	textbox.insert('end','Text_extractor: process finished. Please close the window.\n')
	textbox.insert('end','Now: select the Grevia folder.\n')

def run_build_graph():
	global filepath
	global grevia_path
	global csv_file
	textbox.insert('end','Building the graph...\n')
	print('Building the graph...Please wait.')
	if platform.system() == 'Windows':
		cmd = 'start cmd.exe /K python create_graph_cmd.py '+filepath + ' ' + grevia_path + ' ' + csv_file
		try:
			print('Running {} ...'.format(cmd))
			proc_results = subprocess.run(shlex.split(cmd), shell=True, stdout=subprocess.PIPE)
		except:
			print('Error while calling create_graph_cmd with: {}'.format(cmd))	
	else:
		cmd = 'xterm -hold -e python3 create_graph_cmd.py '+filepath + ' ' + grevia_path + ' ' + csv_file
		#cmd = 'xterm -hold -e python3 create_graph_cmd.py '+filepath + ' ' + grevia_path
		try:
			print('Running {} ...'.format(cmd))
			proc_results = subprocess.run(shlex.split(cmd), stdout=subprocess.PIPE)
		except:
			print('Error while calling create_graph_cmd with: {}'.format(cmd))
	print('Graph done. Please close the window.')	
	textbox.insert('end','Graph done. Please close the window.\n')
	textbox.insert('end','Thank you.\n')

def classify_docs():
	global filepath
	global grevia_path
	global csv_file
	textbox.insert('end','Building the graph...\n')
	print('Building the graph...Please wait.')
	if platform.system() == 'Windows':
		cmd = 'start cmd.exe /K python classify_docs_from_graph.py '+filepath + ' ' + grevia_path + ' ' + csv_file
		try:
			print('Running {} ...'.format(cmd))
			proc_results = subprocess.run(shlex.split(cmd), shell=True, stdout=subprocess.PIPE)
		except:
			print('Error while calling {}'.format(cmd))	
	else:
		cmd = 'xterm -hold -e python3 classify_docs_from_graph.py '+filepath + ' ' + grevia_path + ' ' + csv_file
		#cmd = 'xterm -hold -e python3 create_graph_cmd.py '+filepath + ' ' + grevia_path
		try:
			print('Running {} ...'.format(cmd))
			proc_results = subprocess.run(shlex.split(cmd), stdout=subprocess.PIPE)
		except:
			print('Error while calling {}'.format(cmd))
	print('Graph and classification done. Please close the window.')	
	textbox.insert('end','Classification done. Please close the window.\n')
	textbox.insert('end','Check the csv file.\n')
	textbox.insert('end','Thank you.\n')

def sort_pdf_in_folders():
	global filepath
	global csv_file
	target_folder = os.path.join(filepath,'classif')
	csv_path = os.path.join(filepath,'csv')
	csv_full_name = os.path.join(csv_path,csv_file)

	textbox.insert('end','Sorting the pdfs from the csv file...\n')
	print('Sorting the pdfs...Please wait.')
	if platform.system() == 'Windows':
		cmd = 'start cmd.exe /K python csv2folders.py '+filepath + ' ' + csv_full_name + ' ' + target_folder
		try:
			print('Running {} ...'.format(cmd))
			proc_results = subprocess.run(shlex.split(cmd), shell=True, stdout=subprocess.PIPE)
		except:
			print('Error while calling csv2folders with: {}'.format(cmd))	
	else:
		cmd = 'xterm -hold -e python3 csv2folders.py '+filepath + ' ' + csv_full_name + ' ' + target_folder
		#cmd = 'xterm -hold -e python3 create_graph_cmd.py '+filepath + ' ' + grevia_path
		try:
			print('Running {} ...'.format(cmd))
			proc_results = subprocess.run(shlex.split(cmd), stdout=subprocess.PIPE)
		except:
			print('Error while calling {}'.format(cmd))
	print('File classification done. Please close the window.')	
	textbox.insert('end','File classification done. Please close the window.\n')
	textbox.insert('end','Check the folder {}\n'.format(classif_path))


# Decorator to write the output of the function inside the textbox of the GUI
def decorator(func):
	def inner(inputStr):
		try:
			textbox.insert('end', inputStr)
			return func(inputStr)
		except:
			return func(inputStr)
	return inner

sys.stdout.write=decorator(sys.stdout.write)

# Window configuration
fenetre = tk.Tk()

labelf = tk.LabelFrame(fenetre, text="Evia Software", padx=50, pady=50)
labelf.pack(fill="both", expand="yes")
text_procedure = ("Welcome to Evia!\n" +
	"How to proceed:\n" +
	"1 - choose the directory where the pdfs are located,\n" + 
	"2 - run pdf2txt,\n" +
	"3 - run text_extractor,\n" +
	"4 - Select the folder where Grevia is installed,\n" +
	"5 - Build the graph.")
tk.Label(labelf,text=text_procedure, anchor='e').pack()
bouton_dir = tk.Button(fenetre, text="Choose the pdf files folder", command=ask_path)
bouton_dir.pack()
tk.Button(fenetre, text="Run pdf2txt", command=lambda : run_pdf2txt(filepath)).pack()
tk.Button(fenetre, text="Run text_extractor", command=run_text_extractor).pack()
tk.Button(fenetre, text="Choose Grevia folder", command=ask_grevia_path).pack()
tk.Button(fenetre, text="Build the graph", command=run_build_graph).pack()
tk.Button(fenetre, text="Classify documents", command=classify_docs).pack()
tk.Button(fenetre, text="Classify pdfs in folders", command=sort_pdf_in_folders).pack()
bouton_close = tk.Button(fenetre, text="Close", command=fenetre.quit)
bouton_close.pack()
textbox = tk.Text(fenetre)
textbox.pack()
textbox.insert('1.0','Select the directory where the pdfs are stored\n')



fenetre.mainloop()