Splunk Dashboard Guide — Insider Threat Detection (UEBA)

1. Overview

This dashboard helps a SOC Analyst investigate potentially suspicious employee activity using synthetic security logs and machine-learning-generated risk scores.

Project: Insider Threat Detection & User Behavior Analytics (UEBA)

Tools: Splunk, SPL, Python, Pandas, Scikit-learn

Dashboard objectives:

- Monitor the number of generated security alerts.
- Identify users with repeated suspicious activity.
- Investigate unusually large file transfers.
- Visualize alert severity and activity trends.
- Prioritize events for further investigation.

Important: This project uses synthetic data. An alert is an investigation lead, not proof of malicious activity.

2. Prerequisites

Before building the dashboard, ensure that:

1. The Python detection pipeline has generated "ueba_alerts.csv".
2. The CSV has been imported into Splunk.
3. The imported events contain fields such as:
   - "timestamp"
   - "user_id"
   - "hour"
   - "bytes_transferred"
   - "files_accessed"
   - "sensitive_access"
   - "risk_score"
   - "severity"
   - "alert"
   - "ml_anomaly"

The index and sourcetype depend on your Splunk import configuration. The searches below use "index=main" as an example; replace it with your actual index.

3. Dashboard Panels

Panel 1 — Total Security Alerts

Purpose: Display the total number of events flagged for investigation.

index=main
| eval alert_flag=if(
    lower(tostring(alert))="true"
    OR tostring(alert)="1",
    1, 0
)
| where alert_flag=1
| stats count as total_alerts

Visualization: Single Value

SOC interpretation: A sudden increase in alerts may indicate unusual activity or a change in the detection configuration.

Panel 2 — Alerts by Severity

Purpose: Understand the distribution of alert severity.

index=main
| eval alert_flag=if(
    lower(tostring(alert))="true"
    OR tostring(alert)="1",
    1, 0
)
| where alert_flag=1
| stats count as alert_count by severity
| sort - alert_count

Visualization: Column Chart or Pie Chart

SOC interpretation: Review HIGH and CRITICAL alerts first, while checking whether the scoring rules are generating excessive false positives.

Panel 3 — Top Users by Alert Count

Purpose: Identify accounts that repeatedly generate alerts.

index=main
| eval alert_flag=if(
    lower(tostring(alert))="true"
    OR tostring(alert)="1",
    1, 0
)
| where alert_flag=1
| stats count as alert_count
    max(risk_score) as maximum_risk
    by user_id
| sort - alert_count
| head 10

Visualization: Bar Chart

SOC interpretation: Repeated alerts may justify reviewing the user's activity history, access permissions, and legitimate work responsibilities.

Panel 4 — Large File Transfers

Purpose: Find events with large data-transfer volumes.

index=main
| eval transfer_bytes=tonumber(bytes_transferred)
| where transfer_bytes >= 10000000
| table timestamp user_id transfer_bytes
    files_accessed sensitive_access risk_score severity
| sort - transfer_bytes

Visualization: Table

Threshold: 10,000,000 bytes, approximately 10 MB using decimal units.

SOC interpretation: Confirm whether the transfer was authorized, whether the destination was approved, and whether the activity matches the user's normal behavior. Transfer volume alone does not establish data exfiltration.

Panel 5 — Security Alert Trend

Purpose: Track alerts over time.

index=main
| eval alert_flag=if(
    lower(tostring(alert))="true"
    OR tostring(alert)="1",
    1, 0
)
| where alert_flag=1
| timechart span=1h count as alert_count

Visualization: Line Chart

SOC interpretation: Alert spikes can help identify periods that need investigation. Confirm the timestamps and selected time range before interpreting a spike.

Panel 6 — Sensitive Data Access

Purpose: Review events involving sensitive-resource access.

index=main
| eval sensitive_flag=tonumber(sensitive_access)
| where sensitive_flag=1
| table timestamp user_id sensitive_access
    files_accessed bytes_transferred risk_score severity
| sort - risk_score

Visualization: Table

SOC interpretation: Check whether access was authorized and consistent with the employee's role. Sensitive access is not automatically suspicious.

4. Build the Dashboard in Splunk

1. Open your Splunk Search interface.
2. Confirm that the imported events appear in the expected index.
3. Run each SPL query individually and verify the results.
4. Open Dashboards and create a new dashboard.
5. Give it the title "Insider Threat Detection — UEBA".
6. Add panels using the SPL searches in this guide.
7. Choose the visualization specified for each panel.
8. Set an appropriate time range for your dataset.
9. Save the dashboard and verify that every panel displays meaningful results.

Splunk menu names may differ by version. You can create panels through the dashboard editor or by saving a search as a dashboard panel.

5. Suggested Dashboard Layout

Arrange the panels in this order:

1. Total Security Alerts
2. Alerts by Severity
3. Security Alert Trend
4. Top Users by Alert Count
5. Large File Transfers
6. Sensitive Data Access

This layout gives an analyst a high-level overview first, followed by investigation details.

6. Sample SOC Investigation Workflow

When an alert appears:

1. Identify the user and event timestamp.
2. Review the risk score, severity, and anomaly flag.
3. Check the transfer size and number of files accessed.
4. Determine whether sensitive data was accessed.
5. Search for other alerts involving the same user.
6. Compare the activity with the user's normal baseline.
7. Document findings and recommend additional verification.

Example Investigation Record

Field| Example
Alert ID| UEBA-001
User| employee_012
Detection reason| Off-hours activity and large transfer
Risk score| 70
Initial assessment| Requires investigation
Next action| Verify business justification and authorization

The values above are illustrative, not actual findings from a production environment.

7. Troubleshooting

No events appear

- Verify the index name and time range.
- Confirm that the CSV import succeeded.
- Run "index=main | head 10" after replacing the example index if needed.

The alert count is zero

- Inspect the actual values stored in the "alert" field.
- Check whether the field is represented as "true", "false", "1", or "0".
- Confirm that the Python pipeline generated alerts.

The timechart is empty

- Ensure Splunk recognizes the event timestamp.
- Verify the timestamp field format and event-time extraction.
- Use the correct time range for the synthetic dataset.

Risk scores are not numeric

- Check the field type and import settings.
- Convert the field using "tonumber(risk_score)" if required.

8. Limitations

- The dataset is synthetic and does not represent actual employee behavior.
- The model may flag legitimate activities as anomalous.
- Risk-score thresholds are illustrative and require validation.
- A production deployment would require access controls, privacy safeguards, baseline monitoring, and a validated evaluation process.
- Dashboard metrics depend on the correctness of event timestamps, field extraction, and data ingestion.

9. Portfolio Evidence

Add the following screenshots to the repository's "screenshots/" directory:

- Dashboard overview
- Alert severity distribution
- Top users by alert count
- Large-transfer investigation results
- Alert trend chart

Use synthetic data only and avoid exposing credentials or sensitive information.

10. Future Improvements

- Add a time-based training and test split.
- Compare machine-learning detection with a rule-only baseline.
- Add per-user behavioral baselines.
- Tune thresholds using precision, recall, and F1-score.
- Integrate a validated alert-ingestion pipeline.
- Document false positives and investigation outcomes.

Conclusion

This dashboard demonstrates how a SOC Analyst can combine Python-based anomaly detection with Splunk searches to prioritize potentially suspicious user activity. The output supports investigation and triage; it does not independently establish malicious intent.
