# Import the necessary libraries
import numpy as np
import pandas as pd
import random
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
import joblib
import boto3


# Set the random seed for reproducibility
random.seed(42)
np.random.seed(42)

# Initialize boto3 client for AWS S3
s3 = boto3.client('s3')

# Download the dataset from S3
s3.download_file('cc-fraud-detection-model-dataset','dataset/creditcard.csv', 'dataset/creditcard.csv')

# Load the dataset
cc_fraud_df = pd.read_csv("dataset/creditcard.csv")

# Preprocessing
# Get the features and target
X = cc_fraud_df.drop(columns=['Class'])
y = cc_fraud_df['Class']

# Split the dataset: One for training, One  to simulate retraining
X_train, X_new, y_train, y_new = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)


# Save the new data (X_new, y_new) to S3 for future retraining simulation
X_new.to_csv('dataset/X_new.csv', index=False)
y_new.to_csv('dataset/y_new.csv', index=False)

# Upload X_new and y_new to S3
s3.upload_file('dataset/X_new.csv', 'cc-fraud-detection-model-dataset', 'dataset/X_new.csv')
s3.upload_file('dataset/y_new.csv', 'cc-fraud-detection-model-dataset', 'dataset/y_new.csv')

# Build and train the model, added scaling to the pipeline for preprocessing features
model = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', RandomForestClassifier(random_state=42, class_weight='balanced', n_estimators=500))
])

model.fit(X_train, y_train)

# Move to pkl file
joblib.dump(model, "fraud_pipeline.pkl")

# Upload the trained model to S3 after training
s3.upload_file('fraud_pipeline.pkl', 'cc-fraud-detection-model-dataset', 'fraud_pipeline.pkl')
