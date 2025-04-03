import numpy as np

"""
Identifies a contiguous segment of non-background (non-zero) pixels in a single-row grid.
Determines the color of the pixel at the start of this segment (the boundary color).
Fills the entire segment in the output grid with this boundary color, leaving the background pixels unchanged.
Assumes the input grid is always a single row.
"""

def transform(input_grid_list):
    """
    Transforms the input grid according to the identified rule.

    Args:
        input_grid_list: A list representing the single-row input grid.

    Returns:
        A numpy array representing the transformed grid.
    """
    # Convert list to numpy array for easier manipulation
    input_grid = np.array(input_grid_list, dtype=int)
    
    # Ensure it's treated as a 2D array even if it's 1xN
    if input_grid.ndim == 1:
        input_grid = input_grid.reshape(1, -1)
        
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    
    # --- Workflow ---
    
    # 1. Identify the row (assuming only one row based on examples)
    #    For multi-row grids, this logic might need adjustment or iteration.
    #    Here, we assume row_index is always 0.
    row_index = 0
    row = input_grid[row_index, :]

    # 2. Find the indices of non-zero pixels in the row
    non_zero_indices = np.where(row != 0)[0]

    # 3. If there are no non-zero pixels, the grid is all background; return the copy.
    if len(non_zero_indices) == 0:
        return output_grid

    # 4. Find the start and end indices of the contiguous non-zero segment
    start_index = np.min(non_zero_indices)
    end_index = np.max(non_zero_indices)

    # 5. Identify the boundary color (color at the start of the segment)
    fill_color = input_grid[row_index, start_index]

    # 6. Fill the segment in the output grid with the boundary color
    output_grid[row_index, start_index : end_index + 1] = fill_color

    # --- End Workflow ---

    return output_grid
