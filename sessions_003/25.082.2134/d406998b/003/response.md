```python
"""
1. **Identify Gray Runs:** Examine the input grid and identify contiguous "runs" of gray (5) pixels. A run is defined as a sequence of adjacent gray pixels either horizontally or vertically. Diagonal adjacency does not constitute a run.

2. **Horizontal Runs:** For each horizontal run of gray pixels:
    - Start counting from the leftmost pixel of the run (index 0).
    - Change the color of gray pixels at *odd* indices (1, 3, 5, ...) to green (3).

3. **Vertical Runs:** For each vertical run of gray pixels:
    - Start counting from the topmost pixel of the run (index 0).
    - Change the color of gray pixels at *even* indices (0, 2, 4, ...) to green (3).

4. **Other Pixels:** All pixels that are not part of a gray run remain unchanged.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through each cell to find and process runs
    for r in range(rows):
        for c in range(cols):
            if output_grid[r, c] == 5:
                # Check for horizontal run
                run_length = 0
                while c + run_length < cols and output_grid[r, c + run_length] == 5:
                    run_length += 1
                
                # Apply horizontal rule
                if run_length > 0 :
                  for i in range(run_length):
                      if (i+1) % 2 != 0 and output_grid[r,c+i] == 5:  # use +1 because instructions use 1-based
                        output_grid[r, c + i] = 3
                  c += run_length # move past checked values

    for r in range(rows):
        for c in range(cols):
            if output_grid[r, c] == 5:

                # Check for vertical run
                run_length = 0
                while r + run_length < rows and output_grid[r + run_length, c] == 5:
                    run_length += 1

                # apply vertical rule
                if run_length > 0:
                    for i in range(run_length):
                        if (i+1) % 2 == 0 and output_grid[r+i,c] == 5: # use +1 because instructions use 1-based
                            output_grid[r + i, c] = 3
                    r += run_length

    return output_grid
```