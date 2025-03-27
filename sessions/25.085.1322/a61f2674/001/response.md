```python
import numpy as np

def find_vertical_segments(grid, color):
    """
    Finds all contiguous vertical segments of a specified color in the grid.

    Args:
        grid (np.array): The input grid.
        color (int): The color value to search for.

    Returns:
        list: A list of tuples, where each tuple represents a segment
              (column_index, start_row, end_row, length).
    """
    segments = []
    height, width = grid.shape
    for c in range(width):
        start_row = -1
        for r in range(height):
            # Check if current pixel is the target color
            if grid[r, c] == color:
                # If it's the start of a new segment
                if start_row == -1:
                    start_row = r
            # Check if the segment ends
            # Segment ends if pixel is not the target color OR it's the last row
            if grid[r, c] != color or r == height - 1:
                # If we were tracking a segment
                if start_row != -1:
                    # Determine the end row
                    end_row = r - 1 if grid[r, c] != color else r
                    length = end_row - start_row + 1
                    segments.append((c, start_row, end_row, length))
                    # Reset start_row for the next potential segment in this column
                    start_row = -1
    return segments

def transform(input_grid):
    """
    Identifies the longest and shortest vertical contiguous segments of gray (5)
    pixels in the input grid. In the output grid, pixels corresponding to the
    longest segment(s) are colored blue (1), pixels corresponding to the
    shortest segment(s) are colored red (2), and all other pixels are white (0).
    """
    # Convert input to numpy array for easier processing
    np_grid = np.array(input_grid, dtype=int)
    height, width = np_grid.shape

    # Initialize output grid with white (0)
    output_grid = np.zeros_like(np_grid)

    # Find all vertical gray (5) segments
    gray_segments = find_vertical_segments(np_grid, 5)

    # If no gray segments found, return the all-white grid
    if not gray_segments:
        return output_grid.tolist() # Convert back to list of lists

    # Extract lengths and find min/max
    segment_lengths = [length for _, _, _, length in gray_segments]
    min_length = min(segment_lengths)
    max_length = max(segment_lengths)

    # Color the longest segments blue (1)
    for col, start_row, end_row, length in gray_segments:
        if length == max_length:
            output_grid[start_row : end_row + 1, col] = 1

    # Color the shortest segments red (2)
    # This will overwrite blue if a segment is both the longest and shortest
    # (i.e., all segments have the same length)
    for col, start_row, end_row, length in gray_segments:
        if length == min_length:
            output_grid[start_row : end_row + 1, col] = 2

    # Return the result as a list of lists
    return output_grid.tolist()
```