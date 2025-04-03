import numpy as np

"""
Transforms a 1D grid by identifying contiguous horizontal segments of red (2) pixels 
and changing their color based on the length of the segment.
- Segments of length 1 become blue (1).
- Segments of length 2 become maroon (9).
- Segments of length 3 become gray (5).
White (0) pixels remain unchanged.
"""

def get_color_for_length(length):
  """Maps segment length to the target color."""
  if length == 1:
    return 1  # blue
  elif length == 2:
    return 9  # maroon
  elif length == 3:
    return 5  # gray
  else:
    # In case of unexpected lengths, perhaps return original or a default.
    # Based on examples, lengths other than 1, 2, 3 shouldn't occur for red segments.
    # Returning the original red color (2) might be safest if rules are incomplete.
    # However, for this specific task, we expect only 1, 2, or 3. Let's raise an error if unexpected.
     raise ValueError(f"Unexpected segment length: {length}")


def transform(input_grid):
    """
    Applies the color transformation rule to the input grid.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.
                                Expected to have only one row for this task.

    Returns:
        np.array: The transformed 2D numpy array.
    """
    # Ensure input is a numpy array
    if not isinstance(input_grid, np.ndarray):
        input_grid = np.array(input_grid)

    # Check if grid is effectively 1D (has only one row)
    if input_grid.shape[0] != 1:
        raise ValueError("Input grid must have exactly one row for this transformation.")

    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    
    # Get the dimensions (only need width)
    height, width = input_grid.shape

    # Iterate through the single row to find red segments
    current_segment_start = -1
    current_segment_length = 0
    
    for col in range(width):
        pixel = input_grid[0, col]
        
        if pixel == 2: # Red pixel
            if current_segment_length == 0: # Start of a new segment
                current_segment_start = col
            current_segment_length += 1
        else: # Not a red pixel
            if current_segment_length > 0: # End of a red segment
                # Determine the new color based on the length
                new_color = get_color_for_length(current_segment_length)
                # Apply the new color to the segment in the output grid
                output_grid[0, current_segment_start : current_segment_start + current_segment_length] = new_color
                # Reset segment tracking
                current_segment_length = 0
                current_segment_start = -1

    # Handle case where a red segment ends at the very last pixel of the row
    if current_segment_length > 0:
        new_color = get_color_for_length(current_segment_length)
        output_grid[0, current_segment_start : current_segment_start + current_segment_length] = new_color

    return output_grid