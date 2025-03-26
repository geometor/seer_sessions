```python
"""
Transforms a 3x3 input grid into a single integer code (1, 2, 3, or 6) based on the shape of the non-white pattern.

1. Identify the single non-white color (`pattern_color`) in the 3x3 input grid.
2. Check if the pattern exactly matches a '+' shape template using the `pattern_color`. If it matches, output 6.
3. If not a '+' shape, check if the pattern exactly matches an 'X' shape template using the `pattern_color`. If it matches, output 2.
4. If it matches neither template, check if there exists any 2x2 subgrid within the input grid composed entirely of the `pattern_color`.
5. If such a 2x2 subgrid exists, output 3.
6. Otherwise (doesn't match templates and no 2x2 block), output 1.
"""

import numpy as np

def has_2x2_block(grid, pattern_color):
    """
    Checks if a 2x2 block of the specified pattern_color exists anywhere in the 3x3 grid.
    """
    # Check the four possible top-left corners of a 2x2 block in a 3x3 grid
    # Top-left (0,0)
    if (grid[0, 0] == pattern_color and grid[0, 1] == pattern_color and
        grid[1, 0] == pattern_color and grid[1, 1] == pattern_color):
        return True
    # Top-right (0,1)
    if (grid[0, 1] == pattern_color and grid[0, 2] == pattern_color and
        grid[1, 1] == pattern_color and grid[1, 2] == pattern_color):
        return True
    # Bottom-left (1,0)
    if (grid[1, 0] == pattern_color and grid[1, 1] == pattern_color and
        grid[2, 0] == pattern_color and grid[2, 1] == pattern_color):
        return True
    # Bottom-right (1,1)
    if (grid[1, 1] == pattern_color and grid[1, 2] == pattern_color and
        grid[2, 1] == pattern_color and grid[2, 2] == pattern_color):
        return True
        
    return False

def transform(input_grid):
    """
    Applies the transformation rule based on pattern shape ('+', 'X') or 2x2 block presence.
    """
    # Convert input list of lists to a numpy array
    grid = np.array(input_grid, dtype=int)
    
    # Find the pattern color (assuming exactly one non-white color exists)
    pattern_color = 0
    unique_colors = np.unique(grid)
    for color in unique_colors:
        if color != 0: # 0 is white
            pattern_color = color
            break
            
    # Handle the unlikely case of an all-white grid (or if finding pattern color fails)
    if pattern_color == 0:
        # Based on task examples, a pattern always exists.
        # If needed, we could return a default value or raise an error.
        # Let's assume pattern_color is always found > 0.
        # For robustness, maybe return 0 or None, but based on problem, this shouldn't happen.
        # Returning 1 might be a safe fallback if we consider it 'asymmetric without 2x2'.
        return 1 

    # Define the '+' shape template
    plus_template = np.array([
        [0, pattern_color, 0],
        [pattern_color, pattern_color, pattern_color],
        [0, pattern_color, 0]
    ])

    # Define the 'X' shape template
    x_template = np.array([
        [pattern_color, 0, pattern_color],
        [0, pattern_color, 0],
        [pattern_color, 0, pattern_color]
    ])

    # Check for '+' shape match
    if np.array_equal(grid, plus_template):
        return 6

    # Check for 'X' shape match
    elif np.array_equal(grid, x_template):
        return 2

    # Otherwise, check for a 2x2 block
    else:
        if has_2x2_block(grid, pattern_color):
            # Pattern contains a 2x2 block
            return 3
        else:
            # Pattern does not contain a 2x2 block
            return 1
```