import copy
import numpy as np

"""
Transforms the input grid by horizontally reflecting the shape formed by the digit '8'. 
The reflection axis depends on the total count of '8's. 
If the count is 6 or more, reflection occurs across the right edge of the '8' shape's bounding box. 
Otherwise, reflection occurs across the left edge. 
The reflected '8's are added to the grid, potentially overwriting existing '0's. 
Shapes formed by other digits (like '4') remain unchanged.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies a conditional horizontal reflection to the '8' shapes in the grid.

    Args:
        input_grid: A 2D list of integers representing the input grid.

    Returns:
        A 2D list of integers representing the transformed grid.
    """
    # Convert to numpy array for easier indexing and calculations
    grid_np = np.array(input_grid, dtype=int)
    output_grid_np = np.copy(grid_np)
    rows, cols = grid_np.shape

    # Find all locations (row, column) containing the value 8
    locations_8 = []
    for r in range(rows):
        for c in range(cols):
            if grid_np[r, c] == 8:
                locations_8.append((r, c))

    # Count the total number of '8's
    count_8 = len(locations_8)

    # If no '8's are found, return the original grid copy
    if count_8 == 0:
        return output_grid_np.tolist()

    # Find the minimum and maximum column index for the '8' shape
    min_col = cols
    max_col = -1
    for r, c in locations_8:
        if c < min_col:
            min_col = c
        if c > max_col:
            max_col = c

    # Determine the reflection rule based on count_8
    reflect_right = count_8 >= 6

    # Iterate through each original location containing '8' and apply reflection
    for r, c in locations_8:
        c_reflected = -1 # Initialize reflected column outside grid
        
        # Calculate reflected column based on the rule
        if reflect_right:
            # Reflect across the vertical line just to the right of max_col
            # Axis = max_col + 0.5
            # c_reflected - Axis = Axis - c
            # c_reflected = 2 * Axis - c = 2 * (max_col + 0.5) - c = 2*max_col + 1 - c
            c_reflected = (2 * max_col) + 1 - c
        else:
            # Reflect across the vertical line just to the left of min_col
            # Axis = min_col - 0.5
            # c_reflected - Axis = Axis - c
            # c_reflected = 2 * Axis - c = 2 * (min_col - 0.5) - c = 2*min_col - 1 - c
            c_reflected = (2 * min_col) - 1 - c

        # Check if the reflected column is within the grid bounds
        if 0 <= c_reflected < cols:
            # Update the output grid with the reflected '8'
            output_grid_np[r, c_reflected] = 8

    # Convert back to list of lists and return
    return output_grid_np.tolist()