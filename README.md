# OCR-classif

Set of Python programs to extract text from pdfs.
It requires the installation of 
* [Ghostscript](https://www.ghostscript.com/), for converting the pdf to one or several png files (one per page)
* [Tesseract](https://github.com/tesseract-ocr/tesseract), an open source OCR software to extract the text from the png files. 

You also need the following modules:
- networkx (pip install networkx) . A graph processing toolbox.
- [tqdm](https://github.com/noamraph/tqdm) (pip install tqdm). A progress bar for Python.

The extraction is done by calling:
```
python3 pdf2txt.py
```
The path where the pdf files are stored must be specified inside the python file.

The texts can then be extracted from all the txt files, stored in dictionaries data structures and saved in a single pickle file:
```
python3 text_extractor.py
```
This program relies on the toolbox *textbox.py*. The path of the txt file and the name of the pickle file must be specified within the python script.

The projet [Grevia](https://github.com/bricaud/Grevia) can then be used to analyze the texts.