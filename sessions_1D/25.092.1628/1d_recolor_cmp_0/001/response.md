```python
import copy

def find_contiguous_segments(grid_row, target_color):
    """
    Finds contiguous segments of a target color in a 1D grid row.

    Args:
        grid_row (list): A list of integers representing a row of the grid.
        target_color (int): The color value to search for segments of.

    Returns:
        list: A list of tuples, where each tuple represents a segment
              and contains (start_index, end_index, length).
              Returns an empty list if no segments are found.
    """
    segments = []
    start_index = None
    for i, pixel in enumerate(grid_row):
        if pixel == target_color:
            if start_index is None:
                start_index = i  # Start of a potential segment
        elif start_index is not None:
            # End of the segment found
            end_index = i - 1
            length = end_index - start_index + 1
            segments.append((start_index, end_index, length))
            start_index = None # Reset for next segment

    # Check if a segment extends to the end of the row
    if start_index is not None:
        end_index = len(grid_row) - 1
        length = end_index - start_index + 1
        segments.append((start_index, end_index, length))

    return segments

def transform(input_grid):
    """
    Transforms the input grid by identifying contiguous horizontal segments
    of red (2) pixels with a length of exactly 4 and changing their color
    to blue (1). Other pixels remain unchanged.
    """
    # Since the input is described as 1xN, we assume it's a list of lists
    # with one inner list, or just a flat list. We'll handle the flat list case
    # based on the example format. If it's [[...]], access input_grid[0].
    # For simplicity, let's assume input_grid is the flat list directly.
    if not input_grid:
        return []

    # Initialize output_grid as a copy of the input_grid
    # Using list() creates a shallow copy, sufficient for a 1D list of integers.
    output_grid = list(input_grid)

    # Define the target color (red) and the replacement color (blue)
    target_color = 2
    replacement_color = 1
    required_length = 4

    # Find all contiguous segments of the target color (red)
    red_segments = find_contiguous_segments(input_grid, target_color)

    # Iterate through the found segments
    for start_index, end_index, length in red_segments:
        # Check if the segment has the required length
        if length == required_length:
            # Modify the corresponding pixels in the output grid
            for i in range(start_index, end_index + 1):
                output_grid[i] = replacement_color

    # Return the modified grid
    return output_grid
```