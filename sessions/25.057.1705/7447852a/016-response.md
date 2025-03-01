# 7447852a • 016 • refine_coder

---
```python
"""
Transforms an input grid by replacing white pixels (0) with yellow pixels (4) based on their proximity to red pixels (2). A white pixel becomes yellow if it is directly adjacent (horizontally or diagonally) to a red pixel.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rules.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel in the grid
    for r in range(rows):
        for c in range(cols):
            # Check if the current pixel is white (0)
            if input_grid[r, c] == 0:
                # Check for adjacent red pixels in all 8 directions
                is_adjacent_to_red = False
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue  # Skip the current pixel itself
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and input_grid[nr, nc] == 2:
                            is_adjacent_to_red = True
                            break  # No need to check other neighbors if one is red
                    if is_adjacent_to_red:
                        break
                if is_adjacent_to_red:
                    output_grid[r, c] = 4  # Change to yellow

    return output_grid
```

