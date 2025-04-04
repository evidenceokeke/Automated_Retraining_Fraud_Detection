import joblib
import pandas as pd
import boto3
from flask import Flask, jsonify, request
from prometheus_client import make_wsgi_app, Counter, Gauge, Histogram
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
from flask_prometheus_metrics import register_metrics

# Initialize the flask application
app = Flask(__name__)

# Initialize Prometheus metrics
register_metrics(app, app_version="v1.0", app_config="production")

# Initialize Prometheus custom metrics
# Counter for error counts
error_count = Counter('error_count', 'Number of API errors')

# Gauge for tracking fraudulent predictions
fraud_rate = Gauge('fraud_rate', 'Fraction of fraudulent predictions')

# Histogram for tracking prediction latency (in secs)
prediction_latency = Histogram('prediction_latency_seconds', 'Prediction latency in seconds')

# Initialize boto3 client for AWS S3
s3 = boto3.client('s3')

# Download the model from S3
s3.download_file('cc-fraud-detection-model-dataset', 'fraud_pipeline.pkl', 'fraud_pipeline.pkl')

# Load the model
try:
    model = joblib.load('fraud_pipeline.pkl')
    print(model.classes_)
except Exception as e:
    raise RuntimeError(f"Failed to load model: {str(e)}") from e


@app.route('/predict', methods=['POST'])
def predict():
    # Get the data from the request
    try:
        data = request.get_json()
    except Exception as  e:
        return jsonify({"error": f"No input data provided: {str(e)}"}), 400

    # Convert data to a df
    try:
        data_df = pd.DataFrame([data])
    except Exception as e:
        return jsonify({"error": f"Failed to process data: {str(e)}"}), 400

    # Make predictions with the model, get the probabilities for each class (0 and 1)
    try:
        predictions = model.predict_proba(data_df)
    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500

    # The probability of 1 (fraud detection)
    fraud_probability = predictions[0][1].tolist()

    return jsonify({"fraud_probability": fraud_probability})


# Create a Prometheus metrics endpoint using WSGI
metrics_app = make_wsgi_app()

# Use DispatcherMiddleware to serv both Flask and Prometheus metrics under the same port
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': metrics_app
})

# Run the app using run_simple (for deployment purposes)
if __name__ == '__main__':
    run_simple('localhost', 5000, app)