import pandas as pd
import joblib

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# -----------------------------
# Load Dataset
# -----------------------------
df = pd.read_csv("dataset/raw/cyberthreat.csv")

# -----------------------------
# Data Preprocessing
# -----------------------------

# Convert Flow Bytes/s to numeric
df["Flow Bytes/s"] = df["Flow Bytes/s"].str.replace(",", "")
df["Flow Bytes/s"] = pd.to_numeric(df["Flow Bytes/s"])

# Encode categorical columns
source_encoder = LabelEncoder()
destination_encoder = LabelEncoder()
protocol_encoder = LabelEncoder()
label_encoder = LabelEncoder()

df["Source IP"] = source_encoder.fit_transform(df["Source IP"])
df["Destination IP"] = destination_encoder.fit_transform(df["Destination IP"])
df["Protocol"] = protocol_encoder.fit_transform(df["Protocol"])
df["Label"] = label_encoder.fit_transform(df["Label"])

# -----------------------------
# Features and Target
# -----------------------------
X = df.drop("Label", axis=1)
y = df["Label"]

# -----------------------------
# Split Dataset
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("Training Samples :", len(X_train))
print("Testing Samples  :", len(X_test))

# -----------------------------
# Train Model
# -----------------------------
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# -----------------------------
# Prediction
# -----------------------------
y_pred = model.predict(X_test)

# -----------------------------
# Accuracy
# -----------------------------
accuracy = accuracy_score(y_test, y_pred)

print("\nModel Accuracy:", accuracy)

print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

# -----------------------------
# Save Model
# -----------------------------
joblib.dump(model, "saved_model/cyber_model.pkl")
joblib.dump(label_encoder, "saved_model/label_encoder.pkl")

print("\nModel Saved Successfully!")