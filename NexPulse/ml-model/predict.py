# ml_model/predict.py
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Load the trained models
with open('ml_model/count_vectorizer.pkl', 'rb') as f:
    count_vector = pickle.load(f)
with open('ml_model/naive_bayes.pkl', 'rb') as f:
    naive_bayes = pickle.load(f)


def detect_scam_words(text):
    # Ensure the input is a list of strings
    if not isinstance(text, list) or not all(isinstance(t, str) for t in text):
        raise ValueError("Input text should be a list of strings.")

    # Transform the text data
    predictors = count_vector.transform(text)

    # Predict using Naive Bayes
    result = naive_bayes.predict(predictors)

    # Calculate the average of predictions
    average = sum(result) / len(result)

    # Determine if the average prediction indicates a scam
    return average >= 0.4
