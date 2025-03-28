```python
import numpy as np
from typing import List, Tuple

"""
Identifies a single non-white object (a 3x3 hollow square) in the input grid.
Determines the direction of movement based on the object's color:
- magenta(6): Up
- azure(8): Right
- yellow(4): Down
Calculates the distance of movement as the number of empty spaces (white pixels) between the object's relevant edge and the corresponding grid boundary in the direction of movement.
Creates a new grid of the same dimensions, initialized to white.
Places the object at its new position in the output grid, shifted by the calculated distance in the determined direction.
"""

def find_object(grid: np.ndarray) -> Tuple[List[Tuple[int, int]], int, int, int, int, int]:
    """
    Finds the pixels, color, and bounding box of the single non-white object.

    Args:
        grid: The input grid as a numpy array.

    Returns:
        A tuple containing:
        - object_pixels: List of (row, col) tuples for each pixel of the object.
        - object_color: The color (int) of the object.
        - min_row: Minimum row index of the object's bounding box.
        - max_row: Maximum row index of the object's bounding box.
        - min_col: Minimum column index of the object's bounding box.
        - max_col: Maximum column index of the object's bounding box.
        Returns None for any value if no object is found.
    """
    non_white_pixels = np.where(grid != 0)
    if len(non_white_pixels[0]) == 0:
        return [], -1, -1, -1, -1, -1 # No object found

    rows, cols = non_white_pixels
    object_pixels = list(zip(rows, cols))
    object_color = grid[rows[0], cols[0]] # Get color from the first found pixel
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)

    return object_pixels, object_color, min_row, max_row, min_col, max_col

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Moves the single non-white object within the grid based on its color.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the output grid with the moved object.
    """
    input_np = np.array(input_grid, dtype=int)
    grid_height, grid_width = input_np.shape

    # Find the object, its color, and bounding box
    object_pixels_coords, object_color, min_row, max_row, min_col, max_col = find_object(input_np)

    if object_color == -1: # Handle case where no object is found
        return input_grid # Or return an empty grid, depending on desired behavior

    # Initialize delta row/col for movement
    delta_row, delta_col = 0, 0

    # Determine direction and calculate distance based on color
    if object_color == 6:  # magenta -> Move Up
        distance = min_row
        delta_row = -distance
    elif object_color == 8:  # azure -> Move Right
        distance = (grid_width - 1) - max_col
        delta_col = distance
    elif object_color == 4:  # yellow -> Move Down
        distance = (grid_height - 1) - max_row
        delta_row = distance
    # Add rules for other colors if necessary, otherwise object stays put

    # Create the output grid, initialized with white (0)
    output_grid = np.zeros_like(input_np)

    # Calculate new positions and draw the object in the output grid
    for r, c in object_pixels_coords:
        new_r, new_c = r + delta_row, c + delta_col
        # Ensure the new coordinates are within the grid bounds
        if 0 <= new_r < grid_height and 0 <= new_c < grid_width:
            output_grid[new_r, new_c] = object_color

    return output_grid.tolist()
```