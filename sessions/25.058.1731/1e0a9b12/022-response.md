# 1e0a9b12 • 022 • refine_coder

---
```python
"""
1.  **Blue Pixel Shift:** If a blue pixel is in the 4th column (index 3) and its row index is 2 or greater, move it down by one row *unless* another rule with higher precedence applies.

2.  **Green Pixel Shift:** If a green pixel is in the second column (index 1) and its row index is greater than or equal to 1, move it down by one row *unless* another rule with higher precedence applies.

3.  **Magenta Pixel Shift:** If a magenta pixel is at position [3, 0], move it down by one row *unless* another rule with higher precedence applies.

4. **Red Pixel Shift:** If a red pixel is in the 5th column (index 4) and it's row index is less that 2, move it one row down and one column to the left *unless* another rule with higher precendence applies.

5.  **Copy Remaining:** Any non-zero pixel not affected by the above rules remains in its original position.

6. **Precedence**:
    - Red Pixel Shift
    - Blue Pixel Shift
    - Green Pixel Shift
    - Magenta Pixel Shift
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape
    moved = np.zeros_like(input_grid, dtype=bool) # Keep track of moved pixels

    # Iterate through each pixel of the input grid, applying rules with precedence
    for r in range(rows):
        for c in range(cols):
            # Red pixel Shift (Highest precedence)
            if input_grid[r, c] == 2 and c == 4 and r < 2 and not moved[r,c]:
                if r + 1 < rows and c - 1 >= 0: #bounds check
                    output_grid[r + 1, c - 1] = 2
                    moved[r+1, c-1] = True
            # Blue Pixel Shift
            elif input_grid[r, c] == 1 and c == 3 and r >= 2 and not moved[r,c]:
                if r + 1 < rows:
                    output_grid[r + 1, c] = 1
                    moved[r+1,c] = True
            # Green Pixel Shift
            elif input_grid[r, c] == 3 and c == 1 and r >= 1 and not moved[r,c]:
                if r + 1 < rows:
                    output_grid[r + 1, c] = 3
                    moved[r+1,c]=True
            # Magenta Pixel Shift
            elif input_grid[r, c] == 6 and r == 3 and c == 0 and not moved[r,c]:
                if r + 1 < rows:
                    output_grid[r + 1, c] = 6
                    moved[r+1, c]= True
            # Copy Remaining
            elif input_grid[r, c] != 0 and not moved[r,c]:
                output_grid[r, c] = input_grid[r, c]
                moved[r,c] = True #mark as processed to prevent modification.

    return output_grid
```
