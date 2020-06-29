from flask import Flask, render_template, request, url_for
from awsdb import conn
import os, json, datetime, random
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
from collections import Counter

application = Flask(__name__)

deets = ["Bindhu Shree Hadya Ravi", "1001699836"]
options = { 8: 'fare', 4: 'age', 1: 'survived', 9: 'cabin', 3: 'sex', }

# default
@application.route('/', methods=["GET"])
def hello_world():
	# return render_template('index.html', result=obj)
	return render_template('index.html')

@application.route('/line_chart', methods=["POST"])
def line_chart():
	sql ="select t.ranges as magnitudes, count(*) as occurences from (select case when mag >= 0 and mag < 1 then 0 when mag >= 1 and mag < 2 then 1 when mag >= 2 and mag < 3 then 2 when mag >= 3 and mag < 4 then 3 when mag >= 4 and mag < 5 then 4 when mag >= 5 and mag < 6 then 5 when mag >= 6 and mag < 7 then 6 when mag >= 7 and mag < 8 then 7 when mag >= 8 and mag < 9 then 8 when mag >= 9 and mag < 10 then 9 else -1 end as ranges from database1.quake_data) t group by t.ranges order by magnitudes;"
	cur = conn.cursor()
	cur.execute(sql)

	return render_template('line_chart.html', result=cur.fetchall())


@application.route('/pie_chart', methods=["POST"])
def pie_chart():
	sql ="select t.ranges as magnitudes, count(*) as occurences from (select case when mag >= 0 and mag < 1 then 0 when mag >= 1 and mag < 2 then 1 when mag >= 2 and mag < 3 then 2 when mag >= 3 and mag < 4 then 3 when mag >= 4 and mag < 5 then 4 when mag >= 5 and mag < 6 then 5 when mag >= 6 and mag < 7 then 6 when mag >= 7 and mag < 8 then 7 when mag >= 8 and mag < 9 then 8 when mag >= 9 and mag < 10 then 9 else -1 end as ranges from database1.quake_data) t group by t.ranges order by magnitudes;"
	cur = conn.cursor()
	cur.execute(sql)
	#res = cur.fetchall()
	
	#cur.execute(sql)

	return render_template('pie_chart.html', result=cur.fetchall())
	
@application.route('/bar_chart', methods=["POST"])
def bar_chart():
	sql ="select t.ranges as magnitudes, count(*) as occurences from (select case when mag >= 0 and mag < 1 then 0 when mag >= 1 and mag < 2 then 1 when mag >= 2 and mag < 3 then 2 when mag >= 3 and mag < 4 then 3 when mag >= 4 and mag < 5 then 4 when mag >= 5 and mag < 6 then 5 when mag >= 6 and mag < 7 then 6 when mag >= 7 and mag < 8 then 7 when mag >= 8 and mag < 9 then 8 when mag >= 9 and mag < 10 then 9 else -1 end as ranges from database1.quake_data) t group by t.ranges order by magnitudes;"
	cur = conn.cursor()
	cur.execute(sql)

	return render_template('bar_chart.html', result=cur.fetchall())

@application.route('/scatter_chart', methods=["POST"])
def scatter_chart():
	sql ='SELECT mag, depth FROM quake_data order by "time1" DESC limit 100'
	cur = conn.cursor()
	cur.execute(sql)

	return render_template('scatter_chart.html', result=cur.fetchall())
	
# @application.route('/scatter_chart', methods=["POST"])
# def scatter_chart():
# 	sql = 'SELECT substring(time1, 1, 10) as date, count(*) as occurences from quake_data group by substring(time1, 1, 10) order by date'
# 	cur = conn.cursor()
# 	cur.execute(sql)
# 
# 	return render_template('scatter_chart.html', result=cur.fetchall())
	
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