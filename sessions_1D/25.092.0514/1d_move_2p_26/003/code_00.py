import numpy as np
from typing import List, Tuple

"""
Identifies the single contiguous horizontal segment of non-white pixels in the 
input row. Creates a new output row of the same dimensions, initialized to white (0).
Copies the identified segment into the output row, shifted two positions to the right.
Pixels shifted beyond the right boundary are discarded.
"""

def find_colored_segment_np(row: np.ndarray) -> Tuple[int, int, int]:
    """
    Finds the start index, end index (inclusive), and color of the first 
    contiguous non-white segment in a numpy row.
    Returns (-1, -1, 0) if no segment is found.
    Assumes only one segment exists based on the task description.
    """
    non_white_indices = np.where(row != 0)[0]
    if non_white_indices.size == 0:
        return -1, -1, 0  # No segment found

    start_index = non_white_indices[0]
    end_index = non_white_indices[-1]
    segment_color = row[start_index] # Color of the first pixel in the segment

    # Verify contiguity (optional but good practice if assumption might be violated)
    # expected_indices = np.arange(start_index, end_index + 1)
    # if not np.array_equal(non_white_indices, expected_indices):
    #     # Handle error or unexpected input: multiple segments or gaps
    #     print("Warning: Non-contiguous or multiple segments found, using the span of the first.")
        # Depending on exact rules, might need adjustment. 
        # For this task, assuming contiguity holds per examples.

    return start_index, end_index, segment_color

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Shifts the single horizontal colored segment found in the input grid's row
    two positions to the right.

    Args:
        input_grid: A list containing a single list (the row) of pixel values,
                    or potentially a NumPy array.

    Returns:
        A list containing a single list representing the transformed row.
    """
    # Convert input to numpy array for easier processing
    # Assuming input_grid is always [[row_data]]
    input_row_np = np.array(input_grid[0], dtype=int)
    grid_width = input_row_np.shape[0]

    # Initialize the output row with white (0) pixels
    output_row_np = np.zeros_like(input_row_np)

    # Find the colored segment in the input row
    start_index, end_index, segment_color = find_colored_segment_np(input_row_np)

    # If a segment was found, calculate its new position and place it
    if start_index != -1:
        # Calculate the new start index (shifted right by 2)
        new_start_index = start_index + 2
        segment_length = end_index - start_index + 1

        # Copy the segment to the new position in the output row
        # Iterate through the *original* segment indices to get the color
        for i in range(segment_length):
            current_original_index = start_index + i
            current_output_index = new_start_index + i
            
            # Check if the new position is within the grid bounds
            if 0 <= current_output_index < grid_width:
                # Assign the color from the original segment
                output_row_np[current_output_index] = segment_color 
                # Alternative using slicing:
                # output_row_np[new_start_index : new_start_index + segment_length] = \
                #     input_row_np[start_index : end_index + 1]
                # Need to handle boundary clipping with slicing carefully.
                # The loop handles clipping automatically.


    # Convert the output numpy row back to the required list of lists format
    output_grid = [output_row_np.tolist()]
    
    return output_grid