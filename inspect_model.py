import joblib
model = joblib.load("tuned_random_forest_v1.joblib")  # Load the trained model pipeline

print("Model Type:", type(model))

if hasattr(model, "steps"):
    print("Pipeline Steps:", model.steps)

if hasattr(model, "feature_names_in_"):
    print("Expected features:", model.feature_names_in_)