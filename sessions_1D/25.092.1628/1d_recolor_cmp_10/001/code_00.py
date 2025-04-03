import copy

def find_azure_segments(grid):
    """
    Identifies contiguous segments of azure (8) pixels in a 1D grid.

    Args:
        grid (list[int]): The input 1D grid (list of color integers).

    Returns:
        list[tuple[int, int, int]]: A list of segments, where each segment is represented
                                     by a tuple (start_index, end_index, length).
                                     Returns an empty list if no azure segments are found.
    """
    segments = []
    in_segment = False
    start_index = -1
    for i, pixel in enumerate(grid):
        if pixel == 8 and not in_segment:
            # Start of a new segment
            in_segment = True
            start_index = i
        elif pixel != 8 and in_segment:
            # End of the current segment
            in_segment = False
            end_index = i - 1
            length = end_index - start_index + 1
            segments.append((start_index, end_index, length))

    # Handle segment that goes to the end of the grid
    if in_segment:
        end_index = len(grid) - 1
        length = end_index - start_index + 1
        segments.append((start_index, end_index, length))

    return segments

def transform(input_grid):
    """
    Transforms the input grid by finding the longest contiguous segment of azure (8)
    pixels and changing its color to orange (7). If multiple segments share the
    maximum length, the first one encountered is chosen. Other pixels remain unchanged.
    """

    # Find all contiguous segments of azure (8) pixels
    azure_segments = find_azure_segments(input_grid)

    # If no azure segments are found, return the original grid
    if not azure_segments:
        return copy.deepcopy(input_grid) # Return a copy to avoid modifying the input directly

    # Find the longest segment(s)
    max_length = 0
    for start, end, length in azure_segments:
        if length > max_length:
            max_length = length

    # Select the first segment that has the maximum length
    longest_segment = None
    for segment in azure_segments:
        if segment[2] == max_length:
            longest_segment = segment
            break # Found the first longest segment

    # Initialize output_grid as a copy of the input grid
    output_grid = copy.deepcopy(input_grid)

    # Recolor the pixels within the selected longest segment
    if longest_segment:
        start, end, _ = longest_segment
        for i in range(start, end + 1):
            if output_grid[i] == 8: # Double-check it's still azure
                output_grid[i] = 7 # Change to orange

    return output_grid