import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(BASE_DIR, "dataset", "raw", "cyberthreat.csv")

MODEL_PATH = os.path.join(BASE_DIR, "saved_model", "cyber_model.pkl")

ENCODER_PATH = os.path.join(BASE_DIR, "saved_model", "label_encoder.pkl")