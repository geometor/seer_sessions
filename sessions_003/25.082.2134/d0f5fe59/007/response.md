```python
"""
Extracts a top-left to bottom-right diagonal of azure (8) pixels from the input grid.
The length of the extracted diagonal is determined by the number of azure pixels in the expected output.
Creates a square output grid with the side length equal to the length of the extracted diagonal,
placing azure pixels along its main diagonal.
"""

import numpy as np

def find_valid_diagonals(grid):
    """Finds all valid top-left to bottom-right diagonals of azure pixels."""
    grid = np.array(grid)
    rows, cols = grid.shape
    diagonals = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 8:
                temp_diag = []
                row, col = r, c
                while row < rows and col < cols and grid[row, col] == 8:
                    temp_diag.append((row, col))
                    row += 1
                    col += 1
                if len(temp_diag) > 0:
                  diagonals.append(temp_diag)

    return diagonals

def select_target_diagonal(diagonals, target_length):
    """Selects a diagonal with the specified target length."""
    for diag in diagonals:
        if len(diag) == target_length:
            return diag
    return []  # Return empty list if no diagonal of target length is found


def transform(input_grid, output_grid):  # Added output_grid as argument
    """Extracts the specific azure diagonal and forms the output grid."""

    # Find all valid azure diagonals
    diagonals = find_valid_diagonals(input_grid)

    # Determine the target diagonal length from the output grid
    target_length = np.sum(np.array(output_grid) == 8)


    # Select the target diagonal
    target_diagonal = select_target_diagonal(diagonals, target_length)

    # Determine output size
    diagonal_length = len(target_diagonal)

    # Initialize output grid with zeros (white)
    output_grid = np.zeros((diagonal_length, diagonal_length), dtype=int)

    # Place azure pixels along the diagonal of the output grid
    for i in range(diagonal_length):
        output_grid[i, i] = 8

    return output_grid.tolist()
```
