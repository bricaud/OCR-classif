#!/usr/bin/env python
import tkinter as tk
import tkinter.filedialog as tkd
import shlex,subprocess
import sys
import platform

process_handle = None
filepath = None

def ask_path():
	global filepath
	filepath = tkd.askdirectory(title="Directory for pdf files")#,filetypes=[('png files','.png'),('all files','.*')])
	textbox.insert('end','Directory selected: '+filepath+'\n')
	textbox.insert('end','Now: run pdf2txt.\n')
	return filepath

def run_pdf2txt(filepath):
	if platform.system() == 'Windows':
		cmd_pdf2txt = 'cmd /K python3 pdf2txt.py '+filepath
	else:
		cmd_pdf2txt = 'xterm -hold -e python3 pdf2txt.py '+filepath
	try:
		print('Running pdf2txt...')
		print('Please wait.')
		proc_results = subprocess.run(shlex.split(cmd_pdf2txt), stdout=subprocess.PIPE)
		textbox.insert('pdf2txt: process finished.\n')
		textbox.insert('end','Now: run text_extractor.\n')
	except:
		print('Error while calling pdf2txt.')


def run_text_extractor():
	if platform.system() == 'Windows':
		cmd_pdf2txt = 'cmd /K python3 text_extractor.py '+filepath
	else:
		cmd_pdf2txt = 'xterm -hold -e python3 text_extractor.py '+filepath
	try:
		print('Running text_extractor...')
		print('Please wait.')
		proc_results = subprocess.run(shlex.split(cmd_pdf2txt), stdout=subprocess.PIPE)
	except:
		print('Error while calling text_extractor.')


# Decorator to write the output of the function inside the textbox of the GUI
def decorator(func):
	def inner(inputStr):
		try:
			textbox.insert('insert', inputStr)
			return func(inputStr)
		except:
			return func(inputStr)
	return inner

sys.stdout.write=decorator(sys.stdout.write)

# Window configuration
fenetre = tk.Tk()

labelf = tk.LabelFrame(fenetre, text="Evia Software", padx=50, pady=50)
labelf.pack(fill="both", expand="yes")
text_procedure = ("Welcome to Evia\n" +
	"How to proceed:\n" +
	"1 - choose the directory where the pdfs are located,\n" + 
	"2 - run pdf2txt,\n" +
	"3 - run text_extractor.")
tk.Label(labelf,text=text_procedure).pack()
bouton_dir = tk.Button(fenetre, text="Choose folder", command=ask_path)
bouton_dir.pack()
tk.Button(fenetre, text="Run pdf2txt", command=lambda : run_pdf2txt(filepath)).pack()
tk.Button(fenetre, text="Run text_extractor", command=run_text_extractor).pack()
bouton_close = tk.Button(fenetre, text="Close", command=fenetre.quit)
bouton_close.pack()
textbox = tk.Text(fenetre)
textbox.pack()
textbox.insert('1.0','Select the directory where the pdfs are stored\n')



fenetre.mainloop()