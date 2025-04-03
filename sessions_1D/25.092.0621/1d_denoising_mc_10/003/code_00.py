import numpy as np
import collections

"""
Transformation Rule:
1. Accept the input grid (a 2D NumPy array of color values).
2. Scan the entire grid to find all pixels with non-white colors (colors 1 through 9).
3. If no non-white pixels are found, return the input grid unchanged.
4. Count the occurrences of each distinct non-white color found in step 2.
5. Identify the non-white color that has the highest count; this is the "target color".
6. Create a new grid as a copy of the input grid.
7. Identify all pixel locations in the *original* input grid that contain a non-white color.
8. Set the color of these corresponding locations in the *new* grid to the "target color".
9. White pixels (color 0) remain unchanged in their locations.
10. Return the new grid.
"""

def find_dominant_non_white_color_np(grid):
    """
    Finds the most frequent non-white color in a NumPy grid.

    Args:
        grid: A NumPy array representing the grid.

    Returns:
        The integer value of the most frequent non-white color,
        or None if no non-white colors are present.
    """
    # Flatten the grid to easily iterate through all pixels
    flat_grid = grid.flatten()

    # Filter out white pixels (color 0) using boolean indexing
    non_white_pixels = flat_grid[flat_grid != 0]

    # If the resulting array is empty (no non-white pixels), return None
    if non_white_pixels.size == 0:
        return None

    # Count the frequency of each non-white color
    # collections.Counter works directly on NumPy arrays
    color_counts = collections.Counter(non_white_pixels)

    # Find the color with the highest count.
    # most_common(1) returns a list like [(color, count)], so we access [0][0].
    dominant_color = color_counts.most_common(1)[0][0]

    return dominant_color

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid by replacing all non-white pixels
    with the single most frequent non-white color found in the grid.

    Args:
        input_grid: A NumPy array representing the input grid.

    Returns:
        A NumPy array representing the transformed grid.
    """
    # Find the dominant non-white color in the input grid
    target_color = find_dominant_non_white_color_np(input_grid)

    # If no non-white pixels were found (target_color is None),
    # return the original grid without modification.
    if target_color is None:
        return np.copy(input_grid) # Return a copy to maintain immutability expectation

    # Create a copy of the input grid to modify and return
    output_grid = np.copy(input_grid)

    # Create a boolean mask identifying all non-white pixels in the original grid.
    # This mask will be True where input_grid[row, col] != 0, and False otherwise.
    non_white_mask = (input_grid != 0)

    # Use the boolean mask to assign the target_color to all
    # locations in the output_grid where the mask is True.
    # Pixels where the mask is False (originally white) are not affected.
    output_grid[non_white_mask] = target_color

    # Return the modified grid
    return output_grid