# 7837ac64 • 018 • refine_coder

---
```python
"""
The transformation selects a single, non-black pixel from each of three equal horizontal segments of the input grid and places them in a 3x1 output grid. The selected pixels are placed vertically in the output grid, in the order of the segment from which they were selected. The selection criteria prioritize non-black, and seemingly the left-most colored pixel within a segment.
"""

import numpy as np

def transform(input_grid):
    # Initialize 3x1 output grid with 0s (black)
    output_grid = np.zeros((3, 1), dtype=int)

    input_height = input_grid.shape[0]
    segment_height = input_height // 3
    
    output_row = 0
    # Iterate through each segment
    for segment_index in range(3):
        start_row = segment_index * segment_height
        end_row = (segment_index + 1) * segment_height
        if segment_index == 2 :
            end_row = input_height
        
        # Find a non-black pixel in the current segment
        found = False
        for col in range(input_grid.shape[1]):
             for row in range(start_row, end_row):
                if input_grid[row, col] != 0:
                    output_grid[output_row, 0] = input_grid[row, col]
                    output_row += 1
                    found = True
                    break  # Stop searching after finding the first matching pixel in a column
             if found:
                break

    return output_grid
```
