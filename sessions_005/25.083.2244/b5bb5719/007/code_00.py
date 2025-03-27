"""
1.  **Copy First Row:** Copy the first row of the input grid directly to the first row of the output grid.

2.  **Transform Second Row:**
    *   Identify runs (contiguous blocks of the same color) in the first row of the *input* grid. Represent each run as a tuple: `(color, length)`.
    *   Initialize the second row of the *output* grid. The first element is always '7'.
    *   Iterate through the runs of the first row of the input grid, starting from the *second* run (index 1).
        *   For each run `i` (where `i > 0`):
            *   The *length* of the output run in the second row is determined by the length of the *previous* run (i-1) in the first row.
            *   The *color* of the output run in the second row is the color of the *current* run (i) in the first row.
            *   Append these pixels of the determined *color* and *length* to the second row of the output grid.

3.  **Copy Remaining Rows:** Copy any remaining rows (from the third row onwards) of the input grid directly to the output grid.
"""

import numpy as np

def get_runs(row):
    runs = []
    current_run_color = row[0]
    current_run_length = 1
    for i in range(1, len(row)):
        if row[i] == current_run_color:
            current_run_length += 1
        else:
            runs.append((current_run_color, current_run_length))
            current_run_color = row[i]
            current_run_length = 1
    runs.append((current_run_color, current_run_length))
    return runs

def transform(input_grid):
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Copy the first row
    output_grid[0, :] = input_grid[0, :]

    if rows > 1:
        # Get runs in the first row
        runs = get_runs(input_grid[0, :])

        # Transform the second row
        
        current_index = 0
        output_grid[1,current_index] = 7 #first value is 7
        current_index+=1

        for run_index in range(1, len(runs)):
            prev_length = runs[run_index-1][1]
            current_color = runs[run_index][0]
            
            for _ in range(prev_length):
                if current_index < cols:
                    output_grid[1, current_index] = current_color
                    current_index += 1
                else:
                    break

    #copy remaining rows        
    return output_grid.tolist()