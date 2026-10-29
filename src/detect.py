features = [
    "hour",
    "bytes_transferred",
    "files_accessed",
    "sensitive_access"
]

X = df[features].copy()

# Reduce the impact of very large transfer values
X["bytes_transferred"] = np.log1p(X["bytes_transferred"])

model = IsolationForest(
    n_estimators=150,
    contamination=0.05,
    random_state=42
)

model.fit(X)

# -1 = anomaly; 1 = normal
df["ml_prediction"] = model.predict(X)

df["ml_anomaly"] = (
    df["ml_prediction"] == -1
).astype(int)

print(df["ml_anomaly"].value_counts())
