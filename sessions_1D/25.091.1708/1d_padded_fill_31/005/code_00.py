import numpy as np

"""
Processes a 2D grid row by row. For each row containing non-white pixels:
1. Finds the column index of the first (leftmost) non-white pixel ('start_col').
2. Determines the overall maximum column index containing a non-white pixel across the entire grid ('global_max_end_col').
3. Determines the 'effective_end_col' for the current row:
    - If the input pixel at [row, global_max_end_col] is non-white, effective_end_col = global_max_end_col.
    - If the input pixel at [row, global_max_end_col] is white, effective_end_col = global_max_end_col - 1.
    - Ensures effective_end_col is at least start_col.
4. Fills the segment in the output grid's row from 'start_col' to 'effective_end_col' (inclusive) with the color of the first non-white pixel found in that row.
Rows containing only white pixels remain unchanged.
"""

def transform(input_grid):
    """
    Transforms the input grid based on the row-wise filling rule.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input to numpy array for efficient operations
    input_np = np.array(input_grid, dtype=int)
    # Initialize output grid as a copy of the input
    output_grid = input_np.copy()
    rows, cols = input_np.shape

    # 1. Find the global maximum end column index with a non-white pixel
    # np.argwhere returns coordinates [row, col] for non-zero elements
    non_white_coords = np.argwhere(input_np != 0)
    
    # Handle grid with no non-white pixels (all white)
    if non_white_coords.size == 0:
        # No transformation needed, return a copy as list of lists
        return output_grid.tolist() 

    # Find the maximum column index among all non-white pixels
    global_max_end_col = non_white_coords[:, 1].max()

    # 3. Process Each Row independently
    for r in range(rows):
        # 4. Find Non-White Pixels in the current input row
        # np.where returns indices where the condition is true
        row_non_white_indices = np.where(input_np[r, :] != 0)[0]

        # 5. Check if Row Needs Processing (skip if all white)
        if row_non_white_indices.size > 0:
            # a. Get Start Column: the first index found
            start_col = row_non_white_indices[0]
            # b. Get Fill Color: the color at the starting column
            fill_color = input_np[r, start_col]

            # c. Determine Effective End Column for this row's fill operation
            # Default assumption: fill up to the global max end column
            effective_end_col = global_max_end_col 
            
            # Condition: If the pixel at the global max end column *in this specific row's input* was originally white (0),
            # then the filling for this row should stop one column earlier.
            if input_np[r, global_max_end_col] == 0:
                effective_end_col = global_max_end_col - 1

            # d. Handle Edge Case: Ensure the fill range is valid (end >= start)
            # This covers cases where start_col == global_max_end_col and input was white there,
            # resulting in effective_end_col becoming start_col - 1. We reset it to start_col
            # so the fill operation correctly colors at least the start_col pixel.
            # It also handles the case where global_max_end_col might be 0 and input[r,0] was white.
            if effective_end_col < start_col:
                effective_end_col = start_col

            # e. Fill Pixels in the output grid for the current row
            # Numpy slicing `[start : end + 1]` includes the index 'end'.
            output_grid[r, start_col : effective_end_col + 1] = fill_color

    # 6. Return Output grid, converted back to list of lists format
    return output_grid.tolist()