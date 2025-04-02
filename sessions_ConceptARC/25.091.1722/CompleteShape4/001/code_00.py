import numpy as np

"""
Identify two parallel lines (horizontal or vertical) of the same non-white color in the input grid. 
Replace them with two parallel lines of the same color but rotated 90 degrees. 
The span of the new lines is adjusted inwards by one unit relative to the original lines' boundaries.
For example, if the input has horizontal lines from column C1 to C2 at rows R1 and R2, 
the output will have vertical lines from row R1+1 to R2-1 at columns C1 and C2. 
Conversely, if the input has vertical lines from row R1 to R2 at columns C1 and C2, 
the output will have horizontal lines from column C1+1 to C2-1 at rows R1 and R2.
"""

def find_colored_pixels(grid):
    """Finds the coordinates and color of all non-white pixels."""
    rows, cols = np.where(grid != 0)
    if len(rows) == 0:
        return None, None, None # No colored pixels found
    color = grid[rows[0], cols[0]]
    # Verify all colored pixels have the same color
    for r, c in zip(rows, cols):
        if grid[r, c] != color:
            # This case shouldn't happen based on examples, but good to check
            return None, None, None 
    coords = list(zip(rows, cols))
    return coords, color, (grid.shape[0], grid.shape[1])

def transform(input_grid):
    """
    Transforms the input grid by rotating the two parallel lines by 90 degrees 
    and adjusting their span inwards.
    """
    input_grid_np = np.array(input_grid)
    height, width = input_grid_np.shape

    # Find all non-white pixels, their color, and grid dimensions
    coords, color, dims = find_colored_pixels(input_grid_np)

    if coords is None:
        # Handle cases with no colored pixels or inconsistent colors if needed
        # For this problem, assume valid input as per examples
        return input_grid # Or return an empty grid of same size

    # Separate row and column indices
    rows = sorted(list(set(r for r, c in coords)))
    cols = sorted(list(set(c for r, c in coords)))

    # Initialize the output grid with white (0)
    output_grid = np.zeros_like(input_grid_np)

    # Determine orientation and boundaries
    if len(rows) == 2 and len(cols) > 1: # Horizontal lines in input
        r1, r2 = rows[0], rows[1]
        c1, c2 = cols[0], cols[-1]
        # Draw vertical lines in output, adjusted inwards
        # Ensure indices stay within bounds after adjustment
        start_row = r1 + 1
        end_row = r2 - 1
        if start_row <= end_row: # Check if the lines have non-zero length after adjustment
            output_grid[start_row : end_row + 1, c1] = color
            output_grid[start_row : end_row + 1, c2] = color

    elif len(cols) == 2 and len(rows) > 1: # Vertical lines in input
        c1, c2 = cols[0], cols[1]
        r1, r2 = rows[0], rows[-1]
        # Draw horizontal lines in output, adjusted inwards
        # Ensure indices stay within bounds after adjustment
        start_col = c1 + 1
        end_col = c2 - 1
        if start_col <= end_col: # Check if the lines have non-zero length after adjustment
            output_grid[r1, start_col : end_col + 1] = color
            output_grid[r2, start_col : end_col + 1] = color
            
    # If neither case matches, return the empty grid (or handle as an error/edge case)
    # Based on provided examples, one of the above conditions should always be met.

    return output_grid.tolist()