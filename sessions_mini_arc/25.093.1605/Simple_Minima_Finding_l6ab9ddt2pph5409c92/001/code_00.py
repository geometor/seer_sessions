import copy

"""
Transformation Rule:
1. Copy the input grid to create the output grid.
2. Scan the input grid column by column, from left to right. Within each column, scan row by row, from top to bottom.
3. Find the first non-zero value encountered during this scan. This value becomes the 'fill_value'.
4. Replace all elements in the first row (row index 0) of the output grid with the 'fill_value'.
5. If no non-zero value is found in the input grid, the output grid remains identical to the input grid (specifically, the first row remains unchanged).
"""

def find_first_non_zero_column_major(grid):
    """
    Scans the grid column by column, then row by row, to find the first non-zero value.

    Args:
        grid: A list of lists representing the 2D grid of integers.

    Returns:
        The first non-zero value found, or None if all values are zero or the grid is empty.
    """
    if not grid or not grid[0]: # Check for empty grid or grid with empty rows
        return None
        
    height = len(grid)
    width = len(grid[0])
    
    # Iterate through columns first
    for j in range(width):
        # Then iterate through rows within the current column
        for i in range(height):
            if grid[i][j] != 0:
                return grid[i][j] # Return the first non-zero value found
                
    return None # Return None if no non-zero value is found

def transform(input_grid):
    """
    Applies the transformation rule: copies the grid, finds the first non-zero
    value scanning column-major, and fills the first row of the output grid
    with that value.

    Args:
        input_grid: A list of lists representing the 2D input grid of integers.

    Returns:
        A list of lists representing the 2D output grid.
    """
    # Handle empty input case
    if not input_grid or not input_grid[0]:
        return []
        
    # 1. Initialize output_grid as a deep copy of the input_grid
    #    This preserves rows 1 onwards automatically.
    output_grid = copy.deepcopy(input_grid)
    
    # 2. Determine the fill_value by scanning the input grid
    fill_value = find_first_non_zero_column_major(input_grid)
    
    # 3. Modify the first row of the output grid if a non-zero fill_value was found
    if fill_value is not None:
        width = len(output_grid[0])
        # Iterate through the columns of the first row
        for j in range(width):
            output_grid[0][j] = fill_value
            
    # 4. Return the modified output grid
    return output_grid
