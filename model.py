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

# Tokenize and vectorize URLs
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(url_list)

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# XGBoost parameters
params = {
    'objective': 'binary:logistic',
    'max_depth': 3,
    'learning_rate': 0.1,
    'subsample': 0.8,
    'colsample_bytree': 0.8,
    'eval_metric': 'logloss'
}

# Convert data to DMatrix format
dtrain = xgb.DMatrix(X_train, label=y_train)
dtest = xgb.DMatrix(X_test, label=y_test)

# Train XGBoost model
num_rounds = 100
xgb_model = xgb.train(params, dtrain, num_rounds)

# Model prediction probabilities
y_test_prob = xgb_model.predict(dtest)

# Binarize labels for ROC curve calculation
y_test_binarized = label_binarize(y_test, classes=[0, 1])

# Compute ROC curve
fpr, tpr, thresholds = roc_curve(y_test_binarized, y_test_prob)

# Calculate AUC-ROC
roc_auc = auc(fpr, tpr)

# Plot ROC curve
plt.figure(figsize=(8, 8))
plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'AUC = {roc_auc:.2f}')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC) Curve')
plt.legend(loc="lower right")
plt.show()
joblib.dump(vectorizer, 'vectorizer.joblib')
# Determine optimal threshold based on ROC curve
optimal_threshold_index = np.argmax(tpr - fpr)
optimal_threshold = thresholds[optimal_threshold_index]
print(f"Optimal Threshold based on ROC curve: {optimal_threshold}")

# Save the vectorizer
save_vectorizer(vectorizer)
save_vectorizer(vectorizer)

# Save the XGBoost model
save_xgb_model(xgb_model, 'xgb_model.json')

joblib.dump(vectorizer, 'vectorizer.joblib')
print("Model and vectorizer saved successfully.")
