import numpy as np
from collections import Counter

"""
Identify the central contiguous segment of non-zero pixels in the input 1D array (1xN grid).
Within this segment, find the most frequent non-zero color (dominant color).
Replace all other non-zero colors within this segment with the dominant color.
Leave the leading and trailing zero pixels unchanged.
"""

def find_central_segment_indices(grid_1d):
    """Finds the start and end indices of the central non-zero segment."""
    non_zero_indices = np.where(grid_1d != 0)[0]
    if len(non_zero_indices) == 0:
        return None, None  # No non-zero elements
    start_index = non_zero_indices[0]
    end_index = non_zero_indices[-1] + 1 # End index is exclusive
    return start_index, end_index

def find_dominant_color(segment):
    """Finds the most frequent non-zero color in a segment."""
    if len(segment) == 0:
        return None # No segment or empty segment

    # Filter out zeros if any were included, though segment should be non-zero by definition
    non_zero_segment = segment[segment != 0]
    if len(non_zero_segment) == 0:
        return None # Segment contained only zeros somehow (shouldn't happen with correct segment finding)

    color_counts = Counter(non_zero_segment)
    if not color_counts:
        return None # No non-zero colors found

    # Find the color with the maximum count
    dominant_color = max(color_counts, key=color_counts.get)
    return dominant_color

def transform(input_grid):
    """
    Transforms the input grid by replacing minority colors within the central
    non-zero segment with the dominant color of that segment.

    Args:
        input_grid (np.array): A 1xN numpy array representing the input grid.

    Returns:
        np.array: The transformed 1xN numpy array.
    """
    # Ensure input is a 1D array for easier processing
    if input_grid.shape[0] != 1:
         # Handle potential multi-row grids if needed, or raise error
         # For this specific task description, we assume 1xN
         if input_grid.shape[0] > 1 and input_grid.shape[1] == 1:
             # Treat as 1D if it's Nx1
             grid_1d = input_grid.flatten()
         elif input_grid.shape[0] == 1:
              grid_1d = input_grid[0]
         else:
              # This case is not explicitly handled by the description/examples
              # Let's assume the first row is the target if multiple rows exist
              # Or raise an error depending on stricter interpretation
              # For now, assume input is always 1xN or can be treated as such
               grid_1d = input_grid[0]
               print("Warning: Input grid has multiple rows, processing only the first row.")
    else:
         grid_1d = input_grid[0]


    # Create a copy to modify
    output_grid_1d = grid_1d.copy()

    # 1. Identify the boundaries of the central contiguous segment of non-zero pixels.
    start_index, end_index = find_central_segment_indices(grid_1d)

    # If no central segment exists (e.g., all zeros), return the original grid
    if start_index is None:
        return input_grid # Return original format

    # Extract the central segment
    central_segment = grid_1d[start_index:end_index]

    # 2. Within this central segment, count the frequency and find the dominant color.
    dominant_color = find_dominant_color(central_segment)

    # If no dominant color found (e.g., segment only had zeros - shouldn't happen here)
    # or if the segment was empty (already handled), return original
    if dominant_color is None:
         return input_grid # Return original format

    # 4. Create the output array (already done via copy).
    # 5. Iterate through the pixels within the identified central segment.
    # 6. For each pixel, if its color is non-zero and not the dominant color, change it.
    for i in range(start_index, end_index):
        if output_grid_1d[i] != 0 and output_grid_1d[i] != dominant_color:
            output_grid_1d[i] = dominant_color

    # 7. Pixels outside the central segment are already unchanged.
    # 8. Reshape back to 1xN format and return.
    return output_grid_1d.reshape(1, -1)
