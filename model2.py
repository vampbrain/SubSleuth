import pandas as pd
import itertools
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt
import xgboost as xgb
from lightgbm import LGBMClassifier
import os
import seaborn as sns
from wordcloud import WordCloud
from imblearn.over_sampling import SMOTE
import warnings

# Suppress FutureWarnings
warnings.simplefilter(action='ignore', category=FutureWarning)


df = pd.read_csv("malicious_phish.csv")
print(df.shape)
df.head()

df.type.value_counts()

df_phish = df[df.type=='phishing']
df_mal = df[df.type=='malware']
df_deface = df[df.type=='malface']
df_benign = df[df.type=='benign']

phish_url = " ".join(i for i in df_phish.url)
wc = WordCloud(width = 1600, height = 800, colormap="Paired").generate(phish_url)
plt.figure(figsize = (12,14), facecolor = 'k')
plt.imshow(wc, interpolation = 'bilinear')
plt.axis('off')
plt.tight_layout(pad=0)
plt.show()

import re
def has_ip(url):
  match = re.search(
      '(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.'
        '([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  # IPv4
        '((0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\/)' # IPv4 in hexadecimal
        '(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}', url
  )
  if match:
    return 1
  else:
    return 0

df['use_of_ip'] = df['url'].apply(lambda i: has_ip(i))

from urllib.parse import urlparse

def abnormal(url):
  hostname = urlparse(url).hostname
  hostname = str(hostname)
  match = re.search(hostname,url)
  if match:
    return 1
  else:
    return 0
df['abnormal_url'] = df['url'].apply(lambda i: abnormal(i))

#!pip install googlesearch-python

from googlesearch import search

def gindex(url):
  site = search(url, 5)
  return 1 if site else 0
df['google_index'] = df['url'].apply(lambda i: gindex(i))

def count_dot(url):
    count_dot = url.count('.')
    return count_dot

df['count.'] = df['url'].apply(lambda i: count_dot(i))
df.head()

def count_www(url):
    url.count('www')
    return url.count('www')

df['count-www'] = df['url'].apply(lambda i: count_www(i))

def count_atrate(url):

    return url.count('@')

df['count@'] = df['url'].apply(lambda i: count_atrate(i))


def no_of_dir(url):
    urldir = urlparse(url).path
    return urldir.count('/')

df['count_dir'] = df['url'].apply(lambda i: no_of_dir(i))

def no_of_embed(url):
    urldir = urlparse(url).path
    return urldir.count('//')

df['count_embed_domian'] = df['url'].apply(lambda i: no_of_embed(i))


def shortening_service(url):
    match = re.search('bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                      'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                      'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                      'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                      'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                      'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                      'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|'
                      'tr\.im|link\.zip\.net',
                      url)
    if match:
        return 1
    else:
        return 0


df['short_url'] = df['url'].apply(lambda i: shortening_service(i))

def count_https(url):
    return url.count('https')

df['count-https'] = df['url'].apply(lambda i : count_https(i))

def count_http(url):
    return url.count('http')

df['count-http'] = df['url'].apply(lambda i : count_http(i))

def count_per(url):
    return url.count('%')

df['count%'] = df['url'].apply(lambda i : count_per(i))

def count_ques(url):
    return url.count('?')

df['count?'] = df['url'].apply(lambda i: count_ques(i))

def count_hyphen(url):
    return url.count('-')

df['count-'] = df['url'].apply(lambda i: count_hyphen(i))

def count_equal(url):
    return url.count('=')

df['count='] = df['url'].apply(lambda i: count_equal(i))

def url_length(url):
    return len(str(url))


#Length of URL
df['url_length'] = df['url'].apply(lambda i: url_length(i))
#Hostname Length

def hostname_length(url):
    return len(urlparse(url).netloc)

df['hostname_length'] = df['url'].apply(lambda i: hostname_length(i))

df.head()

def suspicious_words(url):
    match = re.search('PayPal|login|signin|bank|account|update|free|lucky|service|bonus|ebayisapi|webscr',
                      url)
    if match:
        return 1
    else:
        return 0
df['sus_url'] = df['url'].apply(lambda i: suspicious_words(i))


def digit_count(url):
    digits = 0
    for i in url:
        if i.isnumeric():
            digits = digits + 1
    return digits


df['count-digits']= df['url'].apply(lambda i: digit_count(i))


def letter_count(url):
    letters = 0
    for i in url:
        if i.isalpha():
            letters = letters + 1
    return letters


df['count-letters']= df['url'].apply(lambda i: letter_count(i))

df.head()

#Importing dependencies
from urllib.parse import urlparse
from tld import get_tld
import os.path

#First Directory Length
def fd_length(url):
    urlpath= urlparse(url).path
    try:
        return len(urlpath.split('/')[1])
    except:
        return 0

df['fd_length'] = df['url'].apply(lambda i: fd_length(i))

#Length of Top Level Domain
df['tld'] = df['url'].apply(lambda i: get_tld(i,fail_silently=True))


def tld_length(tld):
    try:
        return len(tld)
    except:
        return -1

df['tld_length'] = df['tld'].apply(lambda i: tld_length(i))

import seaborn as sns
df = df.drop("tld", axis=1)

# df.columns

# df['type'].value_counts()

# Assuming 'type' and 'use_of_ip' are integer columns, convert them to strings
df['type'] = df['type'].astype(str)

df['use_of_ip'] = df['use_of_ip'].astype(str)
sns.set(style="darkgrid")
ax = sns.countplot(y="type", data=df,hue="use_of_ip")

ax.legend(loc="best", title="use_of_ip")

df['abnormal_url'] = df['abnormal_url'].astype(str)
sns.set(style="darkgrid")
ax = sns.countplot(y="type", data=df,hue="abnormal_url")

df['google_index'] = df['google_index'].astype(str)
sns.set(style="darkgrid")
ax = sns.countplot(y="type", data=df,hue="google_index")

df['short_url'] = df['short_url'].astype(str)
sns.set(style="darkgrid")
ax = sns.countplot(y="type", data=df,hue="short_url")

df['sus_url'] = df['sus_url'].astype(str)
sns.set(style="darkgrid")
ax = sns.countplot(y="type", data=df,hue="sus_url")

sns.set(style="darkgrid")
ax = sns.catplot(x="type", y="count.", kind="box", data=df)

sns.set(style="darkgrid")
ax = sns.catplot(x="type", y="count-www", kind="box", data=df)

sns.set(style="darkgrid")
ax = sns.catplot(x="type", y="count@", kind="box", data=df)

sns.set(style="darkgrid")
ax = sns.catplot(x="type", y="count_dir", kind="box", data=df)

sns.set(style="darkgrid")
ax = sns.catplot(x="type", y="hostname_length", kind="box", data=df)

sns.set(style="darkgrid")
ax = sns.catplot(x="type", y="fd_length", kind="box", data=df)

sns.set(style="darkgrid")
ax = sns.catplot(x="type", y="tld_length", kind="box", data=df)

from sklearn.preprocessing import LabelEncoder

lb_make = LabelEncoder()
df["type_code"] = lb_make.fit_transform(df["type"])
df["type_code"].value_counts()

label_mapping = {
    0:0,
    1:1,
    2:1,
    3:1
}

df["type_code"] = df["type_code"].map(label_mapping)

#Predictor Variables
# filtering out google_index as it has only 1 value
X = df[['use_of_ip','abnormal_url', 'count.', 'count-www', 'count@',
       'count_dir', 'count_embed_domian', 'short_url', 'count-https',
       'count-http', 'count%', 'count?', 'count-', 'count=', 'url_length',
       'hostname_length', 'sus_url', 'fd_length', 'tld_length', 'count-digits',
       'count-letters']]

#Target Variable
y = df['type_code']

X.head()

X.columns

X.shape

X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2,shuffle=True, random_state=5)

smote = SMOTE(random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)

y_train

X_update = X_train.drop(["count-digits","fd_length","sus_url","count%","count@"], axis="columns")

X_test = X_test.drop(["count-digits","fd_length","sus_url","count%","count@"], axis="columns")



from tensorflow.keras import layers, models

# Define the CNN model
model = models.Sequential()

# Fully connected layers
model.add(layers.Dense(128, activation='relu', input_shape=(21,)))
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(32, activation='relu'))

# Output layer with softmax activation for multi-class classification
model.add(layers.Dense(1, activation='sigmoid'))  # Output layer with 4 neurons for multi-class classification

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Summary of the model architecture
model.summary()

# Define the number of epochs and batch size
epochs = 5
batch_size = 32

# Fit the model to the training data
#history = model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_split=0.2)

"""Prediction"""



def main(url):

    status = []

    status.append(has_ip(url))
    status.append(abnormal(url))
    status.append(count_dot(url))
    status.append(count_www(url))
    status.append(no_of_dir(url))
    status.append(no_of_embed(url))

    status.append(shortening_service(url))
    status.append(count_https(url))
    status.append(count_http(url))

    status.append(count_ques(url))
    status.append(count_hyphen(url))
    status.append(count_equal(url))

    status.append(url_length(url))
    status.append(hostname_length(url))
    status.append(letter_count(url))
    tld = get_tld(url,fail_silently=True)

    status.append(tld_length(tld))




    return status



from sklearn.linear_model import Perceptron
model1 = Perceptron()
model1.fit(X_update, y_train)

def get_prediction_from_url(test_url):
    features_test = main(test_url)
    # Due to updates to scikit-learn, we now need a 2D array as a parameter to the predict function.
    features_test = np.array(features_test).reshape((1, -1))

    pred = model1.predict(features_test)
    # Assuming the model outputs probabilities for the positive class (malware)
    # You may need to adjust this if your model outputs probabilities differently
    malware_prob = pred[0]
    print(pred)

    # Set a threshold for classification (e.g., 0.5)
    threshold = 0.5

    if malware_prob >= threshold:
        res = "MALWARE"
    else:
        res = "SAFE"

    return res

model1.score(X_test, y_test)

urls = ['http://gaup.{BLOCKED}of.com','bharathiraghavan.blogspot.com','http://{BLOCKED}i.ru/stats/00/counter/{hex}/{hex}']
for url in urls:
     print(get_prediction_from_url(url))

import pickle

# Save the model to a file using pickle
with open("url-model.pkl", "wb") as file:
    pickle.dump(model1, file)