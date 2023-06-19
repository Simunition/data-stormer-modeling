import os
import requests


from flask import Flask, request, send_file, make_response, Response
from werkzeug.utils import secure_filename
from model_deployment.ModelClass import WeatherPredictor

#create flask instance
app = Flask(__name__)

UPLOAD_FOLDER = "static/"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Check if the upload folder exists, create it if necessary
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

APP_URL = "https://data-detectives.herokuapp.com/"

#create api
@app.route('/api', methods=['GET', 'POST'])
def predict():
    #get file from request
    data = request.files['gribFile']
    filename = secure_filename(data.filename)
    data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    #
    predictor = WeatherPredictor('regr_model.joblib')
    predictor.make_prediction(os.path.join(UPLOAD_FOLDER, filename))
    csv_out = predictor.output_csv() #outputs CSV with filename as input
    png_out = predictor.plot_geopotential_height() #plots the prediction

    # make a request to /submitCsvOut using requests.post
    with open(csv_out, "rb") as f:
        r = requests.post(APP_URL + '/submitCsvOut', files={'csvOut': f})

    # make a request to /submitPngOut using requests.post
    with open(png_out, "rb") as f:
        q = requests.post(APP_URL + '/submitPngOut', files={'pngOut': f})

    # return a 200 response with make_response, and delete the send file response below


    return "OK"





    #code needed to take X_array, format, and send to model for prediction
    #prediction sends output that will be passed back to app for display and potential csv output

