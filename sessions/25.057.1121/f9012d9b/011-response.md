# f9012d9b • 011 • refine_coder

---
```python
"""
Determine a single color value to represent the entire input grid.

1.  **Count Colors:** Determine the frequency of each color (0-9) in the input grid.
2.  **Handle all white:** If all of the input values are white/0, the result is a
    1 x 1 grid of white
3.  **Find most frequent:** if other values exist, take the most frequent value. If there are ties for frequency, take the largest value.
4.  **Create Output:** Construct a 1x1 output grid containing only the identified
     color.
"""

import numpy as np

def transform(input_grid):
    # Count Occurrences
    unique, counts = np.unique(input_grid, return_counts=True)
    color_counts = dict(zip(unique, counts))

    # Handle All White
    if set(color_counts.keys()) == {0}:
        output_grid = np.array([[0]])
        return output_grid

    # Find Most Frequent (excluding white)
    if 0 in color_counts:
      del color_counts[0]

    if not color_counts:
        output_grid = np.array([[0]])
        return output_grid

    max_count = max(color_counts.values())
    most_frequent_colors = [color for color, count in color_counts.items() if count == max_count]
    most_frequent_color = max(most_frequent_colors)  # Largest if tie

    # Create 1x1 Output
    output_grid = np.array([[most_frequent_color]])
    return output_grid
```
