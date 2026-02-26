# AutoTuneX Research Tasks

## Overview

This document contains all tasks for the AutoTuneX research project, organized by stages. Each task should be completed in order to ensure proper foundation for subsequent work.

---

## STAGE 1: Data Finalization (Foundation)

### Task 1.1: Clean & Validate Dataset

- [x] Remove missing rows from dataset
- [x] Sort data by timestamp
- [x] Ensure fixed interval sampling
- [x] Remove anomalies (if needed)
- [x] Check scaling event frequency
- [x] Verify data quality and document findings

**Output:** Clean dataset ready for modeling  
**Report:** [docs/tasks/task_1_1_report.md](docs/tasks/task_1_1_report.md)  
**Notebook:** [data-cleaning/data_cleaning.ipynb](data-cleaning/data_cleaning.ipynb)

### Task 1.2: Feature Engineering

- [x] Calculate `cpu_per_replica` feature
- [x] Calculate `memory_per_replica` feature
- [x] Calculate `latency_diff = p95 − p50`
- [x] Calculate `traffic_change_rate`
- [x] Add lag features (1–5 steps)
- [x] Add rolling mean (3–5 steps)
- [x] Add rolling std (3–5 steps)
- [x] Validate all new features
- [x] Document feature definitions

**Output:** Time-aware dataset with engineered features  
**Report:** [docs/tasks/task_1_2_report.md](docs/tasks/task_1_2_report.md)  
**Notebook:** [data-cleaning/feature_engineering.ipynb](data-cleaning/feature_engineering.ipynb)

### Task 1.3: Define Prediction Target

- [x] Define primary target: predict next-step `request_rate` and `latency_p95`
- [x] Define secondary target: predict required `replica_count` (derived)
- [x] Implement target variable calculation
- [x] Validate target variables
- [x] Document prediction logic

**Output:** Clear prediction targets defined and implemented  
**Report:** [docs/tasks/task_1_3_report.md](docs/tasks/task_1_3_report.md)  
**Notebook:** [data-cleaning/define_prediction_target.ipynb](data-cleaning/define_prediction_target.ipynb)

---

## STAGE 2: Baseline Modeling (Required for Paper)

### Task 2.1: Prepare Data Splits

- [x] Implement time-series split (not random shuffle)
- [x] Create 70% training set
- [x] Create 15% validation set
- [x] Create 15% test set
- [x] Verify split integrity
- [x] Document split methodology

### Task 2.2: Implement Linear Regression Baseline

- [x] Implement Linear Regression model
- [x] Train on training set
- [x] Validate on validation set
- [x] Test on test set
- [x] Calculate MAE, RMSE, R²
- [x] Calculate spike prediction accuracy
- [x] Save model and results

### Task 2.3: Implement Random Forest Baseline

- [x] Implement Random Forest model
- [x] Tune hyperparameters on validation set
- [x] Train on training set
- [x] Test on test set
- [x] Calculate MAE, RMSE, R²
- [x] Calculate spike prediction accuracy
- [x] Save model and results

### Task 2.4: Implement XGBoost/LightGBM Baseline

- [x] Implement XGBoost or LightGBM model
- [x] Tune hyperparameters on validation set
- [x] Train on training set
- [x] Test on test set
- [x] Calculate MAE, RMSE, R²
- [x] Calculate spike prediction accuracy
- [x] Save model and results

### Task 2.5: Create Baseline Performance Table

- [x] Compile all baseline results
- [x] Create performance comparison table
- [x] Generate visualizations
- [x] Document findings and insights

**Output:** Baseline performance table with all models compared  
**Report:** [docs/tasks/stage_2_baseline_modeling_analysis.md](docs/tasks/stage_2_baseline_modeling_analysis.md)  
**Notebook:** [model/basline/baseline_modeling.ipynb](model/basline/baseline_modeling.ipynb)

---

## STAGE 3: Transformer Modeling (Main Contribution)

### Task 3.1: Prepare Sliding Window Data

- [x] Define input window size (e.g., last 10 timestamps)
- [x] Define prediction horizon (next timestamp)
- [x] Implement sliding window data generator
- [x] Create batches with shape: (batch_size, sequence_length, features)
- [x] Example: (32, 10, 12 features)
- [x] Validate data preparation pipeline
- [x] Document data structure

**Output:** Sliding window sequences created (window_size=10)  
**Notebook:** [model/transformer/transformer_modeling.ipynb](model/transformer/transformer_modeling.ipynb)

### Task 3.2: Build Time-Series Transformer Architecture

- [x] Implement input embedding layer
- [x] Implement positional encoding
- [x] Implement 2–3 encoder layers
- [x] Implement multi-head attention (4–8 heads)
- [x] Implement feed-forward network
- [x] Implement output dense layer
- [x] Configure MSE loss function
- [x] Configure Adam optimizer
- [x] Implement early stopping
- [x] Document architecture details

**Output:** Complete Transformer architecture with 4 attention heads, 2 encoder blocks  
**Notebook:** [model/transformer/transformer_modeling.ipynb](model/transformer/transformer_modeling.ipynb)

### Task 3.3: Train Transformer Model

- [x] Train transformer on training set
- [x] Monitor validation loss
- [x] Apply early stopping
- [x] Save best model checkpoints
- [x] Log training metrics
- [x] Document training process

**Output:** Trained Transformer model with early stopping and learning rate scheduling  
**Notebook:** [model/transformer/transformer_modeling.ipynb](model/transformer/transformer_modeling.ipynb)

### Task 3.4: Evaluate and Compare Transformer

- [x] Evaluate transformer on test set
- [x] Compare transformer vs XGBoost vs Random Forest
- [x] Analyze: Does transformer achieve lower MAE?
- [x] Analyze: Does transformer capture spikes better?
- [x] Analyze: Does transformer predict latency better?
- [x] Create comparison visualizations
- [x] Document findings for main result section

**Output:** Comprehensive comparison analysis with visualizations  
**Notebook:** [model/transformer/transformer_modeling.ipynb](model/transformer/transformer_modeling.ipynb)

---

## STAGE 4: Multi-Objective Decision Engine

### Task 4.1: Define Decision Framework

- [ ] Define normalized score function
- [ ] Set weights: w1 (predicted_latency), w2 (predicted_cpu), w3 (replica_cost_penalty)
- [ ] Document multi-objective optimization approach

### Task 4.2: Implement Candidate Evaluation

- [ ] Implement candidate replica testing: current −1, current, current +1, current +2
- [ ] Calculate score for each candidate
- [ ] Select candidate with lowest score
- [ ] Document decision logic

### Task 4.3: Test Decision Engine

- [ ] Test on validation data
- [ ] Verify decision quality
- [ ] Tune weights if needed
- [ ] Document decision outcomes

**Output:** Intelligent autoscaling decision engine

---

## STAGE 5: Safety Mechanisms

### Task 5.1: Implement Basic Safety Constraints

- [ ] Implement minimum replica constraint
- [ ] Implement maximum replica constraint
- [ ] Implement max step change (±2)
- [ ] Validate constraints work correctly

### Task 5.2: Implement Time-Based Safety

- [ ] Implement cooldown period mechanism
- [ ] Test cooldown behavior
- [ ] Document cooldown parameters

### Task 5.3: Implement Stability Mechanisms

- [ ] Implement oscillation detection
- [ ] Implement rollback if latency increases
- [ ] Test stability mechanisms
- [ ] Document safety features

**Output:** Safety-aware deployment system

---

## STAGE 6: Simulation Evaluation

### Task 6.1: Build Simulation Framework

- [ ] Implement dataset replay mechanism
- [ ] For each timestep: predict next metrics
- [ ] For each timestep: decide replicas
- [ ] For each timestep: apply scaling rule (simulated)
- [ ] Validate simulation logic

### Task 6.2: Collect Simulation Metrics

- [ ] Measure latency improvement
- [ ] Measure cost reduction
- [ ] Measure stability (scaling frequency)
- [ ] Calculate SLA violation rate
- [ ] Document simulation results

### Task 6.3: Compare Against Baselines

- [ ] Implement CPU threshold rule baseline
- [ ] Implement Kubernetes HPA logic (simulated)
- [ ] Compare AutoTuneX against baselines
- [ ] Create comparison visualizations
- [ ] Document comparative advantages

**Output:** Comprehensive simulation evaluation with comparative analysis

---

## STAGE 7: External Validation

### Task 7.1: Obtain Alibaba Dataset

- [ ] Download Alibaba dataset
- [ ] Clean and preprocess Alibaba data
- [ ] Document dataset characteristics

### Task 7.2: Cross-Dataset Validation

- [ ] Train forecasting model on your data
- [ ] Test forecasting generalization on Alibaba CPU traces
- [ ] Compare MAE on external dataset
- [ ] Analyze generalization capability
- [ ] Document external validation results

**Output:** External validation demonstrating model generalization

---

## STAGE 8: Real Prototype Integration (Optional Advanced)

### Task 8.1: Kubernetes Integration

- [ ] Connect model to Kubernetes API
- [ ] Implement scaling action execution
- [ ] Test connection and permissions
- [ ] Document integration approach

### Task 8.2: Live Testing

- [ ] Set up Locust workload
- [ ] Run live scaling with AutoTuneX
- [ ] Measure real performance metrics
- [ ] Compare with simulation results
- [ ] Document real-world deployment findings

**Output:** Real prototype with live Kubernetes integration

---

## STAGE 9: Evaluation Metrics

### Task 9.1: Compile Prediction Metrics

- [ ] Calculate and report MAE
- [ ] Calculate and report RMSE
- [ ] Calculate and report R²
- [ ] Create prediction metrics summary

### Task 9.2: Compile Scaling Metrics

- [ ] Calculate average latency
- [ ] Calculate P95 latency
- [ ] Calculate resource utilization
- [ ] Calculate cost proxy
- [ ] Count number of scaling events
- [ ] Calculate SLA violation rate
- [ ] Create scaling metrics summary

### Task 9.3: Compile Stability Metrics

- [ ] Calculate oscillation rate
- [ ] Calculate recovery time
- [ ] Create stability metrics summary

### Task 9.4: Create Complete Metrics Report

- [ ] Combine all metrics into comprehensive report
- [ ] Create visualizations for all key metrics
- [ ] Prepare tables for paper
- [ ] Document methodology for each metric

**Output:** Complete evaluation metrics report

---

## STAGE 10: Paper Writing

### Task 10.1: Introduction Section

- [ ] Write problem statement
- [ ] Write motivation
- [ ] Write research objectives
- [ ] Write contribution summary
- [ ] Review and refine introduction

### Task 10.2: Literature Review Section

- [ ] Review autoscaling approaches
- [ ] Review time-series forecasting methods
- [ ] Review transformer applications
- [ ] Review multi-objective optimization
- [ ] Identify research gaps
- [ ] Write literature review
- [ ] Create comparison table with related work

### Task 10.3: System Architecture Section

- [ ] Describe AutoTuneX architecture
- [ ] Create architecture diagram
- [ ] Explain component interactions
- [ ] Document design decisions
- [ ] Write architecture section

### Task 10.4: Dataset & Feature Engineering Section

- [ ] Describe dataset characteristics
- [ ] Document data collection
- [ ] Explain feature engineering process
- [ ] Create feature table
- [ ] Write dataset section

### Task 10.5: Modeling Approach Section

- [ ] Describe transformer architecture
- [ ] Explain model design choices
- [ ] Document hyperparameters
- [ ] Write modeling section

### Task 10.6: Multi-Objective Decision Framework Section

- [ ] Explain decision framework
- [ ] Describe objective functions
- [ ] Document weight tuning process
- [ ] Write decision framework section

### Task 10.7: Safety Mechanism Design Section

- [ ] Describe safety constraints
- [ ] Explain oscillation detection
- [ ] Document rollback mechanism
- [ ] Write safety mechanism section

### Task 10.8: Experimental Setup Section

- [ ] Describe experimental environment
- [ ] Document baseline implementations
- [ ] Explain evaluation methodology
- [ ] Write experimental setup section

### Task 10.9: Results & Comparison Section

- [ ] Present prediction results
- [ ] Present scaling results
- [ ] Present comparison with baselines
- [ ] Present external validation results
- [ ] Create all result figures and tables
- [ ] Write results section with analysis

### Task 10.10: Conclusion & Future Work Section

- [ ] Summarize contributions
- [ ] Summarize key findings
- [ ] Discuss limitations
- [ ] Propose future research directions
- [ ] Write conclusion section

### Task 10.11: Abstract and Keywords

- [ ] Write abstract
- [ ] Select keywords
- [ ] Review abstract for clarity

### Task 10.12: Final Paper Review

- [ ] Review entire paper for consistency
- [ ] Check all references
- [ ] Verify all figures and tables
- [ ] Proofread for grammar and style
- [ ] Format according to target venue
- [ ] Submit for feedback

**Output:** Complete research paper

---

## Timeline

### Week 1: Data + Baselines

- Complete Stage 1 (Data Finalization)
- Complete Stage 2 (Baseline Modeling)

### Week 2: Transformer

- Complete Stage 3 (Transformer Modeling)
- Begin Stage 4 (Decision Engine)

### Week 3: Decision Engine + Simulation

- Complete Stage 4 (Decision Engine)
- Complete Stage 5 (Safety Mechanisms)
- Complete Stage 6 (Simulation Evaluation)

### Week 4: Evaluation + Writing

- Complete Stage 7 (External Validation)
- Complete Stage 9 (Evaluation Metrics)
- Begin Stage 10 (Paper Writing)

---

## Final Architecture Summary

**AutoTuneX Pipeline:**

```
Monitor → Feature Engineering → Predict (Transformer) → Score → Safe Decide → Evaluate → Feedback
```

---

## Important Reminders

### DO NOT:

- Jump to Reinforcement Learning
- Add Graph Neural Networks
- Overcomplicate the approach

### DO:

- Build clean foundation first
- Complete each stage before moving to next
- Document everything thoroughly
- Focus on: Clean → Baseline → Transformer → Decision → Safety

**This focused approach is publishable and achievable.**

---

## Progress Tracking

**Current Stage:** Stage 1 - Data Finalization (Foundation) ✓ COMPLETE

**Completed Stages:**

- Stage 1: Data Finalization ✓

**Completed Tasks:**

- Task 1.1: Clean & Validate Dataset ✓
- Task 1.2: Feature Engineering ✓
- Task 1.3: Define Prediction Target ✓

**In Progress:**

- Stage 2: Baseline Modeling (Next)

**Blockers:** None

**Next Milestone:** Stage 2 - Task 2.1 (Prepare Data Splits)
