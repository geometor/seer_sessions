import numpy as np

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
    is_top_border = len(np.unique(top_row)) == 1 and top_row[0] != 0
    is_bottom_border = len(np.unique(bottom_row)) == 1 and bottom_row[0] != 0

    if is_top_border and is_bottom_border:
        return 'horizontal', top_row[0], UP, bottom_row[0], DOWN

    # Check for vertical borders (left/right)
    left_col = grid[:, 0]
    right_col = grid[:, width - 1]
    is_left_border = len(np.unique(left_col)) == 1 and left_col[0] != 0
    is_right_border = len(np.unique(right_col)) == 1 and right_col[0] != 0

    if is_left_border and is_right_border:
        return 'vertical', left_col[0], LEFT, right_col[0], RIGHT

    # Should not happen based on examples, but handle unexpected cases
    return None 


def transform(input_grid):
    """
    Transforms the input grid by placing colored pixels adjacent to blue pixels.
    The color and direction of placement are determined by the two border lines
    (either top/bottom or left/right). A new pixel is placed only if the
    target adjacent cell in the input grid is white (0).
    """
    input_grid_np = np.array(input_grid)
    height, width = input_grid_np.shape
    
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid_np)

    # Identify borders and their properties
    border_info = find_borders(input_grid_np)
    if border_info is None:
        # If borders aren't as expected, return the original grid or handle error
        print("Warning: Could not identify standard borders.")
        return input_grid # Or raise an error

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
            # Check if the current cell is blue (1)
            if input_grid_np[r, c] == 1:
                # Check adjacency for the first border
                r1, c1 = r + direction1[0], c + direction1[1]
                # Check bounds and if the target cell in the *input* was white (0)
                if 0 <= r1 < height and 0 <= c1 < width and input_grid_np[r1, c1] == 0:
                    # Place the first border's color in the *output* grid
                    output_grid[r1, c1] = color1

                # Check adjacency for the second border
                r2, c2 = r + direction2[0], c + direction2[1]
                # Check bounds and if the target cell in the *input* was white (0)
                if 0 <= r2 < height and 0 <= c2 < width and input_grid_np[r2, c2] == 0:
                    # Place the second border's color in the *output* grid
                    output_grid[r2, c2] = color2

    return output_grid.tolist()