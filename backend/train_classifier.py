import json
from ml_classifier import ReceiptClassifier

with open("backend/training_data.json", "r") as f:
    data = json.load(f)

texts = data["texts"]
labels = data["labels"]

clf = ReceiptClassifier()
clf.train(texts, labels)
