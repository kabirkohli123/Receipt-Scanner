import json
from backend.ml_classifier import ReceiptClassifier

with open("backend/training_data.json", "r") as f:
    data = json.load(f)

classifier = ReceiptClassifier()
classifier.train(data["texts"], data["labels"])

print("Model trained and saved!")
