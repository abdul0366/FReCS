# -*- coding: utf-8 -*-
"""nv_fr_r_fr_90.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/12yRqAKkojAz2Y7uqnfDSYiooltUDoDCi
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.pipeline import make_pipeline
import seaborn as sns
import matplotlib.pyplot as plt

# Sample function for text preprocessing
def preprocess_text(text):
    # Lowercasing, removing punctuation, and other text cleaning
    return text.replace("URL", "").replace("@USER", "").strip().lower()

# Load your dataset
df_train = pd.read_csv("/home/aaadfg/fr/90_10/train_90.csv")
df_test = pd.read_csv("/home/aaadfg/fr/90_10/test_90.csv")

# Preprocess the text data
df_train['processed_tweet'] = df_train['Tweet_Text'].apply(preprocess_text)
df_test['processed_tweet'] = df_test['Tweet_Text'].apply(preprocess_text)

# Map labels to integers for multiclass
encoded_dict = {"EMS": 0, "Firefighter": 1, "Firefighter/EMS": 2, "Other": 3,
    "Police": 4, "Police/EMS": 5, "Police/Firefighter": 6, "Police/Firefighter/EMS": 7}

df_train['event'] = df_train['First_Responder'].map(encoded_dict)
df_test['event'] = df_test['First_Responder'].map(encoded_dict)

# Prepare the data
X_train = df_train['processed_tweet']
y_train = df_train['event']
X_test = df_test['processed_tweet']
y_test = df_test['event']

# Initialize the TF-IDF Vectorizer and Naive Bayes classifier within a pipeline
model = make_pipeline(TfidfVectorizer(max_features=1000), MultinomialNB())

# Train the model
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model for multiclass classification
print(classification_report(y_test, y_pred, target_names=list(encoded_dict.keys())))

# Confusion Matrix Visualization for multiclass classification
plt.figure(figsize=(12, 12))
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=list(encoded_dict.keys()), yticklabels=list(encoded_dict.keys()))
plt.title('Confusion Matrix')
plt.ylabel('Actual Labels')
plt.xlabel('Predicted Labels')
plt.show()