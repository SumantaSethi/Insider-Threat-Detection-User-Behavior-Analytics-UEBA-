print(confusion_matrix(
    df["label"],
    df["ml_anomaly"]
))

print(classification_report(
    df["label"],
    df["ml_anomaly"],
    zero_division=0
))
