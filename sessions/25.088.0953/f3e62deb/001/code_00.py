import numpy as np
from typing import List, Tuple

"""
Identifies a single 3x3 hollow square object in the input grid.
Determines the object's color (Azure=8, Yellow=4, or Magenta=6).
Moves the object to a specific edge of the grid based on its color:
- Azure (8) objects move horizontally to align their right edge with the grid's right edge.
- Yellow (4) objects move vertically to align their bottom edge with the grid's bottom edge.
- Magenta (6) objects move vertically to align their top edge with the grid's top edge (row 0).
The object maintains its original relative row position for horizontal moves and original relative column position for vertical moves.
The rest of the grid remains the background color (white=0).
"""

def find_object_properties(grid: np.ndarray) -> Tuple[int, int, int, int, int]:
    """
    Finds the first non-background pixel, assumes it's part of the object,
    and determines the object's color and top-left corner.
    Assumes the object is 3x3.

    Args:
        grid: The input numpy grid.

    Returns:
        A tuple containing:
        - color (int): The color of the object.
        - top_row (int): The row index of the top-left corner of the object's bounding box.
        - left_col (int): The column index of the top-left corner of the object's bounding box.
        - height (int): The height of the object (assumed 3).
        - width (int): The width of the object (assumed 3).
    """
    height, width = grid.shape
    object_color = 0
    top_row, left_col = -1, -1

    for r in range(height):
        for c in range(width):
            if grid[r, c] != 0:
                object_color = grid[r, c]
                # We need the top-left corner of the 3x3 bounding box.
                # Since the shape is hollow, the first pixel found might not be the top-left.
                # We need to find the bounding box containing all pixels of this color.
                pixels = np.argwhere(grid == object_color)
                top_row = pixels[:, 0].min()
                left_col = pixels[:, 1].min()
                # Assuming the object is exactly 3x3 based on examples
                obj_height = 3
                obj_width = 3
                return object_color, top_row, left_col, obj_height, obj_width

    # Should not happen based on task description, but handle defensively
    return 0, -1, -1, 0, 0


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid by moving the single object based on its color.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    input_np = np.array(input_grid, dtype=int)
    grid_height, grid_width = input_np.shape

    # Find the object's properties
    color, obj_top_row, obj_left_col, obj_height, obj_width = find_object_properties(input_np)

    if color == 0: # No object found
        return input_grid # Return original grid or empty grid? Task implies object always exists.

    # Initialize the output grid with background color (0)
    output_np = np.zeros_like(input_np)

    # Determine the target top-left corner based on color
    target_top_row = -1
    target_left_col = -1

    if color == 8:  # Azure -> Move right
        target_top_row = obj_top_row
        target_left_col = grid_width - obj_width
    elif color == 4:  # Yellow -> Move down
        target_top_row = grid_height - obj_height
        target_left_col = obj_left_col
    elif color == 6:  # Magenta -> Move up
        target_top_row = 0
        target_left_col = obj_left_col
    else:
        # Unknown color or no object, return original grid
         return input_grid

    # Copy the object from the input grid to the target position in the output grid
    if target_top_row != -1 and target_left_col != -1:
        for r_offset in range(obj_height):
            for c_offset in range(obj_width):
                # Calculate source and destination coordinates
                source_row = obj_top_row + r_offset
                source_col = obj_left_col + c_offset
                dest_row = target_top_row + r_offset
                dest_col = target_left_col + c_offset

                # Check bounds (though calculated targets should be within bounds for 10x10)
                if 0 <= source_row < grid_height and 0 <= source_col < grid_width and \
                   0 <= dest_row < grid_height and 0 <= dest_col < grid_width:
                    # Copy the pixel value (including the white center of the hollow square)
                    output_np[dest_row, dest_col] = input_np[source_row, source_col]

    # Convert the numpy array back to a list of lists
    output_grid = output_np.tolist()

    return output_grid