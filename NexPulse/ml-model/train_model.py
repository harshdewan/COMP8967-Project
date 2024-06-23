import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

print("Starting model training...")

# Example training data (you should use a larger dataset for real training)
training_texts = [
    "Congratulations! You've won a free iPhone.",
    "Hello, how are you?",
    "This is a limited time offer, claim now!",
    "Don't miss out on this opportunity.",
    "Are we still meeting tomorrow?",
    "You have been selected for a prize."
]

training_labels = [1, 0, 1, 1, 0, 1]  # 1 for scam, 0 for not scam

# Initialize and train CountVectorizer
count_vector = CountVectorizer()
X_train = count_vector.fit_transform(training_texts)

print("CountVectorizer trained.")

# Initialize and train Naive Bayes classifier
naive_bayes = MultinomialNB()
naive_bayes.fit(X_train, training_labels)

print("Naive Bayes classifier trained.")

# Save the trained models
with open('count_vectorizer.pkl', 'wb') as f:
    pickle.dump(count_vector, f)
print("Saved CountVectorizer as count_vectorizer.pkl")

with open('naive_bayes.pkl', 'wb') as f:
    pickle.dump(naive_bayes, f)
print("Saved Naive Bayes classifier as naive_bayes.pkl")

print("Model training and saving completed.")
