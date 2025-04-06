```python
import copy

"""
Processes a 2D grid of integers. For each non-zero cell in the input grid, 
it fills the cells to its right in the same row with its value. 
It also fills the cells below it in the last column of the grid with its value. 
The process iterates through the input grid row by row, then column by column. 
If multiple non-zero cells influence the same output cell, the value from the 
cell processed later (based on the iteration order) prevails.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies a fill transformation based on non-zero cells in the input grid.

    Args:
        input_grid: A list of lists representing the 2D input grid.

    Returns:
        A list of lists representing the transformed 2D output grid.
    """
    # Handle empty or invalid input
    if not input_grid or not input_grid[0]:
        return []

    # Get grid dimensions
    height = len(input_grid)
    width = len(input_grid[0])
    
    # Initialize output_grid as a deep copy of the input_grid
    # This ensures the original input is not modified and the output starts correctly
    output_grid = copy.deepcopy(input_grid)

    # Iterate through each cell of the input grid to find non-zero sources
    for r in range(height):
        for c in range(width):
            # Get the value of the current cell in the *original* input grid
            source_value = input_grid[r][c]

            # Check if the cell is a non-zero source
            if source_value > 0:
                
                # Perform Horizontal Fill (to the right in the same row)
                # Start from the column immediately to the right of the source
                for j in range(c + 1, width):
                    output_grid[r][j] = source_value
                    
                # Perform Vertical Fill (downwards in the last column)
                # Start from the row immediately below the source
                last_col_index = width - 1
                for i in range(r + 1, height):
                    output_grid[i][last_col_index] = source_value

    # Return the modified output grid
    return output_grid

```