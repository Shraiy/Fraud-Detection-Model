from flask import Flask, request, render_template
import joblib
import pandas as pd

# Load the trained model
model = joblib.load('model.pkl')

# Initialize the Flask application
app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html', prediction=None)

@app.route('/predict', methods=['POST'])
def predict():
    # Get input data from the form
    selected_type = request.form['type_PAYMENT']
    # Get input data from the form and convert to appropriate types
    input_data = {
        'step': float(request.form['step']),
        'amount': float(request.form['amount']),
        'oldbalanceOrg': float(request.form['oldbalanceOrg']),
        'newbalanceOrig': float(request.form['newbalanceOrig']),
        'oldbalanceDest': float(request.form['oldbalanceDest']),
        'newbalanceDest': float(request.form['newbalanceDest']),
        
        # Initialize values directly in the code
        'isFlaggedFraud': 0,  # Set this to a constant value
        'type_CASH_IN': 0,    # Set this to a constant value
        'type_CASH_OUT': 0,   # Set this to a constant value
        'type_DEBIT': 0,      # Set this to a constant value
        'type_PAYMENT': 0,    # Set this to a constant value
        'type_TRANSFER': 0     # Set this to a constant value
    }

    # Set the selected payment type to 1
    if selected_type == 'CASH_IN':
        input_data['type_CASH_IN'] = 1
    elif selected_type == 'CASH_OUT':
        input_data['type_CASH_OUT'] = 1
    elif selected_type == 'DEBIT':
        input_data['type_DEBIT'] = 1
    elif selected_type == 'TRANSFER':
        input_data['type_TRANSFER'] = 1
    elif selected_type == 'PAYMENT':
        input_data['type_PAYMENT'] = 1

    # Convert input data to DataFrame
    data_df = pd.DataFrame([input_data])

    # Make predictions
    prediction = model.predict(data_df)

    # Render the result on the page
    return render_template('index.html', prediction=prediction[0])


if __name__ == '__main__':
    app.run(debug=True)
