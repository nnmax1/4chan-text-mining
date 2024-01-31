import os
from flask import Flask
from flask import url_for, redirect, render_template, flash, g, session,request,jsonify
 
from data_api import DataAPI
from word_frequency import wordFrequency
from sentiment_analysis import mostPositiveNegativePosts

# very simple and bad flask web server. 

app = Flask(__name__)

DATABASE_FILE = 'data.db'


@app.route('/')
def index():
	dataapi = DataAPI(DATABASE_FILE)
	data=dataapi.databaseCounter()
	max=len(data['data'])
	return render_template('index.html',data=data,max=max)

@app.route('/wordFrequency')
def wordFrequencyData():
	wordfreqs=wordFrequency(DATABASE_FILE) 
	wordfreqs=wordfreqs[0:200]
	return jsonify(wordfreqs)
@app.route('/most/<pos>/posts')
def mostPosOrNegPosts(pos):
	data=[]
	if pos=='neg' or pos =='pos':
		data=mostPositiveNegativePosts(DATABASE_FILE,pos)
		max=len(data)
		return render_template('posts.html',posts=data, max=max,board=pos,pagetype='sentdata')
	return redirect('/')
	#return jsonify(data)


@app.route('/data/<board>')
def posts(board):
	dataapi = DataAPI(DATABASE_FILE)
	if board not in dataapi.boards:
		return redirect('/')
	post_arr=dataapi.getPostsFromBoard(board)
	max=len(post_arr)
	return render_template('posts.html',posts=post_arr,max=max,board=board,pagetype='data')

from flask import send_file

# e.g) 127.0.0.1:5000/image?filename=wordcloud.png
@app.route('/image')
def get_image():
	images=['word_freq_bar','word_freq_pie','wordcloud','sentiment_bar']
	filename=request.args.get('filename')
	ext=''
	if filename in images :
		ext='png'
		filename = str(filename)+'.png'
	else:
		return redirect('/')
	print(filename)
	return send_file('./'+ext+'/'+filename, mimetype='image/'+ext)

if __name__ == "__main__":
	app.run()