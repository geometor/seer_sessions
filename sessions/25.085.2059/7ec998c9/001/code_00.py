"""
Draw blue lines connecting grid edges based on the position of a single unique pixel, 
with line direction varying based on the pixel's row parity.

1. Identify the background color (bg), the color (px_color) and location (r, c) 
   of the single unique pixel in the input grid. Determine the grid's height (H) 
   and width (W).
2. Create an output grid of the same dimensions (HxW), initially filled with the 
   background color (bg).
3. Draw the vertical blue line: For each row i from 0 to H-1, if i is not equal 
   to r, set the pixel at (i, c) in the output grid to blue (1).
4. Check if the row index r is odd or even.
5. If r is odd:
    a. Draw the top horizontal blue line: For each column j from 0 to c 
       (inclusive), set the pixel at (0, j) to blue (1).
    b. Draw the bottom horizontal blue line: For each column j from c to W-1 
       (inclusive), set the pixel at (H-1, j) to blue (1).
6. If r is even:
    a. Draw the top horizontal blue line: For each column j from c to W-1 
       (inclusive), set the pixel at (0, j) to blue (1).
    b. Draw the bottom horizontal blue line: For each column j from 0 to c 
       (inclusive), set the pixel at (H-1, j) to blue (1).
7. Place the unique pixel color (px_color) at location (r, c) in the output grid, 
   overwriting any blue line if necessary.
8. Return the completed output grid.
"""

import numpy as np
from collections import Counter

def find_unique_pixel(grid):
    """Finds the location (r, c) and color of the single unique pixel."""
    colors, counts = np.unique(grid, return_counts=True)
    
    # Background color is the most frequent
    bg_color_index = np.argmax(counts)
    bg_color = colors[bg_color_index]
    
    # Unique pixel color is the least frequent (assuming only one unique pixel)
    unique_color_index = np.argmin(counts)
    unique_color = colors[unique_color_index]

    # Find the location of the unique pixel
    locations = np.where(grid == unique_color)
    if len(locations[0]) == 1:
        r, c = locations[0][0], locations[1][0]
        return bg_color, unique_color, r, c
    else:
        # Fallback or error handling if assumption is wrong 
        # (e.g., multiple unique pixels or no unique pixel)
        # For simplicity, assume the first non-background pixel found is the unique one
        # if the unique count method fails (e.g. background is not most frequent)
        if len(colors) > 1 :
            other_color = colors[0] if colors[0] != bg_color else colors[1]
            for r_idx, row in enumerate(grid):
                for c_idx, cell in enumerate(row):
                    if cell == other_color:
                         return bg_color, other_color, r_idx, c_idx
        # If still not found, raise an error or return None
        raise ValueError("Could not reliably determine the unique pixel.")


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    input_np = np.array(input_grid, dtype=int)
    H, W = input_np.shape

    # 1. Identify background, unique pixel color, and location
    try:
        bg_color, px_color, r, c = find_unique_pixel(input_np)
    except ValueError as e:
        print(f"Error finding unique pixel: {e}")
        # Return input or an empty grid as fallback? For now, return input.
        return input_grid 

    # 2. Create output grid initialized with background color
    output_grid = np.full((H, W), bg_color, dtype=int)
    
    blue = 1 # Color code for blue

    # 3. Draw the vertical blue line (excluding row r)
    for i in range(H):
        if i != r:
            output_grid[i, c] = blue

    # 4. Check row parity and draw horizontal lines accordingly
    if r % 2 != 0: # r is odd
        # 5a. Top horizontal line: column 0 to c
        output_grid[0, 0:c+1] = blue
        # 5b. Bottom horizontal line: column c to W-1
        output_grid[H-1, c:W] = blue
    else: # r is even
        # 6a. Top horizontal line: column c to W-1
        output_grid[0, c:W] = blue
        # 6b. Bottom horizontal line: column 0 to c
        output_grid[H-1, 0:c+1] = blue

    # 7. Place the unique pixel color at (r, c)
    output_grid[r, c] = px_color

    # Convert back to list of lists if necessary, or return numpy array
    # return output_grid.tolist() 
    return output_grid
