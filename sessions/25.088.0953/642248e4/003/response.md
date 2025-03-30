```python
import numpy as np

"""
Identifies whether the input grid has horizontal (top/bottom) or vertical (left/right) single-pixel thick borders of uniform, non-white, distinct colors.
If borders are found, iterates through the inner grid (excluding borders) looking for blue pixels (color 1).
For each blue pixel, it determines the closest border (top vs. bottom, or left vs. right).
It then checks the orthogonally adjacent white pixel (color 0) located in the direction of the closest border.
If such a white pixel exists, is within the inner grid boundaries, and is white, it is repainted with the color of the closest border.
The original blue pixels and the border pixels remain unchanged.
If no valid borders are identified, the original grid is returned.
Pixels exactly equidistant from both borders do not trigger any painting (based on observed examples).
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
    Applies the border-proximity-based color transformation to white pixels adjacent to blue pixels.
    """
    input_np = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_np)
    height, width = input_np.shape

    border_type = None
    color1 = -1 # Will store top or left color
    color2 = -1 # Will store bottom or right color

    # --- 1. Identify Borders ---
    # Check for horizontal borders (top and bottom rows)
    if height >= 3: # Need at least 3 rows for top border, inner row, bottom border
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
    if border_type is None and width >= 3: # Need at least 3 cols for left border, inner col, right border
        left_col = input_np[:, 0]
        right_col = input_np[:, width - 1]
        left_uniform, left_color = is_uniform_and_non_white(left_col)
        right_uniform, right_color = is_uniform_and_non_white(right_col)

        # Check if both are uniform, non-white, and different from each other
        if left_uniform and right_uniform and left_color != right_color:
            border_type = 'vertical'
            color1 = left_color # color_left
            color2 = right_color # color_right

    # --- 2. No Valid Borders: Return Input ---
    if border_type is None:
        return output_grid.tolist()

    # --- 3. Apply Transformation based on Proximity ---
    if border_type == 'horizontal':
        color_top = color1
        color_bottom = color2
        # Iterate through the inner grid rows (excluding borders)
        for r in range(1, height - 1):
            # Iterate through all columns (borders don't affect column iteration)
            for c in range(width):
                # Find blue pixels (trigger pixels)
                if input_np[r, c] == 1:
                    # Calculate distance to borders (row index is distance from top)
                    dist_top = r
                    dist_bottom = (height - 1) - r

                    # Check proximity and paint adjacent white pixel if applicable
                    if dist_top < dist_bottom:
                        # Closer to top: check pixel above
                        target_r, target_c = r - 1, c
                        # Ensure target is within inner grid (r-1 >= 1) and is white
                        if target_r >= 1 and input_np[target_r, target_c] == 0:
                            output_grid[target_r, target_c] = color_top
                    elif dist_bottom < dist_top:
                        # Closer to bottom: check pixel below
                        target_r, target_c = r + 1, c
                        # Ensure target is within inner grid (r+1 <= height-2) and is white
                        if target_r <= height - 2 and input_np[target_r, target_c] == 0:
                            output_grid[target_r, target_c] = color_bottom
                    # If dist_top == dist_bottom, do nothing (based on examples)

    elif border_type == 'vertical':
        color_left = color1
        color_right = color2
        # Iterate through all rows (borders don't affect row iteration)
        for r in range(height):
            # Iterate through the inner grid columns (excluding borders)
             for c in range(1, width - 1):
                 # Find blue pixels (trigger pixels)
                if input_np[r, c] == 1:
                    # Calculate distance to borders (col index is distance from left)
                    dist_left = c
                    dist_right = (width - 1) - c

                    # Check proximity and paint adjacent white pixel if applicable
                    if dist_left < dist_right:
                        # Closer to left: check pixel left
                        target_r, target_c = r, c - 1
                        # Ensure target is within inner grid (c-1 >= 1) and is white
                        if target_c >= 1 and input_np[target_r, target_c] == 0:
                            output_grid[target_r, target_c] = color_left
                    elif dist_right < dist_left:
                        # Closer to right: check pixel right
                        target_r, target_c = r, c + 1
                        # Ensure target is within inner grid (c+1 <= width-2) and is white
                        if target_c <= width - 2 and input_np[target_r, target_c] == 0:
                            output_grid[target_r, target_c] = color_right
                    # If dist_left == dist_right, do nothing (based on examples)

    # Convert the NumPy array back to a list of lists for the final output
    return output_grid.tolist()
```