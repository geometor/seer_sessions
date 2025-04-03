```python
import numpy as np

"""
Retain only the endpoints of a single contiguous non-white horizontal segment 
found in the first row of the input grid.
1. Receive the input grid and determine its dimensions.
2. Create a new output grid of the same dimensions, filled with white (0).
3. Examine the first row (index 0) of the input grid.
4. Find the start and end column indices of the contiguous non-white segment in this row.
5. If a segment exists:
    a. Get the color of the segment from the input grid's first row.
    b. Set the pixels in the output grid's first row at the start and end column indices to this color.
6. Return the output grid.
"""

def find_segment_indices(row):
    """
    Finds the start and end indices of the first contiguous non-zero segment in a 1D array.

    Args:
        row: A 1D numpy array representing a row of pixels.

    Returns:
        A tuple (start_index, end_index). Returns (-1, -1) if no non-zero
        pixel is found or the row is empty.
    """
    # Find indices of all non-zero elements
    non_zero_indices = np.where(row != 0)[0]

    # If no non-zero elements are found, return (-1, -1)
    if len(non_zero_indices) == 0:
        return -1, -1

    # The start index is the first non-zero index
    start_index = non_zero_indices[0]
    # The end index is the last non-zero index
    end_index = non_zero_indices[-1]

    return start_index, end_index

def transform(input_grid):
    """
    Transforms the input grid by keeping only the endpoints of the first
    contiguous non-white segment found in the first row.

    Args:
        input_grid: A list of lists or numpy array representing the input grid.

    Returns:
        A numpy array representing the transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)

    # Handle empty input
    if input_array.size == 0:
        return input_array.tolist() # Return empty list for empty input

    # Get grid dimensions
    height, width = input_array.shape

    # Initialize the output grid with zeros (white)
    output_array = np.zeros_like(input_array)

    # Extract the first row (handle case of 1D input represented as single row)
    if height > 0:
        first_row = input_array[0, :]
    else:
         # Should not happen if size > 0, but good practice
         return output_array.tolist()

    # Find the start and end indices of the non-white segment in the first row
    start_index, end_index = find_segment_indices(first_row)

    # If a segment was found (start_index is not -1)
    if start_index != -1:
        # Get the color from the input segment's start point (or any point in segment)
        segment_color = first_row[start_index]

        # Set the start endpoint in the first row of the output grid
        output_array[0, start_index] = segment_color

        # Set the end endpoint in the first row of the output grid
        # This correctly handles segments of length 1 where start_index == end_index
        output_array[0, end_index] = segment_color

    # Return the output grid as a list of lists
    return output_array.tolist()
```