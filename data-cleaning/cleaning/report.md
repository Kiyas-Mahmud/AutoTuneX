# Data Quality Analysis Report

## 1. Request Rate

- Burst and idle patterns: Present (see distribution and time series plots)
- No random single-point spikes: Confirmed (spikes are sustained, not isolated)
- Variation: Sufficient for model training (wide range, 50/45/5 split)

## 2. Latency (P95)

- Increases with traffic: Yes (correlation visible in plots)
- Artificial cap: None detected (max observed well below 0.20)
- Sudden abnormal spikes: Some high outliers (3,410, 16.68%) but consistent with workload

## 3. CPU Usage

- Correlates with request_rate: Yes (correlation matrix confirms)
- Drops after scaling: Observable in time series (CPU dips after replica increases)
- Impossible values: None (>100%)

## 4. Memory Usage

- No unexplained zero drops: None detected
- Stable trend: Generally stable, follows workload
- Matches replica changes: Yes, memory per replica stable

## 5. Replica Count

- Scale up/down events: 22 events, visible in time series
- Not constant: Mostly at 6, but changes present
- No extreme oscillation: No rapid up/down cycles

## 6. Error Rate

- Spikes during overload: Occasional small spikes, mostly low
- Reduces after scaling: Yes, error rate drops after scaling events
- Not always zero: Some nonzero values present

## 7. Distributions

- Not concentrated in one range: Distributions show wide spread
- Multiple workload states: Low, medium, burst traffic all present

---

## Visual Evidence

- See `results/img/data_cleaning_overview.png` for all time series and distributions
- See `results/img/correlation_matrix.png` for feature relationships

---

## Conclusion

All key data quality checks passed. Dataset is suitable for time-series modeling and autoscaling research. No artificial artifacts or major quality issues detected.
