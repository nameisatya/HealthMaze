import pandas as pd
import os
import hashlib
import json
import requests
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Load dataset
file_path = "/storage/emulated/0/Download/heart_disease_dataset.csv"

if not os.path.exists(file_path):
    print("❌ Error: File not found!")
    exit()

df = pd.read_csv(file_path)

# Data preprocessing
df.fillna(df.mean(), inplace=True)
df.dropna(inplace=True)

# Train ML model
X = df.drop(columns=['target'])
y = df['target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Encrypt model update
model_update = {
    "coef_": model.coef_.tolist(),
    "intercept_": model.intercept_.tolist()
}

def encrypt_data(data):
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

encrypted_update = encrypt_data(model_update)

# Send data to Fog Node
FOG_NODE_URL = "http://192.168.137.220:5001/receive_from_mobile"
payload = {"encrypted_weights": encrypted_update}

try:
    response = requests.post(FOG_NODE_URL, json=payload)
    print("✅ Response from Fog Node:", response.text)
except Exception as e:
    print("❌ Error sending data:", str(e))