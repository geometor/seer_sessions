import numpy as np
from typing import List

"""
Transformation Rule Natural Language Description:

1. Identify the first occurrence of the maroon pixel (9) which acts as a boundary marker.
2. Consider the segment of the array *before* this boundary marker. If no boundary marker exists, consider the entire array.
3. Within this 'before' segment, locate the contiguous block of non-white (non-0) pixels.
4. Count the number of white (0) pixels in this 'before' segment.
5. Reconstruct the 'before' segment by first placing all the counted white pixels, followed immediately by the contiguous block of non-white pixels.
6. The boundary marker (9), if it exists, and any pixels following it retain their original positions relative to the start of the boundary marker.
7. Combine the reconstructed 'before' segment, the boundary marker (if present), and the 'after' segment (if present) to form the output array.
"""

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input 1D grid according to the described rule.
    Moves all white pixels (0) before the first maroon pixel (9) to the beginning
    of that segment, while keeping the contiguous block of other non-zero colors
    together after the white pixels. Pixels at or after the maroon pixel (9)
    remain unchanged.

    Args:
        input_grid: A list containing a single list representing the 1D input grid.

    Returns:
        A list containing a single list representing the transformed 1D grid.
    """

    # --- Input Processing ---
    # Extract the 1D array from the input grid format
    # Assuming input_grid is always [[...]] for 1D cases based on examples
    if not input_grid or not input_grid[0]:
        return input_grid # Return empty or invalid input as is
    input_array = np.array(input_grid[0])
    
    # --- Core Logic ---
    # 1. Find the index of the boundary marker (maroon pixel, 9)
    boundary_indices = np.where(input_array == 9)[0]
    boundary_index = boundary_indices[0] if len(boundary_indices) > 0 else -1

    # 2. Partition the array based on the boundary index
    if boundary_index != -1:
        segment_before = input_array[:boundary_index]
        boundary_pixel = [input_array[boundary_index]] # Keep as list for concatenation
        segment_after = input_array[boundary_index + 1:]
    else:
        # If no boundary marker, the whole array is the 'before' segment
        segment_before = input_array
        boundary_pixel = []
        segment_after = np.array([]) # Use empty numpy array for consistency

    # 3. Analyze the 'before' segment
    if segment_before.size > 0:
        # 4. Identify the contiguous block of non-white pixels
        # Find all non-zero elements in the 'before' segment
        color_block = segment_before[segment_before != 0]

        # 5. Count the number of white pixels
        num_white = np.sum(segment_before == 0)

        # 6. Reconstruct the 'before' segment
        # Create an array of white pixels
        white_pixels = np.zeros(num_white, dtype=int)
        # Combine white pixels and the color block
        reconstructed_before = np.concatenate((white_pixels, color_block))
    else:
        # If segment_before is empty, the reconstructed part is also empty
        reconstructed_before = np.array([])


    # 7. Combine the parts to form the final output array
    output_array = np.concatenate((reconstructed_before, boundary_pixel, segment_after))

    # --- Output Formatting ---
    # Convert the final NumPy array back to the required list of lists format
    output_grid = [output_array.tolist()]

    return output_grid
