import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import json
import warnings
warnings.filterwarnings('ignore')

print("Loading featured dataset...")
df = pd.read_csv('../data/featured_dataset.csv')
df['timestamp'] = pd.to_datetime(df['timestamp'])
print(f"Loaded: {df.shape}")
input_rows = len(df)

print("\n1. Creating primary targets (next-step prediction)...")
df['target_request_rate'] = df['request_rate'].shift(-1)
df['target_latency_p95'] = df['latency_p95'].shift(-1)
print("   target_request_rate: next-step request_rate")
print("   target_latency_p95: next-step latency_p95")

print("\n2. Creating secondary target...")
df['target_replica_count'] = df['replica_count'].shift(-1)
print("   target_replica_count: next-step replica_count")

print("\n3. Removing rows with NaN targets...")
print(f"   Before: {len(df)} rows")
df_target = df.dropna()
print(f"   After: {len(df_target)} rows")
print(f"   Dropped: {len(df) - len(df_target)} (last row without next-step)")

print("\n4. Validating targets...")
null_count = df_target[['target_request_rate', 'target_latency_p95', 'target_replica_count']].isnull().sum().sum()
print(f"   Null values in targets: {null_count}")
print(f"   All targets valid: {null_count == 0}")

print("\n5. Target statistics:")
print(df_target[['target_request_rate', 'target_latency_p95', 'target_replica_count']].describe())

print("\n6. Identifying feature and target columns...")
feature_cols = [col for col in df_target.columns if col not in ['target_request_rate', 'target_latency_p95', 'target_replica_count']]
target_cols = ['target_request_rate', 'target_latency_p95', 'target_replica_count']
print(f"   Feature columns: {len(feature_cols)}")
print(f"   Target columns: {len(target_cols)}")

print("\n7. Creating visualizations...")
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

axes[0,0].scatter(df_target['request_rate'], df_target['target_request_rate'], alpha=0.3)
axes[0,0].plot([df_target['request_rate'].min(), df_target['request_rate'].max()], 
               [df_target['request_rate'].min(), df_target['request_rate'].max()], 'r--')
axes[0,0].set_xlabel('Current Request Rate')
axes[0,0].set_ylabel('Target Request Rate')
axes[0,0].set_title('Request Rate: Current vs Next-Step')

axes[0,1].scatter(df_target['latency_p95'], df_target['target_latency_p95'], alpha=0.3, color='orange')
axes[0,1].plot([df_target['latency_p95'].min(), df_target['latency_p95'].max()], 
               [df_target['latency_p95'].min(), df_target['latency_p95'].max()], 'r--')
axes[0,1].set_xlabel('Current Latency P95')
axes[0,1].set_ylabel('Target Latency P95')
axes[0,1].set_title('Latency P95: Current vs Next-Step')

axes[1,0].scatter(df_target['replica_count'], df_target['target_replica_count'], alpha=0.3, color='green')
axes[1,0].plot([df_target['replica_count'].min(), df_target['replica_count'].max()], 
               [df_target['replica_count'].min(), df_target['replica_count'].max()], 'r--')
axes[1,0].set_xlabel('Current Replica Count')
axes[1,0].set_ylabel('Target Replica Count')
axes[1,0].set_title('Replica Count: Current vs Next-Step')

df_target[['request_rate', 'target_request_rate']].iloc[:100].plot(ax=axes[1,1])
axes[1,1].set_title('Request Rate Time Series (First 100 samples)')
axes[1,1].legend(['Current', 'Target (Next-Step)'])

plt.tight_layout()
plt.savefig('../results/img/prediction_targets.png', dpi=150, bbox_inches='tight')
print("   Saved: prediction_targets.png")

print("\n8. Saving prediction-ready dataset...")
df_target.to_csv('../data/prediction_ready_dataset.csv', index=False)
print(f"   Saved: prediction_ready_dataset.csv ({len(df_target)} rows, {df_target.shape[1]} columns)")

print("\n9. Saving metadata...")
target_metadata = {
    'input_rows': int(input_rows),
    'output_rows': int(len(df_target)),
    'rows_dropped': int(len(df) - len(df_target)),
    'total_columns': int(df_target.shape[1]),
    'feature_columns': len(feature_cols),
    'target_columns': len(target_cols),
    'primary_targets': [
        'target_request_rate',
        'target_latency_p95'
    ],
    'secondary_targets': [
        'target_replica_count'
    ],
    'prediction_horizon': 'next_step',
    'target_statistics': {
        'target_request_rate': {
            'mean': float(df_target['target_request_rate'].mean()),
            'std': float(df_target['target_request_rate'].std()),
            'min': float(df_target['target_request_rate'].min()),
            'max': float(df_target['target_request_rate'].max())
        },
        'target_latency_p95': {
            'mean': float(df_target['target_latency_p95'].mean()),
            'std': float(df_target['target_latency_p95'].std()),
            'min': float(df_target['target_latency_p95'].min()),
            'max': float(df_target['target_latency_p95'].max())
        },
        'target_replica_count': {
            'mean': float(df_target['target_replica_count'].mean()),
            'std': float(df_target['target_replica_count'].std()),
            'min': float(df_target['target_replica_count'].min()),
            'max': float(df_target['target_replica_count'].max())
        }
    }
}

with open('target_metadata.json', 'w') as f:
    json.dump(target_metadata, f, indent=2)
print("   Saved: target_metadata.json")

print("\n" + "="*60)
print("PREDICTION TARGET SUMMARY")
print("="*60)
print(f"Primary targets:     {', '.join(target_metadata['primary_targets'])}")
print(f"Secondary targets:   {', '.join(target_metadata['secondary_targets'])}")
print(f"Prediction horizon:  {target_metadata['prediction_horizon']}")
print(f"Dataset rows:        {target_metadata['output_rows']}")
print(f"Feature columns:     {target_metadata['feature_columns']}")
print(f"Target columns:      {target_metadata['target_columns']}")
print(f"Total columns:       {target_metadata['total_columns']}")
print("="*60)

print("\n" + "="*60)
print("TARGET STATISTICS")
print("="*60)
for target_name in target_metadata['primary_targets'] + target_metadata['secondary_targets']:
    stats = target_metadata['target_statistics'][target_name]
    print(f"\n{target_name}:")
    print(f"  Mean: {stats['mean']:.2f}")
    print(f"  Std:  {stats['std']:.2f}")
    print(f"  Min:  {stats['min']:.2f}")
    print(f"  Max:  {stats['max']:.2f}")
print("="*60)

print("\n✓✓✓ TASK 1.3 COMPLETE ✓✓✓")
