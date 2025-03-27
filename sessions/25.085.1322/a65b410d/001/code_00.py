import numpy as np

"""
Identifies a horizontal red line (color 2) starting at column 0 in the input grid. 
Copies the input grid to the output grid.
Draws a green triangle (color 3) above the red line. For each row 'r' above the red line's row 'R', the green line extends from column 0 to column L + R - r - 1 (inclusive), where L is the length of the red line.
Draws a blue triangle (color 1) below the red line. For each row 'r' below the red line's row 'R', the blue line extends from column 0 to column L - (r - R) - 1 (inclusive), as long as the width L - (r - R) is positive.
"""

def find_red_line(grid):
    """Finds the row, starting column (assumed 0), and length of the horizontal red line."""
    red_pixels = np.where(grid == 2)
    if len(red_pixels[0]) == 0:
        # Should not happen based on examples, but handle defensively
        return -1, -1, 0 
        
    row_r = red_pixels[0][0]
    # Verify all red pixels are in the same row and start at column 0 and are contiguous
    cols = sorted(red_pixels[1])
    length_l = len(cols)
    
    # Basic validation based on observations
    if not np.all(red_pixels[0] == row_r):
         raise ValueError("Red pixels found in multiple rows.")
    if cols[0] != 0:
         raise ValueError(f"Red line does not start at column 0. Starts at {cols[0]}")
    if not all(cols[i] == i for i in range(length_l)):
        raise ValueError("Red line is not contiguous.")
        
    return row_r, 0, length_l # Return row, start_col (always 0), length

def transform(input_grid):
    """
    Applies the transformation rule: copy grid, find red line, draw green and blue triangles.
    """
    # Convert input to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape
    
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(grid)

    # Find the red line properties
    row_r, start_col_c, length_l = find_red_line(grid)

    if row_r == -1: # No red line found
        return output_grid.tolist() # Return the copy

    # --- Draw the green shape (color 3) above the red line ---
    # Iterate through rows from 0 up to (but not including) the red line's row
    for r in range(row_r):
        # Calculate the end column index (exclusive) for the green line in this row
        # Formula from NL: 0 to L + R - r - 1 inclusive. Slice endpoint is index + 1.
        end_col_green = start_col_c + length_l + row_r - r
        
        # Ensure the end column does not exceed grid boundaries
        end_col_green = min(end_col_green, width)
        
        # Draw the green line segment in the current row
        if end_col_green > start_col_c: # Check if there's anything to draw
             output_grid[r, start_col_c:end_col_green] = 3

    # --- Draw the blue shape (color 1) below the red line ---
    # Iterate through rows starting from the one below the red line
    for r in range(row_r + 1, height):
        # Calculate the width of the blue line for the current row
        # Formula from NL: width = L - (r - R)
        width_blue = length_l - (r - row_r)
        
        # If width is zero or less, stop drawing blue for this and subsequent rows
        if width_blue <= 0:
            break 
            
        # Calculate the end column index (exclusive)
        # Formula from NL: C to C + width - 1 inclusive. Slice endpoint is C + width.
        end_col_blue = start_col_c + width_blue
        
        # Ensure the end column does not exceed grid boundaries
        end_col_blue = min(end_col_blue, width)

        # Draw the blue line segment in the current row
        if end_col_blue > start_col_c: # Check if there's anything to draw
            output_grid[r, start_col_c:end_col_blue] = 1

    # Return the modified grid as a list of lists
    return output_grid.tolist()