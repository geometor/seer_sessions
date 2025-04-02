```python
import numpy as np

"""
This transformation rule identifies a primary structure formed by red pixels (2) and uses its spatial extent and orientation (vertical or horizontal) to filter yellow pixels (4). Yellow pixels that fall strictly 'between' the bounds of the red structure along its minor axis are kept; all other yellow pixels are removed (changed to white, 0).

1. Find all red pixels and determine the bounding box (min/max row and column) and orientation (vertical if more unique rows than columns, horizontal otherwise).
2. Iterate through all yellow pixels.
3. If the red structure is vertical, keep yellow pixels whose column index is strictly between the minimum and maximum red column indices.
4. If the red structure is horizontal, keep yellow pixels whose row index is strictly between the minimum and maximum red row indices.
5. Change all other yellow pixels to white (0).
6. Keep all other pixels (red, white, etc.) unchanged.
"""

def find_pixels(grid, color_value):
    """Finds the coordinates of all pixels with a specific color value."""
    coords = np.argwhere(grid == color_value)
    # np.argwhere returns row, col pairs
    return [tuple(coord) for coord in coords]

def transform(input_grid):
    """
    Filters yellow pixels based on their position relative to the bounds of a red structure.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy()
    height, width = grid.shape

    # Find coordinates of all red pixels (color 2)
    red_coords = find_pixels(grid, 2)

    # If there are no red pixels, return the original grid
    if not red_coords:
        return output_grid.tolist()

    # Determine the bounding box and unique rows/columns of the red structure
    red_rows = {r for r, c in red_coords}
    red_cols = {c for r, c in red_coords}

    min_red_row = min(red_rows)
    max_red_row = max(red_rows)
    min_red_col = min(red_cols)
    max_red_col = max(red_cols)

    num_unique_red_rows = len(red_rows)
    num_unique_red_cols = len(red_cols)

    # Determine the orientation of the red structure
    # Vertical if it spans more rows than columns
    is_vertical = num_unique_red_rows > num_unique_red_cols
    # Horizontal otherwise (including cases where counts are equal, or it's just a point/line)
    is_horizontal = not is_vertical 

    # Iterate through the grid to find yellow pixels (color 4)
    for r in range(height):
        for c in range(width):
            if grid[r, c] == 4:
                # Assume the yellow pixel should be removed unless it meets the criteria
                remove_yellow = True

                # Check criteria based on red structure orientation
                if is_vertical:
                    # Keep if column is strictly between min and max red columns
                    if min_red_col < c < max_red_col:
                        remove_yellow = False
                elif is_horizontal:
                     # Keep if row is strictly between min and max red rows
                    if min_red_row < r < max_red_row:
                         remove_yellow = False
                # Note: If it's neither strictly vertical nor horizontal (e.g., a single point, or equal rows/cols),
                # the 'is_horizontal' branch handles it. For a single red point/line, no yellow pixels will be strictly 'between'.

                # If the yellow pixel does not meet the criteria, change it to white (0)
                if remove_yellow:
                    output_grid[r, c] = 0

    # Convert the result back to a list of lists
    return output_grid.tolist()
```