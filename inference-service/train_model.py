import joblib
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier

X, y = load_iris(return_X_y=True)
model = RandomForestClassifier(n_estimators=50, random_state=42)
model.fit(X, y)
joblib.dump(model, "model/model.joblib")
print("Model saved to model/model.joblib")
