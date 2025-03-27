"""
Identifies the bounding box enclosing all white (0) pixels in the input grid.
Extracts this subgrid.
Creates an output grid of the same dimensions as the subgrid, initialized to white (0).
Copies pixels from the extracted subgrid to the output grid, *unless* the pixel's color matches the input grid's predominant background color (defined as the most frequent color, or the second most frequent if white is the most frequent). Pixels matching the background color remain white (0) in the output.
"""

import numpy as np
from collections import Counter

def find_background_color(grid: np.ndarray) -> int:
    """
    Determines the primary background color of the grid.

    It's the most frequent color, unless white (0) is the most frequent,
    in which case it's the second most frequent color. Handles cases
    where there's only one non-white color or only white.

    Args:
        grid: The input grid as a numpy array.

    Returns:
        The integer representing the background color.
    """
    unique_colors, counts = np.unique(grid, return_counts=True)
    counts_dict = dict(zip(unique_colors, counts))

    # If only one color exists, it's the background
    if len(unique_colors) == 1:
        return unique_colors[0]

    # Sort colors by frequency (descending)
    sorted_colors = sorted(counts_dict, key=counts_dict.get, reverse=True)

    # If the most frequent color is white (0) and there are other colors,
    # return the second most frequent.
    if sorted_colors[0] == 0 and len(sorted_colors) > 1:
        return sorted_colors[1]
    # Otherwise, the most frequent color is the background.
    else:
        return sorted_colors[0]

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on the content within the bounding box
    of white pixels, replacing the original background color with white.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input to a numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)

    # Find the predominant background color of the input grid
    background_color = find_background_color(grid)

    # Find the coordinates of all white (0) pixels
    white_coords = np.where(grid == 0)

    # Check if any white pixels were found
    if not white_coords[0].size:
        # If no white pixels, the rule is undefined by examples.
        # Returning an empty or minimal grid might be appropriate.
        # Based on provided examples, white pixels always exist.
        # Let's return a 1x1 white grid as a fallback.
        print("Warning: No white pixels found in input grid.")
        return [[0]]

    # Calculate the bounding box coordinates enclosing all white pixels
    min_row = np.min(white_coords[0])
    max_row = np.max(white_coords[0])
    min_col = np.min(white_coords[1])
    max_col = np.max(white_coords[1])

    # Calculate the dimensions of the output grid
    output_height = max_row - min_row + 1
    output_width = max_col - min_col + 1

    # Create the output grid, initialized entirely with white (0)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through each position within the bounding box in the input grid
    for r_out in range(output_height):
        for c_out in range(output_width):
            # Map the output grid coordinates back to the input grid coordinates
            r_in = min_row + r_out
            c_in = min_col + c_out

            # Get the color of the pixel from the input grid at that position
            input_color = grid[r_in, c_in]

            # If the input pixel's color is NOT the background color,
            # copy its color to the corresponding position in the output grid.
            # Otherwise, leave the output grid pixel as white (0).
            if input_color != background_color:
                output_grid[r_out, c_out] = input_color

    # Convert the final numpy array back to a list of lists for the return value
    return output_grid.tolist()
