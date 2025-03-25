```python
"""
1. Divide Output: Divide the output grid into three horizontal bands of equal height.
2. Locate Markers: Identify all pixels with the value '5' (gray) in the *input* grid. Note their row positions.
3. Color bands based on markers and their locations:
    - If there are three 5's:
        - iterate through the 5s by row
        - the color for output row $i$ is the column of the $i$-th 5.
    - If there are fewer than three 5's, apply a default of:
        - Top band: 3 (green)
        - Middle band: 4 (yellow)
        - Bottom band: 2 (red)
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on the arrangement of 5s,
    determining top, middle, and bottom sections.
    """
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows, cols), dtype=int)

    # Find positions of 5s
    five_positions = [(r, c) for r in range(rows) for c in range(cols) if input_grid[r, c] == 5]

    # If there are three 5's
    if len(five_positions) == 3:
        # Sort by row
        five_positions.sort()
        # Assign colors based on column of 5
        for i in range(3):
            output_grid[i, :] = five_positions[i][1]
    # If 5s are not in all rows, apply default coloring
    else:
        output_grid[0, :] = 3  # Top
        output_grid[1, :] = 4  # Middle
        output_grid[2, :] = 2  # Bottom

    return output_grid.tolist()
```