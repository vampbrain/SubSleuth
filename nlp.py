from textblob import TextBlob
from collections import Counter
from bs4 import BeautifulSoup
import requests
from retrying import retry

# Define a retry decorator with exponential backoff
@retry(wait_exponential_multiplier=1000, wait_exponential_max=10000, stop_max_attempt_number=3)
def fetch_webpage(url):
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for 4XX or 5XX status codes
    return response.text

@retry(wait_exponential_multiplier=1000, wait_exponential_max=10000, stop_max_attempt_number=5)
def extract_text_from_webpage(url):
    try:
        # Fetch the webpage
        html_content = fetch_webpage(url)

        # Parse the HTML content using Beautiful Soup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find specific elements containing text content
        text_content = ""
        for element in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'span', 'div']):
            text_content += element.get_text(separator='\n', strip=True) + '\n'

        # Filter out empty lines and unnecessary whitespace
        text_content_lines = [line.strip() for line in text_content.split('\n') if line.strip()]

        # Join the lines back into a single string
        text_content_cleaned = '\n'.join(text_content_lines)

        return text_content_cleaned

    except requests.exceptions.RequestException as e:
        print("Error fetching webpage:", e)
        raise

# Define sentiment analysis function
def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    if polarity > 0:
        return "POSITIVE"
    elif polarity < 0:
        return "NEGATIVE"
    else:
        return "NEUTRAL"

# Define dark pattern detection function
# Define dark pattern detection function
def detect_dark_patterns(text):
    dark_patterns = []

    # Define keywords related to false urgency
    false_urgency_keywords = ["limited time offer", "act now","Shop now", "hurry up", "limited offer", "deal of the day", "time-limited", "last chance", "up to", "off", "upto"]

    # Define keywords related to misleading labeling
    misleading_labeling_keywords = ["free", "subscription", "trial", "only", "exclusive", "limited edition", "special offer", "discount"]

    # Define keywords related to confirmshaming
    confirmshaming_keywords = ["you won't", "subscribe", "don't miss out", "don't wait", "don't hesitate", "click now", "buy now", "order now", "join now"]

    # Check for false urgency
    if any(keyword in text.lower() for keyword in false_urgency_keywords):
        dark_patterns.append("False urgency")

    # Check for misleading labeling
    if any(keyword in text.lower() for keyword in misleading_labeling_keywords):
        dark_patterns.append("Misleading labeling")

    # Check for confirmshaming
    if any(keyword in text.lower() for keyword in confirmshaming_keywords):
        dark_patterns.append("Confirmshaming")

    return dark_patterns

def urlget(l):
    global webpage_url,most_common_dark_pattern,most_common_sentiment
    webpage_url=l
    text_content = extract_text_from_webpage(webpage_url)
    if text_content:
        # Split text content into sentences
        sentences = text_content.split('.')
        
        # Store sentiment labels for each sentence
        sentiment_labels = []
        dark_patterns_detected = []
        for sentence in sentences:
            # Analyze sentiment for each sentence
            sentiment_label = analyze_sentiment(sentence)
            sentiment_labels.append(sentiment_label)
            
            # Detect dark patterns for each sentence
            dark_patterns = detect_dark_patterns(sentence)
            dark_patterns_detected.extend(dark_patterns)
        
        # Determine the most frequent sentiment label
        most_common_sentiment = Counter(sentiment_labels).most_common(1)[0][0]
        
        # Determine the most frequent dark pattern detected
        if dark_patterns_detected:
            most_common_dark_pattern = Counter(dark_patterns_detected).most_common(1)[0][0]
        else:
            most_common_dark_pattern = "None"
        
        print("Most frequent sentiment label:", most_common_sentiment)
        print("Most frequent dark pattern detected:", most_common_dark_pattern)
        return most_common_sentiment,most_common_dark_pattern
    else:
        print("Failed to extract text content from the webpage.")