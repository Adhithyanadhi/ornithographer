import flask
import requests
from flask import Flask, render_template, request
import os, random
from fastai.vision import load_learner, open_image
import pandas as pd

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
target = os.path.join("static")
destination = "/".join([target, "temp.jpg"])

@app.route('/')
def home():
    return render_template('index.html')


def is_url(image_url):
    image_formats = ("image/png", "image/jpeg", "image/jpg")
    r = requests.head(image_url)
    if r.headers["content-type"] in image_formats:
        return True
    return False

@app.route('/upload_url', methods=['POST', 'GET'])
def upload_url():
	url = request.form['url']
	if(len(url) > 1000):
		return render_template('error.html', error="URL length too large to parse")
	elif is_url(url):
	    response = requests.get(url)
		file = open(destination, "wb")
		file.write(response.content)
		file.close
		img = open_image(destination)
	    print("image saved")
		return predict_bird_name(img)
	else:
		return render_template('error.html', error="invalid url")

@app.route('/upload', methods=['GET', 'POST'])
def upload():
	imagefile = request.files.get("img")
	imagefile.save(destination);
	img = open_image(destination)
	return predict_bird_name(img)

def predict_bird_name(img):
	learn = load_learner("model/")
	pred_class, pred_idx, outputs = learn.predict(img)
	predictions = []
	cnt = 0

	for image_class, output in zip(learn.data.classes, outputs.tolist()):
		output = round(output, 2)*100
		predictions.append({ "class": image_class.upper(), "probability": output})

	predictions = sorted(predictions, key=lambda x: x["probability"], reverse=True)
	predictions = predictions[0:3]
	result = []

	for x in predictions:
		if x["probability"] > 0 and cnt < 3:
			cnt = cnt +1;
			result.append(x);
	print(result)
	if(result[0]["probability"] >= 50):
		result = result[0:1]
		cnt = 1
	else:
		result = result[0:cnt]

	datasetLocation = "/mnt/c/PythonVirtualEnvironment/bird/taxonamy.xlsx"
	df = pd.read_excel(datasetLocation,"taxonamy",engine='openpyxl')
	bird = result[0]['class']
	data = df[df["Bird"] == bird]
	
	print(data)

	if cnt == 1:
		return render_template('result1.html', predictions = result[0]['probability'], data=data.values.tolist())
	elif cnt == 2:
		return render_template('result2.html', img2 = "./static/1bird1pic/" + result[1]['class'] + "/1.jpg", predictions = result, data=data.values.tolist())
	else:
		return render_template('result3.html', img2 = "./static/1bird1pic/" + result[1]['class'] + "/1.jpg", img3 = "./static/1bird1pic/" + result[2]['class'] + "/1.jpg",  data=data.values.tolist(), predictions = result)
if __name__ == '__main__':
    app.run(debug=True)

