# 7447852a • 020 • example_3 • investigate_coder

---
```python
"""
1.  **Identify Red Pairs:** Scan the input grid to identify all pairs of red (2) pixels that are diagonally adjacent.

2.  **Locate Shared Whites:** For each diagonally adjacent red pair, locate the white (0) pixels. Only consider the case with *two* white pixels.

3. **Fill Yellow:** If a pair of red pixels are at opposite corners of a 2x2 square, examine the two shared "corner" pixels:
    *   If both corner pixels are white (0), change them to yellow (4).
    * note that diagonally adjacent 2's that do not form an opposite corner of
      a 2x2 square are ignored
"""

import numpy as np

def get_diagonally_adjacent_red_pairs(grid):
    red_pixels = np.argwhere(grid == 2)
    diagonal_pairs = []
    for i in range(len(red_pixels)):
        for j in range(i + 1, len(red_pixels)):
            diff = red_pixels[i] - red_pixels[j]
            if np.abs(diff).sum() == 2 and np.abs(diff[0]) == 1 and np.abs(diff[1]) == 1:
                diagonal_pairs.append((red_pixels[i], red_pixels[j]))
    return diagonal_pairs

def get_shared_white_pixels(grid, red_pair):
   
    row1, col1 = red_pair[0]
    row2, col2 = red_pair[1]

    shared_whites = []
    
    potential_whites = [(row1, col2), (row2, col1)]

    for r, c in potential_whites:
        if 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1] and grid[r,c] == 0:
            shared_whites.append((r,c))

    return shared_whites
    

def transform(input_grid):
    """Transforms the input grid according to the diagonal red rule."""
    output_grid = np.copy(input_grid)
    diagonal_red_pairs = get_diagonally_adjacent_red_pairs(input_grid)

    for red_pair in diagonal_red_pairs:
        shared_white_pixels = get_shared_white_pixels(input_grid, red_pair)
        # check there are two
        if len(shared_white_pixels) == 2:          
            for r, c in shared_white_pixels:
                output_grid[r, c] = 4

    return output_grid
```
