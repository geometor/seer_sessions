"""
Transforms a 9x10 input grid into a 4x5 output grid.
The input grid is partitioned into 6 subgrids (2 rows, 3 columns) by white lines (color 0). The specific subgrid areas are: rows 1-3/cols 1-2, rows 1-3/cols 4-6, rows 1-3/cols 8-9, rows 5-7/cols 1-2, rows 5-7/cols 4-6, rows 5-7/cols 8-9.
The output grid has a 1-pixel white border, and its central 2x3 area (rows 1-2, cols 1-3) is filled based on the input subgrids.
Each cell in the output's central 2x3 area corresponds to one input subgrid in reading order (top-left to bottom-right).
The color of an output cell is determined by finding the most frequent non-white (non-zero) color within its corresponding input subgrid. If there's a tie for the most frequent color, the color with the smallest numerical value is chosen. If a subgrid contains only white pixels, the output cell remains white (0).
"""

import numpy as np
from collections import Counter

def find_most_frequent_non_zero_color(subgrid_array: np.ndarray) -> int:
    """
    Finds the most frequent non-zero value in a numpy array (representing a subgrid),
    breaking ties by choosing the smallest color index.

    Args:
        subgrid_array (np.ndarray): A 2D numpy array representing the subgrid.

    Returns:
        int: The most frequent non-zero color value according to the rules.
             Returns 0 if the subgrid contains only zeros or is empty.
    """
    # Flatten the array to easily iterate through pixels
    pixels = subgrid_array.flatten()
    
    # Filter out zero (white) pixels
    non_zero_pixels = [p for p in pixels if p != 0]
    
    # If there are no non-zero pixels, the color is white (0)
    if not non_zero_pixels:
        return 0
        
    # Count the frequency of each non-zero color
    counts = Counter(non_zero_pixels)
    
    # Determine the maximum frequency
    max_freq = 0
    if counts: # Ensure counts is not empty
      max_freq = max(counts.values())

    # Find all colors with the maximum frequency
    most_frequent_colors = [color for color, freq in counts.items() if freq == max_freq]

    # Tie-breaking rule: choose the smallest color index among the most frequent
    # If most_frequent_colors is somehow empty (shouldn't happen if non_zero_pixels was not empty),
    # returning 0 is a safe fallback, though logically the smallest value from the list is desired.
    if not most_frequent_colors:
        return 0 # Fallback, though unexpected if non_zero_pixels was populated
    return min(most_frequent_colors)


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (np.ndarray): A 9x10 numpy array representing the input grid.

    Returns:
        np.ndarray: A 4x5 numpy array representing the transformed output grid.
    """
    # Initialize the output grid (4x5) filled with white (0)
    output_grid = np.zeros((4, 5), dtype=int)
    
    # Define the input subgrid boundaries (using Python slicing) and their
    # corresponding coordinates in the output grid's central area.
    # Format: (input_row_slice, input_col_slice, output_row_index, output_col_index)
    # Note: Slices are exclusive of the end index.
    subgrid_definitions = [
        # Top row of subgrids mapped to output row 1
        (slice(1, 4), slice(1, 3),   1, 1),  # Input[1:4, 1:3]  -> Output[1, 1]
        (slice(1, 4), slice(4, 7),   1, 2),  # Input[1:4, 4:7]  -> Output[1, 2]
        (slice(1, 4), slice(8, 10),  1, 3),  # Input[1:4, 8:10] -> Output[1, 3] # Note: cols 8-9 means slice(8, 10)
        # Bottom row of subgrids mapped to output row 2
        (slice(5, 8), slice(1, 3),   2, 1),  # Input[5:8, 1:3]  -> Output[2, 1]
        (slice(5, 8), slice(4, 7),   2, 2),  # Input[5:8, 4:7]  -> Output[2, 2]
        (slice(5, 8), slice(8, 10),  2, 3)   # Input[5:8, 8:10] -> Output[2, 3] # Note: cols 8-9 means slice(8, 10)
    ]
    
    # Iterate through each defined subgrid
    for row_slice, col_slice, out_r, out_c in subgrid_definitions:
        # Extract the current subgrid from the input grid
        subgrid = input_grid[row_slice, col_slice]
        
        # Calculate the representative color for this subgrid
        representative_color = find_most_frequent_non_zero_color(subgrid)
        
        # Place the calculated color into the correct cell of the output grid
        output_grid[out_r, out_c] = representative_color
        
    # Return the final transformed grid
    return output_grid