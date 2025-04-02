"""
Transforms an input grid by identifying a diagonal line of a single non-white color and filling the area below and to the left of this line with the same color.

The transformation rule is as follows:
1. Identify the single non-white color (fill_color) present in the input grid.
2. Find all coordinates (r_in, c_in) where this fill_color appears in the input grid.
3. Create an output grid of the same dimensions, initially filled with white (0).
4. For each pixel position (r_out, c_out) in the output grid:
   Check if there exists at least one input coordinate (r_in, c_in) such that r_out >= r_in AND c_out <= c_in.
5. If the condition in step 4 is true, set the output pixel at (r_out, c_out) to the fill_color.
6. Otherwise, the output pixel remains white (0).
"""

import numpy as np

def find_fill_color_and_coords(grid):
    """
    Finds the single non-white color and its coordinates in the grid.
    Assumes there is exactly one non-white color present as a diagonal line.
    """
    fill_color = 0
    coords = []
    non_white_colors = np.unique(grid[grid != 0])

    if len(non_white_colors) == 0:
        # Handle case with no non-white colors (though unlikely based on examples)
        return 0, []
    elif len(non_white_colors) > 1:
        # Handle case with multiple non-white colors if necessary,
        # but based on examples, assume only one.
        # For now, just pick the first one found.
        print(f"Warning: Multiple non-white colors found: {non_white_colors}. Using {non_white_colors[0]}.")
        fill_color = non_white_colors[0]
    else:
        fill_color = non_white_colors[0]

    # Find coordinates efficiently using numpy
    coords = list(zip(*np.where(grid == fill_color))) # Returns list of (row, col) tuples
    return int(fill_color), coords

def transform(input_grid):
    """
    Applies the fill transformation based on the diagonal line in the input grid.

    Args:
        input_grid (list of lists or np.ndarray): The input grid.

    Returns:
        np.ndarray: The transformed output grid.
    """
    # Convert input to numpy array for efficient operations
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # 1. & 2. Identify the fill color and the coordinates of the input line pixels
    fill_color, input_coords = find_fill_color_and_coords(input_np)

    # Handle edge case where there's no fill color (e.g., all white input)
    if fill_color == 0 or not input_coords:
        return input_np # Return input as is or an all-white grid

    # 3. Initialize output grid with white (0)
    output_grid = np.zeros_like(input_np, dtype=int)

    # 4. Iterate through each pixel position in the potential output grid
    for r_out in range(height):
        for c_out in range(width):
            # 5. Check the condition against all input coordinates
            fill_pixel = False
            for r_in, c_in in input_coords:
                if r_out >= r_in and c_out <= c_in:
                    fill_pixel = True
                    break # Found a condition match, no need to check further for this output pixel

            # 6. If the condition was met, fill the output pixel
            if fill_pixel:
                output_grid[r_out, c_out] = fill_color
            # 7. Otherwise, it remains white (0) as initialized

    return output_grid.tolist() # Return as list of lists if required by ARC standard