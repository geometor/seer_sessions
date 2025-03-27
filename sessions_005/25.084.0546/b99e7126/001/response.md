```python
"""
1.  **Identify Bands:** Divide the input grid into three main horizontal patterns, separated by rows of white (0) pixels. Each pattern consists of three bands (rows of data).
2.  **Isolate Central Bands:** Within each of the three main patterns, isolate the central band (rows 6-8, rows 10-12, rows 14-16, of the entire 29 x 29 grid).
3. **Shift central bands**. Transform pattern 1 by making the central bands of pattern 1 become the central bands of pattern 2. Transform pattern 2 by making the central bands of pattern 2 become the central bands of pattern 3. The central bands in the output for pattern 3 remain the same as pattern 3 in the input.
4.  **Reconstruct Output:** Combine the unchanged upper and lower bands of each original input pattern with the modified central band. Maintain the white (0) pixel rows as separators.
"""

import numpy as np

def find_patterns(grid):
    # Find rows that are all white (0)
    white_rows = [i for i, row in enumerate(grid) if np.all(row == 0)]
    
    # Identify start and end of each pattern
    patterns = []
    start = 0
    for i in range(len(white_rows)):
        end = white_rows[i]
        patterns.append((start, end))
        start = end+1    
    patterns.append((start, len(grid))) #last segment
    return patterns

def get_central_band(grid, pattern):
    start, end = pattern
    central_start = start + (end-start)//2-1 if end - start > 2 else start  # Approximate middle, favoring earlier row
    
    central_end = central_start+3    
    
    return grid[central_start:central_end]

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    
    # Find the three main patterns
    patterns = find_patterns(input_grid)
    
    # Extract central bands
    central_bands = [get_central_band(input_grid, p) for p in patterns]
        
    # Shift central bands cyclically
    new_central_bands = [central_bands[-1]] + central_bands[:-1] # Modified cyclic shift
    
    
    # Replace central bands in output grid.
    for i in range(len(patterns)-1):
        start, end = patterns[i]
        central_start = start + (end - start)//2 -1 if end - start > 2 else start
        central_end = central_start + 3

        output_grid[central_start:central_end] = new_central_bands[i+1]

    return output_grid
```