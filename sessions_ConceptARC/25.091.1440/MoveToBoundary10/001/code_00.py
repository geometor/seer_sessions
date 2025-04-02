import numpy as np
from typing import List, Tuple

"""
Moves groups of pixels of the same non-background color horizontally to the
nearest edge of the grid. Pixels belonging to the same color group maintain
their relative horizontal positions. The vertical positions remain unchanged.
The direction of movement (left or right) is determined by whether the
horizontal center of the group is to the left or right (or exactly at) the
grid's horizontal center.
"""

def find_pixels_by_color(grid: np.ndarray, color: int) -> List[Tuple[int, int]]:
    """
    Finds the coordinates of all pixels of a specific color in the grid.

    Args:
        grid: The input numpy array representing the grid.
        color: The integer color value to search for.

    Returns:
        A list of (row, col) tuples representing the coordinates of pixels
        matching the specified color.
    """
    coords = np.argwhere(grid == color)
    # Convert numpy array rows to tuples (row, col)
    return [tuple(coord) for coord in coords]

def calculate_shift(pixels: List[Tuple[int, int]], grid_width: int) -> int:
    """
    Calculates the horizontal shift required to move a group of pixels to the
    nearest horizontal edge.

    Args:
        pixels: A list of (row, col) coordinates for the pixels of a single color.
        grid_width: The width of the grid.

    Returns:
        The integer amount to add to the column index of each pixel.
        Negative for left shift, positive for right shift.
    """
    if not pixels:
        return 0 # No shift if there are no pixels for this color

    # Extract column indices
    cols = [col for row, col in pixels]
    min_col = min(cols)
    max_col = max(cols)

    # Calculate the horizontal center of the pixel group and the grid
    group_center = (min_col + max_col) / 2.0
    grid_center = (grid_width - 1) / 2.0 # Use grid_width - 1 for 0-based indexing

    # Determine shift direction and magnitude
    if group_center < grid_center:
        # Move left: shift needed to align min_col with column 0
        shift = 0 - min_col
    else:
        # Move right: shift needed to align max_col with the last column (grid_width - 1)
        shift = (grid_width - 1) - max_col

    return shift

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape
    
    # Assume color 0 (white) is the background
    background_color = 0

    # Initialize the output grid with the background color
    output_grid = np.full((height, width), background_color, dtype=int)

    # Find all unique colors in the input grid, excluding the background
    unique_colors = np.unique(input_grid_np)
    non_background_colors = [color for color in unique_colors if color != background_color]

    # Process each non-background color group
    for color in non_background_colors:
        # 1. Find all pixel coordinates for the current color
        pixels = find_pixels_by_color(input_grid_np, color)

        # Skip if no pixels of this color are found (shouldn't happen with unique filtering)
        if not pixels:
            continue

        # 2. Calculate the horizontal shift required for this color group
        shift = calculate_shift(pixels, width)

        # 3. Apply the shift to each pixel and place it in the output grid
        for r, c in pixels:
            new_c = c + shift
            # Check bounds just in case, though shift calculation should guarantee this
            if 0 <= r < height and 0 <= new_c < width:
                output_grid[r, new_c] = color

    # Convert the final numpy array back to a list of lists
    return output_grid.tolist()