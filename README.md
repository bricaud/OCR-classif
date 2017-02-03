# OCR-classif

Set of Python programs to extract text from pdfs.
It requires the installation of 
* [Ghostscript](https://www.ghostscript.com/), for converting the pdf to one or several png files (one per page)
* [Tesseract](https://github.com/tesseract-ocr/tesseract), an open source OCR software to extract the text from the png files. 

The convertion is done by calling:
```
python3 pdf2txt.py
```
The path where are stored the pdf files must be specified inside the python file.

The text can then be extracted from all the txt files and stored in a pandas dataframe and saved in a pickle file:
```
python3 text_extractor.py
```
This program relies on the toolbox *textbox.py*.