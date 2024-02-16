from model_utils import save_xgb_model, load_xgb_model, load_vectorizer, save_vectorizer
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import label_binarize
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt
import xgboost as xgb
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

# Read data from CSV file (replace 'path_to_dataset.csv' with the actual path)
data = pd.read_csv("data.csv")

# Map categorical labels to numeric values
label_mapping = {'good': 0, 'bad': 1}
data['label_numeric'] = data['label'].map(label_mapping)

# Separate labels and features
y = data["label_numeric"]
url_list = data["url"]

data['contains_subscribe'] = data['url'].apply(lambda x : 1 if "subscribe" in x else 0)

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import TfidfVectorizer
import xgboost as xgb

# Feature Engineering
# Define the list of substrings to check for
substrings = ["subscribe", "login", "signin", "signup", "join"]

# Function to check if any of the substrings are present in the URL
def check_substrings(url):
    for substring in substrings:
        if substring in url:
            return 1
    return 0

# Apply the function to create the 'contains_subscribe' feature
data['contains_subscribe'] = data['url'].apply(check_substrings)

# TF-IDF Vectorization
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(data['url'])
y = data['contains_subscribe']

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# XGBoost Model Training
model = xgb.XGBClassifier()
model.fit(X_train, y_train)

# Predict on Test Data
y_pred = model.predict(X_test)

# Calculate Accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy}")

# Predict on New URLs
new_urls = ['https://sso.rajasthan.gov.in/signin', 'https://example.com/', 'https://example.com/news']
new_X = vectorizer.transform(new_urls)
predictions = model.predict(new_X)

# Print Prediction Results for New URLs
for url, prediction in zip(new_urls, predictions):
    if prediction == 1:
        print(f"{url} is a subscription link")
    else:
        print(f"{url} is not a subscription link")


