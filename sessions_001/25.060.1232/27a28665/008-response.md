# 27a28665 • 008 • refine_coder

---
```python
"""
The transformation rule is as follows:

1. **Count Colors:** For the input grid, count the occurrences of each color (represented by digits 0-9).
2. **Identify Dominant Color:** Determine the color with the highest count. This is the *potential* dominant color.
3. **Check Dominance:** A color is considered "dominant" if its count is greater than or equal to the sum of the counts of all *other* colors minus 1.
4. **Create Output (Conditional):**
    - If a dominant color exists (based on the check in step 3), the output is a 1x1 grid containing the value `1`.
    - If no dominant color exists, the output is `None`.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms an input grid based on color dominance.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list.

    Returns:
        list: A 1x1 grid containing '1' if a dominant color exists, otherwise None.
    """
    # Convert input grid to numpy array
    input_array = np.array(input_grid)

    # Count occurrences of each color
    unique, counts = np.unique(input_array, return_counts=True)
    color_counts = dict(zip(unique, counts))

    # Find the color with the maximum count
    max_count = 0
    dominant_color = None
    for color, count in color_counts.items():
        if count > max_count:
            max_count = count
            dominant_color = color

    # Check if the dominant color count is >= sum of other color counts - 1
    sum_other_colors = sum(count for color, count in color_counts.items() if color != dominant_color)
    
    if max_count >= sum_other_colors - 1:
      output_grid = [[1]]
      return output_grid
    else:
      return None # no transformation
```
