from flask import Flask, request, render_template, Response
from util_functions import wind_dataframe, solar_dataframe
from werkzeug.utils import secure_filename
from dashboard import my_dash_app
import os






server = Flask(__name__)
app = my_dash_app(server)

##My Dashboard App runs at http://127.0.0.1:5001/mydashboard/

@app.route('/upload_csv', methods = ['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/wind_uploader', methods=['GET', 'POST'])
def wind_uploader():
    if request.method == 'POST':
        file = request.files['csvfile']
        wind_data = secure_filename(file.filename)
        file.save(os.path.join('maintenance_files', wind_data))
        return render_template('index.html', message = "Wind Maintenance Schedule was uploaded successful")

@app.route('/solar_uploader', methods=['GET', 'POST'])
def solar_uploader():
    if request.method == 'POST':
        file = request.files['csvfile']
        solar_data = secure_filename(file.filename)
        file.save(os.path.join('maintenance_files', solar_data))
        return "Solar Maintenance Schedule was successful uploaded"

@app.route("/wind_farm_predictions", methods=["GET"])
def wind_predictions():
    x = wind_dataframe()
    dates = list(x.index.strftime("%Y/%m/%d"))
    predictions = x['Power_Output_Predictions']
    result = dict(zip(dates, predictions))
    return result


@app.route("/solar_plant_predictions", methods=["GET"])
def solar_predictions():
    x = solar_dataframe()
    dates = list(x.index.strftime("%Y/%m/%d"))
    predictions = x['Power_Output_Predictions']
    result = dict(zip(dates, predictions))
    return result


if __name__ == '__main__':
    app.run(port=5001, debug=True)
