# f9012d9b • 012 • refine_coder

---
```python
"""
1.  **Examine Input:** Analyze the input grid to identify all unique colors present.
2.  **Count Colors:** Count the number of times each color appears in the input grid, *excluding* color 0 (white/background).
3.  **Handle Empty Counts:** If, after excluding 0, there are no other colors present, the output is 0 (white).
4.  **Find Most Frequent (if applicable):** If there is at least one non-zero, non-white color, output is that single, non-zero color
5.  **Create Output:** Create a 1x1 output grid.
6.  **Set Output:** Set the value of the single pixel in the output grid to:
    *   0 if there were no non-zero colors in the input.
    *   the single non-zero color
"""

import numpy as np

def transform(input_grid):
    """
    Transforms an input grid into a 1x1 output grid based on the most frequent non-zero color.
    """
    # Count Occurrences
    unique, counts = np.unique(input_grid, return_counts=True)
    color_counts = dict(zip(unique, counts))

    # Ignore white (0)
    if 0 in color_counts:
        del color_counts[0]

    # Handle Empty Counts / All Zeros
    if not color_counts:
        output_grid = np.array([[0]])  # Output 0 if no non-zero colors
        return output_grid

    # Find Most Frequent (if applicable)
    #if len(color_counts) >= 1:
    most_frequent_color = max(color_counts, key=color_counts.get)
    output_grid = np.array([[most_frequent_color]])
    return output_grid
```
