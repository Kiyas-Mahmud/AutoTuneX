# Task 1.3: Define Prediction Target - Report

**Task:** Define Prediction Target  
**Status:** Complete  
**Date:** February 26, 2026  
**File:** data-cleaning/define_prediction_target.ipynb

---

## Objectives Completed

### 1. Define Primary Target

- Created `target_request_rate`: next-step request_rate
- Created `target_latency_p95`: next-step latency_p95
- Purpose: Main prediction objectives for autoscaling

### 2. Define Secondary Target

- Created `target_replica_count`: next-step replica_count
- Purpose: Derived target for scaling decisions

### 3. Implement Target Calculation

- Used shift(-1) for next-step prediction
- Prediction horizon: 1 timestep ahead (~10 seconds)
- Maintained temporal alignment

### 4. Validate Target Variables

- Verified no null values in targets
- Confirmed target statistics reasonable
- Validated temporal alignment
- Checked target distributions

### 5. Document Prediction Logic

- Clear prediction horizon defined
- Target creation methodology documented
- Feature-target separation established
- Ready for model training

---

## Key Metrics

### Dataset Statistics

- Input rows: 20,442
- Output rows: 20,441
- Rows dropped: 1 (last row, no next-step available)
- Retention rate: 99.995%

### Column Statistics

- Feature columns: 40
- Target columns: 3
- Total columns: 43

### Prediction Setup

- Prediction horizon: next_step (~10 seconds ahead)
- Primary targets: 2 (request_rate, latency_p95)
- Secondary targets: 1 (replica_count)

---

## Target Statistics

### target_request_rate

- Mean: 9,543.31 requests/sec
- Std: 9,593.21
- Min: 0.00
- Max: 51,368.82
- Purpose: Predict traffic load

### target_latency_p95

- Mean: 0.165 seconds (165 ms)
- Std: 0.068 seconds
- Min: 0.00
- Max: 0.206 seconds
- Purpose: Predict service performance

### target_replica_count

- Mean: 6.00 replicas
- Std: 0.11
- Min: 0.00
- Max: 6.00
- Purpose: Predict required scaling

---

## Deliverables

### Files Created

1. **data-cleaning/define_prediction_target.ipynb**
   - Target definition pipeline
   - Validation checks
   - Visualization generation

2. **data-cleaning/run_define_prediction_target.py**
   - Executable script version
   - Automated pipeline

3. **data/prediction_ready_dataset.csv**
   - 20,441 rows × 43 columns
   - 40 features + 3 targets
   - Ready for model training

4. **data-cleaning/target_metadata.json**
   - Target statistics
   - Prediction horizon
   - Column information

5. **results/img/prediction_targets.png**
   - Current vs target scatter plots
   - Time series comparison
   - Target validation visualization

---

## Prediction Logic

### Next-Step Prediction

- **Horizon**: 1 timestep ahead
- **Method**: shift(-1) on time series
- **Purpose**: Short-term forecasting for proactive autoscaling

### Primary Targets (Main Objectives)

1. **target_request_rate**
   - Predict upcoming traffic load
   - Enables proactive scaling before overload
   - Critical for capacity planning

2. **target_latency_p95**
   - Predict service performance
   - Enables SLA violation prevention
   - Quality of service indicator

### Secondary Target (Derived)

1. **target_replica_count**
   - Predict required replicas
   - Can be used for direct scaling prediction
   - Alternative to multi-objective optimization

---

## Feature-Target Separation

### Features (40 columns)

- Original metrics (9)
- Per-replica features (2)
- Derived metrics (2)
- Lag features (15)
- Rolling statistics (12)

### Targets (3 columns)

- target_request_rate
- target_latency_p95
- target_replica_count

### Training Setup

```python
X = df[feature_columns]  # 40 features
y_primary = df[['target_request_rate', 'target_latency_p95']]  # 2 primary
y_secondary = df['target_replica_count']  # 1 secondary
```

---

## Validation Results

### Data Quality Checks

- [x] No null values in targets
- [x] All targets have valid ranges
- [x] Temporal alignment verified
- [x] Target distributions reasonable
- [x] Current-target correlation positive

### Visual Validation

- [x] Scatter plots show correlation
- [x] Time series alignment verified
- [x] No data leakage detected
- [x] Target predictability confirmed

---

## Prediction Use Cases

### 1. Traffic Forecasting

- Input: 40 features (current state + history)
- Output: next-step request_rate
- Use: Anticipate traffic changes

### 2. Latency Forecasting

- Input: 40 features (current state + history)
- Output: next-step latency_p95
- Use: Prevent SLA violations

### 3. Replica Prediction (Optional)

- Input: 40 features (current state + history)
- Output: next-step replica_count
- Use: Direct scaling decisions

### 4. Multi-Target Prediction

- Input: 40 features
- Output: all 3 targets simultaneously
- Use: Comprehensive system state prediction

---

## Ready for Modeling

### Stage 2: Baseline Models

Can train:

- Linear Regression (request_rate, latency_p95)
- Random Forest (multi-target)
- XGBoost (separate models or multi-output)

### Stage 3: Transformer

Can use:

- Sequence input: (batch, seq_len, 40 features)
- Multi-output head: 2 or 3 targets
- Attention over time series

### Stage 4: Decision Engine

Can integrate:

- Predicted request_rate → load estimation
- Predicted latency_p95 → SLA monitoring
- Predicted replica_count → scaling hint

---

## Technical Notes

### Prediction Horizon

- Current: 1-step ahead (~10 seconds)
- Can extend: multi-step prediction by shifting further
- Trade-off: accuracy vs planning horizon

### Target Engineering

- Simple shift(-1) approach
- No data leakage (future not in features)
- Temporal causality preserved

### Performance

- Execution time: <5 seconds
- Memory efficient
- Single-pass computation

---

## Next Steps

### Stage 2: Baseline Modeling (Next)

- Prepare train/validation/test splits (time-series)
- Implement Linear Regression
- Implement Random Forest
- Implement XGBoost/LightGBM
- Compare baseline performance

### Expected Workflow

1. Split data: 70% train, 15% val, 15% test
2. Train models on features → targets
3. Evaluate: MAE, RMSE, R² on test set
4. Create baseline performance table

---

## Conclusion

Prediction targets successfully defined. Dataset is now prediction-ready with 40 features and 3 targets. Next-step prediction horizon enables proactive autoscaling. 99.995% data retention. Ready for baseline modeling.

**Status: ✓ COMPLETE - Ready for Stage 2 (Baseline Modeling)**
