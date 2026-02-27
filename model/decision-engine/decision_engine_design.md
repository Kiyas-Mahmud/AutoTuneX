# Stage 4: Decision Engine Architecture Design

**Author**: AI Research Assistant  
**Date**: February 27, 2026  
**Version**: 1.0

---

## Design Philosophy

The AutoTuneX decision engine converts ML predictions into actionable autoscaling decisions through **multi-objective optimization**. Unlike traditional threshold-based autoscalers, our approach simultaneously optimizes:

1. **Performance** - Minimize latency, maintain SLO compliance
2. **Cost** - Minimize replica count and resource usage
3. **Efficiency** - Target optimal CPU/memory utilization

---

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Decision Engine                       │
│                                                          │
│  ┌────────────────┐      ┌──────────────────┐          │
│  │  Current State │      │   Predictions    │          │
│  │                │      │                  │          │
│  │  • replicas    │      │  • request_rate  │          │
│  │  • metrics     │      │  • latency_p95   │          │
│  │  • history     │      │  • cpu_usage     │          │
│  └────────┬───────┘      └────────┬─────────┘          │
│           │                       │                     │
│           └───────────┬───────────┘                     │
│                       │                                 │
│            ┌──────────▼───────────┐                     │
│            │  Candidate Generator │                     │
│            │  [n-2, n-1, n, n+1]  │                     │
│            └──────────┬───────────┘                     │
│                       │                                 │
│            ┌──────────▼───────────┐                     │
│            │   Metric Predictor   │                     │
│            │  (Linear Regression) │                     │
│            └──────────┬───────────┘                     │
│                       │                                 │
│            ┌──────────▼───────────┐                     │
│            │  Objective Function  │                     │
│            │  Score = Σ w_i * m_i │                     │
│            └──────────┬───────────┘                     │
│                       │                                 │
│            ┌──────────▼───────────┐                     │
│            │   Safety Validator   │                     │
│            │  • Min/max replicas  │                     │
│            │  • Step limits       │                     │
│            │  • Cooldown check    │                     │
│            └──────────┬───────────┘                     │
│                       │                                 │
│            ┌──────────▼───────────┐                     │
│            │  Optimal Decision    │                     │
│            │   (replica count)    │                     │
│            └──────────────────────┘                     │
└─────────────────────────────────────────────────────────┘
```

---

## Objective Function Design

### Mathematical Formulation

```
Score = w_latency * L_norm + w_cpu * C_norm + w_cost * R_norm

where:
  L_norm = normalized latency penalty [0, 1]
  C_norm = normalized CPU deviation from target [0, 1]
  R_norm = normalized replica cost [0, 1]

Constraints:
  w_latency + w_cpu + w_cost = 1.0
  Score ∈ [0, 1], lower is better
```

### Component Normalization

#### 1. Latency Normalization

```python
def normalize_latency(predicted_latency, slo_target, slo_max):
    """
    Normalize latency with SLO-aware penalty.

    Returns:
      0.0 = at or below target (excellent)
      0.5 = at SLO maximum (acceptable)
      1.0 = 2x SLO maximum (unacceptable)
    """
    if predicted_latency <= slo_target:
        # Below target - scale linearly 0 to 0.3
        return 0.3 * (predicted_latency / slo_target)
    elif predicted_latency <= slo_max:
        # Between target and max - scale linearly 0.3 to 0.5
        excess = (predicted_latency - slo_target) / (slo_max - slo_target)
        return 0.3 + 0.2 * excess
    else:
        # Above max - exponential penalty
        excess = (predicted_latency - slo_max) / slo_max
        return 0.5 + 0.5 * min(1.0, excess)
```

#### 2. CPU Normalization

```python
def normalize_cpu(predicted_cpu, target=70, tolerance=10):
    """
    Normalize CPU deviation from target utilization.

    Target: 70% (efficient but with headroom)
    Returns:
      0.0 = exactly at target
      0.5 = at tolerance boundary (60% or 80%)
      1.0 = extremely over/under utilized
    """
    deviation = abs(predicted_cpu - target)

    if deviation <= tolerance:
        # Within tolerance - linear penalty
        return deviation / tolerance * 0.5
    else:
        # Outside tolerance - stronger penalty
        excess = (deviation - tolerance) / target
        return 0.5 + 0.5 * min(1.0, excess)
```

#### 3. Cost Normalization

```python
def normalize_cost(n_replicas, min_replicas, max_replicas):
    """
    Normalize replica count as cost proxy.

    Returns:
      0.0 = at minimum replicas
      1.0 = at maximum replicas
    """
    return (n_replicas - min_replicas) / (max_replicas - min_replicas)
```

---

## Decision Algorithm

### Pseudocode

```python
def make_decision(current_state, predictions, config):
    """
    Main decision algorithm.

    Input:
        current_state: {replicas, metrics, history}
        predictions: {request_rate, latency, cpu}
        config: {weights, constraints, slo}

    Output:
        decision: {replicas, score, reasoning}
    """
    # Step 1: Generate candidates
    candidates = generate_candidates(
        current_replicas=current_state['replicas'],
        min_replicas=config['constraints']['min_replicas'],
        max_replicas=config['constraints']['max_replicas'],
        max_step=config['constraints']['max_step_change']
    )

    # Step 2: Score each candidate
    scores = []
    for n_replicas in candidates:
        # Predict metrics for this replica count
        metrics = predict_metrics_for_replicas(
            n_replicas=n_replicas,
            predictions=predictions,
            model=linear_regression_model
        )

        # Calculate objective score
        score = calculate_objective_score(
            metrics=metrics,
            n_replicas=n_replicas,
            weights=config['weights'],
            slo=config['slo']
        )

        scores.append(score)

    # Step 3: Select best candidate
    best_idx = argmin(scores)
    optimal_replicas = candidates[best_idx]

    # Step 4: Apply safety constraints
    if not is_safe_transition(
        from_replicas=current_state['replicas'],
        to_replicas=optimal_replicas,
        history=current_state['history'],
        config=config['constraints']
    ):
        # Revert to safe option (usually current state)
        optimal_replicas = current_state['replicas']
        reasoning = "Safety override: cooldown/oscillation detected"
    else:
        reasoning = f"Optimal score: {scores[best_idx]:.3f}"

    return {
        'replicas': optimal_replicas,
        'score': scores[best_idx],
        'candidates': candidates,
        'all_scores': scores,
        'reasoning': reasoning
    }
```

---

## Safety Mechanisms

### 1. Cooldown Period

**Purpose**: Prevent rapid successive scaling actions  
**Implementation**: Track timestamp of last scaling action, enforce minimum wait time

```python
def check_cooldown(last_action_time, current_time, cooldown_seconds):
    elapsed = current_time - last_action_time
    return elapsed >= cooldown_seconds
```

**Default**: 60 seconds

---

### 2. Oscillation Detection

**Purpose**: Prevent up-down-up-down scaling patterns  
**Implementation**: Track last N decisions, detect alternating pattern

```python
def detect_oscillation(decision_history, window_size=5):
    """
    Detect if recent decisions alternate (e.g., 5 -> 6 -> 5 -> 6).
    """
    if len(decision_history) < window_size:
        return False

    recent = decision_history[-window_size:]

    # Check for alternating up/down pattern
    changes = [recent[i+1] - recent[i] for i in range(len(recent)-1)]

    # If all changes alternate sign, it's oscillating
    alternating = all(
        changes[i] * changes[i+1] < 0
        for i in range(len(changes)-1)
    )

    return alternating
```

**Action**: If detected, freeze scaling for extended cooldown period

---

### 3. Step Size Limit

**Purpose**: Prevent dramatic scaling changes  
**Implementation**: Limit replica change to ±N per decision

```python
def enforce_step_limit(current, target, max_step):
    if target > current:
        return min(target, current + max_step)
    else:
        return max(target, current - max_step)
```

**Default**: ±2 replicas per decision

---

### 4. Min/Max Bounds

**Purpose**: Operational constraints  
**Implementation**: Hard limits on replica count

```python
def enforce_bounds(replicas, min_replicas, max_replicas):
    return max(min_replicas, min(replicas, max_replicas))
```

**Defaults**: min=2, max=20

---

### 5. Rollback on SLO Violation

**Purpose**: Undo scaling decisions that harm performance  
**Implementation**: Monitor latency post-scaling, revert if degraded

```python
def check_rollback(
    previous_latency,
    current_latency,
    slo_max,
    tolerance=1.2
):
    """
    Check if we should rollback recent scaling decision.
    """
    # If latency increased significantly and now violates SLO
    if (current_latency > slo_max and
        current_latency > previous_latency * tolerance):
        return True
    return False
```

**Action**: Revert to previous replica count, blacklist decision for cooldown period

---

## Prediction Integration

### Using Linear Regression Model

The decision engine relies on predictions from the Linear Regression model trained in Stage 2:

```python
class MetricPredictor:
    def __init__(self, model_path):
        """Load trained Linear Regression model."""
        self.model = joblib.load(model_path)
        self.scaler_X = joblib.load(model_path.replace('.pkl', '_scaler_X.pkl'))
        self.scaler_y = joblib.load(model_path.replace('.pkl', '_scaler_y.pkl'))

    def predict_for_replicas(self, current_features, n_replicas):
        """
        Predict metrics given a hypothetical replica count.

        Process:
        1. Take current feature vector
        2. Update replica-related features
        3. Scale features
        4. Predict with LR model
        5. Inverse scale predictions
        """
        # Clone features
        features = current_features.copy()

        # Update replica-dependent features
        features['replica_count'] = n_replicas
        features['cpu_per_replica'] = features['total_cpu'] / n_replicas
        features['memory_per_replica'] = features['total_memory'] / n_replicas
        features['requests_per_replica'] = features['request_rate'] / n_replicas

        # Scale
        features_scaled = self.scaler_X.transform([features])

        # Predict
        predictions_scaled = self.model.predict(features_scaled)

        # Inverse scale
        predictions = self.scaler_y.inverse_transform(predictions_scaled)[0]

        return {
            'request_rate': predictions[0],
            'latency_p95': predictions[1]
        }
```

---

## Simulation Framework

### Historical Replay Process

```python
class AutoscalingSimulator:
    def __init__(self, historical_data, decision_engine, config):
        self.data = historical_data
        self.engine = decision_engine
        self.config = config
        self.state = {
            'replicas': config['constraints']['min_replicas'],
            'history': [],
            'last_action_time': 0
        }

    def run_simulation(self):
        """
        Replay historical data, applying decisions in sequence.
        """
        results = []

        for timestep, row in self.data.iterrows():
            # Get predictions (from actual next-step metrics)
            predictions = {
                'request_rate': row['request_rate'],
                'latency_p95': row['latency_p95'],
                'cpu': row['cpu_usage']
            }

            # Make decision
            decision = self.engine.make_decision(
                current_state=self.state,
                predictions=predictions,
                config=self.config
            )

            # Apply decision (in simulation)
            self.state['replicas'] = decision['replicas']
            self.state['history'].append(decision['replicas'])

            # Record results
            results.append({
                'timestamp': row['timestamp'],
                'actual_replicas': decision['replicas'],
                'actual_latency': row['latency_p95'],
                'decision_score': decision['score'],
                'reasoning': decision['reasoning']
            })

        return pd.DataFrame(results)
```

---

## Evaluation Metrics

### Primary KPIs

1. **Cost Reduction**

   ```python
   cost_reduction = 1 - (mean_replicas_autotunex / mean_replicas_baseline)
   ```

   Target: 20-40% reduction vs Kubernetes HPA

2. **SLO Compliance**

   ```python
   slo_compliance = (count(latency <= slo_max) / total_samples) * 100
   ```

   Target: >99%

3. **Scaling Stability**
   ```python
   stability = 1 - (num_scaling_actions / total_timesteps)
   ```
   Target: Reduce scaling frequency by 30-50%

### Secondary KPIs

4. **Resource Efficiency**

   ```python
   efficiency = mean(cpu_utilization)
   ```

   Target: 60-80%

5. **Latency Improvement**

   ```python
   latency_improvement = 1 - (mean_latency_autotunex / mean_latency_baseline)
   ```

   Target: 10-20% improvement

6. **Cost-Performance Trade-off**
   ```python
   pareto_efficiency = cost_reduction / (1 - slo_violations_ratio)
   ```
   Higher is better

---

## Visualization Plan

### 1. Time Series Plots

- Replica count over time (AutoTuneX vs HPA vs Static)
- Latency over time with SLO line
- Cost accumulation over time

### 2. Scatter Plots

- Cost vs Latency (Pareto frontier)
- CPU utilization distribution
- Scaling action frequency

### 3. Heatmaps

- Weight sensitivity analysis
- Decision matrix (current_replicas × predicted_load → decision)

### 4. Box Plots

- Latency distribution by method
- Replica count distribution by method

---

## Testing Strategy

### Unit Tests

- [OK] Objective function returns [0, 1]
- [OK] Normalization functions handle edge cases
- [OK] Safety constraints properly enforced
- [OK] Decision logic selects minimum score

### Integration Tests

- [OK] End-to-end decision flow
- [OK] Simulator produces valid results
- [OK] Model predictions integrate correctly

### Validation Tests

- [OK] Test on held-out validation set
- [OK] Cross-validate weight configurations
- [OK] Stress test with extreme scenarios

---

## Deliverables

1. **Code**
   - `objective_function.py` - Scoring logic
   - `decision_engine.py` - Core algorithm
   - `simulator.py` - Historical replay
   - `safety_constraints.py` - Safety mechanisms

2. **Notebooks**
   - `1_objective_function.ipynb` - Design and testing
   - `2_decision_algorithm.ipynb` - Implementation
   - `3_simulator.ipynb` - Simulation results
   - `4_evaluation.ipynb` - Baseline comparison
   - `5_weight_tuning.ipynb` - Optimization

3. **Results**
   - `simulation_results.json` - Raw data
   - `evaluation_report.md` - Analysis
   - Comparison plots (PNG/PDF)

4. **Documentation**
   - This design document
   - API documentation
   - User guide for weight configuration

---

## Implementation Timeline

**Week 1**: Core implementation (Day 1-5)  
**Week 2**: Simulation and evaluation (Day 6-12)  
**Week 3**: Refinement and documentation (Day 13-14)

**Total**: 2-3 weeks to production-ready system

---

**Document Status**: Design complete, ready for implementation  
**Next Step**: Begin `1_objective_function.ipynb`  
**Last Updated**: February 27, 2026
