STAGE 1 — Data Finalization (Foundation)
Step 1: Clean & Validate Dataset

Remove missing rows

Sort by timestamp

Ensure fixed interval sampling

Remove anomalies (if needed)

Check scaling event frequency

Output:
Clean dataset ready for modeling

Step 2: Feature Engineering

Add:

cpu_per_replica

memory_per_replica

latency_diff = p95 − p50

traffic_change_rate

Lag features (1–5 steps)

Rolling mean (3–5 steps)

Rolling std (3–5 steps)

Now dataset becomes time-aware.

Step 3: Define Prediction Target

Choose:

Primary Target:
👉 Predict next-step request_rate and latency_p95

Secondary:
👉 Predict required replica_count (derived)

This keeps logic clean.

🟢 STAGE 2 — Baseline Modeling (Required for Paper)

You MUST implement:

Linear Regression

Random Forest

XGBoost / LightGBM

Train with:

70% train

15% validation

15% test
(Time-series split, not random shuffle)

Evaluation Metrics:

MAE

RMSE

R²

Spike prediction accuracy

Output:
Baseline performance table

🟢 STAGE 3 — Transformer Modeling (Main Contribution)
Step 1: Prepare Sliding Window Data

Example:

Input window: last 10 timestamps
Predict: next timestamp

Input shape:
(batch_size, sequence_length, features)

Example:
(32, 10, 12 features)

Step 2: Build Time-Series Transformer

Architecture:

Input embedding layer

Positional encoding

2–3 encoder layers

Multi-head attention (4–8 heads)

Feed-forward network

Output dense layer

Loss:

MSE loss

Optimizer:

Adam

Early stopping enabled.

Step 3: Train & Compare

Compare:

Transformer vs XGBoost vs RF

Show:

Lower MAE?

Better spike capture?

Better latency prediction?

This becomes your main result section.

🟢 STAGE 4 — Multi-Objective Decision Engine

Now prediction → decision.

Define normalized score:

Score =
w1 * predicted_latency

w2 * predicted_cpu

w3 * replica_cost_penalty

Test candidate replicas:

current −1

current

current +1

current +2

Choose lowest score.

This becomes intelligent autoscaling brain.

🟢 STAGE 5 — Safety Mechanisms

Add:

Min replicas

Max replicas

Max step change = ±2

Cooldown period

Oscillation detection

Rollback if latency increases

This is your safety-aware deployment pillar.

🟢 STAGE 6 — Simulation Evaluation

Replay dataset:

For each timestep:

Predict next metrics

Decide replicas

Apply scaling rule (simulated)

Measure:

Latency improvement

Cost reduction

Stability (scaling frequency)

Compare against:

CPU threshold rule

Kubernetes HPA logic (simulated)

🟢 STAGE 7 — External Validation

Use Alibaba dataset:

Train forecasting model on your data

Test forecasting generalization on Alibaba CPU traces

Compare MAE

This increases academic strength.

🟢 STAGE 8 — Real Prototype Integration (Optional Advanced Stage)

If time permits:

Connect model to Kubernetes API

Apply scaling live

Run Locust workload

Measure real performance

This makes your work extremely strong.

🟢 STAGE 9 — Evaluation Metrics

You must report:

Prediction:

MAE

RMSE

R²

Scaling:

Average latency

P95 latency

Resource utilization

Cost proxy

Number of scaling events

SLA violation rate

Stability:

Oscillation rate

Recovery time

🟢 STAGE 10 — Paper Writing Structure

Introduction

Literature Review

System Architecture

Dataset & Feature Engineering

Modeling Approach

Multi-Objective Decision Framework

Safety Mechanism Design

Experimental Setup

Results & Comparison

Conclusion & Future Work

⏳ Suggested Timeline

Week 1:
Data + Baselines

Week 2:
Transformer

Week 3:
Decision engine + simulation

Week 4:
Evaluation + writing

🔥 Final Architecture Summary

AutoTuneX =

Monitor → Feature → Predict (Transformer) → Score → Safe Decide → Evaluate → Feedback

Important Advice

Do NOT:

Jump to RL

Add GNN

Overcomplicate

First build:
Clean → Baseline → Transformer → Decision → Safety

That alone is publishable.