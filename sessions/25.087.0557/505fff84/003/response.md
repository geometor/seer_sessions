```python
import numpy as np
from typing import List, Tuple, Union

"""
Identify rows in the input grid containing both a blue pixel (1) and an azure pixel (8). 
For each such row, find the first occurring blue pixel and the first occurring azure pixel. 
Extract the horizontal segment of pixels located strictly between these two marker pixels (their order, left-to-right or right-to-left, does not matter). 
Collect all non-empty extracted segments, preserving their original relative row order from the input grid. 
Return these segments as a list of lists, where each inner list represents a row in the output grid. If no such segments are found, return an empty list.
"""

# Helper function to find indices, kept separate for clarity
def find_indices(row: Union[List[int], np.ndarray], value: int) -> List[int]:
    """Finds all indices of a specific value in a list or 1D numpy array."""
    return [i for i, x in enumerate(row) if x == value]

def transform(input_grid: Union[List[List[int]], np.ndarray]) -> List[List[int]]:
    """
    Transforms the input grid by extracting segments between blue (1) and azure (8) markers.

    Args:
        input_grid: A grid represented as a list of lists or a numpy array.

    Returns:
        A list of lists representing the output grid, containing the extracted segments.
        Returns an empty list if no valid segments are found.
    """
    output_rows: List[List[int]] = [] # Initialize a list to store the rows (segments) for the output grid

    # Iterate through each row of the input grid
    # This works whether input_grid is a list of lists or a numpy array
    for row in input_grid:
        # Find the column indices of blue (1) pixels in the current row
        blue_indices = find_indices(row, 1)
        # Find the column indices of azure (8) pixels in the current row
        azure_indices = find_indices(row, 8)

        # Check if both a blue pixel and an azure pixel exist in the current row
        if blue_indices and azure_indices:
            # Get the column index of the first blue pixel found
            blue_col = blue_indices[0]
            # Get the column index of the first azure pixel found
            azure_col = azure_indices[0]

            # Determine the leftmost and rightmost column indices of this marker pair
            min_col = min(blue_col, azure_col)
            max_col = max(blue_col, azure_col)

            # Extract the segment of the row strictly between the markers
            # Slicing works correctly even if min_col + 1 == max_col (results in empty slice)
            # The type of 'segment' might be list or np.ndarray depending on 'row' type
            segment = row[min_col + 1 : max_col]

            # Ensure the segment is converted to a standard Python list
            # This addresses potential downstream issues with mixed types or numpy array comparisons
            segment_list = list(segment)

            # Only add non-empty segments to the output
            if segment_list: # Check the list representation
                 output_rows.append(segment_list)

    # Return the collected segments as a list of lists
    return output_rows
```