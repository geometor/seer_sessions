```python
import numpy as np

"""
Identify all horizontal contiguous segments of orange (7) pixels in the input grid.
Determine the length of each segment. Find the maximum length among these segments.
Change the color of all orange segments that have this maximum length to yellow (4).
Leave all other pixels unchanged.
"""

def find_horizontal_segments(grid, color):
    """
    Finds all horizontal contiguous segments of a specified color in the grid.

    Args:
        grid (np.array): The input grid.
        color (int): The color value to search for.

    Returns:
        list: A list of tuples, where each tuple represents a segment:
              (row_index, start_col_index, end_col_index, length).
    """
    segments = []
    rows, cols = grid.shape
    for r in range(rows):
        start_col = None
        for c in range(cols):
            # Start of a potential segment
            if grid[r, c] == color and start_col is None:
                start_col = c
            # End of a segment (either color changes or end of row)
            if start_col is not None:
                if grid[r, c] != color: # Color changed before end of row
                    end_col = c - 1
                    length = end_col - start_col + 1
                    segments.append((r, start_col, end_col, length))
                    start_col = None
                elif c == cols - 1: # Segment reaches the end of the row
                    end_col = c
                    length = end_col - start_col + 1
                    segments.append((r, start_col, end_col, length))
                    start_col = None # Reset for safety, though loop ends
    return segments

def transform(input_grid):
    """
    Transforms the input grid by changing the color of the longest horizontal
    orange (7) segments to yellow (4).

    Args:
        input_grid (list of lists or np.array): The input grid.

    Returns:
        np.array: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    grid_np = np.array(input_grid, dtype=int)
    output_grid = grid_np.copy()
    orange_color = 7
    yellow_color = 4

    # 1. & 2. Find all horizontal orange segments and their lengths
    orange_segments = find_horizontal_segments(grid_np, orange_color)

    # If no orange segments exist, return the original grid
    if not orange_segments:
        return output_grid

    # 3. Find the maximum length among the orange segments
    max_length = 0
    for _, _, _, length in orange_segments:
        if length > max_length:
            max_length = length

    # 4. & 5. Iterate through segments and change color if length is maximum
    for r, start_c, end_c, length in orange_segments:
        if length == max_length:
            # Change the color of pixels in this segment to yellow
            for c in range(start_c, end_c + 1):
                output_grid[r, c] = yellow_color

    # 6. Other pixels (background, shorter orange segments) are already preserved
    #    in the initial copy.

    # 7. Return the resulting grid
    return output_grid.tolist() # Convert back to list of lists if needed, though numpy array is often fine

```