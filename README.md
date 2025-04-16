# Fraud Detection Model with Automated Retraining and Monitoring

An end-to-end MLOps system that detects fraudulent transactions, retrains automatically via CI/CD, monitors drift in real-time, and is fully deployed with Flask + AWS + Grafana.

**Hightlights**
1. Automated retraining using GitHub Actions on push and weekly schedule
2. Deployed model as a Flask API with /predict endpoint
3. Monitoring with Prometheus + Grafana (latency, drift, fraud rate)
4. Model & data stored in AWS S3 using IAM-secured GitHub Actions access

**Model Details**
* Algorithm - RandomForestClassifier(SKlearn)
* Dataset - https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud
* Performance: Precision - 93%, Recall - 84%

**Tech Stack**
* Python, Scikit-learn, Flask
* AWS-S3, GitHub Actions, Docker
* Prometheus, Grafana
* Postman for testing

**Project Structure**

├── app.py                      # Flask API for prediction

├── model_training.py           # Model training script

├── retraining.py               # GitHub Actions-triggered retraining logic

├── .github/workflows/          # CI/CD workflows

├── prometheus.yml              # Monitoring config

├── README.md


**Retraining Workflow**
* Triggered by:
  * Push to main
  * Weekly schedule
* Simulates incoming data by splitting dataset (80/20)
* Trains model, saves to AWS S3

**AWS S3 Setup**
* Created bucket: cc-fraud-detection-model-dataset
* Used GitHub Secrets to store AWS credentials
* IAM Policy (excerpt):
  ```
      {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "VisualEditor0",
                "Effect": "Allow",
                "Action": [
                    "s3:PutObject",
                    "s3:GetObject",
                    "s3:ListBucketMultipartUploads",
                    "s3:AbortMultipartUpload",
                    "s3:ListBucket",
                    "s3:DeleteObject",
                    "s3:ListMultipartUploadParts"
                ],
                "Resource": [
                    "arn:aws:s3:::cc-fraud-detection-model-dataset",
                    "arn:aws:s3:::cc-fraud-detection-model-dataset/*"
                ]
            }
        ]
    }
  ```
**Monitoring Setup**

Exposed custom Prometheus metrics in app.py:

* Counter: error count
* Histogram: latency
* Gauge: fraud rate

Run via Docker:
```
    # Prometheus
    docker run -d --name prometheus -p 9090:9090 \
      -v "$PWD/prometheus.yml:/etc/prometheus/prometheus.yml" prom/prometheus
    
    # Grafana
    docker run -d --name=grafana -p 3000:3000 grafana/grafana
```
Access:
* Prometheus - http://localhost:9090
* Grafana - http://localhost:3000

**Testing the API (via Postman)**
* Endpoint: POST http://127.0.0.1:5000/predict
* Body: raw JSON with model input (example below)
  ```
  {
        "Time": 160760,
        "V1": -0.6744660646,
        "V2": 1.40810502,
        "V3": -1.110622054,
        "V4": -1.328365778,
        "V5": 1.388996033,
        "V6": -1.308439067,
        "V7": 1.885878903,
        "V8": -0.6142329663,
        "V9": 0.3116522125,
        "V10": 0.6507570036,
        "V11": -0.8577846615,
        "V12": -0.2299614458,
        "V13": -0.1998170048,
        "V14": 0.2663713263,
        "V15": -0.04654416848,
        "V16": -0.7413980897,
        "V17": -0.6056166441,
        "V18": -0.3925681879,
        "V19": -0.162648311,
        "V20": 0.3943218208,
        "V21": 0.0800842396,
        "V22": 0.8100335956,
        "V23": -0.2243272304,
        "V24": 0.7078992374,
        "V25": -0.1358370227,
        "V26": 0.0451021965,
        "V27": 0.5338372191,
        "V28": 0.2913192526,
        "Amount": 23
    }

Response:
```
{
  "fraud_probability": 0.0
}
```

**Grafana Metrics Visualization**
* Add Prometheus as data source: http://host.docker.internal:9090
* Create dashboard with panels for latency, fraud rate, errors, etc.
* Confirm Prometheus target is "up"

**Cleanup**

Delete S3 bucket & IAM user after use to avoid charges.

**Resources**

https://www.youtube.com/watch?v=JffSxrjx_UM&t=577s

https://docs.github.com/en/enterprise-server@3.15/admin/managing-github-actions-for-your-enterprise/enabling-github-actions-for-github-enterprise-server/enabling-github-actions-with-amazon-s3-storage#enabling-github-actions-with-amazon-s3-storage-using-access-keys

https://pypi.org/project/flask-prometheus-metrics/




