from flask import Flask, request, jsonify, render_template
import pandas as pd
from pypmml import Model
import os

app = Flask(__name__)

# ... (keep your existing code for loading the model and Excel file)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    id_cliente = data.get('ID_CLIENT')
    cliente_data = df[df['ID_CLIENT'] == id_cliente]
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
        return jsonify({'Prediction': float(valor_prediccion)})
    else:
        return jsonify({'Error': 'ID_CLIENT no encontrado'}), 404

@app.route('/status', methods=['GET'])
def status():
    return jsonify({'status': 'Server is running'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)