#!/usr/bin/env python
import tkinter as tk
import tkinter.filedialog as tkd
import shlex,subprocess
import sys
import platform
import txt2graph

process_handle = None
filepath = None
grevia_path = None

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
	if platform.system() == 'Windows':
		cmd_pdf2txt = 'cmd /K python3 pdf2txt.py '+filepath
		#cmd_pdf2txt = 'cmd /C python3 pdf2txt.py '+filepath
	else:
		cmd_pdf2txt = 'xterm -e python3 pdf2txt.py '+filepath
	try:
		textbox.insert('end','Running pdf2txt...\n')
		print('Running pdf2txt..Please wait.')
		proc_results = subprocess.run(shlex.split(cmd_pdf2txt), stdout=subprocess.PIPE)
		textbox.insert('end','pdf2txt: process finished.\n')
		textbox.insert('end','Now: run text_extractor.\n')
	except:
		print('Error while calling pdf2txt.')


def run_text_extractor():
	if platform.system() == 'Windows':
		cmd_pdf2txt = 'cmd /K python3 text_extractor.py '+filepath
	else:
		cmd_pdf2txt = 'xterm -e python3 text_extractor.py '+filepath
	try:
		textbox.insert('end','Running text_extractor...\n')
		print('Running text_extractor...Please wait.')
		proc_results = subprocess.run(shlex.split(cmd_pdf2txt), stdout=subprocess.PIPE)
	except:
		print('Error while calling text_extractor.')

def run_build_graph():
	global filepath
	global grevia_path
	if platform.system() == 'Windows':
		cmd = 'cmd /K python3 create_graph_cmd.py '+filepath + ' ' + grevia_path
	else:
		cmd = 'xterm -e python3 create_graph_cmd.py '+filepath + ' ' + grevia_path
		#cmd = 'xterm -hold -e python3 create_graph_cmd.py '+filepath + ' ' + grevia_path
	try:
		textbox.insert('end','Building the graph...\n')
		print('Building the graph...Please wait.')
		proc_results = subprocess.run(shlex.split(cmd), stdout=subprocess.PIPE)
		textbox.insert('end','Graph and classification done.\n')
		textbox.insert('end','Check the csv file.\n')
		textbox.insert('end','Thank you.\n')
	except:
		print('Error while calling create_graph_cmd.')	

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
	"3 - run text_extractor," +
	"4 - Select the folder where Grevia is installed," +
	"5 - Build the graph.")
tk.Label(labelf,text=text_procedure).pack()
bouton_dir = tk.Button(fenetre, text="Choose the pdf files folder", command=ask_path)
bouton_dir.pack()
tk.Button(fenetre, text="Run pdf2txt", command=lambda : run_pdf2txt(filepath)).pack()
tk.Button(fenetre, text="Run text_extractor", command=run_text_extractor).pack()
tk.Button(fenetre, text="Choose Grevia folder", command=ask_grevia_path).pack()
tk.Button(fenetre, text="Build the graph", command=run_build_graph).pack()
bouton_close = tk.Button(fenetre, text="Close", command=fenetre.quit)
bouton_close.pack()
textbox = tk.Text(fenetre)
textbox.pack()
textbox.insert('1.0','Select the directory where the pdfs are stored\n')



fenetre.mainloop()