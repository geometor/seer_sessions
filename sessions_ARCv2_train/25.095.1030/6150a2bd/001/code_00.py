import copy 

"""
Transforms a 3x3 input grid by rotating it 180 degrees.
Each element at input position (row, column) is moved to the 
output position (2 - row, 2 - column).
"""

def transform(input_grid):
    """
    Rotates a 3x3 grid 180 degrees.

    Args:
        input_grid: A list of lists representing the 3x3 input grid.

    Returns:
        A list of lists representing the 3x3 output grid after rotation.
    """
    
    # Assuming a 3x3 grid based on the examples and description
    rows = 3
    cols = 3

    # Initialize output_grid with the same dimensions, filled with a placeholder (e.g., 0)
    # A deep copy is safer if we were modifying in place, but here we create a new grid.
    output_grid = [[0 for _ in range(cols)] for _ in range(rows)]

    # Iterate through each cell of the input grid
    for r in range(rows):
        for c in range(cols):
            # Calculate the target position for the 180-degree rotation
            # The element at input_grid[r][c] goes to output_grid[rows-1-r][cols-1-c]
            target_r = rows - 1 - r
            target_c = cols - 1 - c
            
            # Place the input grid element into the calculated position in the output grid
            output_grid[target_r][target_c] = input_grid[r][c]

    # Return the transformed grid
    return output_grid
