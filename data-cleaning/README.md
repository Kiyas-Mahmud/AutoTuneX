# Data Cleaning Pipeline

## Overview

This folder contains the data cleaning and validation pipeline for AutoTuneX research project.

## Files

### 1. data_cleaning.ipynb

Main data cleaning notebook with:

- Missing data removal
- Timestamp sorting
- Fixed interval verification
- Logical consistency validation
- Range checks
- Traffic coverage analysis
- Spike preservation
- Correlation analysis
- Visualization generation

### 2. cleaning_metadata.json

Automatically generated metadata containing:

- Original/final row counts
- Retention statistics
- Removed data categories
- Date range information
- Traffic distribution
- Validation results

## Execution

```bash
jupyter notebook data_cleaning.ipynb
```

Or run all cells programmatically:

```bash
jupyter nbconvert --to notebook --execute data_cleaning.ipynb
```

## Key Principles

1. **Preserve Real Workload**: Keep traffic spikes and outliers
2. **Remove Corruption Only**: Not poor performance cases
3. **Logical Validation**: Enforce p50 ≤ p95 ≤ p99
4. **Range Enforcement**: CPU, memory, error_rate within valid bounds
5. **Traffic Diversity**: Maintain low/medium/burst coverage
6. **No Over-Cleaning**: Real systems are noisy

## Output

- **data/cleaned_dataset.csv**: Clean dataset ready for modeling
- **results/img/data_cleaning_overview.png**: Visual quality check
- **results/img/correlation_matrix.png**: Feature correlations

## Validation Checklist

All items verified in notebook execution:

- Fixed time intervals
- Corrupted rows removed
- Real spikes preserved
- Logical consistency
- Sufficient replica changes
- Valid ranges
- Traffic diversity
- Documentation complete
- Versioning maintained
