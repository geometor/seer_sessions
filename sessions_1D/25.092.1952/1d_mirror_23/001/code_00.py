import numpy as np

"""
Reflects a horizontal colored block across a fixed maroon pivot pixel in a 1D grid.

1. Create a new output grid with the same dimensions as the input grid, filled entirely with the background color (white, 0).
2. Find the column index of the single maroon pixel (color 9) in the input grid. Let this be `pivot_col`.
3. Place the maroon pixel (color 9) at `pivot_col` in the output grid.
4. Find the contiguous horizontal block of pixels in the input grid that are not white (0) and not maroon (9). Record its color (`block_color`), its starting column index (`start_col`), and its ending column index (`end_col`).
5. Calculate the starting column index for the block in the output grid: `new_start_col = pivot_col + (pivot_col - end_col)`.
6. Calculate the ending column index for the block in the output grid: `new_end_col = pivot_col + (pivot_col - start_col)`.
7. Fill the pixels in the output grid from `new_start_col` to `new_end_col` (inclusive) with `block_color`.
8. Return the completed output grid.
"""

# Define constants for colors
BACKGROUND_COLOR = 0
PIVOT_COLOR = 9

def find_pivot(grid_row):
    """Finds the column index of the pivot pixel (color 9)."""
    for col, color in enumerate(grid_row):
        if color == PIVOT_COLOR:
            return col
    return -1 # Should not happen based on examples

def find_block(grid_row):
    """Finds the color, start index, and end index of the contiguous colored block."""
    start_col = -1
    end_col = -1
    block_color = -1
    in_block = False
    for col, color in enumerate(grid_row):
        if color != BACKGROUND_COLOR and color != PIVOT_COLOR:
            if not in_block:
                start_col = col
                block_color = color
                in_block = True
            end_col = col # Keep updating end_col while in the block
        elif in_block:
            # We just exited the block
            break
    return block_color, start_col, end_col


def transform(input_grid):
    """
    Transforms the input grid by reflecting the colored block across the pivot pixel.
    """
    # Convert input to numpy array for easier handling, assuming 1xN grid
    input_np = np.array(input_grid, dtype=int)
    if input_np.ndim == 1: # Handle flat list input
        input_np = input_np.reshape(1, -1)
        
    rows, cols = input_np.shape
    
    # Initialize output grid with background color
    output_grid = np.full_like(input_np, BACKGROUND_COLOR)
    
    # Since it's a 1xN grid, we operate on the first (and only) row
    input_row = input_np[0]
    output_row = output_grid[0]

    # Find the pivot pixel location
    pivot_col = find_pivot(input_row)
    if pivot_col == -1:
        # Handle error or unexpected input: no pivot found
        return output_grid.tolist() # Return empty grid or original? Returning empty for now.

    # Place the pivot in the output grid
    output_row[pivot_col] = PIVOT_COLOR

    # Find the colored block details
    block_color, start_col, end_col = find_block(input_row)
    
    if block_color == -1:
        # Handle error or unexpected input: no block found
        return output_grid.tolist() # Return grid with only pivot

    # Calculate the new position of the block by reflection
    # The distance from the pivot to the start of the new block equals the distance from the end of the old block to the pivot.
    # new_start - pivot = pivot - old_end  => new_start = 2 * pivot - old_end
    # The distance from the pivot to the end of the new block equals the distance from the start of the old block to the pivot.
    # new_end - pivot = pivot - old_start  => new_end = 2 * pivot - old_start
    # Adjusting the formula slightly for clarity and direct mapping:
    # distance_end_to_pivot = pivot_col - end_col
    # distance_start_to_pivot = pivot_col - start_col
    # new_start_col = pivot_col + distance_end_to_pivot
    # new_end_col = pivot_col + distance_start_to_pivot
    
    new_start_col = pivot_col + (pivot_col - end_col)
    new_end_col = pivot_col + (pivot_col - start_col)

    # Ensure indices are within bounds (although examples suggest they will be)
    new_start_col = max(0, new_start_col)
    new_end_col = min(cols - 1, new_end_col)

    # Place the reflected block in the output grid
    # Ensure start <= end; if reflection flips order, swap them (though unlikely here)
    if new_start_col <= new_end_col:
        output_row[new_start_col : new_end_col + 1] = block_color
    else: # If reflection resulted in flipped indices (e.g., block crosses pivot)
         output_row[new_end_col : new_start_col + 1] = block_color


    # Return the modified grid as a list of lists
    return output_grid.tolist()