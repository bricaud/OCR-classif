#!/usr/bin/env python3
""" Module to create the graph from the texts in pickle file (dataframe),
and to classify the documents from the graph.
"""

import re
import tqdm
import pickle
import sys
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

def get_document_and_text_from_db(data_dic,data_index,document_id):
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

def get_surrounding_text_sliced(doc_text,position,expression_len,nb_words=10):
	text_list =  filter_text(doc_text)
	start = max(0,position-nb_words)
	end = min(position+expression_len+nb_words,len(doc_text))
	return text_list[start:position],text_list[position+expression_len:end]


def filter_text(text):
	""" filter the text: keep letters and numbers"""
	filtered_text = re.findall('\w+', str(text), re.UNICODE)
	return filtered_text

def filter_text_lower(text):
	""" filter the text: apply lower case and keep letters and numbers"""
	text = text.lower()
	return filter_text(text)

def run_from_db(db_entries_dic,graphdb):
	""" Create the graph from the Django database of documents."""
	data_dic = db_entries_dic
	# Construct the graph
	#print('Creating the graph...')
	GS = graphdb
	#GS = grevia.wordgraph.Graph('GremlinGraph',GRAPH_SERVER_ADDRESS)
	# initiate the progress bar
	nb_of_texts = len(data_dic)
	print('Nb of texts:',nb_of_texts)
	pbar = tqdm.tqdm(total=nb_of_texts)
	similarity_dic = {}
	for key in data_dic.keys():
		data_elem = data_dic[key]
		text_id = data_elem['id']
		list_of_words = filter_text_lower(data_elem['text'])
		document = grevia.Document(text_id,list_of_words,key)
		#GS = grevia.add_merge_document(GS,document)
		miniG = grevia.minigraph.create_minigraph(GS,document)
		similar_documents = grevia.minigraph.merge_minigraph(miniG,GS)
		similarity_dic[text_id] = similar_documents
		pbar.update(1)
	pbar.close()
	print('Graph created.')
	print('Nb of edges: {}, nb of nodes: {}.'.format(GS.number_of_edges(),GS.number_of_nodes()))
	# Save graph
	#nx.write_gpickle(GS,GRAPH_NAME)
	#GS.save_to_file(GRAPH_FILE_NAME)
	#node_dic = grevia.node_dic_from_graph(GS)
	output_message = 'Graph created. Nb of edges: {}, nb of nodes: {}.'.format(GS.number_of_edges(),GS.number_of_nodes())
	return similarity_dic,output_message

def doc_classif_db(graph_server_address,document_index_dic,csv_file):
	""" Classification of the documents from the graph,
	using community detection.
	"""

	wordG = grevia.wordgraph.Graph('GremlinGraph',graph_server_address)#from_file(graph_name)


	docG = grevia.make_document_graph(wordG)
	print('Graph of documents created.')
	print('Nb of edges: {}, nb of nodes: {}'.format(docG.number_of_edges(),docG.number_of_nodes()))
	# Shrink the graph
	#print('Removing weakest links...')
	#threshold = 5
	#G_doc = grevia.remove_weak_links(G_doc,threshold,weight='weight')
	#G_doc.remove_nodes_from(nx.isolates(G_doc))
	print('Nb of connected components: ',docG.number_connected_components())
	# Run the community detection
	print('Running the community detection...')
	subgraph_list = grevia.cluster_graph(docG,6)
	grevia.clusters_info(subgraph_list)
	# Attach the documents infos
	clusters_dic = grevia.subgraphs_doc_info(subgraph_list,document_index_dic)
	# Save the data
	grevia.save_classification_from_dic_to_file(clusters_dic,csv_file)
	print('Graph and classification done.')
	return clusters_dic
