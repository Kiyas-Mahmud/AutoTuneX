import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import json
import warnings
warnings.filterwarnings('ignore')

print("Loading cleaned dataset...")
df = pd.read_csv('../data/cleaned_dataset.csv')
df['timestamp'] = pd.to_datetime(df['timestamp'])
print(f"Loaded: {df.shape}")
original_rows = len(df)

print("\n1. Creating per-replica features...")
df['cpu_per_replica'] = df['cpu_usage'] / df['replica_count'].replace(0, 1)
df['memory_per_replica'] = df['memory_usage'] / df['replica_count'].replace(0, 1)
print("   cpu_per_replica, memory_per_replica")

print("\n2. Creating latency difference...")
df['latency_diff'] = df['latency_p95'] - df['latency_p50']
print("   latency_diff (p95 - p50)")

print("\n3. Creating traffic change rate...")
time_diff = df['timestamp'].diff().dt.total_seconds()
request_diff = df['request_rate'].diff()
df['traffic_change_rate'] = request_diff / time_diff.replace(0, 1)
print("   traffic_change_rate")

print("\n4. Creating lag features (1-5 steps)...")
for i in range(1, 6):
    df[f'request_rate_lag_{i}'] = df['request_rate'].shift(i)
    df[f'latency_p95_lag_{i}'] = df['latency_p95'].shift(i)
    df[f'cpu_usage_lag_{i}'] = df['cpu_usage'].shift(i)
print(f"   Created 15 lag features")

print("\n5. Creating rolling mean features (windows: 3, 5)...")
for window in [3, 5]:
    df[f'request_rate_rolling_mean_{window}'] = df['request_rate'].rolling(window=window).mean()
    df[f'latency_p95_rolling_mean_{window}'] = df['latency_p95'].rolling(window=window).mean()
    df[f'cpu_usage_rolling_mean_{window}'] = df['cpu_usage'].rolling(window=window).mean()
print(f"   Created 6 rolling mean features")

print("\n6. Creating rolling std features (windows: 3, 5)...")
for window in [3, 5]:
    df[f'request_rate_rolling_std_{window}'] = df['request_rate'].rolling(window=window).std()
    df[f'latency_p95_rolling_std_{window}'] = df['latency_p95'].rolling(window=window).std()
    df[f'cpu_usage_rolling_std_{window}'] = df['cpu_usage'].rolling(window=window).std()
print(f"   Created 6 rolling std features")

print("\n7. Removing rows with NaN (from lag/rolling windows)...")
print(f"   Before: {len(df)} rows")
df_featured = df.dropna()
print(f"   After: {len(df_featured)} rows")
print(f"   Dropped: {len(df) - len(df_featured)} rows")

print("\n8. Validating features...")
null_count = df_featured.isnull().sum().sum()
inf_count = np.isinf(df_featured.select_dtypes(include=[np.number])).sum().sum()
print(f"   Null values: {null_count}")
print(f"   Infinite values: {inf_count}")
print(f"   Total features: {df_featured.shape[1]}")

print("\n9. Creating visualizations...")
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

df_featured.plot(x='timestamp', y='cpu_per_replica', ax=axes[0,0], title='CPU per Replica', legend=False)
df_featured.plot(x='timestamp', y='memory_per_replica', ax=axes[0,1], title='Memory per Replica', legend=False, color='orange')
df_featured.plot(x='timestamp', y='latency_diff', ax=axes[1,0], title='Latency Diff (P95-P50)', legend=False, color='green')
df_featured.plot(x='timestamp', y='traffic_change_rate', ax=axes[1,1], title='Traffic Change Rate', legend=False, color='red')

plt.tight_layout()
plt.savefig('../results/img/feature_engineering_overview.png', dpi=150, bbox_inches='tight')
print("   Saved: feature_engineering_overview.png")

print("\n10. Saving featured dataset...")
df_featured.to_csv('../data/featured_dataset.csv', index=False)
print(f"   Saved: featured_dataset.csv ({len(df_featured)} rows, {df_featured.shape[1]} features)")

print("\n11. Saving metadata...")
feature_metadata = {
    'original_rows': int(original_rows),
    'featured_rows': int(len(df_featured)),
    'original_features': 9,
    'total_features': int(df_featured.shape[1]),
    'new_features': int(df_featured.shape[1] - 9),
    'feature_categories': {
        'per_replica': 2,
        'derived': 2,
        'lag_features': 15,
        'rolling_mean': 6,
        'rolling_std': 6
    },
    'rows_dropped': int(len(df) - len(df_featured)),
    'retention_rate': float(len(df_featured) / original_rows)
}

with open('feature_metadata.json', 'w') as f:
    json.dump(feature_metadata, f, indent=2)
print("   Saved: feature_metadata.json")

print("\n" + "="*60)
print("FEATURE ENGINEERING SUMMARY")
print("="*60)
print(f"Original features:  {feature_metadata['original_features']}")
print(f"New features:       {feature_metadata['new_features']}")
print(f"Total features:     {feature_metadata['total_features']}")
print(f"Rows retained:      {feature_metadata['featured_rows']}")
print(f"Retention rate:     {feature_metadata['retention_rate']*100:.2f}%")
print("="*60)

print("\n" + "="*60)
print("FEATURE CATEGORIES")
print("="*60)
print("Per-replica metrics:     2 (cpu_per_replica, memory_per_replica)")
print("Derived metrics:         2 (latency_diff, traffic_change_rate)")
print("Lag features:           15 (request_rate, latency_p95, cpu_usage × 5 steps)")
print("Rolling mean:            6 (3 metrics × 2 windows: 3, 5)")
print("Rolling std:             6 (3 metrics × 2 windows: 3, 5)")
print("="*60)

print("\n✓✓✓ TASK 1.2 COMPLETE ✓✓✓")
