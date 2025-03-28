import numpy as np

"""
Transforms the input grid based on the vertical position and horizontal alignment of the non-background pattern.

1.  Analyze the Input Grid: Check if the input grid contains any non-background pixels (pixels with value != 0).
    - If no non-background pixels exist, return the input grid unchanged.
2.  Identify Pattern Position: Determine the minimum row index (`min_r`) and minimum column index (`min_c`) containing any non-background pixel.
3.  Apply Conditional Transformation:
    - Case 1: Pattern does not touch the top edge (`min_r > 0`)
        a. Find the maximum row index (`max_r`) containing a non-background pixel.
        b. Calculate the height of the pattern's row span: `h = max_r - min_r + 1`.
        c. Extract the block of rows from the input grid spanning `min_r` to `max_r` (inclusive).
        d. Create a new block by vertically flipping the extracted block.
        e. Create the output grid as a copy of the input grid.
        f. Replace the top `h` rows of the output grid (rows 0 to `h-1`) with the flipped block.
    - Case 2: Pattern touches the top edge (`min_r == 0`)
        a. Check if the pattern is already aligned to the left edge (`min_c == 0`). If yes, return the input grid unchanged.
        b. If not left-aligned (`min_c > 0`), create a new output grid of the same dimensions as the input, filled entirely with the background color (0).
        c. Iterate through each pixel `(r, c)` of the input grid. If the input pixel `input[r, c]` is not the background color, copy its value to the output grid at position `(r, c - min_c)`. This effectively shifts the entire pattern left by `min_c` columns.
4.  Return the Output Grid: Return the resulting transformed grid.
"""

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape
    background_pixel = 0

    # Find indices of non-background pixels
    non_bg_coords = np.argwhere(grid != background_pixel)

    # 1. Handle empty grid case
    if non_bg_coords.size == 0:
        return input_grid

    # 2. Identify Pattern Position
    min_r = non_bg_coords[:, 0].min()
    max_r = non_bg_coords[:, 0].max()
    min_c = non_bg_coords[:, 1].min()

    # 3. Apply Conditional Transformation
    
    # Case 1: Pattern does not touch the top edge (min_r > 0)
    if min_r > 0:
        # a. max_r already calculated
        # b. Calculate row span height
        block_height = max_r - min_r + 1
        
        # c. Extract the block of rows
        pattern_block = grid[min_r : max_r + 1, :]
        
        # d. Vertically flip the extracted block
        reversed_block = pattern_block[::-1, :]
        
        # e. Create output grid as a copy
        output_grid = grid.copy()
        
        # f. Replace the top 'block_height' rows with the flipped block
        # Ensure we don't try to write past the grid boundary
        rows_to_overwrite = min(block_height, height)
        output_grid[0:rows_to_overwrite, :] = reversed_block[:rows_to_overwrite, :] # Slice reversed_block too in case it's taller than grid

    # Case 2: Pattern touches the top edge (min_r == 0)
    else: # min_r == 0
        # a. Check if already left-aligned
        if min_c == 0:
            # Pattern touches top and left, return unchanged
            output_grid = grid
        else: # min_c > 0
            # b. Create a new output grid filled with background color
            output_grid = np.full_like(grid, background_pixel)
            
            # c. Shift the pattern left by min_c columns
            for r, c in non_bg_coords:
                 # Check boundary just in case, though c >= min_c should hold
                if c - min_c >= 0:
                   output_grid[r, c - min_c] = grid[r, c]

    # 4. Return the Output Grid
    return output_grid.tolist()