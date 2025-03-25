```python
"""
Gray pixels move to be adjacent to the closest red pixel, prioritizing creating a vertical stack above the red pixels. If there are no red pixels, gray pixels remain unchanged.
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
        
        # If no red pixels, skip transformation for this gray pixel
        if len(red_positions) == 0:
            continue

        # Find the nearest red pixel (prioritize horizontal distance)
        min_dist = float('inf')
        nearest_red = None
        for red_pos in red_positions:
            dist = abs(red_pos[1] - col) + abs(red_pos[0] - row) #Manhattan Distance
            if dist < min_dist:
                min_dist = dist
                nearest_red = red_pos

        # Reposition the gray pixel, remove old one.
        output_grid[row, col] = 0
        if nearest_red is not None: #added condition if red pixels exist
            output_grid[nearest_red[0]-1, nearest_red[1]] = 5
        

    return output_grid
```
