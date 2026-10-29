import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
n = 2000

users = [f"employee_{i:03d}" for i in range(1, 51)]

df = pd.DataFrame({
    "user_id": rng.choice(users, n),
    "hour": rng.integers(0, 24, n),
    "bytes_transferred": rng.lognormal(mean=12, sigma=1.0, size=n).astype(int),
    "files_accessed": rng.poisson(5, n),
    "sensitive_access": rng.binomial(1, 0.08, n)
})

# Synthetic ground-truth labels for demonstration
df["label"] = 0

# Simulate a suspicious subset
idx = rng.choice(df.index, size=100, replace=False)

df.loc[idx, "label"] = 1
df.loc[idx, "hour"] = rng.choice([0, 1, 2, 3, 4], len(idx))
df.loc[idx, "bytes_transferred"] = rng.integers(15_000_000, 100_000_000, len(idx))
df.loc[idx, "files_accessed"] = rng.integers(20, 100, len(idx))
df.loc[idx, "sensitive_access"] = 1

df["timestamp"] = (
    pd.Timestamp("2026-01-01")
    + pd.to_timedelta(rng.integers(0, 30 * 24, n), unit="h")
)

df = df.sort_values("timestamp").reset_index(drop=True)

df.to_csv("employee_activity.csv", index=False)

print(df.head())
print("Rows:", len(df))
print("Synthetic suspicious events:", int(df["label"].sum()))
