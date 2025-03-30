import numpy as np

"""
Identifies border lines (either horizontal top/bottom or vertical left/right) in the input grid.
For each blue pixel (color 1) in the input grid, determines if it's closer to the first border (top/left) or the second border (bottom/right).
If the blue pixel is closer to the first border, it attempts to color the adjacent cell in the direction of the first border (up/left) with the first border's color, but only if that adjacent cell is currently white (color 0).
If the blue pixel is closer to the second border, it attempts to color the adjacent cell in the direction of the second border (down/right) with the second border's color, but only if that adjacent cell is currently white (color 0).
If the blue pixel is equidistant from both borders (only possible if the dimension is odd, which doesn't occur in the examples), it defaults to acting as if it were closer to the first border (top/left).
The coloring actions modify a copy of the input grid, ensuring that original white cells are checked before modification.
"""

def find_borders(grid):
    """
    Identifies the location and colors of the two border lines.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        tuple: A tuple containing:
            - border_type (str): 'horizontal' or 'vertical'.
            - border1_color (int): Color of the first border (top or left).
            - border1_direction (tuple): Relative direction vector for border 1.
            - border2_color (int): Color of the second border (bottom or right).
            - border2_direction (tuple): Relative direction vector for border 2.
        Returns None if two distinct borders are not found as expected.
    """
    height, width = grid.shape

    # Define directions
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

    # Check for horizontal borders (top/bottom)
    top_row = grid[0, :]
    bottom_row = grid[height - 1, :]
    # Ensure the entire row is a single non-white color
    is_top_border = len(np.unique(top_row)) == 1 and top_row[0] != 0
    is_bottom_border = len(np.unique(bottom_row)) == 1 and bottom_row[0] != 0

    if is_top_border and is_bottom_border:
        # Ensure border colors are different (as implied by examples, though not strictly necessary for logic)
        # if top_row[0] != bottom_row[0]:
        return 'horizontal', top_row[0], UP, bottom_row[0], DOWN

    # Check for vertical borders (left/right)
    left_col = grid[:, 0]
    right_col = grid[:, width - 1]
    # Ensure the entire col is a single non-white color
    is_left_border = len(np.unique(left_col)) == 1 and left_col[0] != 0
    is_right_border = len(np.unique(right_col)) == 1 and right_col[0] != 0

    if is_left_border and is_right_border:
        # Ensure border colors are different
        # if left_col[0] != right_col[0]:
        return 'vertical', left_col[0], LEFT, right_col[0], RIGHT

    # Did not find the expected pair of borders
    return None

def transform(input_grid):
    """
    Transforms the input grid by placing colored pixels adjacent to blue pixels
    based on proximity to borders, only on white cells.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape

    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid_np)

    # Identify borders and their properties
    border_info = find_borders(input_grid_np)
    if border_info is None:
        # If borders aren't as expected, return the original grid (or handle error)
        # This case doesn't seem to occur in the provided examples.
        print("Warning: Could not identify standard borders. Returning input.")
        return input_grid # Return original list format

    border_type, color1, direction1, color2, direction2 = border_info

    # Define the range to iterate over (excluding borders)
    if border_type == 'horizontal':
        row_start, row_end = 1, height - 1
        col_start, col_end = 0, width
    else: # vertical
        row_start, row_end = 0, height
        col_start, col_end = 1, width - 1

    # Iterate through the inner part of the grid
    for r in range(row_start, row_end):
        for c in range(col_start, col_end):
            # Check if the current cell in the *input* grid is blue (1)
            if input_grid_np[r, c] == 1:
                target_r, target_c = -1, -1 # Initialize invalid coordinates
                color_to_place = -1 # Initialize invalid color

                # Determine which border is closer and the corresponding action
                if border_type == 'horizontal':
                    dist1 = r - 0 # Distance from top border (row 0)
                    dist2 = (height - 1) - r # Distance from bottom border (row H-1)

                    if dist1 <= dist2: # Closer to top or equidistant (default to top)
                        target_r, target_c = r + direction1[0], c + direction1[1]
                        color_to_place = color1
                    else: # Closer to bottom
                        target_r, target_c = r + direction2[0], c + direction2[1]
                        color_to_place = color2

                else: # vertical borders
                    dist1 = c - 0 # Distance from left border (col 0)
                    dist2 = (width - 1) - c # Distance from right border (col W-1)

                    if dist1 <= dist2: # Closer to left or equidistant (default to left)
                        target_r, target_c = r + direction1[0], c + direction1[1]
                        color_to_place = color1
                    else: # Closer to right
                        target_r, target_c = r + direction2[0], c + direction2[1]
                        color_to_place = color2

                # Check bounds and if the target cell in the *input* grid was white (0)
                if 0 <= target_r < height and 0 <= target_c < width and input_grid_np[target_r, target_c] == 0:
                    # Place the determined color in the *output* grid
                    output_grid[target_r, target_c] = color_to_place

    # Return the transformed grid as a list of lists
    return output_grid.tolist()