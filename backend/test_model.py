import joblib

model = joblib.load("saved_model/cyber_model.pkl")

sample = [[12,45,78,1,0]]

prediction = model.predict(sample)

print(prediction)