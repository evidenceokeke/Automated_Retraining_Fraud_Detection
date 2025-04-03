# Import the necessary libraries
import numpy as np
import pandas as pd
import random
import joblib
import boto3

# Set the random seed for reproducibility
random.seed(42)
np.random.seed(42)

# Initialize boto3 client for AWS S3
s3 = boto3.client('s3')

# Download the "new data" from S3
s3.download_file('cc-fraud-detection-model-dataset', 's3://cc-fraud-detection-model-dataset/dataset/X_new.csv', 'dataset/X_new.csv')
s3.download_file('cc-fraud-detection-model-dataset', 's3://cc-fraud-detection-model-dataset/dataset/y_new.csv', 'dataset/y_new.csv')

# Load the dataset
X_new = pd.read_csv('dataset/X_new.csv')
y_new = pd.read_csv('dataset/y_new.csv')

# Download the original model from S3
s3.download_file('cc-fraud-detection-model-dataset', 's3://cc-fraud-detection-model-dataset/fraud_pipeline.pkl', 'fraud_pipeline.pkl')

# Load the model
model = joblib.load('fraud_pipeline.pkl')

# Retrain model on new data (fine-tune)
model.fit(X_new, y_new)

# Save the updated model
joblib.dump(model, 'fraud_pipeline.pkl')

# Upload the trained model to S3 after training
s3.upload_file('fraud_pipeline.pkl', 'cc-fraud-detection-model-dataset', 's3://cc-fraud-detection-model-dataset/fraud_pipeline.pkl')




