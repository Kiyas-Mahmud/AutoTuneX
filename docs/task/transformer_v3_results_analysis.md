# Transformer V3.0 (Gap-Aware) Results Analysis

**Author**: AI Research Assistant  
**Date**: February 27, 2026  
**Status**: Execution Complete - Partial Success  
**Version**: 3.0 - Gap-Aware Sequences

---

## 📊 Executive Summary

The Transformer V3.0 with proper gap handling was implemented and executed to fix the critical timestamp gap bug from V2.0. The results show **partial success**: the gap handling fixed the catastrophic failure for request rate (R² became positive), but the model still significantly underperforms the Linear Regression baseline and latency prediction remains problematic.

### Key Results

| Metric              | Target | V1.0 (Original) | V2.0 (Broken) | V3.0 (Fixed)    | Baseline (LR) |
| ------------------- | ------ | --------------- | ------------- | --------------- | ------------- |
| **Request Rate R²** | Test   | 0.5067          | -0.1059       | **0.2930** ✅   | **0.8672** 🏆 |
| **Latency P95 R²**  | Test   | -0.1541         | -0.5430       | **-0.4293** ❌  | **0.6894** 🏆 |
| **Status**          |        | Poor            | Catastrophic  | **Partial Fix** | Best          |

**Key Findings**:

- ✅ **Gap handling partially worked** - Request rate R² is now positive (was -0.11 in V2.0)
- ❌ **Still underperforms baseline** - 66% worse than Linear Regression (0.29 vs 0.87)
- ❌ **Latency still negative R²** - Model worse than predicting the mean
- ⚠️ **Pipeline may have additional issues** - Cheating test only R²=0.66 (expected >0.8)

---

## 🔬 Detailed Results Breakdown

### 1. Gap Detection & Data Preparation

#### Gap Analysis Results

```
Total intervals analyzed: 20,441
Gaps found: 21 (0.10% of data)
Largest gap: 114,550 seconds (31.8 hours)
Gap threshold: >15 seconds

First 5 gaps:
  Row 1978: 20,941s (5.8 hours)
  Row 2530: 40s
  Row 3052: 30s
  Row 3602: 37,921s (10.5 hours)
  Row 6719: 13,670s (3.8 hours)
```

**Analysis**:

- Gaps are relatively rare (0.1%) but **extremely large** (hours, not seconds)
- The largest gap is 31.8 hours - this would completely destroy temporal continuity
- V1.0 and V2.0 treated these as 10-second intervals → learned invalid patterns

#### Segmentation Results

```
Total segments created: 22
Valid segments (>40 samples): 11
Samples retained: 20,331 / 20,441 (99.5%)
Samples lost: 110

Largest segments:
  Segment 9: 8,386 samples (23.3 hours)
  Segment 10: 3,835 samples (10.7 hours)
  Segment 4: 3,032 samples (8.4 hours)
```

**Analysis**:

- ✅ Lost only 0.5% of data (110 samples) - minimal data loss
- ✅ Largest segment has 23 hours of continuous data - sufficient for training
- ✅ All segments verified continuous (max internal gap: 10.1s)

#### Sequence Creation

```
Window size: 10 timesteps
Total sequences: 20,221
Sequence shape: (20,221, 10, 39 features)
Train/Val/Test split: 14,154 / 3,033 / 3,034 (70/15/15)
```

**Analysis**:

- ✅ Sequences only created within continuous segments
- ✅ No shuffle applied (preserves temporal order)
- ✅ Sufficient sequences for training (14K training samples)

---

### 2. Model Architecture & Training

#### Model Configuration

```
Architecture: Simple Transformer (2 blocks)
Positional encoding: Learned embedding
Attention heads: 4
Head size: 64
Feed-forward dim: 128
MLP units: [128, 64]

Total parameters: 115,606 (451.59 KB)
Learning rate: 0.0001 (fixed)
Loss function: MSE (no spike weighting)
Data augmentation: None
```

**Analysis**:

- ✅ Simplified from V2.0 (removed all fancy features)
- ✅ Moderate parameter count (vs 213K in V2.0)
- ✅ Standard MSE loss (no custom weighting)

#### Training Results

```
Epochs trained: 24
Best validation loss: 1.1152
Early stopping: Triggered at epoch 24 (restored epoch 9)
```

**Analysis**:

- ⚠️ Training stopped early (24 epochs vs max 100)
- ⚠️ Restored weights from epoch 9 - peak was early in training
- This suggests either:
  - Model converged quickly (good)
  - Model started overfitting (bad)
  - Learning rate too high or data mismatch (needs investigation)

---

### 3. Performance Metrics

#### Request Rate Prediction

| Set            | MAE   | RMSE   | R²         | Status      |
| -------------- | ----- | ------ | ---------- | ----------- |
| **Train**      | 3,441 | 4,927  | **0.5758** | ⚠️ Moderate |
| **Validation** | 7,245 | 9,099  | **0.1465** | ⚠️ Poor     |
| **Test**       | 8,981 | 10,312 | **0.2930** | ⚠️ Poor     |

**Analysis**:

- ✅ **Positive R² across all sets** - Gap handling fixed the negative R² issue
- ❌ **Large gap between train (0.58) and test (0.29)** - Overfitting to training data
- ❌ **High errors** - RMSE of 10,312 requests/sec is significant
- ❌ **66% worse than baseline** - Linear Regression achieves 0.87 R²

**Verdict**: Gap handling worked but model still underperforms significantly.

---

#### Latency P95 Prediction

| Set            | MAE    | RMSE   | R²          | Status           |
| -------------- | ------ | ------ | ----------- | ---------------- |
| **Train**      | 0.0301 | 0.0530 | **0.1887**  | ⚠️ Poor          |
| **Validation** | 0.0228 | 0.0521 | **0.0755**  | ⚠️ Poor          |
| **Test**       | 0.0726 | 0.1106 | **-0.4293** | ❌ **Negative!** |

**Analysis**:

- ❌ **Test R² still negative (-0.43)** - Model worse than predicting the mean
- ❌ **Train R² only 0.19** - Model struggles even on training data
- ❌ **Test MAE 0.0726 seconds** - 72.6ms error on latency predictions
- ❌ **162% worse than baseline** - Linear Regression achieves 0.69 R²

**Verdict**: Gap handling did NOT fix latency prediction. Additional issues present.

---

### 4. Sanity Check: Cheating Test

```
Task: Predict request_rate(t) using ONLY request_rate(t-1)
Model: Simple Linear Regression
Result: R² = 0.6564

Status: ⚠️ MARGINAL - Moderate correlation
Expected: R² > 0.8 for correct pipeline
```

**Analysis**:

- ⚠️ **R² of 0.66 is lower than expected** - Should be >0.8 for time-series data
- This suggests **additional pipeline issues** beyond the gap bug:
  - Possible data distribution shift between segments
  - Temporal patterns may be weak or noisy
  - The t-1 to t correlation is not as strong as expected

**Implication**: Even with perfect gap handling, the underlying data may have challenges that make it difficult to predict.

---

### 5. Comparison to Baseline

#### Request Rate

| Model             | R²         | vs Baseline | Status        |
| ----------------- | ---------- | ----------- | ------------- |
| Linear Regression | **0.8672** | -           | 🏆 Winner     |
| Transformer V1.0  | 0.5067     | -42%        | ⚠️ Poor       |
| Transformer V2.0  | -0.1059    | -112%       | ❌ Broken     |
| Transformer V3.0  | 0.2930     | **-66%**    | ⚠️ Still poor |

**Improvement V2.0 → V3.0**: +0.3989 (gap fix worked!)  
**Gap to baseline**: -0.5742 (still far behind)

---

#### Latency P95

| Model             | R²         | vs Baseline | Status       |
| ----------------- | ---------- | ----------- | ------------ |
| Linear Regression | **0.6894** | -           | 🏆 Winner    |
| Transformer V1.0  | -0.1541    | -122%       | ❌ Bad       |
| Transformer V2.0  | -0.5430    | -179%       | ❌ Worse     |
| Transformer V3.0  | -0.4293    | **-162%**   | ❌ Still bad |

**Improvement V2.0 → V3.0**: +0.1137 (slight improvement)  
**Still negative**: Gap fix was not sufficient

---

## 🔍 Root Cause Analysis: Why Still Underperforming?

### 1. **Gap Handling Fixed Request Rate, Not Latency**

**Observation**: Request rate became positive R² (0.29) but latency still negative (-0.43)

**Possible Reasons**:

- **Latency is inherently noisier** than request rate
  - Request rate: smooth, predictable traffic patterns
  - Latency: influenced by many factors (CPU, memory, network, queuing)
- **Non-linear relationships** dominate latency prediction
  - Latency may spike non-linearly with load
  - Transformer's attention mechanism insufficient to capture these patterns
- **Different temporal dependencies**
  - Request rate: Strong t-1 correlation
  - Latency: May depend on complex interactions over multiple timesteps

---

### 2. **Train-Test Performance Gap (Overfitting)**

**Observation**: Train R²=0.58 but Test R²=0.29 for request rate

**Possible Reasons**:

- **Segments have different characteristics**
  - Training on segment 9 (23 hours, 8K samples)
  - Testing on different segments with different patterns
- **Window size too small (10 timesteps)**
  - Captures only 100 seconds of history
  - May not see full pattern cycling
- **Model complexity vs data variability**
  - 115K parameters may still be too many
  - Overfitting to training segment patterns

---

### 3. **Weak t-1 Correlation (Cheating Test: R²=0.66)**

**Observation**: Simple t-1 prediction only achieves R²=0.66 (expected >0.8)

**Possible Reasons**:

- **Data has high intrinsic noise**
  - Traffic patterns may not be strongly autocorrelated
  - External factors cause unpredictable changes
- **Segmentation disrupts continuity**
  - While segments are continuous, they're from different time periods
  - Each segment may represent different workload characteristics
- **10-second sampling may be too coarse**
  - Important sub-10-second dynamics missed
  - Aliasing effects from undersampling

---

### 4. **Linear Patterns Dominate (Linear Regression R²=0.87)**

**Observation**: Simple Linear Regression beats complex Transformer by 3x

**Possible Reasons**:

- **Autoscaling follows mostly linear patterns**
  - Request rate increases → replicas increase → capacity increases
  - Simple proportional relationships
- **Transformer's complexity is overkill**
  - Attention mechanism adds noise without capturing useful patterns
  - More parameters = more overfitting on small dataset
- **Linear models generalize better**
  - On this dataset size (14K samples, 39 features)
  - Fewer parameters (39 vs 115K) = better generalization

---

## 📈 Progress Summary: V1.0 → V2.0 → V3.0

### Request Rate R² Evolution

```
V1.0 (Original):     0.5067  (poor, gap bug present)
                        ↓
V2.0 (Over-engineered): -0.1059  (catastrophic, gap bug + too many changes)
                        ↓
V3.0 (Gap-aware):    0.2930  (partial fix, but worse than V1.0!)
```

**Surprising Result**: V3.0 is **worse than V1.0** despite fixing the gap bug!

**Why?**

- V1.0 window size = 10 (fewer gap-spanning sequences)
- V3.0 loses 0.5% of data (segments <40 samples removed)
- V3.0 may be splitting data into segments that are harder to learn from
- Segmentation may remove critical transition periods

---

### Latency P95 R² Evolution

```
V1.0 (Original):     -0.1541  (negative, gap bug present)
                        ↓
V2.0 (Over-engineered): -0.5430  (worse, gap bug + more complexity)
                        ↓
V3.0 (Gap-aware):    -0.4293  (slight improvement, still negative)
```

**Result**: All versions fail on latency prediction.

---

## 💡 Lessons Learned

### 1. **Gap Handling Is Necessary But Not Sufficient**

**What we learned**:

- Fixing temporal continuity improved request rate (negative → positive)
- But improvement is modest (can't beat baseline)
- Latency still fails despite gap fix
- **Other factors dominate performance**

---

### 2. **Segmentation Has Trade-offs**

**Pros**:

- ✅ Guarantees temporal continuity
- ✅ Prevents learning from invalid gaps
- ✅ Loses only 0.5% of data

**Cons**:

- ❌ Creates multiple disconnected time periods
- ❌ Each segment has different characteristics
- ❌ Train/test may come from very different segments
- ❌ May remove critical transition periods

**Better approach**:

- Use a single long continuous segment for train/val/test
- If gaps exist, fill them with interpolation instead of splitting
- Or collect better data without gaps

---

### 3. **Window Size Matters More Than We Thought**

**Evidence**:

- Window size 10 = 100 seconds of history
- Autoscaling cycles are likely hourly or daily
- 100 seconds may capture only noise, not true patterns

**Recommendation**:

- Test window sizes: 30 (5 min), 60 (10 min), 180 (30 min), 360 (1 hour)
- Need longer windows to capture autoscaling cycles

---

### 4. **Latency Is Fundamentally Different From RequestRate**

**Key differences**:

| Aspect              | Request Rate           | Latency P95           |
| ------------------- | ---------------------- | --------------------- |
| **Predictability**  | High (R²=0.87 with LR) | Low (R²=0.69 with LR) |
| **Autocorrelation** | Strong (smooth curves) | Weak (spiky, noisy)   |
| **Transformer R²**  | 0.29 (positive)        | -0.43 (negative)      |
| **Linearity**       | Mostly linear          | Non-linear spikes     |

**Recommendation**:

- Use Linear Regression for request rate (R²=0.87 is excellent)
- Try specialized models for latency:
  - Quantile regression for P95 specifically
  - Spike detection + separate model
  - Tree-based methods (XGBoost) for non-linearity

---

### 5. **Transformers Not Suitable for This Dataset**

**Evidence**:

- 3 versions tried, all underperform Linear Regression
- Best Transformer R²=0.51 (V1.0), Linear R²=0.87
- Gap fix didn't close the gap (0.29 vs 0.87)
- Latency: All versions negative R²

**Why Transformers fail here**:

- Dataset too small (14K samples vs 115K parameters)
- Patterns are mostly linear (Transformer overkill)
- Short window size (10 timesteps) doesn't need attention
- High noise-to-signal ratio

**When Transformers work**:

- Large datasets (>100K samples)
- Complex temporal patterns (NLP, multi-scale time-series)
- Long sequences (100+ timesteps)
- Low noise, strong patterns

---

## 🎯 Recommendations

### Immediate Actions

#### 1. **Accept Linear Regression for Production** 🏆

**Rationale**:

- R² = 0.87 for request rate (excellent)
- R² = 0.69 for latency (good)
- Fast inference (<1ms)
- Interpretable coefficients
- No hyperparameter tuning needed
- Production-ready TODAY

**Action**: Move to Stage 4 with Linear Regression as prediction model.

---

#### 2. **Try LSTM for Research Track** 🔬

**Why LSTM instead of Transformer**:

- Better suited for small datasets
- Fewer parameters (10-20K vs 115K)
- Proven track record on time-series
- Expected R² = 0.65-0.75

**Simple LSTM baseline**:

```python
model = keras.Sequential([
    layers.LSTM(64, return_sequences=True, input_shape=(window_size, n_features)),
    layers.Dropout(0.2),
    layers.LSTM(32),
    layers.Dropout(0.2),
    layers.Dense(16, activation='relu'),
    layers.Dense(2)  # request_rate + latency
])
```

**Expected outcome**:

- Request rate R²: 0.60-0.70 (better than Transformer)
- Latency R²: 0.30-0.45 (still below baseline)

---

#### 3. **Separate Models for Request Rate and Latency**

**Rationale**:

- Request rate: Well-predicted by linear models
- Latency: Requires specialized approach

**Strategy**:

- Request rate: Linear Regression (R²=0.87) ✅
- Latency:
  - Option A: XGBoost (handles non-linearity)
  - Option B: Quantile regression (directly model P95)
  - Option C: Ensemble (Linear + tree + neural)

---

### Short-term Experiments (If Continuing Research)

#### 1. **Test Larger Window Sizes**

```python
for window_size in [30, 60, 180, 360]:
    # 30 = 5 min, 60 = 10 min, 180 = 30 min, 360 = 1 hour
    build_sequences(window_size)
    train_model()
    evaluate()
```

**Expected impact**: May improve R² by 0.1-0.2 if cycles are captured.

---

#### 2. **Try Alternative Architectures**

**TCN (Temporal Convolutional Network)**:

- Dilated causal convolutions
- Expected R² = 0.70-0.75
- Better than LSTM on some benchmarks

**1D CNN + LSTM Hybrid**:

- CNN extracts local patterns
- LSTM captures temporal dependencies
- Expected R² = 0.65-0.73

---

#### 3. **Feature Engineering**

Current: Raw 39 features  
Better:

- Add time-of-day encoding (hour, minute)
- Add day-of-week encoding
- Add rolling statistics (mean, std over last N timesteps)
- Add lag features (t-1, t-5, t-10)

**Expected impact**: +0.05-0.15 R²

---

#### 4. **Hyperparameter Tuning (Window Size First)**

Priority order:

1. **Window size** [10, 30, 60, 180] ← **Most important**
2. Learning rate [1e-5, 1e-4, 1e-3]
3. Architecture depth [1, 2, 3, 4 blocks]
4. Batch size [16, 32, 64]

**Don't tune**:

- Head size, number of heads (proven not critical)
- Positional encoding (doesn't help)
- Dropout (0.2 is standard)

---

### Long-term Strategy

#### 1. **Collect More Data**

- Current: 20K samples (0.5% have gaps)
- Target: 100K+ samples
- Duration: Weeks → Months
- Continuity: No gaps if possible

---

#### 2. **Multi-Objective Decision Engine (Stage 4)**

Use Linear Regression predictions to:

- Predict request rate (R²=0.87)
- Predict latency (R²=0.69)
- Input to decision algorithm
- Optimize: cost + performance + SLO compliance

---

#### 3. **Revisit Deep Learning Later**

After:

- Collecting 100K+ samples
- Longer continuous segments
- Linear Regression hits ceiling (<0.9 R²)

Then try:

- Temporal Fusion Transformer
- Autoformer (2021)
- PatchTST (2023)

---

## ✅ Action Items

### Critical (This Week)

- [ ] **Decision**: Accept Linear Regression for production OR continue research?
- [ ] **If production**: Move to Stage 4 (Decision Engine)
- [ ] **If research**: Implement LSTM baseline (1 day)

### High Priority (Next 2 Weeks)

- [ ] Test window sizes [30, 60, 180] with simple Transformer
- [ ] Implement LSTM model
- [ ] Implement XGBoost for latency prediction
- [ ] Compare all models side-by-side

### Medium Priority (Next Month)

- [ ] Separate models for request rate vs latency
- [ ] Feature engineering (time encoding, rolling stats)
- [ ] TCN implementation
- [ ] Hyperparameter tuning

### Low Priority (Future)

- [ ] Collect more data (100K+ samples)
- [ ] Revisit Transformer with proper dataset
- [ ] Research latest time-series architectures
- [ ] Production deployment guide

---

## 📊 Final Performance Summary

| Model                 | Request Rate R² | Latency P95 R² | Parameters | Status                   |
| --------------------- | --------------- | -------------- | ---------- | ------------------------ |
| **Linear Regression** | **0.8672** 🏆   | **0.6894** 🏆  | 80         | **Production Ready**     |
| Random Forest         | 0.6653          | 0.5830         | N/A        | Research                 |
| XGBoost               | 0.6580          | 0.5680         | N/A        | Research                 |
| Transformer V1.0      | 0.5067          | -0.1541        | 213K       | Failed (gap bug)         |
| Transformer V2.0      | -0.1059         | -0.5430        | >213K      | Failed (over-engineered) |
| **Transformer V3.0**  | **0.2930**      | **-0.4293**    | 115K       | **Failed (still poor)**  |
| LSTM (Expected)       | 0.65-0.70       | 0.30-0.45      | 15K        | Research track           |
| TCN (Expected)        | 0.70-0.75       | 0.35-0.50      | 25K        | Research track           |

---

## 🎓 Key Takeaways

### What Worked ✅

1. **Gap detection and segmentation** - Successfully identified and handled temporal discontinuities
2. **Request rate became positive** - Gap fix prevented catastrophic failure
3. **Pipeline correctness** - No shuffle, proper scaling, correct time splits
4. **Simplification approach** - Removed all fancy features to isolate gap fix

### What Didn't Work ❌

1. **Gap fix alone insufficient** - R² improved but still far below baseline
2. **Latency still negative** - Fundamental challenges beyond gap handling
3. **Transformer architecture mismatch** - Not suitable for this dataset size/pattern
4. **Segmentation trade-offs** - May have created harder learning problem

### What We Learned 📚

1. **Data quality > model complexity** - Cannot fix with architecture alone
2. **Linear patterns dominate** - 0.87 R² with simple regression
3. **Latency ≠ request rate** - Different characteristics require different approaches
4. **Small datasets favor simple models** - 14K samples insufficient for 115K parameters
5. **Temporal continuity is necessary but not sufficient** - Other factors matter more

---

## 📁 Related Documents

- [Transformer V2.0 Failure Analysis](transformer_v2_failure_analysis.md) - Deep dive on V2.0 catastrophic failure
- [Stage 3 Transformer Analysis](../tasks/stage_3_transformer_analysis.md) - Original recommendations
- [Alternative Models Recommendation](alternative_models_recommendation.md) - LSTM/TCN guide
- [Transformer Fixed Gap Handling Notebook](../../model/transformer/transformer_fixed_gap_handling.ipynb) - V3.0 source code

---

**Document Status**: Complete - Results Analysis  
**Execution Date**: February 26, 2026 (21:17 UTC)  
**Verdict**: Partial success - Gap handling worked but insufficient  
**Recommendation**: Use Linear Regression for production, LSTM for research

**Last Updated**: February 27, 2026  
**Next Steps**: Decision point - production vs continued research
