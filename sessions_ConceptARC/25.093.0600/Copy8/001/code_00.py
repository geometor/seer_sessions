import numpy as np
from collections import Counter

"""
Identifies the non-zero color with the minimum frequency in the input grid. 
Then, mirrors all cells of that specific color horizontally across the grid's vertical centerline. 
The output grid starts as a copy of the input, and the mirrored cells are added, 
potentially overwriting existing background (0) cells.
"""

def _get_color_frequencies(grid):
    """Counts the frequency of each non-zero color in the grid."""
    # Flatten the grid to a 1D list
    flat_list = [item for sublist in grid for item in sublist]
    # Filter out the background color (0)
    non_zero_colors = [color for color in flat_list if color != 0]
    # Count frequencies
    if not non_zero_colors:
        return {} # Return empty dict if only zeros are present
    return Counter(non_zero_colors)

def _find_min_frequency_color(color_frequencies):
    """Finds the color with the minimum frequency."""
    if not color_frequencies:
        return None # No non-zero colors to choose from
    # Find the color (key) with the minimum frequency (value)
    min_freq_color = min(color_frequencies, key=color_frequencies.get)
    return min_freq_color

def transform(input_grid):
    """
    Transforms the input grid by mirroring the least frequent non-zero color horizontally.

    Args:
        input_grid: A list of lists representing the input 2D grid.

    Returns:
        A list of lists representing the transformed 2D grid.
    """
    # Convert input to numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_array)
    
    # Get grid dimensions
    height, width = input_array.shape
    if height == 0 or width == 0:
        return input_grid # Handle empty grid case

    # 1. & 2. & 3. Identify non-zero colors and count their frequencies
    color_frequencies = _get_color_frequencies(input_grid)

    # 4. Determine the color to mirror (minimum frequency)
    mirror_target_color = _find_min_frequency_color(color_frequencies)

    # If no non-zero colors were found, or grid is empty, return the original
    if mirror_target_color is None:
        return input_grid

    # 5. Get grid width (already done)
    # 6. Iterate through each cell of the input grid
    for r in range(height):
        for c in range(width):
            # 7. Check if the cell color is the target color
            if input_array[r, c] == mirror_target_color:
                # a. Calculate the mirrored column index
                mirrored_col = width - 1 - c
                # b. Set the color in the output grid at the mirrored position
                output_grid[r, mirrored_col] = mirror_target_color

    # 8. Return the modified output grid converted back to list of lists
    return output_grid.tolist()