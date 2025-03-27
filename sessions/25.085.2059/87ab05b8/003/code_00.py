"""
Transforms an input grid into an output grid of the same dimensions.
The output grid is initially filled with magenta (6).
The location of a single red (2) pixel in the input grid determines the position of a 2x2 red (2) square in the output grid.
Specifically, if the input red pixel is at (r, c), the top-left corner (tr, tc) of the output 2x2 red square is calculated as:
tr = min(r, H - 2)
tc = max(0, min(c - 1, W - 2))
where H and W are the height and width of the grid.
The 2x2 region starting at (tr, tc) in the output grid is then filled with red (2).
"""

import numpy as np

def find_first_pixel_location(grid_np, color_value):
    """Finds the row and column of the first pixel matching the color_value."""
    locations = np.argwhere(grid_np == color_value)
    if len(locations) > 0:
        return tuple(locations[0]) # Return (row, col) of the first match
    return None # Should not happen based on task description

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input_grid to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)

    # 1. Determine the dimensions (height H, width W) of the input grid.
    height, width = input_np.shape

    # 2. Locate the coordinates (r, c) of the single pixel with the color red (2)
    red_pixel_loc = find_first_pixel_location(input_np, 2)
    if red_pixel_loc is None:
        # Fallback or error handling if red pixel is missing (though examples suggest it's always present)
        # For now, let's assume it's always found based on the pattern.
        # If this assumption is wrong, we might need to return the input or a default grid.
        # Let's default to the previous behavior's target corner if no red pixel is found,
        # although this is unlikely given the examples.
        r, c = height - 1, width - 1 # Arbitrary fallback, less likely correct
    else:
        r, c = red_pixel_loc

    # 3. Create a new output grid of the same dimensions (H x W).
    # 4. Fill the entire output grid with the background color magenta (6).
    output_grid = np.full((height, width), 6, dtype=int)

    # 5. Calculate the target top-left row coordinate `tr`.
    #    Ensure the 2x2 square fits vertically, bounded by the input pixel's row.
    target_row = min(r, height - 2)

    # 6. Calculate the target top-left column coordinate `tc`.
    #    Shift left by 1 from the input pixel's column, clamped between 0 and W-2.
    target_col = max(0, min(c - 1, width - 2))

    # Define the target color for the square
    target_color = 2

    # 7. Draw a 2x2 square using the color red (2) onto the output grid
    #    at the calculated coordinates (tr, tc).
    # Ensure calculated indices are non-negative (should be guaranteed by max/min, but good practice)
    start_row = max(0, target_row)
    start_col = max(0, target_col)
    end_row = start_row + 2
    end_col = start_col + 2

    # Check if the square fits within the grid boundaries (should always fit due to H-2, W-2 calculation)
    if end_row <= height and end_col <= width:
        output_grid[start_row:end_row, start_col:end_col] = target_color

    # Convert back to list of lists for the expected output format
    return output_grid.tolist()
