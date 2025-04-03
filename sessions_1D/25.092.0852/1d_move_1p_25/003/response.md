```python
"""
Identifies a single contiguous horizontal block of non-white pixels within the first row of a 2D input grid.
Shifts this block one position to the right within its row.
The pixel at the original starting column of the block becomes white (0).
The pixel immediately to the right of the original ending column of the block takes the block's color,
provided this position is within the grid's width.
Assumes the input grid has at least one row and the block, if present, is in the first row.
"""

import numpy as np

def find_horizontal_block_in_row(grid_row):
    """
    Finds the first contiguous block of a non-white color in a 1D grid row.

    Args:
        grid_row: A 1D numpy array representing a single row of the grid.

    Returns:
        A tuple (color, start_index, end_index) if a block is found,
        otherwise (None, -1, -1). Returns the first block found if multiple exist.
    """
    start_index = -1
    end_index = -1
    block_color = None
    width = len(grid_row)

    for i, pixel in enumerate(grid_row):
        if pixel != 0:  # Found the start of a potential block
            if start_index == -1: # Only capture the first block encountered
                start_index = i
                block_color = pixel
                # Continue searching for the end of this specific block
                for j in range(i, width):
                    if grid_row[j] == block_color:
                        end_index = j
                    else:
                        # End of the block found (or different color)
                        break
                # Since we only care about the first block, we can break after finding it
                break # Exit the outer loop once the first block is fully identified

    return block_color, start_index, end_index

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Shifts the single horizontal non-white block in the first row of the input grid one step to the right.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    
    # Get dimensions
    if input_grid.ndim != 2 or input_grid.shape[0] == 0:
        # Handle empty or non-2D grids - return copy
        return output_grid
        
    height, width = input_grid.shape
    
    # Process the first row (based on observations)
    row_index = 0 
    
    # Find the non-white block in the target row
    block_color, start_col, end_col = find_horizontal_block_in_row(input_grid[row_index])

    # If a block was found, perform the shift within that row
    if block_color is not None:
        # Set the original start position to white
        if start_col >= 0: # Check if start_col is valid (should be if block found)
             output_grid[row_index, start_col] = 0

        # Set the position to the right of the original end position to the block color, if within bounds
        new_end_pos_col = end_col + 1
        if new_end_pos_col < width:
            output_grid[row_index, new_end_pos_col] = block_color

    # Return the modified grid
    return output_grid
```