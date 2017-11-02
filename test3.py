import numpy as np
from sklearn.cluster import SpectralClustering, KMeans
import matplotlib.pyplot as plt
# import networkx as nx
from sklearn import neighbors
from scipy.sparse import csgraph
from itertools import combinations, permutations
from sklearn.metrics.pairwise import cosine_similarity
from scipy import spatial
from sklearn import datasets
from sklearn import cross_decomposition as cd
from sklearn.semi_supervised import label_propagation
from sklearn import svm
from sklearn import (manifold, datasets, decomposition, ensemble,
                     discriminant_analysis, random_projection)
from time import time
from sklearn.cluster import AgglomerativeClustering, KMeans, Birch
from sklearn.mixture import GaussianMixture
from sklearn.neighbors import kneighbors_graph
import random

# import lda
# import lda.datasets


# Create distance matrix using updated matrix
# 0 = identical, larger number = greater dissimilarity, infinity = not similar at all
# def getWeightedAdjacencyMatrix(M):
# 	print "Creating features matrix..."
# 	features = np.genfromtxt('../Extracted_features.csv', delimiter = ',')
# 	print "Done creating features matrix"

# 	print "Creating weighted adjacency matrix..."
# 	WM = np.full((6000,6000), float(100))
# 	for i in range(M.shape[0]):
# 		for j in range(M.shape[1]):
# 			if i == j:
# 				WM[i,i] = 0
# 				continue
# 			if M[i,j] == 0:
# 				continue
# 			elif M[i,j] == 1:
# 				euclidean_distance = np.linalg.norm(features[i] - features[j])
# 				WM[i][j] = euclidean_distance
# 				WM[j][i] = euclidean_distance
# 			elif M[i,j] == 2:
# 				WM[i][j] = 0
# 				WM[j][i] = 0

# 	print "Done creating weighted adjacency matrix"
# 	return WM

# def getWeightedAdjacencyMatrix(M):
# 	print "Creating features matrix..."
# 	features = np.genfromtxt('../Extracted_features.csv', delimiter = ',')
# 	print "Done creating features matrix"

# 	print "Creating weighted adjacency matrix..."
# 	WM = np.zeros((6000,6000))
# 	for i in range(M.shape[0]):
# 		for j in range(M.shape[1]):
# 			if i == j:
# 				WM[i,i] = 1
# 				continue
# 			if M[i,j] == 0:
# 				continue
# 			elif M[i,j] == 1:
# 				euclidean_distance = np.linalg.norm(features[i] - features[j])
# 				WM[i][j] = euclidean_distance
# 				WM[j][i] = euclidean_distance
# 			elif M[i,j] == 2:
# 				WM[i][j] = 1
# 				WM[j][i] = 1

# 	print "Done creating weighted adjacency matrix"
# 	return WM

# def findWeightedMatrix(M):
# 	print "Creating features matrix..."
# 	features = np.genfromtxt('../Extracted_features.csv', delimiter = ',')
# 	print "Done creating features matrix"

# 	print "Creating numpy adjacency matrix..."
# 	WM = np.full((6000,6000), float(100))

# 	print "Filling in matrix..."
# 	for i in range(M.shape[0]):
# 		for j in range(M.shape[1]):
# 			if i == j:
# 				WM[i,j] = 0
# 			if M[i,j] == 0:
# 				continue
# 			else:
# 				euclidean_distance = np.linalg.norm(features[i] - features[j])
# 				WM[i,j] = euclidean_distance
# 				WM[j,i] = euclidean_distance

# 	print "Done creating matrix"
# 	return WM

def getWeightedMatrix(M):
	print "Creating features matrix..."
	features = np.genfromtxt('../Extracted_features.csv', delimiter = ',')
	print "Done creating features matrix"

	print "Creating numpy adjacency matrix..."
	WM = np.zeros((6000,6000))

	print "Filling in matrix..."
	for i in range(M.shape[0]):
		for j in range(M.shape[1]):
			if i == j:
				WM[i,j] = 1
			if M[i,j] == 0:
				continue
			else:
				euclidean_distance = np.linalg.norm(features[i] - features[j])
				WM[i,j] = 1.0 / euclidean_distance
				WM[j,i] = 1.0 / euclidean_distance

	print "Done creating matrix"
	return WM

# Return unweighted adjacency matrix
# M[i][j] = 1 if nodes i+1 and j+1 are connected by an edge; else 0
def getUnweightedAdjacencyMatrix():
	with open('../Graph.csv', 'r') as f:
		print "Creating unweighted adjacency matrix..."

		M = np.zeros((6000,6000), dtype=np.int)
		lines = f.readlines()
		for line in lines:
			(node1, node2) = [int(x) for x in line.split(',')]
			M[node1-1][node2-1] = 1
			M[node2-1][node1-1] = 1

		print "Done creating unweighted adjacency matrix"
		return M

def writeUnweightedAdjacencyMatrixToCSV(fileName, M):
	with open(fileName, 'wb') as f:
		print "Writing unweighted adjacency matrix to CSV..."
		for row in M:
			line = ','.join([str(e) for e in row])
			f.write('%s\n' % line)
		print "Wrote unweighted adjacency matrix to CSV"

def loadUnweightedAdjacencyMatrix(fileName):
	with open(fileName, 'r') as f:
		print "Loading unweighted adjacency matrix..."

		M = np.zeros((6000,6000))
		lines = f.readlines()
		for i, line in enumerate(lines):
			M[i,:] = [int(e) for e in line.split(',')]

		print "Done loading unweighted adjacency matrix"
		return M.astype(int)

def loadWeightedAdjacencyMatrix(fileName):
	with open(fileName, 'r') as f:
		print "Loading unweighted adjacency matrix..."

		M = np.zeros((6000,6000))
		lines = f.readlines()
		for i, line in enumerate(lines):
			M[i,:] = [float(e) for e in line.split(',')]

		print "Done loading unweighted adjacency matrix"
		return M.astype(float)

def loadMatrix(fileName, row, col):
	with open(fileName, 'r') as f:
		print "Loading unweighted adjacency matrix..."

		M = np.zeros((row,col))
		lines = f.readlines()
		for i, line in enumerate(lines):
			M[i,:] = [float(e) for e in line.split(',')]

		print "Done loading unweighted adjacency matrix"
		return M.astype(float)


def getLabelsDict():
	with open('../Seed.csv', 'r') as f:
		print "Filling in correct labels dictionary..."

		labels = {}
		lines = f.readlines()
		for line in lines:
			(node, label) = [int(x) for x in line.split(',')]
			labels.setdefault(label, set()).add(node)

		print "Done filling in correct labels dictionary"
		return labels

def pprintDict(d):
	for key, val in d.items():
		print key, ':', val

def plotGraph(adjacency_matrix):
	print "Plotting graph for 6000 nodes..."
	rows, cols = np.where(adjacency_matrix == 1)
	edges = zip(rows.tolist(), cols.tolist())
	G = nx.Graph()
	G.add_edges_from(edges)
	nx.draw(G)
	plt.show()
	print "Done plotting graph for 6000 nodes"

# Print which nodes in correct labels aren't connected
def printConnectedGraphs(M, labels):
	for digit, nodes in labels.items():
		print 'Digit: %i' % digit
		nodes = list(nodes)
		combos = list(combinations(nodes, 2))
		count = 0
		for (i, j) in combos:
			if M[i-1, j-1] == 0:
				print 'nodes %i and %i not connected' % (i, j)
			else:
				count += 1
		print 'Connected nodes: %i/%i' % (count, len(combos))
		print '\n'

# Update unweighted adjacency matrix using correctly labelled nodes
# 2 = definitely connected
# 1 = unknown connected
# 0 = not connected
def updateUnweightedAdjacencyMatrix(M, labels):
	labelledNodes = set() # Set of 60 correctly labelled nodes
	connectedNodes = set() # Set of (i,j) pairs where nodes i and j are connected
	for _, nodes in labels.items():
		labelledNodes.update(nodes)
		nodeCombos = set(combinations(nodes, 2))
		connectedNodes.update(nodeCombos)

	# All possible 2-element combos of 60 correctly labelled nodes
	allCombos = list(combinations(labelledNodes, 2))

	for (i, j) in allCombos:
		if (i, j) in connectedNodes or (j, i) in connectedNodes:
			M[i-1, j-1] = 1
			M[j-1, i-1] = 1
		else:
			M[i-1, j-1] = 0
			M[j-1, i-1] = 0

	return M

def runSpectralClustering(M):
	# delta = np.std(M)
	# M = np.exp(- M ** 2 / (2. * delta ** 2))
	features = np.genfromtxt('../Extracted_features.csv', delimiter = ',')

	spectral = SpectralClustering(n_clusters=10, eigen_solver='arpack', affinity='precomputed')
	spectralClusters = spectral.fit_predict(features) # 1 x 6000

	clusters = {}
	for idx, cluster in enumerate(spectralClusters):
		clusters.setdefault(cluster, set()).add(idx+1)

	return clusters

def writeClustersToCSV(clusters):
	with open('new_clusters.csv', 'wb') as f:
		for cluster, nodes in clusters.items():
			line = ','.join([str(n) for n in list(nodes)])
			f.write(line)
			f.write('\n')
	print "Wrote clusters to csv"

def validateClusters(clusterAssignments):
	labels = getLabelsDict()

	labelledClusters = {}
	for digit, labelledNodes in labels.items():
		for node in labelledNodes:
			for clusterIdx, nodes in clusterAssignments.items():
				if node in nodes:
					labelledClusters.setdefault(digit, []).append(clusterIdx)

	print "Clusters dict"
	for num, clusters in labelledClusters.items():
		print num, ': ', clusters

def load_clusters():
	with open('clusters.csv', 'r') as f:
		lines = f.readlines()

		clusters = {}
		for idx, line in enumerate(lines):
			clusters[idx] = set([int(e) for e in line.split(',')])

		return clusters

def runLabelPropagationSVM():
	labels = getLabelsDict()

	# Dict of node to digit for 60 labelled nodes
	labelledNodes = {}
	for digit, nodes in labels.items():
		for node in nodes:
			labelledNodes[node] = digit

	features = np.genfromtxt('../Extracted_features.csv', delimiter = ',')

	y_train = [-1] * 6000
	unlabeled_set = []
	for i in range(6000):
		if i+1 in labelledNodes:
			y_train[i] = labelledNodes[i+1]
		else:
			unlabeled_set.append(i)

	y_train = np.array(y_train)
	unlabeled_set = np.array(unlabeled_set)

	print "Start propagating labels..."
	lp_model = label_propagation.LabelSpreading(gamma=0.25, max_iter=5)
	lp_model.fit(features[:6000], y_train)
	predicted_labels = lp_model.transduction_[unlabeled_set]
	print "Done propagating labels"

	for idx, label in zip(unlabeled_set, predicted_labels):
		labels[label].add(idx+1)

	# for digit, nodes in labels.items():
	# 	print 'Digit %i: %i' % (digit, len(nodes))

	newLabelledNodes = {}
	for digit, nodes in labels.items():
		for node in nodes:
			newLabelledNodes[node] = digit

	y = []
	for i in range(len(newLabelledNodes)):
		y.append(newLabelledNodes[i+1])

	# for i in range(10):
	# 	print i, y.count(i)

	print "Start running SVM..."
	svmModel = svm.SVC()
	svmModel.fit(features[:6000], y)
	print "Finished running SVM"

	finalLabelsDict = {}
	final_labels = svmModel.predict(features[6000:])

	for idx, label in enumerate(final_labels):
		finalLabelsDict.setdefault(label, []).append(6001+idx)

	for digit, nodes in finalLabelsDict.items():
		print 'Digit %i: %i' % (digit, len(nodes))

	output = np.zeros((4000,2), dtype='int32')
	for digit, nodes in finalLabelsDict.items():
		for node in nodes:
			output[node-6001,0] = node
			output[node-6001,1] = digit

	np.savetxt("label_prop_svm.csv", output.astype(int), fmt='%i', delimiter=",", header="Id,Label", comments='')

def run_svm(train_set, test_set, train_labels, file_name):
	print "Start running SVM..."
	svmModel = svm.SVC()
	svmModel.fit(train_set, train_labels)
	print "Finished running SVM"

	finalLabelsDict = {}
	final_labels = svmModel.predict(test_set)

	for idx, label in enumerate(final_labels):
		finalLabelsDict.setdefault(label, []).append(6001+idx)

	for digit, nodes in finalLabelsDict.items():
		print 'Digit %i: %i' % (digit, len(nodes))

	output = np.zeros((4000,2), dtype='int32')
	for digit, nodes in finalLabelsDict.items():
		for node in nodes:
			output[node-6001,0] = node
			output[node-6001,1] = digit

	np.savetxt(file_name, output.astype(int), fmt='%i', delimiter=",", header="Id,Label", comments='')



def run_svm_updated(train_set, test_set, train_labels, file_name, goodNodes, badNodes):
	print "Start running updated SVM..."
	svmModel = svm.SVC()
	svmModel.fit(train_set, train_labels)
	print "Finished running SVM"

	finalLabelsDict = {}
	final_labels = svmModel.predict(test_set)

	for idx, label in enumerate(final_labels):
		finalLabelsDict[badNodes[idx]] = label

	output = np.zeros((4000,2), dtype='int32')
	index = 6000
	for node in range(6001,10001):
		if node in goodNodes:
			output[node-6001,0] = node
			output[node-6001,1] = train_labels[index]
			index += 1
		else:
			output[node-6001,0] = node
			output[node-6001,1] = finalLabelsDict[node]

	np.savetxt(file_name, output.astype(int), fmt='%i', delimiter=",", header="Id,Label", comments='')




# Do spectral clustering to get 10 clusters
def runSpectralClustering(M):
	# delta = np.std(M)
	# M = np.exp(- M ** 2 / (2. * delta ** 2))

	print "Performing spectral clustering..."
	spectral = SpectralClustering(n_clusters=10, affinity='precomputed', n_init=100, assign_labels='discretize')
	predicted_labels = spectral.fit_predict(M) # 1 x 6000
	print "Done performing spectral clustering"

	return predicted_labels

# Do agglomerative clustering to get 10 clusters
def runAgglomerativeClustering(X, linkage='ward'):
	print "Performing agglomerative clustering..."
	clustering = AgglomerativeClustering(linkage=linkage, n_clusters=10)
	predicted_labels = clustering.fit_predict(X)
	print "Done performing agglomerative clustering"

	return predicted_labels

# Do K-means clustering to get 10 clusters
def runKMeansClustering(M):
	print "Performing KMeans clustering..."
	kmeans = KMeans(n_clusters=10, n_init=1000)
	predicted_labels = kmeans.fit_predict(M)
	print "Done performing KMeans clustering"

	return predicted_labels

# Brute force 10! to find labelling that maximizes seed accuracy
def getOptimalClusterLabelling(clusterAssignments):
	print "Looking for optimal cluster labelling..."
	clusters = clusterAssignments.keys()
	digits = [i for i in range(10)]
	perms = list(permutations(digits)) # 10! possibilities

	labels = getLabelsDict()

	maxAccuracy = 0.0
	maxPerm = []
	for i, perm in enumerate(perms):
		numCorrectLabels = 0.0
		mapping = zip(clusters, perm) # cluster_no, digit
		for (cluster_no, digit) in mapping:
			clusterNodes = clusterAssignments[cluster_no]
			labelledNodes = labels[digit]
			overlap = clusterNodes.intersection(labelledNodes)
			numCorrectLabels += len(overlap)
		accuracy = numCorrectLabels / float(60)
		if accuracy > maxAccuracy:
			maxAccuracy = accuracy
			maxPerm = perm
	print "Found optimal cluster labelling"
	print "Max accuracy: %f" % maxAccuracy

	print "Optimal digit-cluster mapping"
	clusterMapping = zip(maxPerm, clusters)
	sortedMapping = sorted(clusterMapping, key=lambda x: x[0])
	for (digit, cluster) in sortedMapping:
		print digit, ':', cluster

	clusterDigitMapping = dict(zip(clusters, maxPerm))

	return clusterDigitMapping

def getClusterAssignments(predictedLabels):
	# labelledDict stores the cluster -> nodes in cluster
	labelledDict = {}
	for idx, label in enumerate(predictedLabels):
		node = idx + 1
		labelledDict.setdefault(label, set()).add(node)

	# Print out number of nodes in each cluster
	for cluster, nodes in labelledDict.items():
		print 'Cluster %i: %i' % (cluster, len(nodes))

	return labelledDict

#Similar to CCA, performs dimensional reduction
def runLDA(M):
	model = lda.LDA(n_topics = 1084, n_iter = 1500, random_state = 1)
	X = model.fit_transform(M)
	return X

def run():
	"""
	TRY THIS:

	How we can get > 70%:
	- Use the 6000 x 6000 edges matrix of 0 and 1 values as the affinity matrix to pass into spectral embedding
		- Note: I'm not completely sure what the value of n_components is supposed to be but I think 1084 could work?
	- Perform Spectral embedding to get X_se
		- What spectral embedding does is that it allows you to apply your own clustering algorithm
		- Spectral clustering is just a combination of spectral embedding and k-means clustering
		- We prob want to use single linkage clustering or our own clustering in place of k-means
		  since k-means doesn't do that well.
	- Pass X_se into the clustering algorithm with n_clusters = 10
		- I'm using agglomerative clustering right now, which is related to single linkage clustering
	- Get the predicted labels for the 6000 nodes using the clustering algorithm
	- Using predicted labels, group the clusters into labelledDict
	- Brute force 10! to find the labelling for the clusters that maximizes seed accuracy (60 labelled nodes)
	- Label clusters such that seed accuracy is maximized (similar to cluster mapping we did before)
	- Now you should have a 1 x 6000 array where every element at index i corresponds to the digit that node i+1 is assigned to
		- Call this array Y for example
	- Now you can call run_svm function above
		- run_svm(train_set, test_set, train_labels, file_name)
			- train_set = features[:6000]
			- test_set = features[6000:]
			- train_labels = Y from above
	- You should be able to submit the csv made in run_svm to Kaggle directly
	"""
	# Load in 6000 x 6000 edges matrix of 0 and 1
	# M = loadWeightedAdjacencyMatrix('newWeightedAdjacencyMatrix.csv')
	# M = loadUnweightedAdjacencyMatrix('updatedWeightedMatrx.csv')

	# replace72 = np.genfromtxt('replacescore72.csv')
	# replace75 = np.genfromtxt('replacescore75.csv')
	# replaceinit15 = np.genfromtxt('replaceinit15.csv')

	# replaceDict = {}
	# for i in replaceinit15:
	# 	if replaceDict.has_key(i):
	# 		replaceDict[i][0] = replaceDict[i][0]+1
	# 		replaceDict[i].append(15)
	# 	else:
	# 		replaceDict[i] = [1,15]
	# for i in replace72:
	# 	if replaceDict.has_key(i):
	# 		replaceDict[i][0] = replaceDict[i][0]+1
	# 		replaceDict[i].append(72)
	# 	else:
	# 		replaceDict[i] = [1, 72]
	# for i in replace75:
	# 	if replaceDict.has_key(i):
	# 		replaceDict[i][0] = replaceDict[i][0]+1
	# 		replaceDict[i].append(75)
	# 	else:
	# 		replaceDict[i] = [1, 75]
	# counter = []
	# for k, v in replaceDict.items():
	# 	if v[0] > 1 or 75 in v:
	# 		counter.append(k)
	# 	else:
	# 		if bool(random.getrandbits(1)):
	# 			counter.append(k)
	# print len(counter)

	# replace = np.array(counter)
	# np.savetxt('final_replace.csv', replace.astype(int))
	# quit()

	# init15_2 = np.genfromtxt('se_gmm_svm_init15_2.csv', delimiter = ',', skip_header=1, dtype='int32')
	# final_replace = np.genfromtxt('final_replace.csv', delimiter=',',dtype = 'int32')

	# for j in final_replace:
	# 	init15_2[j-6001,1] = 9

	# np.savetxt("se_gmm_svm_modifying.csv", init15_2.astype(int), fmt='%i', delimiter=",", header="Id,Label", comments='')
	# quit()

	print "Generating features matrix"
	features = np.genfromtxt('../Extracted_features.csv', delimiter = ',')
	print "Done generating features matrix"

	# # M = getUnweightedAdjacencyMatrix()

	# # # Do spectral embedding
	print "Load spectral embedding..."
	X_se = loadMatrix('../X_se.csv', 6000, 1084)
	print "Done loading spectral embedding"

	print "Performing CCA"
	k = 80
	# cca = cd.CCA(n_components=k, max_iter=5000)
	# Y1, Y2 = cca.fit_transform(X_se, features[:6000,:])
	# np.savetxt('../X_se_cca_'+str(k)+'_y1.csv', Y1)
	# np.savetxt('../X_se_cca_'+str(k)+'_y2.csv', Y2)
	# print "Loading"
	Y1 = np.genfromtxt('../X_se_cca_'+str(k)+'_y1.csv')
	Y2 = np.genfromtxt('../X_se_cca_'+str(k)+'_y2.csv')
	# print "Done Loading"
	print "Done performing CCA"

	Y = np.concatenate((Y1, Y2), axis=1)

	# print "Performing gmm"
	# gmm = GaussianMixture(n_components=10, n_init = 15)
	# gmm.fit(Y)
	# predictedLabels = gmm.predict(Y)
	# print "Done performing gmm"

	#print "Performing Birch"
	# brc = Birch(n_clusters=10)
	# predictedLabels = brc.fit_predict(newX_se70)
	#print "Done performing birch"

	print "Performing KMeans clustering..."
	# kmeans = KMeans(n_clusters=10, n_init=2000)
	# predictedLabels = kmeans.fit_predict(Y)
	# print "Done performing KMeans clustering"

	# print "Writing to file..."
	# with open('../predictedLabels.csv', 'w') as f:
	# 	for label in predictedLabels:
	# 		f.write(str(label))
	# 		f.write('\n')

	predictedLabels = []
	with open('../predictedLabels.csv', 'r') as f:
		lines = f.readlines()
		for label in lines:
			predictedLabels.append(int(label))
	predictedLabels = np.array(predictedLabels)
	print predictedLabels.shape

	# print "Performing Agglomerative"
	# A = kneighbors_graph(newX_se70, 800)
	# linkage = AgglomerativeClustering(n_clusters = 10, linkage = 'ward', affinity='euclidean', connectivity=A)
	# # linkage2 = AgglomerativeClustering(n_clusters = 10)
	# predictedLabels = linkage.fit_predict(newX_se70)
	# predictedLabels2 = linkage2.fit_predict(newY_se)
	# print "Done performing Agglomerative"

	# print "Performing Spectral Clustering"
	# spectral = SpectralClustering(n_clusters = 10)
	# # spectral2 = SpectralClustering(n_clusters = 10)
	# predictedLabels = spectral.fit_predict(newX_se70)
	# # predictedLabels2 = spectral2.fit_predict(ewY_se)
	# print "Done performing spectral Clustering"

	# # # Do clustering to get 10 clusters
	# predictedLabels = runAgglomerativeClustering(X_se)
	# predictedLabels = runSpectralClustering(M) # 1 x 6000ssssssss

	clusterAssignments = getClusterAssignments(predictedLabels)
	clusterDigitMapping = getOptimalClusterLabelling(clusterAssignments)
	validateClusters(clusterAssignments)

	# clusterAssignments2 = getClusterAssignments(predictedLabels2)
	# clusterDigitMapping2 = getOptimalClusterLabelling(clusterAssignments2)
	# validateClusters(clusterAssignments2)

	train_labels = []
	for cluster in predictedLabels:
		train_labels.append(clusterDigitMapping[cluster])
	print "tl", len(train_labels)

	# np.savetxt('train_labels_spectral_clustering.csv', train_labels)

	# train_labels2 = []
	# for cluster in predictedLabels:
	# 	train_labels2.append(clusterDigitMapping2[cluster])

	# train_labels2 = np.array(train_labels2)

	print "Adjusting train labels..."
	badNodes = []
	with open('../bad.csv') as f:
		lines = f.readlines()
		for node in lines:
			badNodes.append(int(node))

	goodNodes = []
	with open('../se_cca80_kmeans_2000init_svm.csv', 'r') as f:
		lines = f.readlines()
		for line in lines[1:]:
			node, digit = [int(e) for e in line.split(',')]
			if node not in badNodes:
				train_labels.append(digit)
				goodNodes.append(node)

	train_labels = np.array(train_labels)
	print "tl", train_labels.shape

	# # # Run SVM
	print "More adjusting..."
	train_set, test_set = np.zeros((9171,1084)), np.zeros((829,1084))
	print "trs", train_set.shape
	print "tes", test_set.shape
	train_set[:6000,:] = features[:6000]
	for i, node in enumerate(goodNodes):
		train_set[i,:] = features[node-1]
	print "trs", train_set.shape
	for i, node in enumerate(badNodes):
		test_set[i,:] = features[node-6001]
	print "tes", test_set.shape

	run_svm_updated(train_set, test_set, train_labels, "../willThisWork.csv", goodNodes, badNodes)
	# run_svm(train_set, test_set, train_labels2)


	"""
	IGNORE COMMENTS BELOW THIS (WAS TESTING OUT RANDOM STUFF)
	"""

	# clusterAssignments = load_clusters()
	# validateClusters(clusterAssignments)



	# M = loadUnweightedAdjacencyMatrix('unweightedAdjacencyMatrix.csv')
	# WM = findWeightedMatrix(M)

	# 1 : [2, 5, 111, 50, 19, 37]

	# labels = getLabelsDict()

	# for label, nodes in labels.items():
	# 	print "label %i" % label
	# 	result = []
	# 	for i in range(6000):
	# 		count = 0
	# 		for node in nodes:
	# 			if M[i,node-1] == 1:
	# 				count += 1
	# 		if count == 6: result.append(i+1)
	# 	print len(result)

	# combos = list(combinations(labels[1],2))
	# for (i, j) in combos:
	# 	if M[i,j] == 0:
	# 		print "nodes %i and %i are not connected" % (i, j)

	# clusterAssignments = runSpectralClustering(WM)
	# validateClusters(clusterAssignments)

	# features = np.genfromtxt('../Extracted_features.csv', delimiter = ',')

	# labels = getLabelsDict()


	# # seedFile = open('../Seed.csv', 'r')

	# # centroids = np.zeros((10,1084))
	# # for cluster, nodes in clusters.items():
	# # 	featureVectors = np.zeros((len(nodes), 1084))
	# # 	for i, node in enumerate(nodes):
	# # 		featureVectors[i,:] = features[node-1,:]

	# # 	avgVector = np.mean(featureVectors, axis=0)

	# # 	centroids[cluster,:] = avgVector

	# for digit, nodes in labels.items():
	# 	print "Digit %i" % digit
	# 	combos = list(combinations(nodes, 2))
	# 	totalDist = 0.0
	# 	for (node1, node2) in combos:
	# 		feature1, feature2 = features[node1-1], features[node2-1]
	# 		euclideanDist = np.linalg.norm(feature1 - feature2)
	# 		print "Euclidean Distance b/w %i and %i is %f" % (node1, node2, euclideanDist)
	# 		totalDist += euclideanDist
	# 	print "Avg Distance: %f" % (totalDist / len(combos))



	# for (node1, node2) in combos:
	# 	feature1, feature2 = features[node1-1], features[node2-1]
	# 	similarity = 1 - spatial.distance.cosine(feature1, feature2)
	# 	print "Similarity b/w %i and %i is %f" % (node1, node2, similarity)

	# print '\n'

	# for node1 in nodes:
	# 	for node2 in labels[5]:
	# 		feature1, feature2 = features[node1-1], features[node2-1]
	# 		similarity = 1 - spatial.distance.cosine(feature1, feature2)
	# 		print "Similarity b/w %i and %i is %f" % (node1, node2, similarity)






# You can see here that running spectral clustering on the adjacency matrix
# for the 60 labelled nodes gets the perfect clustering
def checkLabelledNodes():
 	labels = getLabelsDict()

	labelledNodes = set() # Set of 60 correctly labelled nodes
	connectedNodes = set() # Set of (i,j) pairs where nodes i and j are connected
	for _, nodes in labels.items():
		labelledNodes.update(nodes)
		nodeCombos = set(combinations(nodes, 2))
		connectedNodes.update(nodeCombos)

	idxToNodeMapping = {}
	nodeToIdxMapping = {}
	for idx, node in enumerate(list(labelledNodes)):
		nodeToIdxMapping[node] = idx
		idxToNodeMapping[idx] = node

	M = np.zeros((60,60), dtype=np.int)
	for (node1, node2) in connectedNodes:
		idx1, idx2 = nodeToIdxMapping[node1], nodeToIdxMapping[node2]
		M[idx1, idx2] = 1
		M[idx2, idx1] = 1

	clusterAssignments = runSpectralClustering(M)

	for clusterIdx, nodes in clusterAssignments.items():
		clusterAssignments[clusterIdx] = [idxToNodeMapping[n-1] for n in nodes]

	labelledClusters = {}
	for digit, labelledNodes in labels.items():
		for node in labelledNodes:
			for clusterIdx, nodes in clusterAssignments.items():
				if node in nodes:
					labelledClusters.setdefault(digit, []).append(clusterIdx)

	print "Digit | Clusters"
	for num, clusters in labelledClusters.items():
		print num, '  :  ', clusters


if __name__ == '__main__':
	np.set_printoptions(threshold=np.nan)
	run()
