# aedd82e4 • 010 • refine_coder

---
```python
"""
1.  **Preserve Reds:** Copy the input grid to the output grid, ensuring all pixels that are red (2) in the input remain red in the output.
2.  **Identify Blue Candidates:** White pixels (0) that are directly adjacent (horizontally or vertically) to a red pixel (2) are candidates to become blue.
3. **Propagate Blue Transformation**: Any white pixel that is adjacent to a blue candidate pixel is also a candidate to become blue.
4.  **Change to Blue:** All identified candidate pixels change from white (0) to blue (1).
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Create a set to store the coordinates of blue candidates
    blue_candidates = set()

    # Identify initial blue candidates (adjacent to red pixels)
    for r in range(rows):
        for c in range(cols):
            if output_grid[r, c] == 0:  # Check if white
                is_adjacent_to_red = False
                # Check adjacent cells (up, down, left, right)
                if r > 0 and output_grid[r - 1, c] == 2:
                    is_adjacent_to_red = True
                if r < rows - 1 and output_grid[r + 1, c] == 2:
                    is_adjacent_to_red = True
                if c > 0 and output_grid[r, c - 1] == 2:
                    is_adjacent_to_red = True
                if c < cols - 1 and output_grid[r, c + 1] == 2:
                    is_adjacent_to_red = True

                if is_adjacent_to_red:
                    blue_candidates.add((r, c))

    # Propagate blue transformation
    new_candidates = blue_candidates.copy()
    while new_candidates:
        next_candidates = set()
        for r, c in new_candidates:
            # Check adjacent white pixels
            if r > 0 and output_grid[r - 1, c] == 0 and (r - 1, c) not in blue_candidates:
                next_candidates.add((r - 1, c))
            if r < rows - 1 and output_grid[r + 1, c] == 0 and (r + 1, c) not in blue_candidates:
                next_candidates.add((r + 1, c))
            if c > 0 and output_grid[r, c - 1] == 0 and (r, c - 1) not in blue_candidates:
                next_candidates.add((r, c - 1))
            if c < cols - 1 and output_grid[r, c + 1] == 0 and (r, c + 1) not in blue_candidates:
                next_candidates.add((r, c + 1))
        blue_candidates.update(next_candidates)
        new_candidates = next_candidates

    # Change all identified candidates to blue
    for r, c in blue_candidates:
        output_grid[r, c] = 1

    return output_grid
```
