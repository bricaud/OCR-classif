#!/usr/bin/env python3
""" Module to create the graph from the texts in pickle file (dataframe),
and to classify the documents from the graph.
"""
import sys
import pandas as pd
import re
import networkx as nx
import tqdm



def run(PICKLE_FILE,GRAPH_NAME,GREVIA_PATH):
	""" Create the graph from the dataframe of texts."""
	sys.path.append(GREVIA_PATH)
	import grevia
	df = pd.read_pickle(PICKLE_FILE)

	# filter the texts, make a list of words for each text
	filtered_text_list = []
	for row in df.itertuples():
		text = ' '.join(row.text_list)
		filtered_text = re.findall('\w+', str(text), re.UNICODE)
		#tokens = str(text).split()
		filtered_text_list.append(filtered_text)
	dataframe_f = df[['filename','text','text_length']].copy()
	dataframe_f.loc[:,'filtered_text'] = filtered_text_list

	# Construct the graph
	print('Creating the graph...')
	GS = nx.DiGraph()
	# initiate the progress bar
	nb_of_texts = len(dataframe_f)
	pbar = tqdm.tqdm(total=nb_of_texts)
	for row in dataframe_f.itertuples():
		text_id = row.Index
		text_data = {}
		text_data['length'] = len(row.filtered_text)
		list_of_words = row.filtered_text
		GS = grevia.add_string_of_words(GS,list_of_words,text_id,text_data)
		pbar.update(1)
	pbar.close()
	print('Graph created.')
	print('Nb of edges: {}, nb of nodes: {}.'.format(GS.size(),len(GS.nodes())))

	# Merge the strongly connected nodes
	GS = grevia.merge_strongly_connected_nodes_fast(GS,min_weight=15,max_iter=20000)
	print('New graph size:')
	print('Nb of edges: {}, nb of nodes: {}.'.format(GS.size(),len(GS.nodes())))
	
	# Save graph
	nx.write_gpickle(GS,GRAPH_NAME)

def doc_classif(graph_name,text_pickle_file,GREVIA_PATH,csv_file):
	""" Classification of the documents from the graph,
	using community detection.
	"""
	sys.path.append(GREVIA_PATH)
	import grevia
	G = nx.read_gpickle(graph_name)
	G_doc = grevia.doc_graph(G)
	print('Graph of documents created.')
	print('Nb of edges: {}, nb of nodes: {}'.format(G_doc.size(),len(G_doc.nodes())))
	# Shrink the graph
	print('Removing weakest links...')
	threshold = 5
	G_doc = grevia.remove_weak_links(G_doc,threshold,weight='weight')
	G_doc.remove_nodes_from(nx.isolates(G_doc))
	print('Nb of connected components: ',nx.number_connected_components(G_doc))
	df = pd.read_pickle(text_pickle_file)
	# Run the community detection
	print('Running the community detection...')
	subgraph_list = grevia.cluster_graph(G_doc,20)
	grevia.clusters_info(subgraph_list)
	cluster_name_list = grevia.subgraphs_to_filenames(subgraph_list,df)
	clusters_table = grevia.output_filename_classification(cluster_name_list,csv_file)
	print('Graph and classification done.')
