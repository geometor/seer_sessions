import numpy as np

def find_separator_row(grid):
    """Finds the row index of the horizontal gray (5) separator line."""
    h, w = grid.shape
    for r in range(h):
        if np.all(grid[r, :] == 5):
            return r
    return -1 # Should not happen based on examples

def find_color_above(grid, r_start, c, separator_row):
    """
    Searches upwards from just above the separator in a given column 
    to find the first non-white(0), non-gray(5) color.
    """
    for search_r in range(separator_row - 1, -1, -1): # Search from separator_row-1 up to 0
        color = grid[search_r, c]
        if color != 0 and color != 5:
            return color
    return -1 # Return -1 if no suitable color is found above

def transform(input_grid):
    """
    Transforms the input grid based on the following rule:
    1. Identify the horizontal gray (5) separator line.
    2. Keep the part of the grid above and including the separator line unchanged.
    3. For each green (3) pixel below the separator line:
       a. Look upwards in the same column, starting from the row just above the separator.
       b. Find the first non-white (0) and non-gray (5) pixel encountered during this upward search.
       c. Change the color of the green (3) pixel to the color found in step b.
       d. If no such color is found above (e.g., the column above the separator is all white or gray), 
          the green pixel remains unchanged (though this case might not occur based on examples).
    4. All other pixels below the separator line remain unchanged.
    """
    
    # Convert input_grid list of lists to numpy array if necessary
    input_grid_np = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input
    output_grid = input_grid_np.copy()
    
    h, w = output_grid.shape
    
    # Find the separator row
    separator_row = find_separator_row(output_grid)
    
    # If no separator is found, return the original grid (or handle error)
    if separator_row == -1:
        # Based on examples, a separator always exists. 
        # If it might not, add error handling or return copy.
        return output_grid 

    # Iterate through rows below the separator
    for r in range(separator_row + 1, h):
        # Iterate through columns
        for c in range(w):
            # Check if the current pixel is green (3)
            if output_grid[r, c] == 3:
                # Find the color in the column above the separator
                color_above = find_color_above(input_grid_np, r, c, separator_row)
                
                # If a valid color was found above, change the green pixel
                if color_above != -1:
                    output_grid[r, c] = color_above
                # Else: keep the original green color (output_grid[r, c] already holds 3)

    return output_grid.tolist() # Convert back to list of lists if required by framework
