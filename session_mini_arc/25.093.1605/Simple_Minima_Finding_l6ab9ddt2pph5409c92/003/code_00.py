import numpy as np
import copy

"""
Transformation Rule:
1. Copy the input grid to create the output grid.
2. Find the first non-zero value (`v_first`) by scanning the input grid column by column (left to right), and within each column, row by row (top to bottom).
3. Check if the first column (index 0) of the input grid contains only zeros.
4. If the first column contains at least one non-zero value, the value to fill the first row (`fill_value`) is `v_first`.
5. If the first column contains only zeros:
    a. Get the value from the center cell (index 2, 2, assuming a 5x5 grid) - `v_center`.
    b. If `v_center` is non-zero, the `fill_value` is `v_center`.
    c. If `v_center` is zero, the `fill_value` is `v_first`.
6. If a `fill_value` was determined (i.e., the input grid contained at least one non-zero value), replace all elements in the first row (row index 0) of the output grid with the `fill_value`.
7. If the input grid contains only zeros, the output grid is identical to the input grid.
"""

def find_first_non_zero_col_major(grid):
    """
    Scans the grid column by column, then row by row, to find the first non-zero value.

    Args:
        grid: A NumPy array representing the 2D grid of integers.

    Returns:
        The first non-zero value found, or None if all values are zero or the grid is empty.
    """
    if grid.size == 0: 
        return None
        
    height, width = grid.shape
    
    # Iterate through columns first
    for j in range(width):
        # Then iterate through rows within the current column
        for i in range(height):
            if grid[i, j] != 0:
                return grid[i, j] # Return the first non-zero value found
                
    return None # Return None if no non-zero value is found

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A NumPy array representing the 2D input grid.

    Returns:
        A NumPy array representing the transformed 2D output grid.
    """
    # Ensure input is a numpy array
    input_grid_np = np.array(input_grid)

    # Handle empty input case
    if input_grid_np.size == 0:
        return input_grid_np.tolist() # Return as list if needed, or just input_grid_np

    # 1. Initialize output_grid as a deep copy of the input_grid
    output_grid = np.copy(input_grid_np)
    
    # 2. Find the first non-zero value scanning column-major
    v_first = find_first_non_zero_col_major(input_grid_np)
    
    # If no non-zero value found, return the copy
    if v_first is None:
        return output_grid.tolist() # Return original grid if all zeros

    fill_value = None
    height, width = input_grid_np.shape

    # 3. Check if the first column (index 0) contains only zeros
    first_col = input_grid_np[:, 0]
    first_col_all_zero = np.all(first_col == 0)

    # 4. Determine fill_value: If first column has non-zeros
    if not first_col_all_zero:
        fill_value = v_first
    # 5. Determine fill_value: If first column is all zeros
    else:
        # Check center value (assuming 5x5 for center at (2, 2))
        # A more general center could be (height // 2, width // 2)
        center_row, center_col = 2, 2 
        if height > center_row and width > center_col: # Check if grid is large enough for center
             v_center = input_grid_np[center_row, center_col]
             if v_center != 0:
                 fill_value = v_center # Use center value if non-zero
             else:
                 fill_value = v_first # Otherwise, use the first non-zero found
        else: # Grid too small for defined center, fallback to v_first
             fill_value = v_first
             
    # 6. Modify the first row of the output grid if a fill_value was determined
    if fill_value is not None:
        output_grid[0, :] = fill_value
            
    # Return the modified output grid
    return output_grid.tolist() # Convert back to list of lists if required by the environment
