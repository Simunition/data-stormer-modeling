from flask import Flask, request, make_response
from werkzeug.utils import secure_filename
#import cfgrib

#create flask instance
app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "static/"

#create api
@app.route('/api', methods=['GET', 'POST'])
def predict():
    #get file from request
    data = request.files['gribFile']
    filename = secure_filename(data.filename)
    data.save(app.config['UPLOAD_FOLDER'] + filename)

  #  data_xarray = cfgrib.open_datasets(data)[0]

    #code needed to take X_array, format, and send to model for prediction
    #prediction sends output that will be passed back to app for display and potential csv output

    return make_response(200)