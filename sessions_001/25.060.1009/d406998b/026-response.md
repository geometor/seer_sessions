# d406998b • 026 • refine_coder

---
```python
"""
Identifies horizontal sequences of gray (5) pixels. If all gray pixels in
a sequence have white (0) pixels directly above and below, the center
gray pixel of that sequence is replaced with green (3).
"""

import numpy as np

def get_horizontal_gray_sequences(grid):
    """
    Finds all horizontal sequences of gray pixels.
    Returns a list of lists, where each inner list contains the 
    (row, col) coordinates of gray pixels in a sequence.
    """
    rows, cols = grid.shape
    gray_sequences = []
    for row in range(rows):
        current_sequence = []
        for col in range(cols):
            if grid[row, col] == 5:
                current_sequence.append((row, col))
            else:
                if len(current_sequence) > 0:
                    gray_sequences.append(current_sequence)
                    current_sequence = []
        if len(current_sequence) > 0:  # Handle sequences at the end of a row
            gray_sequences.append(current_sequence)
    return gray_sequences

def check_white_borders(grid, sequence):
    """
    Checks if a horizontal sequence of gray pixels has white pixels 
    above and below *all* its pixels.
    """
    rows, cols = grid.shape
    for row, col in sequence:
        # Check above
        if row - 1 < 0 or grid[row - 1, col] != 0:
            return False
        # Check below
        if row + 1 >= rows or grid[row + 1, col] != 0:
            return False
    return True

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    
    # find gray sequences
    gray_sequences = get_horizontal_gray_sequences(input_grid)
    
    for sequence in gray_sequences:
        # check the white borders
        if check_white_borders(output_grid, sequence):
            # change the center gray to green
            center_index = len(sequence) // 2
            center_row, center_col = sequence[center_index]
            output_grid[center_row, center_col] = 3

    return output_grid
```
