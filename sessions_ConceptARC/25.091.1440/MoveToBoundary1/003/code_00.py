import numpy as np
from typing import List, Tuple, Dict, Optional

"""
Moves a blue (1) object away from a red (2) line based on the line's orientation
and the gap between them.
The distance moved is equal to the number of background (0) cells strictly
between the blue object's bounding box and the red line.
The movement is perpendicular to the line, increasing the distance between
the object and the line.
The red line and background remain unchanged.
"""

# Helper function to find all coordinates of pixels with a specific color
def find_object_pixels(grid: np.ndarray, color: int) -> List[Tuple[int, int]]:
    """Finds all coordinates (row, col) of pixels with the specified color."""
    rows, cols = np.where(grid == color)
    return list(zip(rows, cols))

# Helper function to calculate the bounding box of a set of pixels
def get_bounding_box(pixels: List[Tuple[int, int]]) -> Optional[Tuple[int, int, int, int]]:
    """Calculates the bounding box (min_row, min_col, max_row, max_col) for a set of pixels."""
    if not pixels:
        return None
    min_row = min(r for r, c in pixels)
    min_col = min(c for r, c in pixels)
    max_row = max(r for r, c in pixels)
    max_col = max(c for r, c in pixels)
    return min_row, min_col, max_row, max_col

# Helper function to determine if a set of pixels forms a straight line and its orientation/position
def determine_line_orientation_and_position(pixels: List[Tuple[int, int]]) -> Optional[Tuple[str, int]]:
    """
    Determines if the pixels form a vertical or horizontal line.
    Returns the orientation ('vertical' or 'horizontal') and the fixed coordinate (column or row index).
    Returns None if the pixels don't form a straight line or are empty.
    """
    if not pixels:
        return None

    rows = {r for r, c in pixels}
    cols = {c for r, c in pixels}

    if len(cols) == 1:
        # All pixels share the same column -> vertical line
        return 'vertical', list(cols)[0]
    elif len(rows) == 1:
        # All pixels share the same row -> horizontal line
        return 'horizontal', list(rows)[0]
    else:
        # Not a straight line
        return None

# Helper function to calculate the shift vector based on object/line relationship
def calculate_shift_vector(blue_pixels: List[Tuple[int, int]], red_pixels: List[Tuple[int, int]]) -> Tuple[int, int]:
    """
    Calculates the shift vector (dx, dy) for the blue object based on the gap
    between its bounding box and the red line. Movement is away from the line.
    Returns (0, 0) if no shift is needed or possible (e.g., objects not found,
    line invalid, object touches line, or zero gap).
    """
    blue_bbox = get_bounding_box(blue_pixels)
    line_info = determine_line_orientation_and_position(red_pixels)

    # Default shift is none
    dx, dy = 0, 0

    # Return no shift if objects/line aren't found correctly
    if not blue_bbox or not line_info:
        return dx, dy

    min_r, min_c, max_r, max_c = blue_bbox
    orientation, line_pos = line_info
    gap = -1 # Initialize gap to indicate not yet calculated or invalid

    # Calculate gap and determine shift direction (away from line)
    if orientation == 'vertical':
        red_col = line_pos
        if max_c < red_col: # Blue is left of line
            gap = red_col - max_c - 1
            if gap >= 0: dx = gap # Move right (increase col index)
        elif min_c > red_col: # Blue is right of line
            gap = min_c - red_col - 1
            if gap >= 0: dx = -gap # Move left (decrease col index)
        # dy remains 0 for vertical lines
    elif orientation == 'horizontal':
        red_row = line_pos
        if max_r < red_row: # Blue is above line
            gap = red_row - max_r - 1
            if gap >= 0: dy = gap # Move down (increase row index)
        elif min_r > red_row: # Blue is below line
            gap = min_r - red_row - 1
            if gap >= 0: dy = -gap # Move up (decrease row index)
        # dx remains 0 for horizontal lines

    # Only return calculated shift if a valid, positive gap was found (gap > 0)
    # If gap is 0 or negative (touching/overlapping/error), return (0, 0)
    if gap <= 0:
        return 0, 0
    else:
        # Ensure results are standard integers
        return int(dx), int(dy)

# Main transformation function
def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid by moving the blue object away from the red line
    by a distance equal to the gap between them.
    """
    # Find coordinates of blue (1) and red (2) pixels
    blue_pixels = find_object_pixels(input_grid, 1)
    red_pixels = find_object_pixels(input_grid, 2)

    # Handle edge cases: If no blue object or no red line exists, return the grid unchanged.
    if not blue_pixels or not red_pixels:
        return input_grid.copy() # Return a copy to prevent modifying the original input

    # Calculate the required shift vector (dx, dy)
    dx, dy = calculate_shift_vector(blue_pixels, red_pixels)

    # If no shift is required (dx=0 and dy=0), return the original grid.
    # This covers cases where the line is invalid, objects touch, or the calculated gap is zero.
    if dx == 0 and dy == 0:
         return input_grid.copy()

    # Initialize the output grid with the same shape as the input, filled with background color (0)
    output_grid = np.zeros_like(input_grid)

    # Copy the red line from the input to the output grid at its original position.
    # This ensures the red line remains static.
    for r, c in red_pixels:
        # Basic boundary check, although red pixels should always be within bounds.
        if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
             output_grid[r, c] = 2

    # Apply the calculated shift to each blue pixel and draw it on the output grid.
    for r, c in blue_pixels:
        new_r, new_c = r + dy, c + dx
        # Check if the new coordinates are within the grid boundaries.
        if 0 <= new_r < output_grid.shape[0] and 0 <= new_c < output_grid.shape[1]:
            # Place the blue pixel at the new location.
            # The order ensures that if blue moves onto red, red persists (copied last).
            # However, the gap calculation should prevent overlap if initially separated.
             if output_grid[new_r, new_c] == 0: # Only draw if cell is background
                 output_grid[new_r, new_c] = 1
        # Pixels moved outside the grid boundaries are effectively removed.

    # Return the newly constructed output grid
    return output_grid