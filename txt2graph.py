#!/usr/bin/env python3
""" Module to create the graph from the texts in pickle file (dataframe),
and to classify the documents from the graph.
"""
import sys
import re
import networkx as nx
import tqdm
import pickle
import os
grevia_path = '../grevia'
sys.path.append(grevia_path)
import grevia

def read_file(filename):
	""" Read the pickle filename and return a list with 2 elements:
		the dict of texts and the document index.
	"""
	with open(filename, 'rb') as handle:
   		unserialized_data = pickle.load(handle)
	return unserialized_data

def get_document_and_text(data_dic,data_index,document_id):
	""" return the document name and its text from its id and the output of read_file
	"""
	document_name = data_index[int(document_id)]
	return document_name,data_dic[document_name]['text']

def get_surrounding_text(doc_text,position,nb_words=10):
	text_list = filter_text(doc_text)
	start = max(0,position-nb_words)
	if position+nb_words>len(doc_text)-1:
		return " ".join(text_list[start:])
	else:
		return " ".join(text_list[start:position+nb_words])


def filter_text(text):
	""" filter the text: apply lower case and keep letters and numbers"""
	text = text.lower()
	filtered_text = re.findall('\w+', str(text), re.UNICODE)
	return filtered_text

def run(TXT_PICKLE,GRAPH_NAME,min_weight,max_iter):
	""" Create the graph from the dataframe of texts."""
	loaded_data = read_file(TXT_PICKLE)
	data_dic = loaded_data[0]
	data_index = loaded_data[1]

	# Construct the graph
	print('Creating the graph with threshold = {} ...'.format(min_weight))
	GS = nx.DiGraph()
	# initiate the progress bar
	nb_of_texts = len(data_dic)
	pbar = tqdm.tqdm(total=nb_of_texts)
	for key in data_dic.keys():
		data_elem = data_dic[key]
		text_id = data_elem['id']
		list_of_words = filter_text(data_elem['text'])
		text_data = {}
		text_data['length'] = len(list_of_words)
		GS = grevia.add_string_of_words(GS,list_of_words,text_id,text_data)
		pbar.update(1)
	pbar.close()
	print('Graph created.')
	print('Nb of edges: {}, nb of nodes: {}.'.format(GS.size(),len(GS.nodes())))

	# Merge the strongly connected nodes
	GS = grevia.merge_strongly_connected_nodes_fast(GS,min_weight,max_iter)
	print('New graph size:')
	print('Nb of edges: {}, nb of nodes: {}.'.format(GS.size(),len(GS.nodes())))
	# Normalize the weights and cut the weakest links 
	#GS = grevia.normalize_weights(GS,weight=None,weight_n='weight_n')
	# Save graph
	nx.write_gpickle(GS,GRAPH_NAME)
	output_message = 'Graph created. Nb of edges: {}, nb of nodes: {}.'.format(GS.size(),len(GS.nodes()))
	return output_message

def doc_classif(graph_name,text_pickle_file,EX_TXT_PICKLE,csv_file):
	""" Classification of the documents from the graph,
	using community detection.
	"""
	if not os.path.isfile(EX_TXT_PICKLE):
		print('No file with info on extracted text. Please extract the text first with pdf2txt. ')
		return 'No file with info on extracted text. Please extract the text first with pdf2txt. '
	G = nx.read_gpickle(graph_name)
	G_doc = grevia.doc_graph(G)
	print('Graph of documents created.')
	print('Nb of edges: {}, nb of nodes: {}'.format(G_doc.size(),len(G_doc.nodes())))
	# Shrink the graph
	#print('Removing weakest links...')
	#threshold = 5
	#G_doc = grevia.remove_weak_links(G_doc,threshold,weight='weight')
	#G_doc.remove_nodes_from(nx.isolates(G_doc))
	print('Nb of connected components: ',nx.number_connected_components(G_doc))
	[data_dic,data_index] = read_file(text_pickle_file)

	# Get info from the pdf initial files
	file_infos = read_file(EX_TXT_PICKLE)
	# Run the community detection
	print('Running the community detection...')
	subgraph_list = grevia.cluster_graph(G_doc,20)
	grevia.clusters_info(subgraph_list)
	cluster_name_list = grevia.subgraphs_to_filenames_to_dic(subgraph_list,data_index,file_infos,density=True)
	clusters_table = grevia.output_filename_classification_from_dic(cluster_name_list,csv_file)
	print('Graph and classification done.')
