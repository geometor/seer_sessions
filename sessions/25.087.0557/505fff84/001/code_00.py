import numpy as np
from typing import List, Tuple

"""
Identify rows in the input grid containing both a blue pixel (1) and an azure pixel (8). 
For each such row, extract the horizontal segment of pixels located strictly between the blue and azure pixels. 
The order of blue and azure doesn't matter; the segment is between the leftmost and rightmost of the two.
Stack these extracted segments vertically, preserving their original relative row order, to form the output grid. 
Pixels not part of these segments, including the blue and azure markers themselves, are excluded from the output. 
Only the colors present in the segments (typically white (0) and red (2)) appear in the output.
"""

def find_indices(row: List[int], value: int) -> List[int]:
    """Finds all indices of a specific value in a list."""
    return [i for i, x in enumerate(row) if x == value]

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid based on blue (1) and azure (8) marker pairs.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    output_rows = [] # Initialize a list to store the rows (segments) for the output grid

    # Iterate through each row of the input grid
    for row in input_grid:
        # Find the column indices of blue (1) pixels in the current row
        blue_indices = find_indices(row, 1)
        # Find the column indices of azure (8) pixels in the current row
        azure_indices = find_indices(row, 8)

        # Check if both a blue pixel and an azure pixel exist in the current row
        # We assume based on examples there's at most one of each relevant marker per row defining a segment.
        # If multiple exist, this takes the first found blue and first found azure index.
        if blue_indices and azure_indices:
            # Get the column index of the (first) blue pixel
            blue_col = blue_indices[0]
            # Get the column index of the (first) azure pixel
            azure_col = azure_indices[0]

            # Determine the leftmost and rightmost column indices of the marker pair
            min_col = min(blue_col, azure_col)
            max_col = max(blue_col, azure_col)

            # Extract the segment of the row strictly between the markers
            # Slicing works correctly even if min_col + 1 == max_col (empty segment)
            segment = row[min_col + 1 : max_col]

            # Only add non-empty segments to the output
            if segment:
                 output_rows.append(segment)

    # Assemble the collected segments into the final output grid
    # If no segments were found, return an empty grid
    return output_rows
