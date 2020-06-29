from flask import Flask, render_template, request, url_for
from awsdb import conn
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
from collections import Counter

application = Flask(__name__)

deets = ["Yash Bardapurkar", "1001731650"]
options = { 8: 'fare', 4: 'age', 1: 'survived', 9: 'cabin', 3: 'sex', }

@application.route('/', methods=["GET"])
def hello_world():
	return render_template('index.html', deets=deets)


@application.route('/cluster', methods=["POST"])
def stringvalue():
	clusterno = int(request.form['clusterno'])

	column1 = int(request.form['column1'])
	column2 = int(request.form['column2'])

	cur = conn.cursor()
	sql = "SELECT " +  options[column1] + ", " +  options[column2] + " from titanic2 where " + options[column1] + " != '' and " + options[column2] + " != '';"
	cur.execute(sql)

	npArray = np.array(cur.fetchall())

	if (column1 == 9 or column1 == 3) :
		label_encoder = LabelEncoder()
		npArray[:, 0] = label_encoder.fit_transform(npArray[:, 0])
	if (column2 == 9 or column2 == 3) :
		label_encoder = LabelEncoder()
		npArray[:, 1] = label_encoder.fit_transform(npArray[:, 1])

	k_means = KMeans(n_clusters=clusterno)
	print(npArray)
	k_means.fit(npArray)

	arr_centroids = k_means.cluster_centers_
	arr_labels = k_means.labels_

	count = Counter(arr_labels)
	number = list(count.items())

	centers = []
	centroids = arr_centroids.tolist()
	for i in range(clusterno):
		centers.append([arr_centroids[i][0], arr_centroids[i][1], number[i][1]])


	return render_template('cluster.html', points=npArray.tolist(), centroids=centers, deets=deets)


@application.route('/centroid_distance', methods=["POST"])
def centroid_distance():
	clusterno = int(request.form['clusterno'])

	column1 = int(request.form['column1'])
	column2 = int(request.form['column2'])

	cur = conn.cursor()
	sql = "SELECT " +  options[column1] + ", " +  options[column2] + " from titanic2 where " + options[column1] + " != '' and " + options[column2] + " != '';"
	cur.execute(sql)

	npArray = np.array(cur.fetchall())

	if (column1 == 9 or column1 == 3) :
		label_encoder = LabelEncoder()
		npArray[:, 0] = label_encoder.fit_transform(npArray[:, 0])
	if (column2 == 9 or column2 == 3) :
		label_encoder = LabelEncoder()
		npArray[:, 1] = label_encoder.fit_transform(npArray[:, 1])


	k_means = KMeans(n_clusters=clusterno)
	k_means.fit(npArray)

	arr_centroids = k_means.cluster_centers_
	arr_labels = k_means.labels_

	distance_table = []
	for i in range(len(arr_centroids)):
		for j in range(len(arr_centroids)):
			dist = np.linalg.norm(arr_centroids[i] - arr_centroids[j])
			distance_table.append([arr_centroids[i], arr_centroids[j], dist])

	
	return render_template('centroid_distance.html', points=npArray.tolist(), distance_table=distance_table, deets=deets)

@application.route('/inertia', methods=["POST"])
def inertia():
	clusterno = int(request.form['clusterno'])

	column1 = int(request.form['column1'])
	column2 = int(request.form['column2'])

	cur = conn.cursor()
	sql = "SELECT " +  options[column1] + ", " +  options[column2] + " from titanic2 where " + options[column1] + " != '' and " + options[column2] + " != '';"
	cur.execute(sql)

	npArray = np.array(cur.fetchall())

	if (column1 == 9 or column1 == 3) :
		label_encoder = LabelEncoder()
		npArray[:, 0] = label_encoder.fit_transform(npArray[:, 0])
	if (column2 == 9 or column2 == 3) :
		label_encoder = LabelEncoder()
		npArray[:, 1] = label_encoder.fit_transform(npArray[:, 1])


	distortions = []
	for k in range(2, clusterno + 1):
		k_means = KMeans(n_clusters=k)
		k_means.fit(npArray)
		distortions.append([k, k_means.inertia_])

	return render_template('inertia.html', distortions=distortions, deets=deets)

# run the app.
if __name__ == '__main__':
	application.debug = True
	application.run()