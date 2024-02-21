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
substrings = ["subscribe", "login", "signin", "signup", "join","unsubscribe"]

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
def check(ul):
    new_urls = []
    new_urls.append(ul)
    new_X = vectorizer.transform(new_urls)
    predictions = model.predict(new_X)
    # Print Prediction Results for New URLs
    for url, prediction in zip(new_urls, predictions):
        if prediction == 1:
            return True
        else:
            print(f"{url} is not a subscription link")
            return False
r=check('https://www.amazon.in/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Feu.primevideo.com%2Fauth%2Freturn%2Fref%3Dav_auth_ap%3F_t%3Dsgya-K3TNw1ubTS5mwZVuiXu4e6xpx2PPHgpq1rzWQXE0AAAAAQAAAABlz5nBcmF3AAAAAPgWC9WfHH8iB-olH_E9xQ%26location%3D%2Fdetail%2FLogin%2F0HBWDH95AN3UG2SX0M4YXRQ80W%3Fref_%253Datv_unknown&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&accountStatusPolicy=P1&openid.assoc_handle=amzn_prime_video_sso_in&openid.mode=checkid_setup&siteState=259-1074053-3776640&language=en_US&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0')
print(r)
