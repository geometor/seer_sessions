# 5582e5ca • 004 • example_1 • investigate_coder

---
```python
"""
1.  **Identify the most frequent color:** Examine the input grid and determine the color code (integer) that appears most frequently.
2.  **Replace all colors:** Create the output grid by replacing every cell in the input grid with the most frequent color identified in step 1.
"""

import numpy as np
from collections import Counter

def transform(input_grid):
    """Transforms the input grid by replacing all cells with the most frequent color."""

    # Convert input_grid to a numpy array for easier manipulation.
    input_array = np.array(input_grid)

    # Flatten the array to 1D for counting color frequencies.
    flattened_array = input_array.flatten()

    # Use Counter to find the most frequent color.
    color_counts = Counter(flattened_array)
    most_frequent_color = color_counts.most_common(1)[0][0]

    # Create an output array with the same shape as the input, filled with the most frequent color.
    output_grid = np.full(input_array.shape, most_frequent_color)

    return output_grid.tolist()
```

