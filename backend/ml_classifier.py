# backend/ml_classifier.py
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

MODEL_PATH = "backend/classifier.pkl"

class ReceiptClassifier:

    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.model = LogisticRegression(max_iter=2000)

    def train(self, texts, labels):
        X = self.vectorizer.fit_transform(texts)
        self.model.fit(X, labels)

        with open(MODEL_PATH, "wb") as f:
            pickle.dump({
                "vectorizer": self.vectorizer,
                "model": self.model
            }, f)

        print("Model trained and saved successfully!")

    def load(self):
        with open(MODEL_PATH, "rb") as f:
            data = pickle.load(f)
            self.vectorizer = data["vectorizer"]
            self.model = data["model"]

    def predict(self, text):
        X = self.vectorizer.transform([text])
        return self.model.predict(X)[0]
