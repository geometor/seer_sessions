# 2281f1f4 • 014 • refine_coder

---
```python
"""
The transformation identifies horizontal ranges defined by pairs of gray pixels in each row. Within these horizontal ranges, excluding grey pixels, white pixels are replaced with red pixels. The transformation occurs only if a row contains at least two gray pixels.
"""

import numpy as np

def find_gray_pairs(row):
    """Finds pairs of gray pixel indices in a row."""
    gray_indices = np.where(row == 5)[0]
    pairs = []
    for i in range(len(gray_indices) - 1):
        pairs.append((gray_indices[i], gray_indices[i+1]))
    return pairs

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    output_grid = np.copy(input_grid)
    rows, _ = input_grid.shape

    for r in range(rows):
        # Find gray pixel pairs in the current row
        gray_pairs = find_gray_pairs(input_grid[r])

        # Check if there are any gray pairs
        if len(gray_pairs) > 0 :
            # Iterate through each pair
            for start, end in gray_pairs:
                # Replace white pixels with red within the range (exclusive of gray pixels)
                for c in range(start + 1, end):
                    if output_grid[r, c] == 0:
                        output_grid[r, c] = 2

    return output_grid
```
