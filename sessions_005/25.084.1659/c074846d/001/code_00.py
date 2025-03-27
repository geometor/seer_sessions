import numpy as np

"""
Identify the single gray (5) pixel which acts as a pivot.
Identify all red (2) pixels.
For each red pixel:
1. Change its color to green (3) in its original position.
2. Calculate its position relative to the gray pivot.
3. Rotate this relative position 90 degrees clockwise.
4. Calculate the new absolute position by adding the rotated relative position to the pivot's position.
5. If the new position is within the grid boundaries, place a red (2) pixel there.
The output grid contains the original gray pivot, the green pixels where the red pixels used to be, and the new red pixels at the rotated positions.
"""

def find_pixels(grid, color):
    """Finds all coordinates of pixels with a specific color."""
    return list(zip(*np.where(grid == color)))

def transform(input_grid):
    """
    Transforms the input grid based on the rotation rule.

    Args:
        input_grid (np.array): The input grid.

    Returns:
        np.array: The transformed output grid.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find the single gray pivot pixel (color 5)
    gray_coords = find_pixels(input_grid, 5)
    if not gray_coords:
        # Or raise an error if a pivot is always expected
        print("Warning: No gray pivot pixel (5) found.")
        return output_grid
    if len(gray_coords) > 1:
        # Or raise an error
        print("Warning: Multiple gray pivot pixels (5) found.")
        return output_grid # Assuming only one pivot is allowed
    r_gray, c_gray = gray_coords[0]

    # Find all red pixels (color 2)
    red_coords = find_pixels(input_grid, 2)

    # Process each red pixel found in the input
    for r_red, c_red in red_coords:
        # 1. Change the original red pixel to green (3) in the output grid
        output_grid[r_red, c_red] = 3

        # 2. Calculate the relative position vector from gray pivot to red pixel
        dr = r_red - r_gray
        dc = c_red - c_gray

        # 3. Calculate the new relative position after 90-degree clockwise rotation
        # (dr', dc') = (dc, -dr)
        dr_new = dc
        dc_new = -dr

        # 4. Calculate the new absolute position
        r_new = r_gray + dr_new
        c_new = c_gray + dc_new

        # 5. Check if the new position is within grid bounds
        if 0 <= r_new < rows and 0 <= c_new < cols:
            # Place a new red pixel (2) at the calculated rotated position
            # This assumes the rotation won't overwrite the pivot itself,
            # which is true for non-zero relative vectors. If dr=0 and dc=0
            # (red pixel is the pivot), it's handled because the original
            # color is changed to green first.
            # It also assumes the new red pixels don't overlap with the
            # positions being changed to green in the same step, which holds true.
            output_grid[r_new, c_new] = 2
        # else:
            # The rotated position is outside the grid, do nothing.
            # print(f"Rotated position ({r_new}, {c_new}) out of bounds.")


    return output_grid