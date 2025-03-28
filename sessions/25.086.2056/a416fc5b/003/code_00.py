import numpy as np

"""
Transformation Rule Natural Language Program:

1.  **Analyze Grid Structure:** Examine the input 11x11 grid. Identify the nine 3x3 subgrids defined by the magenta (6) lines at rows 3, 7 and columns 3, 7. The subgrids start at coordinates (0,0), (0,4), (0,8), (4,0), (4,4), (4,8), (8,0), (8,4), and (8,8), corresponding to indices 0 through 8 respectively.
2.  **Identify Red Plus Shapes:** Scan each of the nine 3x3 subgrids. Locate all subgrids that exactly match the "Red Plus" pattern: `[[7, 2, 7], [2, 7, 2], [7, 2, 7]]`.
3.  **Count and Record Locations:** Count the total number of Red Plus shapes found (`N`). Record the indices (0-8) of the subgrids containing these shapes in a set (`R_set`).
4.  **Apply Transformation Rules:**
    a.  **Case 1:** If `N` equals 2 AND `R_set` is exactly `{4, 7}`:
        i.  Create a copy of the input 11x11 grid.
        ii. Modify the subgrid at index 0 (coordinates 0,0) by replacing its content with the "Gray Plus" pattern: `[[7, 5, 7], [5, 7, 5], [7, 5, 7]]`.
        iii.Modify the subgrid at index 2 (coordinates 0,8) by replacing its content with the "Azure Plus" pattern: `[[7, 8, 7], [8, 7, 8], [7, 8, 7]]`.
        iv. Return the modified 11x11 grid.
    b.  **Case 2:** If `N` equals 2 AND `R_set` is exactly `{2, 4}`:
        i.  Create a copy of the input 11x11 grid.
        ii. Modify the subgrid at index 3 (coordinates 4,0) by replacing its content with the "Azure Plus" pattern: `[[7, 8, 7], [8, 7, 8], [7, 8, 7]]`.
        iii.Modify the subgrid at index 7 (coordinates 8,4) by replacing its content with the "Gray Plus" pattern: `[[7, 5, 7], [5, 7, 5], [7, 5, 7]]`.
        iv. Return the modified 11x11 grid.
    c.  **Default Case:** If neither Case 1 nor Case 2 applies (i.e., if `N` is not equal to 2, OR if `N` equals 2 but `R_set` is neither `{4, 7}` nor `{2, 4}`):
        i.  Construct a new 16x16 grid.
        ii. Fill this entire grid with the color orange (7).
        iii.Return the 16x16 orange grid.
"""

def get_subgrid(grid, row, col):
    """Extracts the 3x3 subgrid starting at (row, col)."""
    return grid[row:row+3, col:col+3]

def set_subgrid(grid, row, col, pattern):
    """Places the 3x3 pattern into the grid starting at (row, col)."""
    grid[row:row+3, col:col+3] = pattern

def is_red_plus(subgrid):
    """Checks if a 3x3 subgrid matches the red plus pattern."""
    red_plus_pattern = np.array([[7, 2, 7], [2, 7, 2], [7, 2, 7]])
    return np.array_equal(subgrid, red_plus_pattern)

def transform(input_grid):
    # Convert input list of lists to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape

    # Define the coordinates for the top-left corner of each 3x3 subgrid
    subgrid_coords = [
        (0, 0), (0, 4), (0, 8),  # Indices 0, 1, 2
        (4, 0), (4, 4), (4, 8),  # Indices 3, 4, 5
        (8, 0), (8, 4), (8, 8)   # Indices 6, 7, 8
    ]

    # Define the modification patterns
    gray_pattern = np.array([[7, 5, 7], [5, 7, 5], [7, 5, 7]])
    azure_pattern = np.array([[7, 8, 7], [8, 7, 8], [7, 8, 7]])

    # Identify red plus shapes and their subgrid indices
    red_plus_indices = []
    for i, (r, c) in enumerate(subgrid_coords):
        # Ensure coordinates are within bounds (expects 11x11)
        if r + 3 <= rows and c + 3 <= cols:
            subgrid = get_subgrid(input_np, r, c)
            if is_red_plus(subgrid):
                red_plus_indices.append(i)

    # Get the count (N) and the set of indices (R_set)
    num_red_plus_shapes = len(red_plus_indices)
    red_plus_set = set(red_plus_indices)

    # Apply transformation rules based on N and R_set
    if num_red_plus_shapes == 2:
        if red_plus_set == {4, 7}:
            # Case 1: Modify subgrids 0 and 2
            output_grid = input_np.copy()
            set_subgrid(output_grid, subgrid_coords[0][0], subgrid_coords[0][1], gray_pattern) # Index 0
            set_subgrid(output_grid, subgrid_coords[2][0], subgrid_coords[2][1], azure_pattern) # Index 2
            return output_grid.tolist() # Return as list of lists

        elif red_plus_set == {2, 4}:
            # Case 2: Modify subgrids 3 and 7
            output_grid = input_np.copy()
            set_subgrid(output_grid, subgrid_coords[3][0], subgrid_coords[3][1], azure_pattern) # Index 3
            set_subgrid(output_grid, subgrid_coords[7][0], subgrid_coords[7][1], gray_pattern)  # Index 7
            return output_grid.tolist() # Return as list of lists
        
        else:
            # Default Case (N=2, but not the specified sets)
            output_grid = np.full((16, 16), 7, dtype=int)
            return output_grid.tolist() # Return as list of lists
    else:
        # Default Case (N != 2)
        output_grid = np.full((16, 16), 7, dtype=int)
        return output_grid.tolist() # Return as list of lists
