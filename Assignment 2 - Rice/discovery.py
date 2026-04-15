import pandas as pd
from scipy.io import arff
from pycaret.classification import setup, compare_models, plot_model, finalize_model, save_model
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier

data, meta = arff.loadarff("Rice_Cammeo_Osmancik.arff")
df = pd.DataFrame(data)

for col in df.columns:
    if df[col].dtype == object:
        df[col] = df[col].apply(lambda x: x.decode("utf-8") if isinstance(x, bytes) else x)

print("Data preview:")
print(df.head())

clf_setup = setup(
    data=df,
    target="Class",
    session_id=42,
    train_size=0.8,
    normalize=True,
    verbose=True,
    html=False
)

top3 = compare_models(n_select=3)
best_model = top3[0]

print("\nTop 3 models:")
print(top3)

plot_model(best_model, plot="confusion_matrix", save=True)

final_model = finalize_model(best_model)
save_model(final_model, "best_pipeline")

# Manual sklearn workflow
X = df.drop("Class", axis=1)
y = df["Class"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

manual_model = Pipeline([
    ("scaler", StandardScaler()),
    ("classifier", RandomForestClassifier(random_state=42))
])

manual_model.fit(X_train, y_train)
y_pred = manual_model.predict(X_test)

print("\nClassification Report:")
print(classification_report(y_test, y_pred))
