from flask import Flask, jsonify , request , send_file
from werkzeug.utils import secure_filename
from flask import Flask, render_template
import requests
import json
from MLRFID_Script_Complet import result
from MLRFID_Script_Complet import RandomForestML
from MLRFID_Script_Complet import logistic_regression
from MLRFID_Script_Complet import train_svc_model
from MLRFID_Script_Complet import knn_classifier
from MLRFID_Script_Complet import compare_resultats
import pandas as pd
import os
import matplotlib.pyplot as plt


app = Flask(__name__, static_folder="C:\\Users\\ROUCH\\source\\repos\\Safietoundoye\\PROJET\\Images")

@app.route('/analytical', methods=['POST'])
def analytical_route():

    # Call the predict() function to make a prediction
    analytic = result()
    # Return the prediction as JSON
    return jsonify({'analytic': analytic})


@app.route('/RFClassifier', methods=['POST'])
def analyticalWithParams_route():
    # Charger les DataFrames a partir des fichiers CSV
    params1 = request.get_json()
    # Call the predict() function to make a prediction
    MLRF = RandomForestML(int(params1['Hyperparameter1']), int(params1['Hyperparameter2']))
    # Return the prediction as JSON
    return jsonify({'MLRF': MLRF})


@app.route('/LRClassifier', methods=['POST'])
def LRClassifier_route():
    # Charger les DataFrames a partir des fichiers CSV
    params2 = request.get_json()
    # Call the predict() function to make a prediction
    MLLR = logistic_regression(params2['Hyperparameter1'], float(params2['Hyperparameter2']), params2['Hyperparameter3'])
    # Return the prediction as JSON
    return jsonify({'MLLR': MLLR})


@app.route('/SVCClassifier', methods=['POST'])
def SVCClassifier_route():
    # Charger les DataFrames a partir des fichiers CSV
    params3 = request.get_json()
    # Call the predict() function to make a prediction
    MLSVC = train_svc_model(params3['Hyperparameter1'], float(params3['Hyperparameter2']), float(params3['Hyperparameter3']), int(params3['Hyperparameter4']), int(params3['Hyperparameter5']), float(params3['Hyperparameter6']))
    # Return the prediction as JSON
    return jsonify({'MLSVC': MLSVC})

@app.route('/KNNClassifier', methods=['POST'])
def KNNClassifier_route():
    # Charger les DataFrames a partir des fichiers CSV
    params4 = request.get_json()
    # Call the predict() function to make a prediction
    MLKNN = knn_classifier(int(params4['Hyperparameter1']), params4['Hyperparameter2'], params4['Hyperparameter3'], params4['Hyperparameter4'])
    # Return the prediction as JSON
    return jsonify({'MLKNN': MLKNN})

@app.route('/Graph', methods=['POST'])
def Graph_route():
     #Charger les DataFrames a partir des fichiers CSV
    params = request.get_json()
     #Call the predict() function to make a prediction
    Nom_methode = []
    Valeur_resultats = []
    Nom_methode.clear()
    Valeur_resultats.clear()


    if params['Hyperparameter1'] == "1" :
        Nom_methode.append("Analytical")
        analytic = result()
        Valeur_resultats.append(analytic)

    if params['Hyperparameter2'] == "1" :
        Nom_methode.append("RandomForestML")
        MLRF = RandomForestML(int(params['Hyperparameter3']), int(params['Hyperparameter4']))
        Valeur_resultats.append(MLRF)

    if params['Hyperparameter5'] == "1" :
        Nom_methode.append("logistic_regression")
        MLLR = logistic_regression(params['Hyperparameter6'], float(params['Hyperparameter7']), params['Hyperparameter8'])
        Valeur_resultats.append(MLLR)

    if params['Hyperparameter9'] == "1" :
        Nom_methode.append("train_svc_model")
        MLSVC = train_svc_model(params['Hyperparameter10'], float(params['Hyperparameter11']), float(params['Hyperparameter12']), int(params['Hyperparameter13']), int(params['Hyperparameter14']), float(params['Hyperparameter15']))
        Valeur_resultats.append(MLSVC)

    if params['Hyperparameter16'] == "1" :
        Nom_methode.append("knn_classifier")
        MLKNN = knn_classifier(int(params['Hyperparameter17']), params['Hyperparameter18'], params['Hyperparameter19'], params['Hyperparameter20'])
        Valeur_resultats.append(MLKNN)

    Graph = compare_resultats(Valeur_resultats, Nom_methode)

    #os.remove("C:\\Users\\ROUCH\\source\\repos\\Safietoundoye\\PROJET\\Images\\Graph.png")
    filename = 'Graph.png'
    Images = os.path.join(app.static_folder, filename)

    plt.savefig(Images)

    return send_file(Images, mimetype='image/png')



app.run(host='0.0.0.0', port=5000)


