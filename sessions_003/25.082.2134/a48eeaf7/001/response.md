```python
"""
The transformation rule repositions gray (5) pixels relative to red (2) pixels. If a gray pixel is not in the same column as any red pixel, it's moved to the next column, maintaining its row. If it is in the same column, it seems to create a copy next to the red, or get repositioned according to some more complex logic that will be iterated.
"""

import numpy as np

def find_objects(grid, color):
    """Finds the positions of all pixels of a given color."""
    return np.argwhere(grid == color)

def transform(input_grid):
    """Transforms the input grid according to the observed rules."""
    
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    
    # Find the positions of gray (5) and red (2) pixels
    gray_positions = find_objects(input_grid, 5)
    red_positions = find_objects(input_grid, 2)

    # Iterate through gray pixels and apply transformation rules
    for gray_pos in gray_positions:
        row, col = gray_pos
        
        red_cols = [r[1] for r in red_positions]

        if col not in red_cols:
            # if no red color in same column, move to next column
            output_grid[row, col] = 0
            if col + 1 < output_grid.shape[1]:
              output_grid[row,col+1]=5
        else:
            #find if any red pixels exists
            if len(red_positions)>0:
                output_grid[row, col] = 0
                #put next to red blocks
                min_dist = float('inf')
                nearest_red = None
                for r_pos in red_positions:
                    dist = abs(r_pos[1] - col)
                    if dist < min_dist:
                        min_dist = dist
                        nearest_red = r_pos

                if nearest_red is not None:  # Check if nearest_red was found
                    if col<nearest_red[1]:
                        output_grid[row,nearest_red[1]-1]=5
                    else:
                        output_grid[row,nearest_red[1]+1]=5

    return output_grid
```