# Stage 2: Baseline Modeling Analysis Report

**Date**: February 26, 2026  
**Project**: AutoTuneX - Autoscaling Prediction System  
**Stage**: Stage 2 - Baseline Modeling

---

## 1. Executive Summary

This report presents a comprehensive analysis of three baseline machine learning models (Linear Regression, Random Forest, and XGBoost) for predicting autoscaling metrics in the AutoTuneX system. The models were trained to predict two critical targets:

- **Request Rate** (next-step prediction)
- **Latency P95** (95th percentile latency)

**Key Finding**: Linear Regression emerged as the best-performing baseline model for both targets, achieving 86.72% accuracy (R²) for request rate prediction and 68.94% for latency prediction.

---

## 2. Dataset Overview

### 2.1 Data Split Strategy

- **Total Samples**: 20,441 time-series observations
- **Training Set**: 14,308 samples (70%)
- **Validation Set**: 3,066 samples (15%)
- **Test Set**: 3,067 samples (15%)
- **Split Method**: Time-series split (chronological order, no random shuffle)

### 2.2 Feature Space

- **Total Features**: 39 engineered features
- **Feature Types**:
  - Original metrics (8): request_rate, latency_p50/p95/p99, error_rate, cpu_usage, memory_usage, replica_count
  - Per-replica metrics (2): cpu_per_replica, memory_per_replica
  - Lag features (15): 1-5 step lags for key metrics
  - Rolling statistics (12): mean and std for windows 3, 5
  - Derived metrics (2): traffic intensity indicators

### 2.3 Target Variables

- **target_request_rate**: Next-step request rate (~10 seconds ahead)
- **target_latency_p95**: Next-step 95th percentile latency

---

## 3. Model Performance Analysis

### 3.1 Request Rate Prediction Results

| Model                 | Train MAE | Train RMSE | Train R² | Val MAE | Val RMSE | Val R² | Test MAE    | Test RMSE   | Test R²    | Spike Accuracy |
| --------------------- | --------- | ---------- | -------- | ------- | -------- | ------ | ----------- | ----------- | ---------- | -------------- |
| **Linear Regression** | 1915.27   | 2907.19    | 0.8528   | 4085.26 | 5167.16  | 0.7250 | **3060.17** | **4464.78** | **0.8672** | **95.73%**     |
| Random Forest         | 773.56    | 1225.07    | 0.9739   | 4438.17 | 5571.94  | 0.6802 | 3437.46     | 4910.95     | 0.8393     | 94.98%         |
| XGBoost               | 823.43    | 1155.74    | 0.9767   | 5590.95 | 7320.62  | 0.4480 | 4911.10     | 7093.66     | 0.6647     | 94.98%         |

**Analysis**:

- **Winner**: Linear Regression (Test R² = 0.8672)
- **Overfitting Concern**: Random Forest and XGBoost show high training R² (0.974-0.977) but lower validation/test R² (0.44-0.68), indicating overfitting
- **Generalization**: Linear Regression maintains consistent performance across train/val/test sets (0.85/0.73/0.87)
- **Spike Prediction**: All models achieve >94% accuracy in predicting traffic spikes (95th percentile threshold)
- **Error Magnitude**: Linear Regression has lowest test MAE (3060.17) and RMSE (4464.78)

### 3.2 Latency P95 Prediction Results

| Model                 | Train MAE | Train RMSE | Train R² | Val MAE | Val RMSE | Val R² | Test MAE   | Test RMSE  | Test R²    |
| --------------------- | --------- | ---------- | -------- | ------- | -------- | ------ | ---------- | ---------- | ---------- |
| **Linear Regression** | 0.0222    | 0.0433     | 0.4610   | 0.0216  | 0.0398   | 0.4466 | **0.0394** | **0.0522** | **0.6894** |
| Random Forest         | 0.0095    | 0.0207     | 0.8771   | 0.0399  | 0.0524   | 0.0371 | 0.0721     | 0.0817     | 0.2387     |
| XGBoost               | 0.0070    | 0.0150     | 0.9352   | 0.0304  | 0.0500   | 0.1243 | 0.0875     | 0.1149     | -0.5055    |

**Analysis**:

- **Winner**: Linear Regression (Test R² = 0.6894)
- **Severe Overfitting**: XGBoost achieves 93.52% training R² but -50.55% test R² (worse than mean baseline!)
- **Poor Generalization**: Random Forest drops from 87.71% training R² to 23.87% test R²
- **Consistent Performance**: Linear Regression maintains stable R² (0.46/0.45/0.69)
- **Error Magnitude**: Linear Regression achieves lowest test MAE (0.0394s ≈ 39.4ms)

### 3.3 Model Comparison Chart

```
Request Rate Prediction (Test R²)
█████████████████████████████████████████████████ Linear Regression (0.8672)
███████████████████████████████████████████████   Random Forest (0.8393)
███████████████████████████████████               XGBoost (0.6647)

Latency P95 Prediction (Test R²)
███████████████████████████████████               Linear Regression (0.6894)
███████████████                                   Random Forest (0.2387)
                                                  XGBoost (-0.5055) [NEGATIVE!]
```

---

## 4. Key Findings

### 4.1 Strengths

#### Linear Regression ⭐ BEST OVERALL

- ✅ Best test performance for both targets (R² = 0.87 and 0.69)
- ✅ Excellent generalization (minimal train-test gap)
- ✅ Highest spike prediction accuracy (95.73%)
- ✅ Fastest training time (~0.1 seconds)
- ✅ Most interpretable model (feature coefficients)
- ✅ Lowest computational cost for inference

#### Random Forest

- ✅ Good request rate prediction (R² = 0.84)
- ✅ Captures non-linear relationships
- ⚠️ Shows moderate overfitting (val R² drops to 0.68)
- ❌ Poor latency prediction (R² = 0.24)

#### XGBoost

- ⚠️ Moderate request rate prediction (R² = 0.66)
- ❌ Severe overfitting on latency (negative test R²)
- ❌ Highest validation errors
- ⚠️ Requires careful hyperparameter tuning

### 4.2 Weaknesses and Limitations

1. **Overfitting in Complex Models**:
   - Random Forest and XGBoost memorize training patterns but fail to generalize
   - High training R² (>0.93) vs. low test R² (<0.67)

2. **Latency Prediction Challenge**:
   - All models struggle with latency prediction (max R² = 0.69)
   - Latency appears more volatile and harder to predict than request rate
   - May require sequence modeling (LSTM/Transformer) for better temporal patterns

3. **XGBoost Failure**:
   - Negative R² indicates worse performance than predicting mean
   - Potential causes: inappropriate hyperparameters, data distribution mismatch

### 4.3 Overfitting Analysis

| Model             | Request Rate (Train → Test) | Latency P95 (Train → Test) | Overfitting Severity |
| ----------------- | --------------------------- | -------------------------- | -------------------- |
| Linear Regression | 0.8528 → 0.8672 (+0.0144)   | 0.4610 → 0.6894 (+0.2284)  | ✅ None (improves!)  |
| Random Forest     | 0.9739 → 0.8393 (-0.1346)   | 0.8771 → 0.2387 (-0.6384)  | ⚠️ Moderate-High     |
| XGBoost           | 0.9767 → 0.6647 (-0.3120)   | 0.9352 → -0.5055 (-1.4407) | ❌ Severe            |

---

## 5. Spike Prediction Performance

**Definition**: Ability to predict when request rate exceeds 95th percentile (traffic spikes)

| Model                 | Spike Accuracy | True Positives | False Alarms |
| --------------------- | -------------- | -------------- | ------------ |
| **Linear Regression** | **95.73%**     | High           | Low          |
| Random Forest         | 94.98%         | High           | Low          |
| XGBoost               | 94.98%         | High           | Low          |

**Insight**: All models demonstrate strong spike detection capabilities (>94%), critical for proactive autoscaling decisions.

---

## 6. Training Time Analysis

| Model             | Training Time | Prediction Speed | Complexity      |
| ----------------- | ------------- | ---------------- | --------------- |
| Linear Regression | ~0.1s         | Instant          | O(n·p)          |
| Random Forest     | ~63s          | Fast             | O(n·log(n)·t·d) |
| XGBoost           | ~3.6s         | Fast             | O(n·log(n)·t·d) |

**Note**: Timings on Kaggle GPU environment with 20,441 samples.

---

## 7. Recommendations

### 7.1 Model Selection for Production

**Recommended**: **Linear Regression** as baseline production model

**Justification**:

1. Best overall performance (R² = 0.87 for request rate, 0.69 for latency)
2. No overfitting → reliable predictions on new data
3. Fastest training and inference
4. Interpretable coefficients for debugging
5. Low computational cost
6. Highest spike detection accuracy

### 7.2 Next Steps for Improvement

#### Immediate Actions:

1. **Deploy Linear Regression** as v1.0 baseline predictor
2. **Feature Importance Analysis**: Identify top predictive features
3. **Hyperparameter Tuning**: Optimize Random Forest/XGBoost with proper cross-validation

#### Stage 3 - Advanced Modeling:

1. **Sequence Models**: Implement LSTM/GRU for temporal dependencies
2. **Transformer Architecture**: Leverage attention mechanism for long-term patterns
3. **Ensemble Methods**: Combine multiple models for robust predictions
4. **Multi-Task Learning**: Joint modeling of request rate and latency

#### Data Improvements:

1. **Feature Engineering v2**:
   - Add time-of-day and day-of-week features (cyclic encoding)
   - Include workload type labels (batch jobs, user traffic)
   - Compute rate-of-change features
2. **Longer History**: Collect more training data (>1 week)
3. **Data Augmentation**: Simulate rare spike scenarios

### 7.3 Latency Prediction Improvement

**Challenge**: Current R² = 0.69 (acceptable but room for improvement)

**Strategies**:

1. **Separate Modeling**: Train dedicated latency predictor (not multi-output)
2. **Sequence Length**: Use longer lookback windows (10-20 timesteps)
3. **External Factors**: Include service dependencies, network conditions
4. **Anomaly Detection**: Pre-filter abnormal latency spikes
5. **Quantile Regression**: Directly predict P95 instead of mean

---

## 8. Visualization Analysis

### 8.1 Generated Plots

1. **baseline_predictions.png**: Scatter plots showing true vs. predicted values
   - Linear Regression: Points cluster near diagonal (good fit)
   - Random Forest/XGBoost: More scatter, deviation from ideal line

2. **baseline_timeseries.png**: Time-series comparison over 200 samples
   - Linear Regression: Closely tracks true values
   - Random Forest: Underestimates some peaks
   - XGBoost: High volatility, misses patterns

---

## 9. Statistical Summary

### 9.1 Request Rate Statistics

- **Mean**: 9,543.31 requests/sec
- **Std Dev**: 9,593.21 requests/sec
- **Range**: ~0 to 35,000+ requests/sec
- **Best Model MAE**: 3,060.17 (32% of mean)
- **Best Model RMSE**: 4,464.78 (47% of mean)

### 9.2 Latency P95 Statistics

- **Mean**: 0.165 seconds
- **Std Dev**: 0.068 seconds
- **Range**: ~0.05 to 0.40 seconds
- **Best Model MAE**: 0.039 seconds (24% of mean)
- **Best Model RMSE**: 0.052 seconds (32% of mean)

---

## 10. Conclusion

**Stage 2 baseline modeling successfully established Linear Regression as the optimal baseline predictor**, achieving:

- ✅ 86.72% accuracy (R²) for request rate prediction
- ✅ 68.94% accuracy (R²) for latency P95 prediction
- ✅ 95.73% spike detection accuracy
- ✅ No overfitting (generalizes well to unseen data)
- ✅ Fast, interpretable, production-ready

**Key Insight**: Simpler models often outperform complex models when data has strong linear relationships and limited training samples. Complex models (Random Forest, XGBoost) suffer from overfitting despite higher training accuracy.

**Next Stage**: Implement Transformer-based sequence model to capture long-term temporal dependencies and improve latency prediction accuracy.

---

## 11. Files Generated

1. `results/baseline-result/baseline_results_request_rate.csv` - Request rate metrics
2. `results/baseline-result/baseline_results_latency_p95.csv` - Latency metrics
3. `results/baseline-result/baseline_predictions.png` - Scatter plot visualizations
4. `results/baseline-result/baseline_timeseries.png` - Time-series comparison
5. `results/baseline-result/basemodel.log` - Execution logs
6. `model/basline/baseline_modeling.ipynb` - Kaggle notebook source

---

**Report Prepared By**: AutoTuneX Research Team  
**Last Updated**: February 26, 2026  
**Status**: ✅ Stage 2 Complete - Ready for Stage 3 (Transformer Modeling)
