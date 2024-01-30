# scanner.py
from web_app import app
import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
import xgboost as xgb
from model_utils import load_vectorizer, load_xgb_model

# Load your trained vectorizer
vectorizer = load_vectorizer()

# Load your trained XGBoost model
xgb_model = load_xgb_model('xgb_model.json')

# Load optimal_threshold from your saved file or define it here
# optimal_threshold = load_optimal_threshold()  # Implement load_optimal_threshold() based on your saving method
optimal_threshold = 0.13664253056049347  # You can replace this with the actual value

def classify_links(links, vectorizer, model, threshold):
    malicious_links = []
    subscription_links = []

    for link in links:
        link_vectorized = vectorizer.transform([link])
        dlink = xgb.DMatrix(link_vectorized)

        # Make predictions using the trained model
        predicted_probability = model.predict(dlink)[0]

        # Classify links based on threshold
        if predicted_probability >= threshold:
            malicious_links.append(link)
        elif "subscribe" in link.lower() or "unsubscribe" in link.lower():
            subscription_links.append(link)

    return malicious_links, subscription_links

def extract_links(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [a['href'] for a in soup.find_all('a', href=True)]
        return links
    except Exception as e:
        print(f"Error extracting links: {e}")
        return []

if __name__ == "__main__":
    # Example usage
    webpage_url = "https://daily.thesignal.co/p/hungary-consumer-gaming-warner-bros-zee-sony?utm_campaign=email-half-post&r=30q08c&utm_source=substack&utm_medium=email"
    all_links = extract_links(webpage_url)

    # Classify links
    malicious_links, subscription_links = classify_links(all_links, vectorizer, xgb_model, optimal_threshold)

    print("All Links:", all_links)
    print("Malicious Links:", malicious_links)
    print("Subscription/Unsubscription Links:", subscription_links)
