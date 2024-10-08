from flask import Flask, request, jsonify, render_template
import pandas as pd
from pypmml import Model
import os

app = Flask(__name__)

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to the PMML file
pmml_path = "/home/ec2-user/app-lempira/model_lempira2.pmml"

# Load the model with error handling
try:
    modelo_lempira = Model.load(pmml_path)
except Exception as e:
    print(f"Error loading PMML model: {str(e)}")
    # You might want to exit the script here if the model can't be loaded
    # import sys
    # sys.exit(1)

# Construct the full path to the Excel file
excel_path = "/home/ec2-user/app-lempira/BDBank.xlsx"

# Load the Excel file
df = pd.read_excel(excel_path)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict')
def predict_page():
    return render_template('predict.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    id_cliente = data.get('ID_CLIENT')
    # Convertir id_cliente a número
    try:
        id_cliente = int(id_cliente)
    except (ValueError, TypeError):
        return jsonify({'Error': 'ID_CLIENT debe ser un número entero válido'}), 400
    print('data frame', df)
    cliente_data = df[df['ID_CLIENT'] == id_cliente]
    print('cliente_data', cliente_data)
    if not cliente_data.empty:
        data = cliente_data[[
            'AGE', 'AREA_CODE_RESIDENCIAL_PHONE', 'PAYMENT_DAY',
            'MONTHS_IN_RESIDENCE', 'MONTHS_IN_THE_JOB', 'PROFESSION_CODE',
            'MATE_INCOME', 'PERSONAL_NET_INCOME', 'F_SEX', 'V_MARITAL_STATUS',
            'N_FLAG_RESIDENCIAL_PHONE', 'C_RESIDENCE_TYPE',
            'N_FLAG_RESIDENCE_TOWN=WORKING_TOWN', 'N_FLAG_RESIDENCE_STATE=WORKING_STATE',
            'N_FLAG_RESIDENCIAL_ADDRESS=POSTAL_ADDRESS'
        ]]
        prediccion = modelo_lempira.predict(data)
        valor_prediccion = prediccion['predicted_TARGET_LABEL_BAD=1'].iloc[0]
        probability = prediccion['probability'].iloc[0]
        probability_BAD = prediccion['probability_BAD'].iloc[0]
        probability_GOOD = prediccion['probability_GOOD'].iloc[0]
        return jsonify({'Prediction': valor_prediccion, 'Probability':probability, 'Probability_BAD':probability_BAD, 'Probability_GOOD': probability_GOOD})
    else:
        return jsonify({'Error': 'ID_CLIENT no encontrado'}), 404

@app.route('/status', methods=['GET'])
def status():
    return jsonify({'status': 'Server is running'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
