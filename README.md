# Fraud Detection Model with Automated Retraining and Monitoring

In this project, I created a fraude detection model using scikit-learn's RandomForestClassfier and set up Github Actions for automatic retraining. The retraining is triggered either upon a new push to the repository or on a weekly basis. Additionally, I used Prometheus and Grafana to monitor the model's performance and visualize various metrics.

The model was trained used the Credit Card Fraud Detection dataset from Kaggle. For more detailed information on hyperparameter tuning and exploratory analysis, refer to the Model_Prototyping_Fraud_Detection.ipynb Jupyter notebook in the repository.

*Model Performance*

* Test Precision: 93%
* Test Recall: 84%


**Files Overview**
* model_training.py - Contained the code to train the fraud detection model using Random Forest Classifier.
* retraining.py - Simulates retraining using existing data to mimic new data coming in. This script is triggered vis GitHub Actions.
* app.py - Flask application that serves the model for real-time predictions.
* prometheus.yml - Configuration file for Prometheus to scrape metrics from the Flask app.
* workflow.yaml - Github Actions configuration file to trigger retraining and automate the pipeline.

*Retraining Simulation*

Since there is no new data being generated, I simulated retraining by splittting the dataset into an 80/20 split, where the 20% portion represents "new data'.


**Setting up AWS S3 for Data Storage**

To store the dataset and model, I used AWS S3. I created an S3 bucket, configured access permissions, and added the access key and secret access key to GitHub repository secrets.

JSON configuration for the AWS S3 user permissions:

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

* Bucket Name: cc-fraud-detection-model-dataset
* Add the access key and secret access key to the GitHub repository secrets under Settings -> Secrets and Variables

Once set up, you can check the Actions tab in GitHub to see retraining process in action.


**Model Deployment**

I then deployed the trained model as a Flask application. The model is served through the ```/predict``` endpoint, and the app pulls the model directly from AWS S3. To allow the Flask app to access the S3 bucket, make sure you configure AWS CLI usint the following command:

```aws configure`` 

on your terminal. This will prompt you for the AWS Access Key ID and Secret Access Key, the same credentials added to GitHub secrets.

The Flask app is running in app.py, and I used Prometheus to collect custom metrics. Here are the metrics I track:

* Counter: Tracks error counts
* Histogram: Tracks prediction latency
* Gauge: Tracks fraudulent predictions


**Monitoring with Prometheus and Grafana**

I used Prometheus to collect metrics and Grafana to visualize them. Here's how you can set up both in Docker:

1. Prometheus: Run the following command on your terminal to start Prometheus in Docker:
  ```
  docker run -d --name prometheus \
    -p 9090:9090 \
    -v "./prometheus.yml:/etc/prometheus/prometheus.yml" \
    prom/prometheus
  ```
2. Grafana: Run the following command to start Grafana in Docker:
   ```
   docker run -d --name=grafana -p 3000:3000 grafana/grafana
   ```

Ensure Docker is running on your system before starting both containers. Once Prometheus and Grafana are up and running, you can access them at:

1. Prometheus: ```http://localhost:9090```
2. Grafana: ```http://localhost:3000```

**Testing the Flask API**

You can test the Flask API using Postman:
1. Send a POST request to: ```http://127.0.0.1:5000/predict```
2. In the ```Body``` section, select ```raw``` and paste the following JSON data:
   ``` {
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
 ``` ```

 You should receive a response like:
 ```
{
    "fraud_probability": 0.0
}
```
After sending requests to the Flask app, you can visualize the metrics in Grafana:
1. Go to Grafana and create a new Data Source.
2. Select Prometheus and set URL to: ```http://host.docker.internal:9090``` (since you''re using Docker).
3. Create a Dashboard and panels to visualize your metrices. (under ```Queries``` section in dashboard)

Make sure Prometheus is collectin metrics by checking the ```Targets``` page in Prometheus. It should show "up" in the state for your Flask app.

**Cleanup**

After testing, make sure to delete the S3 bucket and user from AWS to avoid unexpected charges!

*Resources*
https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud

https://www.youtube.com/watch?v=JffSxrjx_UM&t=577s

https://docs.github.com/en/enterprise-server@3.15/admin/managing-github-actions-for-your-enterprise/enabling-github-actions-for-github-enterprise-server/enabling-github-actions-with-amazon-s3-storage#enabling-github-actions-with-amazon-s3-storage-using-access-keys

https://pypi.org/project/flask-prometheus-metrics/




