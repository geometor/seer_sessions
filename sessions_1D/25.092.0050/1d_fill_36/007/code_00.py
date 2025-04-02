"""
Fill the horizontal segment between two identical non-white pixels found in a single-row input grid.

1. Verify that the input grid consists of exactly one row. If not, return the input grid unchanged.
2. Extract the single row from the input grid.
3. Find the column indices and colors of all non-white pixels (value > 0) in the row.
4. Check if precisely two non-white pixels were found.
5. If two were found, check if they have the identical color value.
6. If both conditions are met (exactly two non-white pixels found, and they have the same color):
    a.  Identify the shared color of these two pixels (let this be `fill_color`).
    b.  Determine the minimum column index (`start_index`) and the maximum column index (`end_index`) from the two non-white pixels.
    c.  Create a copy of the original input grid to serve as the output grid.
    d.  Access the single row within the output grid copy.
    e.  Iterate through the column indices from `start_index` to `end_index` (inclusive). For each index `i` in this range, set the pixel value at `output_grid[0][i]` to `fill_color`.
    f.  Return the modified output grid.
7. If the conditions in steps 5 or 6 are not met, return the original input grid unchanged.
"""

import numpy as np
import copy

def transform(input_grid):
    """
    Applies the fill-between transformation to a single-row grid if specific conditions are met.

    Args:
        input_grid (list): A list containing a single list representing the input grid row. 
                           Example: [[0, 0, 4, 0, 4, 0]]

    Returns:
        list: A list containing a single list representing the transformed output grid row,
              or a deep copy of the original input_grid if transformation conditions are not met.
    """
    
    # Initialize output_grid as a deep copy to handle non-transformation cases safely
    output_grid = copy.deepcopy(input_grid)

    # 1. Verify input grid structure (must be list containing exactly one list which is the row)
    if not isinstance(input_grid, list) or len(input_grid) != 1 or not isinstance(input_grid[0], list):
        # Invalid format, return the original grid copy
        return output_grid 

    # 2. Extract the single row
    input_row_list = input_grid[0]
    
    # Use numpy for efficient searching
    input_row_np = np.array(input_row_list)
    
    # 3. Find non-white pixels (indices and values)
    non_white_indices = np.where(input_row_np > 0)[0] # np.where returns a tuple, take first element (indices for dim 0)

    # 4. Check if exactly two non-white pixels were found
    if len(non_white_indices) == 2:
        idx1 = non_white_indices[0]
        idx2 = non_white_indices[1]
        color1 = input_row_np[idx1]
        color2 = input_row_np[idx2]

        # 5. Check if they have the same color value
        if color1 == color2:
            # 6. Conditions met, perform the transformation
            
            # 6a. Identify fill_color
            fill_color = color1 
            
            # 6b. Determine start and end indices
            start_index = min(idx1, idx2)
            end_index = max(idx1, idx2)

            # 6c. Output grid is already a deep copy 
            
            # 6d. Access the row list within the output grid copy
            output_row_list = output_grid[0] 

            # 6e. Iterate and fill the segment in the output row list
            for i in range(start_index, end_index + 1):
                # Basic bounds check (although indices from np.where should be valid)
                if 0 <= i < len(output_row_list):
                    output_row_list[i] = fill_color
            
            # 6f. Return the modified output grid
            return output_grid

    # 7. If conditions were not met (step 4 or 5 failed, or initial validation failed), 
    # return the unmodified deep copy of the original input grid.
    return output_grid