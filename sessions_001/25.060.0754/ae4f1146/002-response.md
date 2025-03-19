# ae4f1146 • 002 • example_4 • investigate_coder

---
```python
"""
The transformation extracts a specific 3x3 region from the input grid.  The selection of this region is based on identifying the most consistent region of alternating blue (1) and azure (8) pixels. The search for the subgrid prioritizes locations closer to the center of the input grid. The colors and relative positions of that 3x3 region are maintained as it becomes the output.
"""

import numpy as np

def find_best_subgrid(input_grid):
    """Finds the 3x3 subgrid with the most alternating 1s and 8s, prioritizing center."""
    best_subgrid = None
    best_score = -1
    center_x, center_y = 4, 4  # Center of the 9x9 grid

    for row in range(input_grid.shape[0] - 2):
        for col in range(input_grid.shape[1] - 2):
            subgrid = input_grid[row:row+3, col:col+3]
            score = 0
            # Count alternating 1s and 8s
            for i in range(3):
                for j in range(3):
                    if subgrid[i, j] == 1 or subgrid[i, j] == 8:
                        if i > 0 and subgrid[i-1, j] != subgrid[i, j] and (subgrid[i-1,j] == 1 or subgrid[i-1,j] == 8):
                            score += 1
                        if j > 0 and subgrid[i, j-1] != subgrid[i, j] and (subgrid[i, j-1] == 1 or subgrid[i, j-1] == 8):
                            score += 1
            # Prioritize center:  Reduce score based on distance from center
            distance_from_center = abs(row - center_x) + abs(col - center_y)
            score -= distance_from_center * 0.1 # slight penalty

            if score > best_score:
                best_score = score
                best_subgrid = subgrid

    return best_subgrid

def transform(input_grid):
    """
    Extracts a 3x3 subgrid from the input grid and returns it.
    """
    input_grid = np.array(input_grid)  # Convert to NumPy array

    # Find the best 3x3 subgrid
    output_grid = find_best_subgrid(input_grid)

    return output_grid.tolist() # Return as list
```
