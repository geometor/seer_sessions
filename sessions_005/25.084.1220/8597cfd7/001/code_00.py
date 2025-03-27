"""
Identifies a horizontal gray divider line in the input grid. 
Counts the number of red (2) and yellow (4) pixels in the region below the divider.
If the count of red pixels is greater than or equal to the count of yellow pixels, 
the output is a 2x2 grid filled with red (2). Otherwise, the output is a 2x2 grid 
filled with yellow (4).
"""

import numpy as np

def find_divider_row(grid):
    """Finds the index of the horizontal gray divider line."""
    for r_idx, row in enumerate(grid):
        if all(pixel == 5 for pixel in row):
            return r_idx
    return -1 # Should not happen based on examples

def count_colors_below_divider(grid, divider_row_idx, color_val):
    """Counts the occurrences of a specific color below the divider row."""
    count = 0
    height, width = grid.shape
    # Start counting from the row immediately below the divider
    for r in range(divider_row_idx + 1, height):
        for c in range(width):
            if grid[r, c] == color_val:
                count += 1
    return count

def transform(input_grid):
    """
    Transforms the input grid based on the count of red and yellow pixels 
    below the gray divider line.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    
    # 1. Identify the horizontal line composed entirely of gray pixels (color 5).
    divider_row_idx = find_divider_row(input_np)
    
    if divider_row_idx == -1:
        # Handle cases where no divider is found, although examples suggest one always exists.
        # For now, return an empty or default grid, but this might need adjustment.
        return np.zeros((2, 2), dtype=int) 

    # 2. Isolate the region of the grid located below this gray line. 
    # (Implicitly handled in the counting function)

    # 3. Count the total number of red pixels (color 2) within this lower region.
    red_count = count_colors_below_divider(input_np, divider_row_idx, 2)

    # 4. Count the total number of yellow pixels (color 4) within this lower region.
    yellow_count = count_colors_below_divider(input_np, divider_row_idx, 4)

    # 5. Compare the count of red pixels to the count of yellow pixels.
    # 6. If the count of red pixels is greater than or equal to the count of yellow pixels, determine the output color to be red (2).
    # 7. Otherwise (if the count of yellow pixels is greater than the count of red pixels), determine the output color to be yellow (4).
    if red_count >= yellow_count:
        output_color = 2 # red
    else:
        output_color = 4 # yellow

    # 8. Construct a 2x2 output grid filled entirely with the determined output color.
    output_grid = np.full((2, 2), output_color, dtype=int)

    return output_grid.tolist() # Return as list of lists as per standard ARC format