import os.path
import requests


from flask import Flask, request, send_file, make_response, Response
from werkzeug.utils import secure_filename
from model_deployment.ModelClass import WeatherPredictor

#create flask instance
app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "static/"

APP_URL = "http://127.0.0.1:5000"

#create api
@app.route('/api', methods=['GET', 'POST'])
def predict():
    #get file from request
    data = request.files['gribFile']
    filename = secure_filename(data.filename)
    data.save(app.config['UPLOAD_FOLDER'] + filename)
    #
    predictor = WeatherPredictor('../model_deployment/regr_model.joblib')
    predictor.make_prediction(os.path.join("static/", filename))
    csv_out = predictor.output_csv() #outputs CSV with filename as input
    png_out = predictor.plot_geopotential_height() #plots the prediction

    # make a request to /submitCsvOut using requests.post
    r = requests.post(APP_URL + '/submitCsvOut', files={'csvOut':open(csv_out,"rb")})
    # ex: requests.post(url, files={'gribFile': open(f_location,'rb')})

    # make a request to /submitPngOut using requests.post
    q = requests.post(APP_URL + '/submitPngOut', files={'pngOut':open(png_out,"rb")})

    # return a 200 response with make_response, and delete the send file response below


    return "OK"





    #code needed to take X_array, format, and send to model for prediction
    #prediction sends output that will be passed back to app for display and potential csv output


