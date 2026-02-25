# Task 1.2: Feature Engineering - Report

**Task:** Feature Engineering  
**Status:** Complete  
**Date:** February 26, 2026  
**File:** data-cleaning/feature_engineering.ipynb

---

## Objectives Completed

### 1. Per-Replica Features

- Created `cpu_per_replica = cpu_usage / replica_count`
- Created `memory_per_replica = memory_usage / replica_count`
- Handled division by zero (replaced 0 with 1)

### 2. Derived Metrics

- Created `latency_diff = latency_p95 - latency_p50`
- Created `traffic_change_rate = Δrequest_rate / Δtime`

### 3. Lag Features (1-5 Steps)

- `request_rate_lag_1` to `request_rate_lag_5`
- `latency_p95_lag_1` to `latency_p95_lag_5`
- `cpu_usage_lag_1` to `cpu_usage_lag_5`
- Total: 15 lag features

### 4. Rolling Mean Features (Windows: 3, 5)

- `request_rate_rolling_mean_3`, `request_rate_rolling_mean_5`
- `latency_p95_rolling_mean_3`, `latency_p95_rolling_mean_5`
- `cpu_usage_rolling_mean_3`, `cpu_usage_rolling_mean_5`
- Total: 6 rolling mean features

### 5. Rolling Std Features (Windows: 3, 5)

- `request_rate_rolling_std_3`, `request_rate_rolling_std_5`
- `latency_p95_rolling_std_3`, `latency_p95_rolling_std_5`
- `cpu_usage_rolling_std_3`, `cpu_usage_rolling_std_5`
- Total: 6 rolling std features

### 6. Data Validation

- Removed NaN rows (from lag/rolling windows): 5 rows
- Verified no null values remain
- Verified no infinite values
- All features validated

### 7. Documentation

- Created feature metadata
- Generated visualizations
- Documented feature definitions

---

## Key Metrics

### Feature Statistics

- Original features: 9
- New features: 31
- Total features: 40
- Feature gain: 344%

### Data Retention

- Input rows: 20,447
- Output rows: 20,442
- Rows dropped: 5 (0.02%)
- Retention rate: 99.98%

### Feature Categories

| Category     | Count  | Features                                                                                         |
| ------------ | ------ | ------------------------------------------------------------------------------------------------ |
| Original     | 9      | timestamp, request_rate, latency_p50/p95/p99, error_rate, cpu_usage, memory_usage, replica_count |
| Per-replica  | 2      | cpu_per_replica, memory_per_replica                                                              |
| Derived      | 2      | latency_diff, traffic_change_rate                                                                |
| Lag          | 15     | 3 metrics × 5 steps                                                                              |
| Rolling mean | 6      | 3 metrics × 2 windows                                                                            |
| Rolling std  | 6      | 3 metrics × 2 windows                                                                            |
| **Total**    | **40** |                                                                                                  |

---

## Deliverables

### Files Created

1. **data-cleaning/feature_engineering.ipynb**
   - Complete feature engineering pipeline
   - Short comments for each step
   - Validation and visualization

2. **data-cleaning/run_feature_engineering.py**
   - Executable script version
   - Automated pipeline

3. **data/featured_dataset.csv**
   - 20,442 rows × 40 features
   - Time-aware dataset
   - Ready for modeling

4. **data-cleaning/feature_metadata.json**
   - Feature statistics
   - Categories breakdown
   - Retention information

5. **results/img/feature_engineering_overview.png**
   - 4-panel visualization
   - Per-replica metrics
   - Derived features

---

## Feature Definitions

### Per-Replica Metrics

- **cpu_per_replica**: CPU usage normalized by replica count
  - Purpose: Understand per-instance load
  - Formula: `cpu_usage / replica_count`
- **memory_per_replica**: Memory usage normalized by replica count
  - Purpose: Understand per-instance memory consumption
  - Formula: `memory_usage / replica_count`

### Derived Metrics

- **latency_diff**: Latency spread between p95 and p50
  - Purpose: Measure latency variance/tail behavior
  - Formula: `latency_p95 - latency_p50`
- **traffic_change_rate**: Rate of traffic change
  - Purpose: Detect traffic ramps and drops
  - Formula: `Δrequest_rate / Δtime`

### Lag Features

- **request_rate_lag_1 to 5**: Historical request rates
  - Purpose: Time-series pattern learning
  - Captures recent traffic history
- **latency_p95_lag_1 to 5**: Historical latency
  - Purpose: Latency trend prediction
  - Captures performance history
- **cpu_usage_lag_1 to 5**: Historical CPU usage
  - Purpose: Resource utilization trends
  - Captures load history

### Rolling Statistics

- **rolling_mean_3, 5**: Short-term averages
  - Purpose: Smooth out noise
  - Capture recent trends
- **rolling_std_3, 5**: Short-term variability
  - Purpose: Detect stability/volatility
  - Capture traffic patterns

---

## Validation Results

### Data Quality Checks

- [x] No null values in final dataset
- [x] No infinite values
- [x] All features have valid ranges
- [x] Time-series continuity maintained
- [x] Feature distributions reasonable

### Feature Quality

- [x] Per-replica features calculated correctly
- [x] Latency diff always non-negative
- [x] Traffic change rate captures ramps
- [x] Lag features aligned properly
- [x] Rolling windows computed correctly

---

## Time-Aware Dataset

The dataset is now time-aware with:

- Historical context (lag features)
- Temporal patterns (rolling statistics)
- Rate of change (traffic_change_rate)
- Per-instance metrics (per-replica features)

Ready for:

- Time-series forecasting models
- LSTM/Transformer training
- Sequence prediction
- Multi-step ahead prediction

---

## Next Steps

### Task 1.3: Define Prediction Target

- Define primary target: predict `request_rate`, `latency_p95` (next step)
- Define secondary target: predict `replica_count` (derived)
- Implement target variable calculation
- Validate target variables
- Document prediction logic

### Dataset Ready For

- Baseline model training (Stage 2)
- Transformer model training (Stage 3)
- Time-series forecasting
- Multi-objective optimization

---

## Technical Notes

### Performance

- Execution time: ~5 seconds
- Memory usage: <600 MB
- Vectorized operations used throughout

### Reproducibility

- All steps documented
- Metadata saved
- Original dataset preserved
- Featured dataset versioned

---

## Conclusion

Feature engineering complete. Created 31 new features for a total of 40 features. Dataset is now time-aware with historical context, temporal patterns, and derived metrics. 99.98% data retention. Ready for modeling.

**Status: ✓ COMPLETE - Ready for Task 1.3 (Define Prediction Target)**
