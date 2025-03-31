# Import the necessary libraries
import numpy as np
import pandas as pd
import random
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
import joblib


# Set the random seed for reproducibility
random.seed(42)
np.random.seed(42)

# Load the dataset
cc_fraud_df = pd.read_csv("dataset/creditcard.csv")

# Preprocessing
# Get the features and target
X = cc_fraud_df.drop(columns=['Class'])
y = cc_fraud_df['Class']

# Split the dataset: One for training, One  to simulate retraining
X_train, X_new, y_train, y_new = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

# Save the splits to CSV files so that we can access them in retraining.py
X_train.to_csv('dataset/X_train.csv', index=False)
X_new.to_csv('dataset/X_new.csv', index=False)
y_train.to_csv('dataset/y_train.csv', index=False)
y_new.to_csv('dataset/y_new.csv', index=False)

# Build and train the model, added scaling to the pipeline for preprocessing features
model = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', RandomForestClassifier(random_state=42, class_weight='balanced', n_estimators=500))
])

model.fit(X_train, y_train)

# Move to pkl file
joblib.dump(model, "fraud_pipeline.pkl")
