from flask import Flask, request, jsonify, send_from_directory
import pickle
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_url_path='', static_folder='.')

@app.route('/')
def index():
    return app.send_static_file('index.html')

# Load the model
try:
    model = pickle.load(open('insurancemodelf.pkl', 'rb'))
    logger.info("Model loaded successfully")
except Exception as e:
    logger.error(f"Error loading model: {str(e)}")
    model = None

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Check if model is loaded
        if model is None:
            return jsonify({"error": "Model not loaded"}), 500

        # Get data from request
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['age', 'bmi', 'children', 'smoker']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        # Convert inputs to appropriate types
        try:
            age = int(data['age'])
            bmi = float(data['bmi'])
            children = int(data['children'])
            smoker = int(data['smoker'])
        except ValueError:
            return jsonify({"error": "Invalid input types"}), 400

        # Validate input ranges
        if age < 0 or age > 120:
            return jsonify({"error": "Age must be between 0 and 120"}), 400
        if bmi < 10 or bmi > 50:
            return jsonify({"error": "BMI must be between 10 and 50"}), 400
        if children < 0 or children > 10:
            return jsonify({"error": "Number of children must be between 0 and 10"}), 400
        if smoker not in [0, 1]:
            return jsonify({"error": "Smoker must be 0 or 1"}), 400

        # Make prediction
        input_data = [[age, bmi, children, smoker]]
        prediction = model.predict(input_data)[0]
        
        # Round prediction to 2 decimal places
        prediction = round(float(prediction), 2)
        
        return jsonify({"prediction": prediction})

    except Exception as e:
        logger.error(f"Error making prediction: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8000)