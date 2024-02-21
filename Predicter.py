from tensorflow import keras
from urllib.parse import urlparse
import os.path

threshold = 50.0  

# def digit_count(url):
#     digits = 0
#     for i in url:
#         if i.isnumeric():
#             digits = digits + 1
#     return digits
def fd_length(url):
    urlpath= urlparse(url).path
    try:
        return len(urlpath.split('/')[1])
    except:
        return 0
def letter_count(url):
    letters = 0
    for i in url:
        if i.isalpha():
            letters = letters + 1
    return letters
def no_of_dir(url):
    urldir = urlparse(url).path
    return urldir.count('/')
import re

#Use of IP or not in domain
def having_ip_address(url):
    match = re.search(
        '(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.'
        '([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  # IPv4
        '((0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\/)' # IPv4 in hexadecimal
        '(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}', url)  # Ipv6
    if match:
        # print match.group()
        return -1
    else:
        # print 'No matching pattern found'
        return 1

def get_prediction(url):
    model_path = "Caffeine_Prediction.h5"
    # print("Loading the model...")
    model = keras.models.load_model(model_path)

    # print("Extracting features from url...")
    l=[]
    l.append(len(urlparse(url).netloc))
    l.append(len(urlparse(url).path))
    l.append(fd_length(url))
    l.append(url.count('-'))
    l.append(url.count('@'))
    l.append(url.count('?'))
    l.append(url.count('%'))
    l.append(url.count('.'))
    l.append(url.count('='))
    l.append(url.count('http'))
    l.append(url.count('https'))
    l.append(url.count('www'))
    # l.append(digit_count(url))
    l.append(letter_count(url))
    l.append(no_of_dir(url))
    l.append(having_ip_address(url))


    url_features = l
    # print(url_features)

    # print("Making prediction...")
    prediction = model.predict([url_features])

    probability = prediction[0][0] * 100
    probability = round(probability, 3)
    # print("There is a", probability, "% chance that the URL is malicious.")

    # Classify as malicious if probability exceeds the threshold
    if probability >= threshold:
        return "Malicious"
    else:
        return "Not Malicious"

# Example usage:
model_path = "Caffeine_Prediction.h5"
def predict(l):
    mali=[]
    for i in l:
        s=i.replace('http://','')
        result = get_prediction(s)
        if result=="Malicious":
            mali.append(i)
        else:
            pass
    return mali

