import xgboost as xgb
import joblib

def load_vectorizer():
    vectorizer = joblib.load('vectorizer.joblib')
    return vectorizer

def save_xgb_model(model, filename):
    model.save_model(filename)
    print(f"XGBoost model saved to {filename}")

def load_xgb_model(filename):
    loaded_model = xgb.Booster()
    loaded_model.load_model(filename)
    return loaded_model
def save_vectorizer(vectorizer, filename='vectorizer.joblib'):
    joblib.dump(vectorizer, filename)
    print(f"Vectorizer saved to {filename}")