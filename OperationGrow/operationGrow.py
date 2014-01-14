#!c:/Python27/python.exe -u

from flask import Flask, render_template, request
import growMoisture, growConfig, growLogger, growCommon, growServer
app = Flask(__name__)

@app.route("/")
def dashboard():
    return "Dashboard"

@app.route("/log", methods=['GET'])
def log():
    f = file(growLogger.filename, 'r')
    messages = f.readlines()
    return render_template('log.html', messages=messages)

@app.route("/moisture/<int:plant>", methods=['GET'])
def moisture(plant):
    c = growConfig.Configuration()
    names = c.getNames()
    
    return render_template('graph.html', plant=plant, names=names)

@app.route("/currentMoisture/<int:plant>", methods=['GET'])
def currentMoisture(plant):
    return '%d' % 233

@app.route("/moistureData/<int:plant>", methods=['GET'])
def moistureData(plant):
    m = growMoisture.Moisture(plant)
    return '%s' % m.read()

@app.route("/dryLevel/<int:plant>", methods=['POST'])
def dryLevel(plant):
    return 'Success' + request.form['moisture']

@app.route("/configuration", methods=['POST'])
def setConfiguration():
    c = growConfig.Configuration()
    
    for i in range(0,growCommon.NUM_PLANTS):
        if ('enabled%d' % i) in request.form:
            enabled = 1
        else:
            enabled = 0
        
        c.push(
            i,
            request.form['name%d' % i],
            enabled,
            int(request.form['dry%d' % i])
            )

    return '', 200

@app.route("/configuration", methods=['POST', 'GET'])
def getConfiguration():
    c = growConfig.Configuration()
    
    if request.method == 'POST':
        for i in range(0,2):
            c.push(
                i,
                request.form['name%d' % i],
                request.form['enabled%d' % i],
                request.form['dry%d' % i]
                )

        return '', 200
    else:
        configTable = c.read()
        
        return render_template('configuration.html', configTable = configTable, configSize = len(configTable), NUM_PLANTS = growCommon.NUM_PLANTS)

if __name__ == "__main__":
    growServer.init()
    app.run(host='0.0.0.0', debug=True)
