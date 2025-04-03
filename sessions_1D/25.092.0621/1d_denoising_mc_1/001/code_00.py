"""
Identifies a contiguous sequence of non-white pixels within a 1D input grid.
Determines the most frequent non-white color (dominant color) within that sequence.
Replaces all other non-white colors within the sequence with the dominant color.
Pixels outside the sequence (leading/trailing white pixels) remain unchanged.
"""

import numpy as np
from collections import Counter
import copy

def find_non_white_sequence(grid_1d):
    """
    Finds the start and end indices of the first contiguous non-white sequence.

    Args:
        grid_1d: A 1D numpy array representing the grid row.

    Returns:
        A tuple (start_index, end_index) or None if no non-white sequence is found.
        Indices are inclusive.
    """
    non_white_indices = np.where(grid_1d != 0)[0]
    if len(non_white_indices) == 0:
        return None  # No non-white pixels

    start_index = non_white_indices[0]
    end_index = non_white_indices[-1]

    # Verify contiguity (optional but good practice)
    # In this specific task structure (bordered by zeros), the min and max
    # index of non-zero elements define the sequence.
    # If the task allowed multiple sequences separated by zeros, more logic would be needed.
    # sequence_len = end_index - start_index + 1
    # non_white_count_in_range = np.count_nonzero(grid_1d[start_index : end_index + 1])
    # if non_white_count_in_range != sequence_len:
    #     # This indicates zeros within the supposed sequence, which contradicts the task examples
    #     # Handle error or adjust logic if needed
    #     print("Warning: Zeros found within the identified non-white sequence range.")
        
    return start_index, end_index

def get_dominant_color(sequence):
    """
    Finds the most frequent non-white color in a sequence.

    Args:
        sequence: A 1D numpy array representing the non-white sequence.

    Returns:
        The most frequent non-white color value, or None if the sequence is empty or all white.
    """
    non_white_pixels = sequence[sequence != 0]
    if len(non_white_pixels) == 0:
        return None

    color_counts = Counter(non_white_pixels)
    # most_common(1) returns a list of tuples [(color, count)]
    dominant_color, _ = color_counts.most_common(1)[0]
    return dominant_color


def transform(input_grid):
    """
    Transforms the input grid by replacing minority non-white colors within
    a contiguous non-white sequence with the majority non-white color.

    Args:
        input_grid: A list of lists representing the input grid (assumed 1xN).

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Ensure input is a numpy array for easier handling
    # Assuming input is always 1xN as per examples
    if not isinstance(input_grid, np.ndarray):
        input_np = np.array(input_grid, dtype=int)
    else:
        input_np = input_grid.astype(int)

    # Handle empty or non-1D grids if necessary, though examples are 1D
    if input_np.ndim != 2 or input_np.shape[0] != 1:
         # Or handle potential multi-row grids if the task scope expands
        raise ValueError("Input grid must be 1xN")

    grid_1d = input_np[0] # Work with the single row

    # Create a copy to modify
    output_grid_1d = grid_1d.copy()

    # 1. Identify the contiguous sequence of non-white pixels
    sequence_indices = find_non_white_sequence(grid_1d)

    if sequence_indices is None:
        # No non-white sequence found, return the original grid
        return input_np.tolist()

    start_index, end_index = sequence_indices

    # 2. Extract the sequence
    sequence = grid_1d[start_index : end_index + 1]

    # 3. Determine the dominant color within the sequence
    dominant_color = get_dominant_color(sequence)

    if dominant_color is None:
         # Should not happen if sequence_indices were found, but good for safety
         return input_np.tolist()

    # 4. Iterate through the sequence in the output grid and replace noise pixels
    for i in range(start_index, end_index + 1):
        # Check if the pixel is non-white and not the dominant color
        if output_grid_1d[i] != 0 and output_grid_1d[i] != dominant_color:
            # Replace with the dominant color
            output_grid_1d[i] = dominant_color

    # Reshape back to list of lists format
    output_grid = output_grid_1d.reshape(1, -1).tolist()

    return output_grid