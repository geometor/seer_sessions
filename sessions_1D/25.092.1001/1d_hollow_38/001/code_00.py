"""
Find the contiguous horizontal segment of non-white pixels within the input grid.
Record the color of this segment, its starting column index, and its ending column index.
Create an output grid identical in size to the input grid, filled entirely with white pixels (0).
In the output grid, change the color of the pixel at the recorded starting column index to the recorded color.
In the output grid, change the color of the pixel at the recorded ending column index to the recorded color.
The resulting grid is the final output.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by keeping only the start and end pixels of a
    contiguous horizontal non-white segment.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.
                                       Expected to be a single row.

    Returns:
        list[list[int]]: A 2D list representing the transformed grid.
    """
    # Convert input to numpy array for easier processing
    input_array = np.array(input_grid, dtype=int)

    # Since the grid is always 1 row, we can work with the first row directly
    row = input_array[0]

    # Find the indices of all non-white pixels (pixels != 0)
    non_white_indices = np.where(row != 0)[0]

    # Check if there are any non-white pixels
    if len(non_white_indices) == 0:
        # If the input row is all white, return it as is (or an empty grid of same size)
        # Based on examples, there's always a segment, but this handles the edge case.
        return input_grid # Or np.zeros_like(input_array).tolist()

    # Identify the start index (first non-white pixel)
    start_index = non_white_indices[0]
    # Identify the end index (last non-white pixel)
    end_index = non_white_indices[-1]

    # Get the color of the segment (all non-white pixels in the segment have the same color)
    segment_color = row[start_index]

    # Initialize the output grid with the same shape as the input, filled with white (0)
    output_grid = np.zeros_like(input_array)

    # Place the segment color at the start position in the output grid
    output_grid[0, start_index] = segment_color

    # Place the segment color at the end position in the output grid
    # This handles the case where start_index == end_index (segment of length 1) correctly
    output_grid[0, end_index] = segment_color

    # Convert the output numpy array back to a list of lists before returning
    return output_grid.tolist()