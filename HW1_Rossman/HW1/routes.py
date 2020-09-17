import flask
from flask import Flask, request, render_template
from sklearn.externals import joblib
import numpy as np

app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
    return flask.render_template('index.html')


@app.route('/predict', methods=['POST'])
def make_prediction():
	if request.method=='POST':

		entered_li = []


		# ---YOUR CODE FOR Part 2.2.3 ----  

		# Define "day", "open", "prn", "state", "school", and "store" variables



		# --- THE END OF CODE FOR Part 2.2.3 --- 

		# StoreType, Assortment, CompetitionDistance... arbitrary values
		for val in [1, 1, 290.0, 10.0, 2011.0, 1, 40.0, 2014.0, 0, 0, 0]:
			entered_li.append(val)


		# ---YOUR CODE FOR Part 2.2.4 ---- 
		
		# Predict from the model




		# --- THE END OF CODE FOR Part 2.2.4 --- 
		
		label = str(np.squeeze(prediction.round(2)))

		return render_template('index.html', label=label)


if __name__ == '__main__':

	# ---YOUR CODE FOR Part 2.2.1 ----  
	
	#Load ML model



	# --- THE END OF CODE FOR Part 2.2.1 --- 

	# start API
	app.run(host='0.0.0.0', port=8000, debug=True)


