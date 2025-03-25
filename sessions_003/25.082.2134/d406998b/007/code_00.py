"""
1.  **Identify Gray Runs:** Locate all contiguous sequences ("runs") of gray (5) pixels in the input grid. Runs are defined by horizontal or vertical adjacency (not diagonal).

2.  **Process Horizontal Runs:** For each row in the grid:
    *   Identify all horizontal runs of gray pixels.
    *   Within each run, starting from the leftmost pixel (index 0), change the color of gray pixels at *even* indices (0, 2, 4, ...) to green (3).

3.  **Process Vertical Runs:** For each column in the *modified* grid (after horizontal processing):
    *   Identify all vertical runs of gray pixels.
    *   Within each run, starting from the topmost pixel (index 0), change the color of gray pixels at *odd* indices (1, 3, 5, ...) to green (3).

4.  **Preserve Other Pixels:** All pixels that are not gray, or gray pixels not meeting the alternating criteria within runs, maintain their original colors.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Process Horizontal Runs
    for r in range(rows):
        c = 0
        while c < cols:
            if output_grid[r, c] == 5:
                # Find horizontal run length
                run_length = 0
                while c + run_length < cols and output_grid[r, c + run_length] == 5:
                    run_length += 1

                # Change color of gray pixels at even indices within the run
                for i in range(run_length):
                    if i % 2 == 0:  # Even index (0-based)
                        output_grid[r, c + i] = 3

                # Move to the next cell after the run
                c += run_length
            else:
                c += 1

    # Process Vertical Runs (on the modified grid)
    for c in range(cols):
        r = 0
        while r < rows:
            if output_grid[r, c] == 5:
                # Find vertical run length
                run_length = 0
                while r + run_length < rows and output_grid[r + run_length, c] == 5:
                    run_length += 1

                # Change color of gray pixels at odd indices within the run
                for i in range(run_length):
                    if i % 2 != 0:  # Odd index (0-based)
                        output_grid[r + i, c] = 3
                
                # Move to next cell after run
                r += run_length

            else:
                r+=1

    return output_grid