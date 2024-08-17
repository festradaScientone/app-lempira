from flask import Flask, request, jsonify
import pandas as pd
from pypmml import Model

app = Flask(__name__)

# Cargar el modelo PMML
modelo_lempira = Model.load('/path/to/model_lempira2.pmml')

# Cargar el archivo Excel
df = pd.read_excel('/path/to/BDBank.xlsx')

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
        return jsonify({'Prediction': valor_prediccion})
    else:
        return jsonify({'Error': 'ID_CLIENT no encontrado'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
