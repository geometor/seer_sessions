import numpy as np

def find_segments(row, color):
    """
    Finds contiguous segments of a specific color in a 1D array.

    Args:
        row (np.array): A 1D numpy array representing a row of the grid.
        color (int): The color value to search for segments of.

    Returns:
        list: A list of tuples, where each tuple is (start_index, end_index, length).
              Returns an empty list if no segments of the specified color are found.
    """
    segments = []
    start_index = -1
    for i, pixel in enumerate(row):
        if pixel == color and start_index == -1:
            # Start of a new segment
            start_index = i
        elif pixel != color and start_index != -1:
            # End of the current segment
            end_index = i - 1
            length = end_index - start_index + 1
            segments.append((start_index, end_index, length))
            start_index = -1  # Reset for the next segment

    # Check if a segment extends to the end of the row
    if start_index != -1:
        end_index = len(row) - 1
        length = end_index - start_index + 1
        segments.append((start_index, end_index, length))

    return segments

def transform(input_grid):
    """
    Identifies all contiguous horizontal segments of yellow (4) pixels in the input row.
    Calculates the length of each yellow segment.
    Finds the maximum length among these segments.
    If there is exactly one yellow segment with the maximum length, it changes the color
    of all pixels within that segment to magenta (6). Otherwise, the grid remains unchanged.
    All other pixels retain their original color.
    """
    # Ensure input is a numpy array
    input_grid_np = np.array(input_grid)

    # Work with the first (and only) row
    # Create a copy to modify for the output
    output_grid = input_grid_np.copy()
    row = output_grid[0]
    
    # 1. Scan the input grid row to identify all contiguous horizontal segments
    #    composed solely of yellow (4) pixels.
    # 2. Calculate the length of each identified yellow segment.
    yellow_segments = find_segments(row, 4) # 4 is yellow

    # If no yellow segments, return the original grid
    if not yellow_segments:
        return output_grid

    # 3. Determine the maximum length found among all yellow segments.
    max_length = 0
    for start, end, length in yellow_segments:
        if length > max_length:
            max_length = length

    # 4. Identify the yellow segment(s) possessing this maximum length.
    longest_segments = []
    for start, end, length in yellow_segments:
        if length == max_length:
            longest_segments.append((start, end, length))

    # 5. If there is exactly one segment with the maximum length, change the color
    #    of every pixel within that specific segment from yellow (4) to magenta (6).
    # 6. If there is no longest segment or multiple segments share the same maximum
    #    length, make no changes to the grid.
    if len(longest_segments) == 1:
        # Get the details of the uniquely longest segment
        start_idx, end_idx, _ = longest_segments[0]
        
        # Change the color in the output grid row
        for i in range(start_idx, end_idx + 1):
             # 6 is magenta
            row[i] = 6

    # 7. All pixels not part of the uniquely longest yellow segment retain their
    #    original color. (This is handled by modifying the copy).
    
    # 8. Output the resulting grid.
    # The modification was done in place on the row, which is part of output_grid
    return output_grid.tolist() # Return as list of lists per ARC standard