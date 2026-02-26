# Stage 3: Transformer Modeling - Detailed Analysis & Improvement Recommendations

**Author**: AI Research Assistant  
**Date**: February 27, 2026  
**Status**: Analysis Complete - Recommendations Provided

---

## 📊 Executive Summary

The Transformer model was successfully implemented for time-series autoscaling prediction but **underperformed compared to baseline models** (Linear Regression, Random Forest, XGBoost). This document analyzes the current configuration, identifies root causes, and provides actionable improvement recommendations.

### Key Findings

- **Request Rate R²**: 0.5067 (26.5% worse than Linear Regression's 0.6894)
- **Latency P95 R²**: -0.1541 (122% worse than Linear Regression's 0.6894)
- **Spike Detection**: 95% accuracy (excellent!)
- **Best Performing Model**: Linear Regression for both metrics

---

## 🔍 Current Model Configuration Analysis

### 1. Architecture Configuration

| Component                      | Current Value | Assessment                                   |
| ------------------------------ | ------------- | -------------------------------------------- |
| **Window Size**                | 10 timesteps  | ⚠️ Too small - insufficient temporal context |
| **Number of Attention Heads**  | 4             | ✅ Adequate for small dataset                |
| **Head Size**                  | 64            | ✅ Reasonable                                |
| **Feed-Forward Dimension**     | 128           | ✅ Appropriate                               |
| **Transformer Blocks**         | 2             | ⚠️ Too shallow for complex patterns          |
| **MLP Units**                  | [128, 64]     | ✅ Good architecture                         |
| **Dropout Rate (Transformer)** | 0.2           | ⚠️ May need adjustment                       |
| **Dropout Rate (MLP)**         | 0.3           | ✅ Reasonable                                |

### 2. Training Configuration

| Parameter                   | Current Value | Assessment                        |
| --------------------------- | ------------- | --------------------------------- |
| **Learning Rate**           | 0.001         | ⚠️ May be too high                |
| **Batch Size**              | 32            | ✅ Appropriate                    |
| **Max Epochs**              | 100           | ✅ Sufficient with early stopping |
| **Early Stopping Patience** | 10            | ✅ Good                           |
| **Optimizer**               | Adam          | ✅ Standard choice                |
| **Loss Function**           | MSE           | ✅ Appropriate for regression     |

### 3. Data Configuration

| Aspect                | Current State  | Assessment       |
| --------------------- | -------------- | ---------------- |
| **Train Split**       | 70%            | ✅ Standard      |
| **Validation Split**  | 15%            | ✅ Adequate      |
| **Test Split**        | 15%            | ✅ Adequate      |
| **Feature Scaling**   | StandardScaler | ✅ Correct       |
| **Target Scaling**    | StandardScaler | ✅ Correct       |
| **Sequence Creation** | Sliding window | ✅ Proper method |

---

## 🚨 Root Cause Analysis: Why Transformer Underperformed

### 1. **Insufficient Temporal Context** (Critical)

**Problem**: Window size of 10 timesteps is too small for the Transformer to capture meaningful temporal patterns.

**Impact**:

- Transformers excel at long-range dependencies
- With only 10 timesteps, the model can't learn complex seasonal or trend patterns
- Linear models perform better on short windows due to simpler relationships

**Evidence**: Strong baseline performance suggests simple linear relationships exist in short windows.

---

### 2. **Dataset Size vs Model Complexity** (Critical)

**Problem**: Deep learning models like Transformers typically require large datasets (10K-1M+ samples), but your dataset appears to be limited.

**Impact**:

- Model may be overfitting to noise
- Complex attention mechanisms can't generalize well
- Simple models (Linear Regression) generalize better on small datasets

**Evidence**:

- Training set has only ~70% of total samples (minus window size)
- Negative R² on Latency P95 indicates worse than mean prediction

---

### 3. **Linear Relationships Dominate** (High Priority)

**Problem**: Your data appears to have strong linear patterns that don't require complex modeling.

**Impact**:

- Linear Regression captures 68.9% of variance
- Added complexity of Transformer introduces unnecessary noise
- Occam's Razor: simpler model is better when performance is similar

**Evidence**: Linear Regression is the best baseline for both targets.

---

### 4. **Hyperparameter Sub-Optimization** (Medium Priority)

**Problem**: No systematic hyperparameter tuning was performed.

**Impact**:

- Learning rate may be causing convergence issues
- Window size is arbitrary (not optimized)
- Architecture depth and width not tuned for this specific problem

---

### 5. **Positional Encoding Limitations** (Low Priority)

**Problem**: Simple learned positional embeddings may not capture complex time patterns.

**Impact**:

- Time-specific patterns (hourly, daily cycles) may not be encoded properly
- Absolute vs relative positioning matters for autoscaling

---

## 💡 Improvement Recommendations

### 🔥 Priority 1: Critical Changes (Implement First)

#### 1.1 **Increase Window Size**

```python
# Current
WINDOW_SIZE = 10

# Recommended: Test multiple values
WINDOW_SIZES = [20, 30, 50, 100]  # Start with 30-50 for balanced approach
```

**Rationale**:

- Autoscaling patterns likely have hourly/daily cycles
- Larger windows capture more temporal context
- Test 30-50 first (1-2 hours if 5-min intervals)

**Expected Impact**: +10-20% R² improvement

---

#### 1.2 **Implement Proper Hyperparameter Tuning**

```python
# Use Keras Tuner or similar
import keras_tuner as kt

def build_tuned_model(hp):
    return build_transformer_model(
        input_shape=input_shape,
        num_outputs=num_outputs,
        head_size=hp.Int('head_size', min_value=32, max_value=128, step=32),
        num_heads=hp.Int('num_heads', min_value=2, max_value=8, step=2),
        ff_dim=hp.Int('ff_dim', min_value=64, max_value=256, step=64),
        num_transformer_blocks=hp.Int('num_blocks', min_value=1, max_value=4),
        mlp_units=[hp.Int('mlp_1', 64, 256, 64)],
        dropout=hp.Float('dropout', 0.1, 0.5, step=0.1)
    )

tuner = kt.BayesianOptimization(
    build_tuned_model,
    objective='val_loss',
    max_trials=20
)
```

**Expected Impact**: +5-15% R² improvement

---

#### 1.3 **Lower Learning Rate with Warm-Up**

```python
# Current
learning_rate = 0.001

# Recommended: Use learning rate schedule
def lr_schedule(epoch, lr):
    # Warm-up for first 5 epochs
    if epoch < 5:
        return 0.0001 * (epoch + 1) / 5
    # Decay after
    return 0.0001 * 0.95 ** (epoch - 5)

lr_scheduler = keras.callbacks.LearningRateScheduler(lr_schedule)

# Or use Transformer-specific schedule
initial_learning_rate = 0.0001
lr_schedule = keras.optimizers.schedules.CosineDecay(
    initial_learning_rate, decay_steps=1000
)
```

**Expected Impact**: +5-10% R² improvement

---

### ⚡ Priority 2: Architecture Enhancements

#### 2.1 **Add More Transformer Blocks**

```python
# Current
num_transformer_blocks = 2

# Recommended
num_transformer_blocks = 4  # Deeper for complex patterns
```

**Expected Impact**: +3-8% R² improvement (if data supports)

---

#### 2.2 **Implement Sinusoidal Positional Encoding**

```python
def get_positional_encoding(seq_len, d_model):
    """
    Create sinusoidal positional encoding for better time representation.
    """
    positions = np.arange(seq_len)[:, np.newaxis]
    dimensions = np.arange(d_model)[np.newaxis, :]

    angle_rates = 1 / np.power(10000, (2 * (dimensions // 2)) / d_model)
    angle_rads = positions * angle_rates

    # Apply sin to even indices, cos to odd indices
    angle_rads[:, 0::2] = np.sin(angle_rads[:, 0::2])
    angle_rads[:, 1::2] = np.cos(angle_rads[:, 1::2])

    return tf.cast(angle_rads, dtype=tf.float32)

# In model building:
x = x + get_positional_encoding(input_shape[0], input_shape[1])
```

**Expected Impact**: +2-5% R² improvement

---

#### 2.3 **Add Layer-wise Learning Rate Decay**

```python
# Apply different learning rates to different layers
optimizer = keras.optimizers.Adam(
    learning_rate=0.0001,
    beta_1=0.9,
    beta_2=0.98,  # Transformer-specific
    epsilon=1e-9
)
```

---

### 🎯 Priority 3: Data & Training Enhancements

#### 3.1 **Data Augmentation for Time-Series**

```python
def augment_sequences(X, y, noise_level=0.01):
    """
    Add slight noise to prevent overfitting on small datasets.
    """
    X_aug = X + np.random.normal(0, noise_level, X.shape)
    return X_aug, y

# Use during training
X_train_aug, y_train_aug = augment_sequences(X_train_seq, y_train_seq)
```

**Expected Impact**: +2-5% R² improvement on test set

---

#### 3.2 **Implement Custom Loss for Spike Detection**

```python
def spike_weighted_mse(y_true, y_pred, spike_weight=2.0):
    """
    Weight errors more heavily during traffic spikes.
    """
    threshold = tf.reduce_mean(y_true) + tf.math.reduce_std(y_true)
    is_spike = tf.cast(y_true > threshold, tf.float32)

    weights = 1.0 + is_spike * (spike_weight - 1.0)
    mse = tf.square(y_true - y_pred)
    weighted_mse = mse * weights

    return tf.reduce_mean(weighted_mse)

# Compile with custom loss
model.compile(optimizer=optimizer, loss=spike_weighted_mse)
```

**Expected Impact**: +5-10% spike accuracy, +2-5% R² on spikes

---

#### 3.3 **Ensemble Approach**

```python
# Train multiple models with different configurations
models = []
for seed in [42, 123, 456, 789, 1011]:
    np.random.seed(seed)
    tf.random.set_seed(seed)
    model = build_transformer_model(...)
    model.fit(...)
    models.append(model)

# Average predictions
predictions = np.mean([m.predict(X_test) for m in models], axis=0)
```

**Expected Impact**: +3-7% R² improvement

---

### 🔬 Priority 4: Advanced Techniques (Optional)

#### 4.1 **Implement Attention Visualization**

```python
# Extract attention weights to understand what model learns
attention_layer = model.get_layer('multi_head_attention')
attention_weights = attention_layer.get_attention_weights()

# Visualize which timesteps are most important
```

---

#### 4.2 **Try Hybrid Architecture**

```python
# Combine CNN (for local patterns) + Transformer (for global patterns)
def build_hybrid_model(input_shape, num_outputs):
    inputs = layers.Input(shape=input_shape)

    # CNN for local feature extraction
    x = layers.Conv1D(64, kernel_size=3, activation='relu', padding='same')(inputs)
    x = layers.Conv1D(128, kernel_size=3, activation='relu', padding='same')(x)

    # Transformer for global dependencies
    x = transformer_encoder(x, head_size=64, num_heads=4, ff_dim=256)
    x = transformer_encoder(x, head_size=64, num_heads=4, ff_dim=256)

    # Output
    x = layers.GlobalAveragePooling1D()(x)
    x = layers.Dense(128, activation='relu')(x)
    outputs = layers.Dense(num_outputs)(x)

    return keras.Model(inputs, outputs)
```

**Expected Impact**: +5-10% R² improvement

---

#### 4.3 **Multi-Task Learning**

```python
# Train on both targets simultaneously with shared representation
# Current approach is already multi-target, but consider:
# - Separate heads for each target
# - Task-specific losses
# - Gradient balancing
```

---

#### 4.4 **Temporal Convolutional Network (TCN) Alternative**

```python
# TCN can sometimes outperform Transformers on small time-series datasets
from tensorflow.keras.layers import Conv1D, Dropout

def residual_block(x, dilation_rate, n_filters, kernel_size):
    # Dilated causal convolution
    conv1 = Conv1D(n_filters, kernel_size, padding='causal',
                   dilation_rate=dilation_rate, activation='relu')(x)
    conv1 = Dropout(0.2)(conv1)

    conv2 = Conv1D(n_filters, kernel_size, padding='causal',
                   dilation_rate=dilation_rate, activation='relu')(conv1)
    conv2 = Dropout(0.2)(conv2)

    # Residual connection
    if x.shape[-1] != n_filters:
        x = Conv1D(n_filters, 1)(x)

    return layers.Add()([x, conv2])
```

**Expected Impact**: May outperform Transformer by +10-20% R²

---

## 📈 Expected Improvement Roadmap

### Phase 1: Quick Wins (1-2 days)

1. ✅ Increase window size to 30-50
2. ✅ Lower learning rate to 0.0001 with warm-up
3. ✅ Add 2 more transformer blocks (total 4)

**Expected Result**: R² improves from 0.51 to 0.60-0.65

---

### Phase 2: Systematic Optimization (3-5 days)

1. ✅ Implement hyperparameter tuning
2. ✅ Add sinusoidal positional encoding
3. ✅ Implement data augmentation

**Expected Result**: R² improves to 0.65-0.73 (competitive with Linear Regression)

---

### Phase 3: Advanced Techniques (1 week)

1. ✅ Ensemble multiple models
2. ✅ Implement custom spike-weighted loss
3. ✅ Try hybrid CNN-Transformer

**Expected Result**: R² improves to 0.73-0.80 (surpass Linear Regression)

---

### Phase 4: Alternative Approaches (Optional)

1. TCN implementation
2. LSTM-Attention hybrid
3. Prophet + ML hybrid

**Expected Result**: Find optimal architecture for this specific dataset

---

## 🎓 Learning Topics for Understanding This Work

Based on your request to learn everything needed to understand Transformer models and architectures:

### 1. **Fundamentals (Start Here)** - 2-3 weeks

- **Neural Network Basics**
  - Perceptrons, activation functions (ReLU, sigmoid, tanh)
  - Forward and backward propagation
  - Loss functions (MSE, MAE, Cross-Entropy)
  - Gradient descent and optimization algorithms
- **Deep Learning Framework**
  - TensorFlow/Keras basics
  - Layer types (Dense, Conv1D, Dropout, etc.)
  - Model compilation, training, and evaluation
  - Callbacks (EarlyStopping, ModelCheckpoint)

**Resources**:

- Andrew Ng's Deep Learning Specialization (Coursera)
- "Deep Learning with Python" by François Chollet
- TensorFlow official tutorials

---

### 2. **Sequence Modeling** - 2-3 weeks

- **Time-Series Fundamentals**
  - Temporal dependencies and autocorrelation
  - Trend, seasonality, and noise
  - Sliding window approach
  - Train/validation/test splits for time-series
- **Recurrent Neural Networks (RNNs)**
  - RNN architecture and hidden states
  - Long Short-Term Memory (LSTM)
  - Gated Recurrent Units (GRU)
  - Vanishing gradient problem

**Resources**:

- "Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow" (Chapter 15)
- Stanford CS230 Deep Learning (Time-Series section)

---

### 3. **Attention Mechanism** - 1-2 weeks

- **Attention Basics**
  - Query, Key, Value concept
  - Attention scores and softmax
  - Context vector computation
- **Self-Attention**
  - How self-attention differs from RNN attention
  - Scaled dot-product attention
  - Why attention solves long-range dependencies

**Resources**:

- "Attention Is All You Need" paper (Vaswani et al., 2017)
- Jay Alammar's "The Illustrated Transformer" blog
- Stanford CS224N NLP with Deep Learning (Attention lectures)

---

### 4. **Transformer Architecture** - 2-3 weeks

- **Core Components**
  - Multi-head attention mechanism
  - Positional encoding (learned vs sinusoidal)
  - Feed-forward networks in Transformers
  - Layer normalization and residual connections
- **Encoder-Decoder Structure**
  - Encoder stack (self-attention + FFN)
  - Decoder stack (masked self-attention + cross-attention)
  - When to use encoder-only vs full Transformer
- **Transformer for Time-Series**
  - Adapting Transformers from NLP to time-series
  - Temporal Fusion Transformers
  - Informer, Autoformer architectures

**Resources**:

- "Attention Is All You Need" paper (read multiple times!)
- "The Annotated Transformer" (Harvard NLP)
- Hugging Face Transformers documentation
- "Temporal Fusion Transformers" paper (Lim et al., 2021)

---

### 5. **Training Strategies** - 1-2 weeks

- **Regularization Techniques**
  - Dropout and its variants
  - Weight decay (L2 regularization)
  - Early stopping strategies
- **Optimization**
  - Adam optimizer and variants (AdamW, RAdam)
  - Learning rate schedules (warm-up, decay, cosine)
  - Batch size effects
  - Gradient clipping
- **Preventing Overfitting**
  - Cross-validation for time-series
  - Data augmentation for sequences
  - Ensemble methods

**Resources**:

- "Deep Learning" book by Goodfellow, Bengio, Courville (Chapter 7-8)
- Papers on learning rate schedules and optimization

---

### 6. **Evaluation & Metrics** - 1 week

- **Regression Metrics**
  - MAE, MSE, RMSE interpretation
  - R² score and adjusted R²
  - Custom metrics (spike accuracy)
- **Model Comparison**
  - Baseline establishment
  - Statistical significance testing
  - Cross-validation strategies
- **Visualization**
  - Learning curves (loss/accuracy over epochs)
  - Prediction vs actual plots
  - Attention weight visualization

**Resources**:

- Scikit-learn documentation on metrics
- "Interpretable Machine Learning" by Christoph Molnar

---

### 7. **Code Understanding & Debugging** - Ongoing

- **Reading AI-Generated Code**
  - Code structure and modularity
  - Function documentation and type hints
  - Debugging strategies (print statements, pdb, TensorBoard)
- **Version Control**
  - Git basics (branch, commit, merge)
  - Reproducibility (random seeds, requirements.txt)
  - Documentation practices

**Resources**:

- "Pro Git" book (free online)
- Real Python tutorials on debugging
- Jupiter notebook best practices

---

### 8. **Advanced Topics (Optional)** - As needed

- **Transformer Variants**
  - BERT (bidirectional encoder)
  - GPT (decoder-only)
  - Vision Transformers (ViT)
  - Time-series specific: Informer, Autoformer, PatchTST
- **Recent Research**
  - Efficient attention mechanisms (Linformer, Performer)
  - Sparse attention patterns
  - Continuous-time modeling

**Resources**:

- Papers With Code (browse state-of-the-art models)
- Arxiv Sanity Preserver (keep up with new papers)
- NeurIPS/ICML conference papers

---

### 9. **Practical Projects** - Throughout Learning

1. **Week 4-6**: Build simple LSTM for time-series
2. **Week 7-9**: Implement basic Transformer from scratch
3. **Week 10-12**: Apply Transformer to your own dataset
4. **Week 13+**: Experiment with improvements and variations

---

### 10. **Recommended Learning Path** (12-16 weeks total)

```
Week 1-3:  Neural Network Fundamentals
Week 4-6:  Sequence Modeling & RNNs
Week 7-8:  Attention Mechanism
Week 9-11: Transformer Architecture
Week 12-13: Training & Optimization
Week 14:   Evaluation & Metrics
Week 15-16: Advanced Topics & Projects
```

**Daily Learning Plan** (2-3 hours/day):

- 40% Theory (videos, reading papers)
- 40% Coding (implementing concepts)
- 20% Practice (Kaggle competitions, projects)

---

## 🔧 Implementation Priority for Your Project

### Immediate Actions (This Week)

1. ✅ Increase window size to 30
2. ✅ Reduce learning rate to 0.0001
3. ✅ Add 2 more transformer blocks
4. ✅ Run experiment and compare

### Short-term (Next 2 Weeks)

1. ✅ Implement hyperparameter tuning
2. ✅ Add sinusoidal positional encoding
3. ✅ Experiment with ensemble approach

### Medium-term (Next Month)

1. ✅ Try TCN as alternative architecture
2. ✅ Implement hybrid CNN-Transformer
3. ✅ Complete comprehensive comparison

---

## 📝 Conclusion

The Transformer model's underperformance is **expected and explainable** given the dataset characteristics:

- Small dataset size (deep learning needs more data)
- Strong linear relationships (simple models excel here)
- Short window size (insufficient temporal context)

**Key Takeaways**:

1. ✅ Linear Regression should remain your production model for now
2. ⚠️ Transformer has potential but needs tuning (window size, learning rate, depth)
3. 🔬 Consider TCN or LSTM as middle-ground between simple and complex
4. 📊 Focus on data collection to support deep learning long-term

**Next Steps**:

1. Proceed to Stage 4 (Multi-Objective Decision Engine)
2. Use Linear Regression as prediction backbone
3. Revisit Transformer after collecting more data
4. Keep Transformer code for future research

---

## 📚 References

1. Vaswani et al. (2017). "Attention Is All You Need"
2. Lim et al. (2021). "Temporal Fusion Transformers for Interpretable Multi-horizon Time Series Forecasting"
3. Goodfellow, Bengio, Courville (2016). "Deep Learning"
4. Chollet (2021). "Deep Learning with Python, Second Edition"
5. Bai et al. (2018). "An Empirical Evaluation of Generic Convolutional and Recurrent Networks for Sequence Modeling"

---

**Document Status**: Complete  
**Action Required**: Review and implement Priority 1 recommendations  
**Next Stage**: Stage 4 - Multi-Objective Decision Engine
