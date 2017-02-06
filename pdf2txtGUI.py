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
	textbox.insert('end',filepath)
	return filepath

def run_pdf2txt(filepath):
	if platform.system() == 'Windows':
		cmd_pdf2txt = 'cmd /K python3 pdf2txt.py '+filepath
	else:
		cmd_pdf2txt = 'xterm -hold -e python3 pdf2txt.py '+filepath
	try:
		#print(shlex.split(cmd_pdf2txt))
		#process_handle = subprocess.Popen(cmd_pdf2txt, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		#p = subprocess.Popen("exec " + cmd, stdout=subprocess.PIPE, shell=True)
		print('Running pdf2txt...')
		print('Please wait.')
		proc_results = subprocess.run(shlex.split(cmd_pdf2txt), stdout=subprocess.PIPE)

		#print('Process pid: {}'.format(process_handle.pid))
	except:
		print('Error while calling pdf2txt.')

	#while process_handle.poll() is None:
	#	out = process_handle.stdout.read(1)
	#	sys.stdout.write(out.decode('utf-8'))
	#	sys.stdout.flush()


def stop_pdf2txt():
	if process_handle is not None:
		process_handle.terminate()
		print('Terminate signal sent to pdf2txt.')

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

fenetre = tk.Tk()

label = tk.Label(fenetre, text="Hello World", padx=50, pady=50)
label.pack()
bouton = tk.Button(fenetre, text="Fermer", command=fenetre.quit)
bouton.pack()
bouton2 = tk.Button(fenetre, text="Choose folder", command=ask_path)
bouton2.pack()
bouton_run = tk.Button(fenetre, text="Run pdf2txt", command=lambda : run_pdf2txt(filepath))
bouton_run.pack()
bouton_stop = tk.Button(fenetre, text="Stop pdf2txt", command=stop_pdf2txt)
bouton_stop.pack()
textbox = tk.Text(fenetre)
textbox.pack()
textbox.insert('1.0','Choose a path\n')
textbox.insert('insert',' test \n')



fenetre.mainloop()