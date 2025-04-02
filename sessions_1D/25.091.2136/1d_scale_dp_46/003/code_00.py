"""
Transforms the input grid based on the following rules:
1. Locate the single maroon (9) pixel at position (R, C).
2. Determine the most frequent color in the entire input grid, excluding white (0) and maroon (9). This is the 'fill_color'.
3. In the row R containing the maroon pixel, identify the contiguous block of white (0) pixels located immediately to the left of the maroon pixel (ending at column C-1).
4. Change the color of all pixels within this contiguous white block to the 'fill_color'.
5. Return the modified grid. If the marker is not found, return the original grid.
"""

import numpy as np
from collections import Counter
import logging # Optional: can be removed if not debugging

# Configure logging - useful for debugging during development, can be commented out
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Helper Functions ---

def _find_pixel_location(grid, color_value):
    """
    Finds the (row, col) coordinates of the first occurrence of a specified color value.

    Args:
        grid (np.array): The input grid (2D NumPy array).
        color_value (int): The color value to search for.

    Returns:
        tuple: A tuple (row, col) if the color is found, otherwise None.
    """
    locations = np.where(grid == color_value)
    if locations[0].size > 0:
        row_index = locations[0][0]
        col_index = locations[1][0]
        # logging.debug(f"Found color {color_value} at ({row_index}, {col_index})")
        return row_index, col_index
    # logging.debug(f"Color {color_value} not found in grid.")
    return None

def _determine_fill_color(grid, exclude_colors=(0, 9)):
    """
    Determines the most frequent color in the grid, excluding specified colors.

    Args:
        grid (np.array): The input grid (2D NumPy array).
        exclude_colors (tuple): Color values to exclude from frequency counting.

    Returns:
        int: The most frequent color value after exclusions. Returns 0 as a fallback
             if no other candidate colors exist.
    """
    flat_grid = grid.flatten()
    color_counts = Counter(flat_grid)
    # logging.debug(f"Initial color counts: {color_counts}")

    for color in exclude_colors:
        if color in color_counts:
            del color_counts[color]
    # logging.debug(f"Counts after excluding {exclude_colors}: {color_counts}")

    if not color_counts:
        # logging.warning("No candidate fill colors found after exclusions. Defaulting to 0.")
        return 0 # Fallback if only excluded colors are present

    fill_color = color_counts.most_common(1)[0][0]
    # logging.debug(f"Determined fill color: {fill_color}")
    return fill_color

# --- Main Transformation Function ---

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input to NumPy array for efficient processing
    grid = np.array(input_grid, dtype=int)
    # logging.info(f"Input grid shape: {grid.shape}")

    # Initialize output_grid as a copy of the input grid
    output_grid = grid.copy()

    # --- Workflow Steps ---

    # 1. Identify the Marker: Locate the maroon (9) pixel.
    marker_location = _find_pixel_location(grid, 9)

    # If the marker pixel (9) is not found, return the original grid unchanged.
    if marker_location is None:
        # logging.warning("Maroon (9) marker pixel not found. Returning original grid.")
        return output_grid.tolist()

    marker_row, marker_col = marker_location
    # logging.info(f"Maroon (9) marker found at: Row={marker_row}, Col={marker_col}")

    # 2. Determine the Fill Color: Find the most frequent color excluding white (0) and maroon (9).
    fill_color = _determine_fill_color(grid, exclude_colors=(0, 9))
    # logging.info(f"Determined fill color: {fill_color}")

    # 3. & 4. Modify the Grid Contiguously:
    # Iterate leftwards from the column immediately left of the marker (C-1).
    # Change contiguous white (0) pixels to the fill_color until a non-white pixel
    # or the start of the row is encountered.
    # logging.info(f"Applying fill color {fill_color} contiguously leftwards from ({marker_row}, {marker_col-1})")
    for col in range(marker_col - 1, -1, -1): # Iterate from C-1 down to 0
        # Check if the current pixel in the output grid is white (0)
        if output_grid[marker_row, col] == 0:
            # If it's white, change its color to the determined fill_color
            output_grid[marker_row, col] = fill_color
            # logging.debug(f"Changed pixel at ({marker_row}, {col}) from 0 to {fill_color}")
        else:
            # If a non-white pixel is encountered, stop the contiguous fill process.
            # logging.debug(f"Encountered non-white pixel at ({marker_row}, {col}). Stopping fill.")
            break # Exit the loop

    # 5. Output: Return the modified grid.
    # Convert the NumPy array back to a list of lists format.
    return output_grid.tolist()