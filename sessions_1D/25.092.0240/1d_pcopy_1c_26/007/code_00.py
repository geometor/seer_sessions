import numpy as np

"""
Transforms the input grid based on a rule involving horizontally isolated pixels and a row offset based on column position.

1. Identify all non-white pixels (value > 0) in the input grid.
2. Filter these pixels to find those that are "horizontally isolated": their immediate left neighbor is white (or it's the first column) AND their immediate right neighbor is white (or it's the last column).
3. Further filter these horizontally isolated pixels: only consider those that are *not* located in the first row (row index 0). These are the "trigger pixels".
4. For each trigger pixel found at position (r, c) with color C:
    a. Determine the target row index (r_target) to modify in the output grid.
    b. The target row is r_target = r + 1 if the trigger pixel is in the last column (c == width - 1).
    c. Otherwise (if the trigger pixel is not in the last column), the target row is r_target = r.
    d. Record the target row and the color C. If multiple triggers target the same row, the color of the last processed trigger for that row will be used (consistent with example logic where colors seem unique per target row or the rule implies which one matters).
5. Initialize the output grid as a copy of the input grid.
6. For every recorded target row and its corresponding color, fill the entire target row in the output grid with that color, ensuring the target row index is within the grid's bounds.
7. Rows without a corresponding trigger pixel remain unchanged from the input.
"""

def is_horizontally_isolated(grid, r, c):
    """Checks if the pixel at (r, c) is horizontally isolated."""
    rows, cols = grid.shape
    pixel_color = grid[r, c]
    
    # Pixel must be non-white
    if pixel_color == 0:
        return False
        
    # Check left neighbor (handles first column case c=0)
    left_is_white = (c == 0) or (grid[r, c-1] == 0)
    
    # Check right neighbor (handles last column case c=cols-1)
    right_is_white = (c == cols - 1) or (grid[r, c+1] == 0)
    
    return left_is_white and right_is_white

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    
    Args:
        input_grid (list of lists): The input grid represented as a 2D list.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input list of lists to a NumPy array for easier processing
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape
    last_col_index = cols - 1

    # Initialize the output grid as a copy of the input
    output_np = np.copy(input_np)

    # Dictionary to store which target rows need modification and with which color
    # {target_row_index: fill_color}
    rows_to_fill = {} 

    # Iterate through each pixel of the input grid, skipping row 0
    for r in range(1, rows):
        for c in range(cols):
            # Check if the pixel is non-white and horizontally isolated
            if input_np[r, c] != 0 and is_horizontally_isolated(input_np, r, c):
                # This is a trigger pixel (non-white, horizontally isolated, not in row 0)
                pixel_color = input_np[r, c]
                
                # Determine the target row based on the column index
                if c == last_col_index:
                    target_row = r + 1
                else:
                    target_row = r
                    
                # Store the instruction to fill the target row with this color
                # If multiple triggers target the same row, the last one processed will determine the color
                rows_to_fill[target_row] = pixel_color

    # Apply the modifications to the output grid based on found triggers
    for target_row, fill_color in rows_to_fill.items():
        # Ensure the target row is within the grid bounds before filling
        if 0 <= target_row < rows:
            output_np[target_row, :] = fill_color

    # Convert the final NumPy array back to a list of lists
    output_grid = output_np.tolist()
    
    return output_grid