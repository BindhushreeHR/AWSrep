from flask import Flask, render_template, request, url_for
from awsdb import connect
import os, json, datetime, random
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
from collections import Counter
import requests
import csv
from collections import OrderedDict
import pandas as pd
from itertools import chain
from glob import glob

application = Flask(__name__)

deets = ["Bindhu Shree Hadya Ravi", "1001699836"]
options = { 8: 'fare', 4: 'age', 1: 'survived', 9: 'cabin', 3: 'sex', }

# default
# @application.route('/', methods=["GET"])
# def hello_world():
# 	# return render_template('index.html', result=obj)
# 	ip = requests.get('https://checkip.amazonaws.com').text.strip()
# 	print(ip)
# 	
# 	return render_template('index.html', ipaddr=ip)

@application.route('/line_chart', methods=["POST"])
def line_chart():
	sql ="select t.ranges as magnitudes, count(*) as occurences from (select case when mag >= 0 and mag < 1 then 0 when mag >= 1 and mag < 2 then 1 when mag >= 2 and mag < 3 then 2 when mag >= 3 and mag < 4 then 3 when mag >= 4 and mag < 5 then 4 when mag >= 5 and mag < 6 then 5 when mag >= 6 and mag < 7 then 6 when mag >= 7 and mag < 8 then 7 when mag >= 8 and mag < 9 then 8 when mag >= 9 and mag < 10 then 9 else -1 end as ranges from database1.quake_data) t group by t.ranges order by magnitudes;"
	cur = conn.cursor()
	cur.execute(sql)

	return render_template('line_chart.html', result=cur.fetchall())
	
@application.route('/', methods=["GET"])
def hello_world():
	# print("Every line in a file:")
# 	f = open("try.txt", "r")
# 	f1 = f.readlines()
# 	for x in f1:
# 		print(x)
# 	f.close();
# 	
#  	print("Sentences with . as delim:")
#  	result2 = []
#  	with open('data.txt', newline='') as myFile:
#  		reader = csv.reader(myFile, delimiter='.', quoting=csv.QUOTE_NONE)
#  		for row in reader:
#  			print(row)
#  			result2.append(row)
#  			
#  	print(len(result2))
#  			
  	return render_template('index.html', result = 0, deets=deets)
# 			
# 			
# 	print("Sentences with , as delim:")
# 	with open('csv2.csv', newline='') as myFile:
# 		reader2 = csv.reader(myFile, delimiter=',', quoting=csv.QUOTE_NONE)
# 		for row2 in reader2:
# 			print(row2)
# 			
# 	
# 	print("Words in a file:")
# 	with open('csv3.csv','r') as file:
# 		for line in file:
# 			for word in line.split():
# 				print(word)
	
@application.route('/str', methods=["POST"])
def top_words20():
	num = int(request.form["num"])
	
	
	return render_template('top.html', result = freq, deets=deets)
	
	
	
	
def xb(filename):
    lines = set(chain.from_iterable(open(f, encoding='utf-8') for f in glob('./'+filename+".txt")))
    lines = [line.lower() for line in lines]
    
    g = ""
    for l in lines:
#         print(type(l),l)
        if ". " in l:
            l = l.replace(". ", "\n")
        if "." in l:
            l = l.replace(".", "\n")
        if "," in l:
            l =  l.replace(",", " ")
#         if "'" in l:
#             l =  l.replace(",", " ")
        g = g + l
#     g.replace("  "," ")


    with open(filename+'g.txt', 'w') as out:
        out.writelines((g))
         
    #Read processed data
#     lines = set(chain.from_iterable(open(f) for f in glob('./datag.txt')))
    f = open(filename+'g.txt',"r")
     
    lines = f.readlines()
    
    return lines





@application.route('/bot', methods=["POST"])
def top_words4():
	r = []
	lines = xb("Alamo")
	for l in lines:
		if any(char.isdigit() for char in l):
			print("here")
			r.append(l)
	
	return render_template('index.html', result = r, deets=deets)
	
	
@application.route('/bot2', methods=["POST"])
def top_words49():
	name = request.form["name"]
	r = []
	lines = xb("Alamo")
	for l in lines:
		if name in l:
			#print("here")
			r.append(l)
	
	return render_template('index.html', result = r, deets=deets)
	
@application.route('/top2', methods=["POST"])
def top_words2():
	num = int(request.form["num"])
	result3 = []
	count = []
	found = []
	counts = dict()
	
	print("Words in a file:")
	with open('Alamo.txt','r') as file:
		for line in file:
			for word in line.split():
				#print(word)
				word = word.lower()
				result3.append(word)


	for word in result3:
		counts[word] = result3.count(word)
	
	print("OCCURRANCES")	
	#print(counts)

	a = OrderedDict(sorted(counts.items(), key=lambda x: x[1], reverse=False))
	
	#print(a)
	#a = a[:20]
	#print(a)
	
	freq = list(a)[:num]
	
	print("Least N words")
	print(freq)

	return render_template('top.html', result = freq, deets=deets)
	
@application.route('/all', methods=["POST"])
def all():
	result4 = []
	sql = """select * from SpanishStopWords"""
	print(sql)
	cursor = connect.cursor()
	cursor.execute(sql)
	
	result2=cursor.fetchall()
	
	result3 = []
	with open('Alamo.txt','r') as file:
		for line in file:
			for word in line.split():
				#print(word)
				word = word.lower()
				result3.append(word)
				
	result2 = pd.DataFrame(list(result2))
	result2[0] = result2[0].str.strip('\r')
	stoplist = list(result2[0])
    
	#print(result3)
	#print(stoplist)
	for i in stoplist:
		#print(i)
		
		if i in result3:
# 			pri# nt("i")
# # 			print(i)
			#print("j")
			#print(j)
# 			if i == j:
			result4.append(i)
	
	#print(result4)
	
# 	counts = dict()
	
	# print("Words in a file:")
# 	with open('data.txt','r') as file:
# 		for line in file:
# 			for word in line.split():
# 				#print(word)
# 				word = word.lower()
# 				result2.append(word)
# 
# 
# 	for word in result2:
# 		counts[word] = result2.count(word)
# 	
# 	print("OCCURRANCES")	
# 	print(counts)
# 
# 	a = OrderedDict(sorted(counts.items(), key=lambda x: x[1], reverse=True))
# 	
# 	#print(a)
# 	#a = a[:20]
# 	#print(a)
# 	
# 	freq = list(a.keys())[:num]
# 	
# 	print("TOP 20 words")
# 	print(freq)

	return render_template('index.html', result=result4, deets=deets)
	
@application.route('/top', methods=["POST"])
def top_words():
	num = int(request.form["num"])
	result2 = []
	count = []
	found = []
	counts = dict()
	
	print("Words in a file:")
	with open('data.txt','r') as file:
		for line in file:
			for word in line.split():
				#print(word)
				word = word.lower()
				result2.append(word)


	for word in result2:
		counts[word] = result2.count(word)
	
	print("OCCURRANCES")	
	print(counts)

	a = OrderedDict(sorted(counts.items(), key=lambda x: x[1], reverse=True))
	
	#print(a)
	#a = a[:20]
	#print(a)
	
	freq = list(a.keys())[:num]
	
	print("TOP 20 words")
	print(freq)

	return render_template('top.html', result = freq, deets=deets)
	
@application.route('/word', methods=["POST"])
def word_search():
	words = request.form["word"]
	num = int(request.form["num"])
	result2 = []
	count = []
	found = []
	counts = dict()
	print(words)
	print("Words in a file:")
	with open('data.txt','r') as file:
		for line in file:
			for word in line.split():
				#print(word)
				word = word.lower()
				result2.append(word)
				
	for i in range(0,len(result2)):
		if result2[i] == words:
			print("********* Found")
			print(result2[i])
			found.append(result2[i+num])

	for word in result2:
		counts[word] = result2.count(word)
	
	print("OCCURRANCES")	
	print(counts)
	
	a = OrderedDict(sorted(counts.items(), key=lambda x: x[1], reverse=True))
	
	freq = list(a.keys())[:num]
	
	print("TOP words")
	print(freq)
	
	return render_template('index.html', result = found, deets=deets)
	

@application.route('/calc', methods=["POST"])
def calc():
    datehere = datetime.datetime.now()
    print(datehere)
    d1 = request.form["numberuno"]
    d2 = request.form["numberdo"]
    op = request.form["op"]
    
    result = 0
    
    if d1 is "" :
        print("here1")
        result = "invalid"
        return render_template('index.html', result = result, datehere= datehere)
    
    if d2 is "" :
        print("here2")
        result = "invalid"
        return render_template('index.html', result = result, datehere= datehere)
    
    if op is "" or (op != "+" and op != "*" and op != "/" and op != "-" and op != "!" and op != "%") :
        print("here3")
        result = "invalid"
        return render_template('index.html', result = result, datehere= datehere)
    
    if op == "+":
        result = float(d1) + float(d2)
        return render_template('index.html', result = result, datehere= datehere)
    elif op == "*":
        result = float(d1) * float(d2)
        return render_template('index.html', result = result, datehere= datehere)
    elif op == "-":
        result = float(d1) - float(d2)
        return render_template('index.html', result = result, datehere= datehere)
    elif op == "/":
        result = float(d1) / float(d2)
        return render_template('index.html', result = result, datehere= datehere)
    elif op == "%":
        result = float(d1) % float(d2)
        return render_template('index.html', result = result, datehere= datehere)
    elif op == "!":
        result = math.factorial(float(d1))
        return render_template('index.html', result = result, datehere= datehere)
    
    return render_template('index.html', result = result, datehere= datehere)
	
@application.route('/cal2', methods=["POST"])
def stringvalue2():
	clusterno = int(request.form['number1'])
	r1 = int(request.form['number1'])
	r2 = int(request.form['number2'])

	column1 = int(request.form['column1'])
	
	
	return render_template('index.html', result=r3, errm=err)

@application.route('/fact', methods=["POST"])
def fact():
	r1 = int(request.form['number1'])
	#print(r1)
	#r2 = int(request.form['number2'])
	err = ''
	r3 = 0
	
	if r2 <= 0:
		err = "Enter number > 0"
	else:
		for i in range (1,int(n)+1):
   			factorial = factorial * i

	return render_template('index.html', result=factorial, errm=err)
		
@application.route('/div', methods=["POST"])
def div():
	r1 = int(request.form['number1'])
	#print(r1)
	r2 = int(request.form['number2'])
	err = ''
	r3 = 0
	
	if r2 == 0:
		err = "Divide by 0"
	else:
		r3 = r1/r2

	return render_template('index.html', result=r3, errm=err)
	
	
@application.route('/add', methods=["POST"])
def add():
	r1 = int(request.form['number1'])
	#print(r1)
	r2 = int(request.form['number2'])
	#print(r2)
	r3 = r1+r2
	err = ''
	#print(r3)

	return render_template('index.html', result=r3, errm=err)
	
@application.route('/mul', methods=["POST"])
def mul():
	r1 = int(request.form['number1'])
	#print(r1)
	r2 = int(request.form['number2'])
	#print(r2)
	r3 = r1*r2
	err = ''
	#print(r3)

	return render_template('index.html', result=r3, errm=err)
	
@application.route('/mod', methods=["POST"])
def mod():
	r1 = int(request.form['number1'])
	#print(r1)
	r2 = int(request.form['number2'])
	err = ''
	r3 = 0
	if r2 == 0:
		err = "Modulo by 0"
	else:
		r3 = r1%r2
	#print(r2)
	#print(r3)

	return render_template('index.html', result=r3, errm=err)


@application.route('/pieq_chart', methods=["POST"])
def pieq_chart():
	r1 = request.form["r1"]
	r2 = request.form["r2"]
	r1 = str(int(r1)*100000)
	r2 = str(int(r2)*100000)
	year = "y"+request.form["year"]
	sql = """select State , {} from sp where {} between {} and {}""".format(year,year,r1,r2)
	print(sql)
	cursor = connect.cursor()
	cursor.execute(sql)
	#print(cursor.fetchone())
	
	return render_template('pieq_chart.html', result=cursor.fetchall())
    

@application.route('/barq_chart', methods=["POST"])
def barq_chart():
    partition = request.form["part"]
    year = request.form["year"]
    year_s = "y"+str(year)
    sql1 = "select MAX({}) from sp;".format(year_s)
    cursor = connect.cursor()
    cursor.execute(sql1)
    s = cursor.fetchall()
    print(round(float(s[0][0]),-3))
    max_pop = int(round(float(s[0][0]),-3))
    incr = int(max_pop / int(partition))
    print(incr)
   
    sql2 = """select t.ranges as magnitudes, count(*) as occurences from (
        select case"""
           
    sql3 = """        else -1 end as ranges
        from sp) t
    group by t.ranges order by magnitudes;"""
   
   
    sql4 = ""
    x = 0
    for i in range(0, max_pop, incr):
        sql4 = sql4 + " when {} >= {} and {} < {} then {}".format(year_s,i,year_s, i+incr, x )
        x = x+incr
       
    sql = sql2 + sql4 + sql3
   
    print(sql)
   
    cursor = connect.cursor()
    cursor.execute(sql)
   
    return render_template('barq_chart.html', result=cursor.fetchall(), inr = incr)
    
@application.route('/pie_chart', methods=["POST"])
def pie_chart():
	year = request.form['year']
	pop = request.form['pop'] * 100000
	sql ="select t.ranges as magnitudes, count(*) as occurences from (select case when mag >= 0 and mag < 1 then 0 when mag >= 1 and mag < 2 then 1 when mag >= 2 and mag < 3 then 2 when mag >= 3 and mag < 4 then 3 when mag >= 4 and mag < 5 then 4 when mag >= 5 and mag < 6 then 5 when mag >= 6 and mag < 7 then 6 when mag >= 7 and mag < 8 then 7 when mag >= 8 and mag < 9 then 8 when mag >= 9 and mag < 10 then 9 else -1 end as ranges from database1.quake_data) t group by t.ranges order by magnitudes;"
	cur = conn.cursor()
	cur.execute(sql)
	#res = cur.fetchall()
	
	#cur.execute(sql)

	return render_template('pie_chart.html', result=cur.fetchall())

# @application.route('/pie_chart', methods=["POST"])
# def pie_chart():
# 	sql ="select t.ranges as magnitudes, count(*) as occurences from (select case when mag >= 0 and mag < 1 then 0 when mag >= 1 and mag < 2 then 1 when mag >= 2 and mag < 3 then 2 when mag >= 3 and mag < 4 then 3 when mag >= 4 and mag < 5 then 4 when mag >= 5 and mag < 6 then 5 when mag >= 6 and mag < 7 then 6 when mag >= 7 and mag < 8 then 7 when mag >= 8 and mag < 9 then 8 when mag >= 9 and mag < 10 then 9 else -1 end as ranges from database1.quake_data) t group by t.ranges order by magnitudes;"
# 	cur = conn.cursor()
# 	cur.execute(sql)
# 	#res = cur.fetchall()
# 	
# 	#cur.execute(sql)
# 
# 	return render_template('pie_chart.html', result=cur.fetchall())


@application.route('/partition', methods=["POST"])
def partition():
	year = request.form['year']
	parts = request.form['part']
	sql ="select t.ranges as magnitudes, count(*) as occurences from (select case when mag >= 0 and mag < 1 then 0 when mag >= 1 and mag < 2 then 1 when mag >= 2 and mag < 3 then 2 when mag >= 3 and mag < 4 then 3 when mag >= 4 and mag < 5 then 4 when mag >= 5 and mag < 6 then 5 when mag >= 6 and mag < 7 then 6 when mag >= 7 and mag < 8 then 7 when mag >= 8 and mag < 9 then 8 when mag >= 9 and mag < 10 then 9 else -1 end as ranges from database1.quake_data) t group by t.ranges order by magnitudes;"
	cur = conn.cursor()
	cur.execute(sql)

	return render_template('bar_chart.html', result=cur.fetchall())
		
# @application.route('/bar_chart', methods=["POST"])
# def bar_chart():
# 	sql ="select t.ranges as magnitudes, count(*) as occurences from (select case when mag >= 0 and mag < 1 then 0 when mag >= 1 and mag < 2 then 1 when mag >= 2 and mag < 3 then 2 when mag >= 3 and mag < 4 then 3 when mag >= 4 and mag < 5 then 4 when mag >= 5 and mag < 6 then 5 when mag >= 6 and mag < 7 then 6 when mag >= 7 and mag < 8 then 7 when mag >= 8 and mag < 9 then 8 when mag >= 9 and mag < 10 then 9 else -1 end as ranges from database1.quake_data) t group by t.ranges order by magnitudes;"
# 	cur = conn.cursor()
# 	cur.execute(sql)
# 
# 	return render_template('bar_chart.html', result=cur.fetchall())

@application.route('/scatter_chart', methods=["POST"])
def scatter_chart():
	year1 = request.form['year1']
	year2 = request.form['year2']
	name = request.form['name']
	sql = 'SELECT * from sp'
	
	cur = connect.cursor()
	cur.execute(sql)

	return render_template('scatter_chart.html', result=cur.fetchall())
	
# @application.route('/scatter_chart', methods=["POST"])
# def scatter_chart():
# 	numlimit = request.form['numlimit']
# 	sql ='SELECT mag, depth FROM quake_data order by "time1" DESC limit ' + numlimit + ''
# 	cur = conn.cursor()
# 	cur.execute(sql)
# 
# 	return render_template('scatter_chart.html', result=cur.fetchall())
	
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