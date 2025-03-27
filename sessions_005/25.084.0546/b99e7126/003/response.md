```python
"""
1. **Identify Patterns:** Divide the input grid into three horizontal patterns, separated by rows of white (0) pixels.
2. **Isolate Central Bands:** Within each of the three patterns, identify the central three rows.
3. **Shift Central Bands:**
   - The central band of Pattern 1 is replaced by the central band of Pattern 2.
   - The central band of Pattern 2 is replaced by the central band of Pattern 3.
   - The central band of Pattern 3 remains unchanged.
4. **Reconstruct Output:** Combine the unchanged upper and lower bands of each original input pattern with the modified central band. Maintain the white (0) pixel rows as separators.
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
        
    
    # Replace central bands in output grid.
    for i in range(len(patterns)-1):
        start, end = patterns[i]
        central_start = start + (end - start)//2 -1 if end - start > 2 else start
        central_end = central_start + 3
        if i < len(central_bands) -1:
          output_grid[central_start:central_end] = central_bands[i+1]

    return output_grid
```