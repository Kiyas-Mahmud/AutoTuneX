# Stage 4: Multi-Objective Decision Engine

**Status**: In Progress  
**Started**: February 27, 2026  
**Objective**: Convert Linear Regression predictions into intelligent autoscaling decisions

---

## Overview

This stage implements the **core innovation** of AutoTuneX: a multi-objective decision engine that balances:

- **Performance** (latency SLO compliance)
- **Cost** (replica count minimization)
- **Resource Efficiency** (CPU/memory utilization)

### Selected Prediction Model

Based on Stage 2-3 evaluation:

- **Production Model**: Linear Regression
- **Request Rate R²**: 0.8672 (excellent)
- **Latency P95 R²**: 0.6894 (good)
- **Inference Time**: <1ms
- **Status**: [Production-ready]

---

## Stage 4 Goals

1. **Design Multi-Objective Function**
   - Define weighted scoring: `Score = w1*latency + w2*cpu + w3*cost`
   - Normalize all metrics to [0, 1] scale
   - Find optimal weights (w1, w2, w3)

2. **Implement Decision Algorithm**
   - Evaluate candidate replica counts: [current-1, current, current+1, current+2]
   - Predict metrics for each candidate using Linear Regression
   - Select minimum-score candidate

3. **Add Safety Constraints**
   - Minimum replicas: 2
   - Maximum replicas: 20
   - Maximum step change: ±2
   - Cooldown period: 60 seconds
   - Rollback on latency degradation

4. **Build Simulator**
   - Replay historical data
   - Apply decisions in sequence
   - Measure: cost reduction, latency improvement, stability

5. **Evaluate Against Baselines**
   - Kubernetes HPA (Horizontal Pod Autoscaler)
   - Static provisioning
   - Rule-based autoscaling

---

## Folder Structure

```
decision-engine/
├── README.md                          # This file
├── decision_engine_design.md          # Architecture and design decisions
├── notebooks/
│   ├── 1_objective_function.ipynb    # Design and test objective function
│   ├── 2_decision_algorithm.ipynb    # Implement decision logic
│   ├── 3_simulator.ipynb             # Build replay simulator
│   ├── 4_evaluation.ipynb            # Compare against baselines
│   └── 5_weight_tuning.ipynb         # Optimize w1, w2, w3
├── src/
│   ├── objective_function.py         # Multi-objective scoring
│   ├── decision_engine.py            # Core decision logic
│   ├── simulator.py                  # Historical replay simulator
│   ├── safety_constraints.py         # Safety mechanisms
│   └── utils.py                      # Helper functions
├── configs/
│   ├── weights_default.json          # Default weight configuration
│   ├── weights_cost_optimized.json   # Cost-focused weights
│   └── weights_performance.json      # Performance-focused weights
└── results/
    ├── simulation_results.json        # Simulation outputs
    ├── comparison_plots/              # Visualization outputs
    └── evaluation_report.md           # Final evaluation report
```

---

## Implementation Plan

### Week 1: Design & Core Implementation

#### Day 1-2: Objective Function Design

- [ ] Define metrics: latency_normalized, cpu_normalized, cost_normalized
- [ ] Implement normalization functions (min-max scaling)
- [ ] Test different weight combinations
- [ ] Visualize trade-offs (Pareto frontier)

**Deliverable**: `1_objective_function.ipynb` with tested scoring function

---

#### Day 3-4: Decision Algorithm

- [ ] Load Linear Regression model from Stage 2
- [ ] Implement candidate evaluation logic
- [ ] Add constraint checking (min/max replicas, step size)
- [ ] Unit tests for decision logic

**Deliverable**: `2_decision_algorithm.ipynb` with working decision engine

---

#### Day 5: Safety Mechanisms

- [ ] Implement cooldown period tracking
- [ ] Add oscillation detection (check last N decisions)
- [ ] Implement rollback logic
- [ ] Test edge cases

**Deliverable**: `safety_constraints.py` with comprehensive safety checks

---

### Week 2: Simulation & Evaluation

#### Day 6-8: Simulator Development

- [ ] Build historical replay framework
- [ ] Track state: time, current_replicas, metrics
- [ ] Apply decisions sequentially
- [ ] Collect metrics: cost, latency violations, scaling actions

**Deliverable**: `3_simulator.ipynb` with complete simulation

---

#### Day 9-10: Baseline Comparison

- [ ] Implement Kubernetes HPA logic
- [ ] Implement static provisioning baseline
- [ ] Run all methods on same dataset
- [ ] Generate comparison plots

**Deliverable**: `4_evaluation.ipynb` with comparison results

---

#### Day 11-12: Weight Optimization

- [ ] Grid search over weight space
- [ ] Identify Pareto-optimal configurations
- [ ] Test on validation set
- [ ] Document trade-offs

**Deliverable**: `5_weight_tuning.ipynb` with optimal weights

---

### Week 3: Refinement & Documentation

#### Day 13-14: Results Analysis

- [ ] Generate final plots (cost vs latency scatter, time-series)
- [ ] Calculate improvement percentages
- [ ] Write evaluation report
- [ ] Document limitations

**Deliverable**: `evaluation_report.md` with publication-ready results

---

## Success Metrics

### Primary Metrics

- **Cost Reduction**: Target 20-40% vs Kubernetes HPA
- **SLO Compliance**: Maintain >99% latency target
- **Stability**: Reduce scaling frequency by 30-50%

### Secondary Metrics

- **Decision Time**: <10ms per decision
- **Resource Efficiency**: Average CPU utilization 60-80%
- **Robustness**: Handle traffic spikes without SLO violations

---

## Evaluation Scenarios

1. **Normal Traffic**: Gradual increase/decrease
2. **Traffic Spike**: Sudden 3-5x increase
3. **Traffic Drop**: Sudden 50% decrease
4. **Oscillating Load**: Periodic variations
5. **Sustained High Load**: Long-term high traffic

---

## Key Concepts

### Multi-Objective Optimization

```python
# Objective function
def calculate_score(predicted_metrics, n_replicas, weights):
    """
    Calculate multi-objective score for a candidate replica count.

    Lower score = better trade-off
    """
    # Normalize latency (0=best, 1=worst)
    latency_norm = (predicted_metrics['latency'] - latency_min) / (latency_max - latency_min)

    # Normalize CPU (target 70%, penalize over/under)
    cpu_target = 0.70
    cpu_norm = abs(predicted_metrics['cpu'] - cpu_target) / cpu_target

    # Normalize cost (0=min replicas, 1=max replicas)
    cost_norm = (n_replicas - min_replicas) / (max_replicas - min_replicas)

    # Weighted sum
    score = (
        weights['latency'] * latency_norm +
        weights['cpu'] * cpu_norm +
        weights['cost'] * cost_norm
    )

    return score
```

### Decision Logic

```python
def make_decision(current_state, predictions, weights, constraints):
    """
    Decide optimal replica count given current state and predictions.

    Returns:
        optimal_replicas: int
        decision_info: dict with scores and reasoning
    """
    current_replicas = current_state['replicas']

    # Generate candidates
    candidates = [
        max(current_replicas - 2, constraints['min_replicas']),
        max(current_replicas - 1, constraints['min_replicas']),
        current_replicas,
        min(current_replicas + 1, constraints['max_replicas']),
        min(current_replicas + 2, constraints['max_replicas'])
    ]

    # Remove duplicates
    candidates = sorted(set(candidates))

    # Score each candidate
    scores = []
    for n_replicas in candidates:
        # Predict metrics for this replica count
        predicted = predict_metrics(n_replicas, predictions)

        # Calculate score
        score = calculate_score(predicted, n_replicas, weights)
        scores.append(score)

    # Select best
    best_idx = argmin(scores)
    optimal = candidates[best_idx]

    # Apply safety constraints
    if not check_safety(current_state, optimal, constraints):
        optimal = current_replicas  # Stay safe

    return optimal, {
        'candidates': candidates,
        'scores': scores,
        'best_score': scores[best_idx]
    }
```

---

## Dependencies

### From Previous Stages

- **Stage 1**: Clean dataset (`prediction_ready_dataset.csv`)
- **Stage 2**: Trained Linear Regression model
- **Stage 3**: Analysis confirming LR as production model

### Python Packages

```
numpy>=1.24.0
pandas>=2.0.0
scikit-learn>=1.3.0
matplotlib>=3.7.0
seaborn>=0.12.0
joblib>=1.3.0
```

---

## References

### Multi-Objective Optimization

- Deb, K. (2001). Multi-Objective Optimization using Evolutionary Algorithms
- Miettinen, K. (1999). Nonlinear Multiobjective Optimization

### Autoscaling

- Kubernetes HPA: https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/
- AWS Auto Scaling: https://aws.amazon.com/autoscaling/
- Gandhi et al. (2012). "Autoscaling to Minimize Cost and Meet Application Deadlines"

### Related Work

- Rzadca et al. (2020). "Autopilot: workload autoscaling at Google" (EuroSys'20)
- Verma et al. (2015). "Large-scale cluster management at Google with Borg" (EuroSys'15)

---

## Getting Started

### Quick Start

1. **Review Linear Regression Model**

   ```bash
   cd ../basline  # Note: folder has typo
   # Check model performance: R²=0.8672 (request rate), R²=0.6894 (latency)
   ```

2. **Design Objective Function**

   ```bash
   cd notebooks
   jupyter notebook 1_objective_function.ipynb
   ```

3. **Run Simulator**
   ```bash
   python src/simulator.py --weights configs/weights_default.json
   ```

### Configuration Example

```json
{
  "weights": {
    "latency": 0.5,
    "cpu": 0.3,
    "cost": 0.2
  },
  "constraints": {
    "min_replicas": 2,
    "max_replicas": 20,
    "max_step_change": 2,
    "cooldown_seconds": 60
  },
  "slo": {
    "latency_p95_target_ms": 100,
    "latency_p95_max_ms": 150
  }
}
```

---

## Next Steps

1. [DONE] Create folder structure
2. [TODO] Design objective function (Next: Day 1)
3. [TODO] Implement decision algorithm (Day 3)
4. [TODO] Build simulator (Day 6)
5. [TODO] Run evaluation (Day 9)

---

**Document Status**: Initial setup complete  
**Ready for**: Objective function design  
**Timeline**: 2-3 weeks to completion  
**Last Updated**: February 27, 2026
