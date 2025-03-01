# cce03e0d • 012 • refine_coder

---
```python
"""
Transforms an input grid into an output grid based on size comparisons and pattern recognition.
"""

import numpy as np

def rotate_90_clockwise(grid):
    return np.rot90(grid, k=-1)

def rotate_270_clockwise(grid):
    return np.rot90(grid, k=1)

def detect_cross(grid):
    """Detects if a 3x3 grid forms a cross shape and extracts vertical lines."""
    rows, cols = grid.shape
    if rows != 3 or cols != 3:
        return None

    # Check for cross structure (center pixel must be same color as adjacent)
    center_color = grid[1, 1]
    if center_color == 0:  # background
        return None
    
    if (grid[0, 1] == center_color and grid[2, 1] == center_color and
        grid[1, 0] == center_color and grid[1, 2] == center_color):
       
        # Extract vertical lines
        vertical_line = [grid[0, 1], grid[1, 1], grid[2, 1]]  # center doesn't matter now
        return vertical_line
    return None
    

def transform(input_grid):
    input_grid = np.array(input_grid)
    in_rows, in_cols = input_grid.shape
    
    # Case 1: Output is a multiple of the input size.
    if in_rows * 3 == 9 and in_cols * 3 == 9 and in_rows == 3 and in_cols ==3:
        output_grid = np.zeros((9, 9), dtype=int)
        rotated_grid_90 = rotate_90_clockwise(input_grid)
        output_grid[0:3, 6:9] = rotated_grid_90
        rotated_grid_270 = rotate_270_clockwise(input_grid)
        output_grid[6:9, 0:3] = rotated_grid_270
        return output_grid.tolist()

    # Case 2 & 3: Input and output sizes are the same.
    elif in_rows == 3 and in_cols == 3:
        output_grid = np.zeros((3, 3), dtype=int)
        vertical_lines = detect_cross(input_grid)
        if vertical_lines:
            output_grid[0:3, 0] = vertical_lines
            output_grid[0:3, 2] = vertical_lines
            return output_grid.tolist()
        else:
            # assume no rotation needed, return blank
            return output_grid.tolist()
            
    elif in_rows == 2 and in_cols == 2:
        output_grid = rotate_90_clockwise(input_grid)
        return output_grid.tolist()
        

    # Default: Return input if no rules applied, or make empty grid same
    # dimensions as input
    return np.zeros_like(input_grid).tolist()
```
