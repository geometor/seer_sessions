```python
"""
Extracts non-zero values from the 3x3 input grid and constructs a new grid where each non-zero value is repeated according to its count in the input.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms a 3x3 input grid into a new grid containing only the non-zero values,
    repeated as many times as they appear in the input.
    """
    # Count occurrences of each non-zero value
    unique_values, counts = np.unique(input_grid, return_counts=True)
    non_zero_indices = np.where(unique_values != 0)
    non_zero_values = unique_values[non_zero_indices]
    non_zero_counts = counts[non_zero_indices]

    # Construct the output grid
    output_list = []
    for value, count in zip(non_zero_values, non_zero_counts):
        output_list.extend([value] * count)

    output_grid = np.array(output_list)

    return output_grid
```