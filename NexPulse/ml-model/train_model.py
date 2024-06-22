import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import pickle
import chardet

print("Starting model training...")

try:
    # Detect the file encoding
    with open('spam.csv', 'rb') as f:
        result = chardet.detect(f.read())
    encoding = result['encoding']

    # Read the CSV file with detected encoding
    df = pd.read_csv('spam.csv', encoding=encoding, delimiter=",")
    df = df.reindex(np.random.permutation(df.index))
    df.reset_index(inplace=True, drop=True)
    print(df.head())

    # Drop unnecessary columns and keep only relevant ones
    df = df[['v1', 'v2']]
    print(df.head())

    # Replace labels with numeric values
    df['v1'] = df['v1'].replace('ham', 0)
    df['v1'] = df['v1'].replace('spam', 1)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(df['v2'], df['v1'], test_size=0.2, random_state=42)

    # Vectorize the text data
    count_vector = CountVectorizer(ngram_range=(1, 1), lowercase=True, stop_words='english')
    X_train_count = count_vector.fit_transform(X_train)
    X_test_count = count_vector.transform(X_test)

    # Train the Naive Bayes model
    naive_bayes = MultinomialNB()
    naive_bayes.fit(X_train_count, y_train)
    predictions = naive_bayes.predict(X_test_count)

    # Evaluate the Naive Bayes model
    print('Naive Bayes Model')
    print('Accuracy score: ', accuracy_score(y_test, predictions))
    print('Precision score: ', precision_score(y_test, predictions))
    print('Recall score: ', recall_score(y_test, predictions))
    print('F1 score: ', f1_score(y_test, predictions))

    # Train the SVM model
    svc_model = SVC()
    svc_model.fit(X_train_count, y_train)
    svc_predictions = svc_model.predict(X_test_count)

    # Evaluate the SVM model
    print('SVM Model')
    print('Accuracy score: ', accuracy_score(y_test, svc_predictions))
    print('Precision score: ', precision_score(y_test, svc_predictions))
    print('Recall score: ', recall_score(y_test, svc_predictions))
    print('F1 score: ', f1_score(y_test, svc_predictions))

    # Save the best model and the count vectorizer using pickle
    with open('model.pkl', 'wb') as f:
        pickle.dump(naive_bayes, f)
        print("Model saved successfully.")

    with open('count_vector.pkl', 'wb') as f:
        pickle.dump(count_vector, f)
        print("Count vectorizer saved successfully.")

    # To load the model and vectorizer (if needed)
    with open('model.pkl', 'rb') as f:
        loaded_naive_bayes = pickle.load(f)

    with open('count_vector.pkl', 'rb') as f:
        loaded_count_vector = pickle.load(f)

    print("Model training and saving completed.")
except Exception as e:
    print(f"An error occurred: {e}")
