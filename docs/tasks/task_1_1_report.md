# Task 1.1: Clean & Validate Dataset - Report

**Task:** Clean & Validate Dataset  
**Status:** Complete  
**Date:** February 26, 2026  
**File:** data-cleaning/data_cleaning.ipynb

---

## Objectives Completed

### 1. Remove Missing/Corrupted Rows

- Identified and removed rows with null/missing values
- Preserved only corrupted data, not poor performance cases
- Maintained data integrity for analysis

### 2. Sort by Timestamp

- Converted timestamp to datetime format
- Sorted chronologically
- Verified time series continuity

### 3. Ensure Fixed Interval Sampling

- Analyzed time intervals between samples
- Identified most common sampling interval
- Documented interval statistics

### 4. Remove Anomalies (Validation Only)

- Applied logical consistency checks:
  - Verified: latency_p50 ≤ latency_p95 ≤ latency_p99
  - Removed logically impossible measurements
- Validated value ranges:
  - cpu_usage: 0-100%
  - memory_usage: ≥ 0
  - error_rate: 0-1
  - replica_count: ≥ 0
  - request_rate: ≥ 0
  - latencies: ≥ 0

### 5. Check Scaling Event Frequency

- Counted replica_count changes
- Calculated scaling frequency percentage
- Verified sufficient events for learning

### 6. Verify Data Quality

- Confirmed traffic diversity (low/medium/burst)
- Preserved real workload spikes (not removed as outliers)
- Generated correlation analysis
- Created comprehensive visualizations

---

## Key Metrics

### Data Retention

- Original rows: 20,468
- Final rows: 20,447
- Retention rate: 99.90%

### Validation Results

- Corrupted rows removed: 1
- Logical consistency errors removed: 3
- Invalid range violations removed: 17
- Replica scaling events: 22

### Traffic Coverage

- Low traffic (≤P50): 10,224 (50.0%)
- Medium traffic (P50-P95): 9,200 (45.0%)
- Burst traffic (>P95): 1,023 (5.0%)

### Time Range

- Start: 2026-02-11 17:31:26
- End: 2026-02-16 17:50:10
- Duration: 5 days 00:18:44

---

## Deliverables

### Files Created

1. **data-cleaning/data_cleaning.ipynb**
   - Complete cleaning pipeline
   - Validation checks
   - Statistical analysis
   - Visualization generation

2. **data-cleaning/run_cleaning.py**
   - Executable Python script version
   - Parallel-optimized operations
   - Automated execution

3. **data/cleaned_dataset.csv**
   - Clean, validated dataset: 20,447 rows
   - Ready for feature engineering

4. **data-cleaning/cleaning_metadata.json**
   - Cleaning statistics
   - Versioning information
   - Reproducibility metadata

5. **results/img/data_cleaning_overview.png**
   - Time series plots (request_rate, latency, CPU, memory, replicas, errors)
   - Distribution histograms
   - Visual quality assessment

6. **results/img/correlation_matrix.png**
   - Feature correlation heatmap
   - Relationship analysis

7. **data-cleaning/README.md**
   - Pipeline documentation
   - Execution instructions
   - Key principles

---

## Validation Checklist

- [x] Fixed time intervals verified
- [x] Corrupted rows removed (not performance issues)
- [x] Real workload spikes preserved
- [x] Logical consistency validated (p50≤p95≤p99)
- [x] Replica changes sufficient for learning
- [x] Valid ranges enforced (CPU, memory, error_rate)
- [x] Traffic diversity confirmed (low/med/burst)
- [x] Outliers preserved (no over-cleaning)
- [x] Documentation complete
- [x] Dataset versioning maintained

---

## Research Considerations

### Preserved for Analysis

- **Traffic spikes**: Kept all 1,023 high request_rate events
- **Outliers**: Maintained extreme values for real workload analysis
  - request_rate: 0 outliers
  - latency_p95: 3,410 outliers (16.68%) - Real latency variations
  - cpu_usage: 12 outliers (0.06%)
  - memory_usage: 21 outliers (0.10%)
- **Scaling events**: All 22 replica changes preserved
- **Real-world noise**: System variability maintained

### Removed Elements

- **Null/corrupted data**: Missing values
- **Logical errors**: Impossible percentile relationships
- **Invalid ranges**: Out-of-bound measurements

---

## Next Steps

### Task 1.2: Feature Engineering

- Calculate cpu_per_replica
- Calculate memory_per_replica
- Calculate latency_diff (p95-p50)
- Calculate traffic_change_rate
- Add lag features (1-5 steps)
- Add rolling statistics (mean, std)

### Dataset Ready For

- Time-series modeling
- Baseline model training
- Transformer input preparation
- Multi-objective optimization

---

## Technical Notes

### Execution

- Notebook uses parallel computation where applicable
- NumPy vectorized operations for efficiency
- Pandas optimized for time-series operations

### Reproducibility

- All cleaning steps documented
- Metadata saved in JSON format
- Original dataset preserved
- Cleaned dataset versioned

---

## Conclusion

Dataset cleaning and validation complete. The cleaned dataset maintains real-world characteristics while removing only corrupted and logically inconsistent data. Traffic spikes, scaling events, and system variability are preserved for accurate model training.

**Status: ✓ COMPLETE - Ready for Task 1.2 (Feature Engineering)**
