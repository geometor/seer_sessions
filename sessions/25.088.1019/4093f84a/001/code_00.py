import numpy as np

"""
Transformation Rule Natural Language Description:

1. Initialize the output grid as a copy of the input grid.
2. Identify the horizontal band of gray (5) pixels. Determine the row index of the top edge of this band. The top edge is defined as the first row (from top to bottom) that contains at least one gray pixel.
3. Iterate through each column of the input grid.
4. For the current column, scan the rows *above* the top edge of the gray band. Check if any pixel in this upper section of the column has an "active" color: blue (1), red (2), or green (3).
5. If such an active colored pixel is found in the current column above the gray band:
    a. Locate the pixel in the output grid that is in the same column and in the row immediately *above* the top edge of the gray band (if such a row exists, i.e., if the band doesn't start at row 0).
    b. Change the color of this specific pixel in the output grid to gray (5).
6. After checking all columns and potentially modifying pixels above the band, iterate through the entire output grid. Change any pixel that still has an active color (blue (1), red (2), or green (3)) to white (0).
7. The resulting grid is the final output.
"""

def find_band_top_row(grid):
    """
    Finds the index of the first row containing a gray (5) pixel.
    Returns the row index or -1 if no gray pixel is found.
    """
    height, width = grid.shape
    for r in range(height):
        for c in range(width):
            if grid[r, c] == 5:
                return r
    return -1 # Should not happen based on examples

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    - Finds the top of the gray band.
    - Identifies columns with active colors (1, 2, 3) above the band.
    - Colors the cell immediately above the band gray in those columns.
    - Replaces all active colors (1, 2, 3) with white (0).
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    output_np = np.copy(input_np)
    height, width = input_np.shape
    
    active_colors = {1, 2, 3} # Blue, Red, Green

    # 1. Find the top row of the gray band
    band_top_row = find_band_top_row(input_np)

    # If no gray band found, return the original grid (or handle as error)
    # Based on examples, a band is always present.
    if band_top_row == -1:
        print("Warning: No gray band found.")
        # Decide behavior: return copy or original? Let's return copy.
        # Also remove active colors as per step 6? Yes.
        for r in range(height):
             for c in range(width):
                 if output_np[r, c] in active_colors:
                     output_np[r, c] = 0
        return output_np.tolist()


    # 2. Identify columns with active colors above the band
    columns_to_modify = set()
    if band_top_row > 0: # Only check if there are rows above the band
        for c in range(width):
            for r in range(band_top_row): # Iterate rows *above* the band
                if input_np[r, c] in active_colors:
                    columns_to_modify.add(c)
                    break # Found one in this column, move to the next column

    # 3. Modify the pixels immediately above the band in identified columns
    if band_top_row > 0: # Ensure there is a row above the band
        target_row = band_top_row - 1
        for c in columns_to_modify:
             # Check if the target cell is within grid bounds (already guaranteed by band_top_row > 0)
            output_np[target_row, c] = 5 # Change to gray

    # 4. Remove all original active colors (replace with white)
    for r in range(height):
        for c in range(width):
            if output_np[r, c] in active_colors:
                output_np[r, c] = 0 # Change to white

    # Convert the result back to a list of lists
    return output_np.tolist()