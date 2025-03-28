import numpy as np

"""
Transforms the input grid according to the following rules:
1. Create a copy of the input grid to serve as the output grid.
2. Identify the single "main color" (C), which is the color present in the input grid other than white (0) and gray (5).
3. Locate the coordinates (gr, gc) of the top-leftmost gray (5) pixel (minimum row, then minimum column).
4. Locate the coordinates (mr, mc) of the top-leftmost main color (C) pixel (minimum row, then minimum column).
5. In the output grid, change all pixels with the gray color (5) to white (0).
6. Determine the starting coordinates (sr, sc) for a new diagonal line:
   - If the column index of the top-leftmost gray pixel (`gc`) is greater than the column index of the top-leftmost main color pixel (`mc`), then the start point is (0, gc).
   - Otherwise (if `gc` is less than or equal to `mc`), the start point is (gr, 0).
7. Draw a diagonal line starting from the calculated coordinates (sr, sc). This line uses the main color (C) and extends downwards and to the right (incrementing both row and column indices by 1 at each step) until it goes beyond the grid boundaries. Set the pixels along this path in the output grid to the main color (C), overwriting any previous color at those locations.
8. Return the modified output grid.
"""

def find_top_leftmost_pixel(grid, color):
    """
    Finds the (row, col) coordinates of the top-leftmost pixel of a given color.
    Searches row by row, then column by column within the first row containing the color.
    Returns None if the color is not found.
    """
    rows, cols = np.where(grid == color)
    if len(rows) == 0:
        return None  # Color not found
    min_row = np.min(rows)
    # Find the minimum column index among pixels in the minimum row
    min_col_in_min_row = np.min(cols[rows == min_row])
    return (int(min_row), int(min_col_in_min_row)) # Cast to int for consistency

def identify_main_color(grid):
    """
    Identifies the main color in the grid, excluding white (0) and gray (5).
    Assumes there is exactly one such color based on the task examples.
    Returns the main color value, or None if none is found.
    """
    unique_colors = np.unique(grid)
    for color in unique_colors:
        if color != 0 and color != 5:
            return color
    return None # Should not happen based on examples

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    
    # Step 1: Initialize output_grid as a copy of the input
    output_np = np.copy(input_np)

    # Step 2: Identify the main color (C)
    main_color = identify_main_color(input_np)
    # If no main color other than 0 or 5 is found, handle gracefully (though not expected)
    # Based on analysis, gray pixels are removed even if main/gray pixels are missing
    if main_color is None:
        output_np[output_np == 5] = 0
        return output_np.tolist() 

    # Step 3: Locate the top-leftmost gray (5) pixel
    gray_coords = find_top_leftmost_pixel(input_np, 5)
    
    # Step 4: Locate the top-leftmost main color (C) pixel
    main_coords = find_top_leftmost_pixel(input_np, main_color)

    # Step 5: Change all gray (5) pixels to white (0) in the output grid *before* drawing the line
    output_np[output_np == 5] = 0

    # If either gray or main color pixels are missing (not expected based on examples),
    # return the grid after removing gray.
    if gray_coords is None or main_coords is None:
        return output_np.tolist()

    gr, gc = gray_coords
    mr, mc = main_coords

    # Step 6: Determine the starting coordinates (sr, sc) for the new diagonal line
    if gc > mc:
        # Case 1: Gray column is further right than main color column
        sr, sc = 0, gc
    else: # gc <= mc
        # Case 2: Gray column is not further right than main color column
        sr, sc = gr, 0
        
    # Step 7: Draw the diagonal line starting from (sr, sc) using the main color C
    r, c = sr, sc
    while 0 <= r < height and 0 <= c < width:
        # Set the pixel at the current position to the main color
        output_np[r, c] = main_color
        # Move down and right for the next pixel
        r += 1
        c += 1

    # Step 8: Convert the final numpy array back to a list of lists before returning
    return output_np.tolist()