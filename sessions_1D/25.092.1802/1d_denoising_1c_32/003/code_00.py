import numpy as np
import itertools

"""
Identify the single non-white color present in the input grid (a 1D sequence of pixels).
Scan the input grid horizontally to find all contiguous segments composed solely of this non-white color. Record the start index, end index, and length of each segment.
Compare the lengths of all segments and select the segment with the maximum length. If multiple segments share the maximum length, the one appearing earliest in the grid scanning process is chosen.
Create a new output grid of the same dimensions as the input, filled entirely with the background color (white, 0).
Copy the pixels of the selected longest segment from their original positions in the input grid to the corresponding positions in the new output grid.
If the input contains only white pixels or no segments of the non-white color, return an all-white grid.
"""

def find_segments(grid_row, target_color):
    """
    Finds contiguous segments of a specific color in a 1D list (grid row).

    Args:
        grid_row (list or np.array): The input 1D sequence representing a row of the grid.
        target_color (int): The color of the segments to find.

    Returns:
        list: A list of tuples, where each tuple represents a segment
              (start_index, end_index, length). end_index is exclusive.
              Returns an empty list if no segments are found.
    """
    segments = []
    start_index = -1
    for i, pixel in enumerate(grid_row):
        if pixel == target_color and start_index == -1:
            # Start of a potential segment
            start_index = i
        elif pixel != target_color and start_index != -1:
            # End of the current segment (pixel at i is not part of it)
            end_index = i
            length = end_index - start_index
            segments.append((start_index, end_index, length))
            start_index = -1 # Reset for the next segment

    # Check if the row ends with an active segment
    if start_index != -1:
        # The segment runs to the end of the row
        end_index = len(grid_row)
        length = end_index - start_index
        segments.append((start_index, end_index, length))

    return segments

def transform(input_grid):
    """
    Transforms the input grid by keeping only the longest contiguous segment
    of the non-background color.

    Args:
        input_grid (list): A 1D list representing the input grid row.

    Returns:
        list: A 1D list representing the transformed output grid row.
    """
    # Convert input list to numpy array for efficient operations
    input_array = np.array(input_grid)
    
    # Initialize output grid with the background color (white = 0)
    # Use the same dimensions as the input grid.
    output_array = np.zeros_like(input_array)

    # 1. Examine the input grid to identify the unique non-white color present.
    non_white_colors = np.unique(input_array[input_array != 0])

    # If no non-white color exists, return the all-white grid.
    if non_white_colors.size == 0:
        return output_array.tolist()

    # Assume only one non-white color per task based on examples
    target_color = non_white_colors[0]

    # 2. Scan the input grid to find all contiguous segments of the target color.
    # 3. Record start, end, and length for each segment.
    segments = find_segments(input_array, target_color)

    # If no segments of the target color are found, return the all-white grid.
    if not segments:
        return output_array.tolist()

    # 4. Compare segment lengths and determine the maximum length.
    # 5. Select the segment with the maximum length.
    #    max() with a key naturally selects the first encountered element in case of ties.
    longest_segment = max(segments, key=lambda item: item[2]) # item[2] is the length

    # Extract start and end indices of the longest segment
    start, end, _ = longest_segment

    # 6. Create a new output grid (already initialized above).
    # 7. Copy the pixels of the longest segment into the new output grid.
    output_array[start:end] = input_array[start:end]

    # 8. Return the newly constructed output grid as a list.
    return output_array.tolist()