# ce602527 • 002 • example_4 • investigate_coder

---
```python
"""
The transformation identifies the smallest, non-overlapping rectangular region that contains all pixels *not* equal to the most frequent color in the input grid. It then extracts and constructs a new grid containing only the pixels within this bounding box.
"""

import numpy as np
from collections import Counter

def get_bounding_box(grid):
    """Finds the bounding box of non-background pixels."""
    # Find the most frequent color (background)
    flat_grid = grid.flatten()
    color_counts = Counter(flat_grid)
    background_color = color_counts.most_common(1)[0][0]

    # Find rows and cols with non-background pixels
    rows, cols = np.where(grid != background_color)
    
    if len(rows) == 0:  # Handle the case where the grid is all background
        return None, None, None, None

    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)

    return min_row, max_row, min_col, max_col
    

def transform(input_grid):
    """Transforms the input grid by extracting the bounding box of non-background pixels."""
    # Convert input_grid to numpy array
    grid = np.array(input_grid)

    # Get bounding box coordinates
    min_row, max_row, min_col, max_col = get_bounding_box(grid)
    
    if min_row is None:  # If the grid is all background, return an empty grid
        return []

    # Extract the subgrid using the bounding box
    output_grid = grid[min_row:max_row+1, min_col:max_col+1]

    return output_grid.tolist()
```
