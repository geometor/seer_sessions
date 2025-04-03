import numpy as np
from collections import Counter

"""
Identifies the most frequent non-background color (0) in the input 1D grid.
Defines a modification span from the first to the last occurrence of this dominant color.
Within this span, replaces any pixel that is neither the dominant color nor the background color with the dominant color.
Pixels outside the span or pixels matching the dominant or background color remain unchanged.
"""

def find_dominant_non_background_color(grid_1d):
    """Finds the most frequent color excluding the background color 0."""
    counts = Counter(c for c in grid_1d if c != 0)
    if not counts:
        return None  # No non-background colors found
    # Find the color with the maximum count
    dominant_color = counts.most_common(1)[0][0]
    return dominant_color

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list or np.ndarray): A 1D array representing the input grid row.

    Returns:
        np.ndarray: The transformed 1D array.
    """
    # Ensure input is a numpy array for efficient operations
    grid_1d = np.array(input_grid)

    # Handle edge case: empty input
    if grid_1d.size == 0:
        return grid_1d.copy()

    # Initialize output_grid as a copy of the input
    output_grid = grid_1d.copy()

    # 1. Identify the background color (assumed to be 0)
    background_color = 0

    # 2. Find the dominant non-background color
    dominant_color = find_dominant_non_background_color(grid_1d)

    # If no non-background color exists, return the original grid
    if dominant_color is None:
        return output_grid

    # 3. Find the first and last indices of the dominant color
    indices = np.where(grid_1d == dominant_color)[0]

    # If dominant color is not found (shouldn't happen if find_dominant_color returned a value, but defensive check)
    if indices.size == 0:
        return output_grid # Or potentially raise an error depending on expected behavior

    first_index = indices[0]
    last_index = indices[-1]

    # 4. Define the modification span
    start_span = first_index
    end_span = last_index # Inclusive end index for iteration

    # 5. Iterate through the modification span and apply changes
    for i in range(start_span, end_span + 1):
        current_color = output_grid[i]
        # Check if the color is an 'impurity' (not dominant and not background)
        if current_color != dominant_color and current_color != background_color:
            # Replace impurity with the dominant color
            output_grid[i] = dominant_color

    return output_grid
