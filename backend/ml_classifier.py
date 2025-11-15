import os
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

MODEL_PATH = "ml/receipt_classifier.pkl"
VEC_PATH = "ml/tfidf_vectorizer.pkl"

# Create folder if missing
os.makedirs("ml", exist_ok=True)

class ReceiptClassifier:
    def __init__(self):
        self.model = None
        self.vectorizer = None

    def train(self, texts, labels):
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
        X = self.vectorizer.fit_transform(texts)

        self.model = LogisticRegression(max_iter=200)
        self.model.fit(X, labels)

        joblib.dump(self.model, MODEL_PATH)
        joblib.dump(self.vectorizer, VEC_PATH)

    def load(self):
        self.model = joblib.load(MODEL_PATH)
        self.vectorizer = joblib.load(VEC_PATH)

    def predict(self, text):
        if self.model is None:
            self.load()
        X = self.vectorizer.transform([text])
        return self.model.predict(X)[0]
