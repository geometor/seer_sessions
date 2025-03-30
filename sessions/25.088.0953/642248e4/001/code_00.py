import numpy as np

"""
Identifies whether the input grid has horizontal (top/bottom) or vertical (left/right) single-pixel thick borders of uniform, non-white, distinct colors.
If borders are found, iterates through the grid looking for blue pixels (color 1).
For each blue pixel found, it checks its adjacent white pixels (color 0) that are within the non-border area.
If the borders are horizontal, a white pixel directly above a blue pixel is changed to the top border's color, and a white pixel directly below is changed to the bottom border's color.
If the borders are vertical, a white pixel directly to the left of a blue pixel is changed to the left border's color, and a white pixel directly to the right is changed to the right border's color.
The original blue pixels and the border pixels remain unchanged.
If no valid borders are identified, the original grid is returned.
"""

def is_uniform_and_non_white(arr):
    """Checks if a 1D numpy array is uniform (all elements same) and not color 0 (white)."""
    if arr.size == 0:
        return False, -1 # Cannot be uniform if empty
    first_val = arr[0]
    if first_val == 0: # Check if the color is white
        return False, -1
    # Check if all elements are the same as the first element
    is_uniform = np.all(arr == first_val)
    return is_uniform, first_val

def transform(input_grid):
    """
    Applies the border-based color transformation to white pixels adjacent to blue pixels.
    """
    input_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_np)
    height, width = input_np.shape

    border_type = None
    color1 = -1
    color2 = -1

    # Check for horizontal borders (top and bottom rows)
    # Ensure grid is tall enough for distinct top/bottom borders and content area
    if height >= 3:
        top_row = input_np[0, :]
        bottom_row = input_np[height - 1, :]
        top_uniform, top_color = is_uniform_and_non_white(top_row)
        bottom_uniform, bottom_color = is_uniform_and_non_white(bottom_row)

        # Check if both are uniform, non-white, and different from each other
        if top_uniform and bottom_uniform and top_color != bottom_color:
            border_type = 'horizontal'
            color1 = top_color  # color_top
            color2 = bottom_color # color_bottom

    # If horizontal borders not found or not valid, check for vertical borders
    # Ensure grid is wide enough for distinct left/right borders and content area
    if border_type is None and width >= 3:
        left_col = input_np[:, 0]
        right_col = input_np[:, width - 1]
        left_uniform, left_color = is_uniform_and_non_white(left_col)
        right_uniform, right_color = is_uniform_and_non_white(right_col)

        # Check if both are uniform, non-white, and different from each other
        if left_uniform and right_uniform and left_color != right_color:
            border_type = 'vertical'
            color1 = left_color # color_left
            color2 = right_color # color_right

    # If no valid borders found, return the original grid copy
    if border_type is None:
        return output_grid.tolist()

    # Apply transformations based on border type
    if border_type == 'horizontal':
        color_top = color1
        color_bottom = color2
        # Iterate through the inner grid (excluding borders)
        for r in range(1, height - 1):
            for c in range(width):
                # Find blue pixels (trigger pixels)
                if input_np[r, c] == 1:
                    # Check pixel above (must be within inner grid, i.e., r-1 >= 1)
                    if r - 1 >= 1 and input_np[r - 1, c] == 0:
                        output_grid[r - 1, c] = color_top
                    # Check pixel below (must be within inner grid, i.e., r+1 <= height-2)
                    if r + 1 <= height - 2 and input_np[r + 1, c] == 0:
                        output_grid[r + 1, c] = color_bottom

    elif border_type == 'vertical':
        color_left = color1
        color_right = color2
        # Iterate through the inner grid (excluding borders)
        for r in range(height):
             for c in range(1, width - 1):
                 # Find blue pixels (trigger pixels)
                if input_np[r, c] == 1:
                    # Check pixel left (must be within inner grid, i.e., c-1 >= 1)
                    if c - 1 >= 1 and input_np[r, c - 1] == 0:
                        output_grid[r, c - 1] = color_left
                    # Check pixel right (must be within inner grid, i.e., c+1 <= width-2)
                    if c + 1 <= width - 2 and input_np[r, c + 1] == 0:
                        output_grid[r, c + 1] = color_right

    return output_grid.tolist()