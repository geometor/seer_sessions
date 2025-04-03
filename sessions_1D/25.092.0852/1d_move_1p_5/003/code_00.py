"""
Identifies a single contiguous horizontal segment (block) of non-white pixels 
in a single-row input grid and shifts this block one position to the right 
in the output grid. The background remains white, and the grid size is preserved. 
If the shift causes the block to extend beyond the right boundary, it is truncated.
"""

import numpy as np

def find_non_white_segment(grid_row):
    """
    Finds the first contiguous segment of non-white pixels in a grid row.

    Args:
        grid_row: A 1D numpy array representing the row.

    Returns:
        A tuple (start_index, end_index, color) if found, otherwise None.
        start_index: The starting column index of the segment.
        end_index: The ending column index (inclusive) of the segment.
        color: The color of the pixels in the segment.
    """
    non_white_indices = np.where(grid_row != 0)[0]
    if non_white_indices.size == 0:
        return None # No non-white pixels found

    start_index = -1
    end_index = -1
    color = 0
    in_segment = False
    
    for i, pixel in enumerate(grid_row):
        if pixel != 0:
            if not in_segment:
                start_index = i
                color = pixel
                in_segment = True
            end_index = i # Keep updating end_index while in segment
        elif in_segment:
            # We've reached the end of the first segment
            break
            
    if start_index != -1:
         return start_index, end_index, color
    else:
         # This case should theoretically not be reached if non_white_indices was not empty,
         # but included for robustness.
         return None


def transform(input_grid):
    """
    Transforms the input grid by shifting the non-white horizontal segment 
    one position to the right.

    Args:
        input_grid: A numpy array representing the input grid.

    Returns:
        A numpy array representing the transformed grid.
    """
    # Ensure input is a NumPy array
    input_grid = np.array(input_grid, dtype=int)

    # Handle empty input grid case
    if input_grid.size == 0:
        return np.array([[]], dtype=int) # Return empty grid in correct format

    # Get grid dimensions
    height, width = input_grid.shape

    # Initialize output_grid with the same shape and background color (0)
    output_grid = np.zeros_like(input_grid)

    # Since the examples are all 1 row high, we process the first row.
    # If the task evolves to handle multiple rows, this logic would need adjustment.
    if height > 0:
        input_row = input_grid[0, :]

        # Find the non-white segment in the input row
        segment_info = find_non_white_segment(input_row)

        if segment_info:
            start_index, end_index, color = segment_info
            block_length = end_index - start_index + 1

            # Calculate the new starting position for the segment
            new_start_index = start_index + 1

            # Determine the actual end position (exclusive) for slicing, respecting boundaries
            # Numpy slicing automatically handles out-of-bounds on the upper end
            new_end_index_exclusive = new_start_index + block_length

            # Place the segment in the output grid at the new position
            # Ensure the starting index is within bounds before attempting to write
            if new_start_index < width:
                 output_grid[0, new_start_index:new_end_index_exclusive] = color

        # If no segment was found, output_grid remains all zeros (white),
        # which is correct as per the observed transformation.
        # If the input had non-white pixels but find_segment returned None (error case),
        # it would also return all white.

    # Copy any other rows directly if the problem generalizes later (currently no examples)
    if height > 1:
        output_grid[1:, :] = input_grid[1:, :]


    return output_grid.tolist() # Return as list of lists per ARC standard