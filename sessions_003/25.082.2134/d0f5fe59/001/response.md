```python
"""
Extracts the main diagonal of azure (8) pixels from the input grid and forms a smaller, square output grid.
"""

import numpy as np

def get_main_diagonal(grid):
    """Finds the longest diagonal of azure pixels starting from the top-left."""
    rows, cols = grid.shape
    diagonal_length = 0
    
    # determine maximum possible diagonal start row/col
    for start_row in range(rows):
        temp_length = 0
        for i in range(min(rows - start_row, cols)):
            if grid[start_row + i, i] == 8:
                temp_length += 1
            else:
                break
        diagonal_length = max(diagonal_length, temp_length)

    for start_col in range(1, cols):  # Start from 1 to avoid recounting (0,0)
        temp_length = 0
        for i in range(min(rows, cols - start_col)):
            if grid[i, start_col + i] == 8:
                temp_length += 1
            else:
                break

        diagonal_length = max(diagonal_length, temp_length)
    
    return diagonal_length

def transform(input_grid):
    """Extracts diagonal and forms the output grid"""
    # Convert to numpy array for easier manipulation
    input_grid = np.array(input_grid)

    # Find the length of the main diagonal
    diagonal_length = get_main_diagonal(input_grid)

    # Initialize output grid with zeros (white)
    output_grid = np.zeros((diagonal_length, diagonal_length), dtype=int)

    # Place azure pixels along the diagonal of the output grid
    for i in range(diagonal_length):
        output_grid[i, i] = 8

    return output_grid.tolist()
```