```python
import copy

"""
Transforms an input grid based on marker cells (value 5).

1. Creates an output grid of the same dimensions as the input, initialized with 0s.
2. Iterates through each cell of the input grid.
3. If a cell contains the marker value 5, it identifies the 3x3 neighborhood centered on that cell.
4. For every cell within the valid bounds of this 3x3 neighborhood in the output grid, it sets the value to 1.
5. Overlapping neighborhoods result in the corresponding output cells remaining 1.
6. Returns the final output grid.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies a 3x3 stamp of 1s onto an output grid for every 5 found 
    in the input grid.
    """
    if not input_grid:
        return []
        
    num_rows = len(input_grid)
    if num_rows == 0:
        return [[]]
    num_cols = len(input_grid[0])
    if num_cols == 0:
        return [[] for _ in range(num_rows)]

    # Initialize output_grid with zeros, matching input dimensions
    # Using deepcopy to avoid modifying the input if it were mutable in a different context,
    # but a simple list comprehension creating zeros is more direct here.
    output_grid = [[0 for _ in range(num_cols)] for _ in range(num_rows)]

    # Iterate through each cell of the input grid
    for r in range(num_rows):
        for c in range(num_cols):
            # Check if the current cell is a marker (value 5)
            if input_grid[r][c] == 5:
                # Define the 3x3 neighborhood boundaries centered at (r, c)
                for rr in range(r - 1, r + 2):
                    for cc in range(c - 1, c + 2):
                        # Check if the neighborhood cell coordinates (rr, cc) are within the grid bounds
                        if 0 <= rr < num_rows and 0 <= cc < num_cols:
                            # Set the corresponding cell in the output grid to 1
                            output_grid[rr][cc] = 1

    # Return the transformed grid
    return output_grid

```