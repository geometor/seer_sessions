```python
import numpy as np

"""
Identify blue (1) marker pixels in the input grid.
Determine if the markers indicate a horizontal or vertical operation based on whether they are confined to the top row or the first column.
Count the number of blue markers (N).
Extract the 'pattern block' which is the portion of the grid before the markers (columns to the left for horizontal, rows above for vertical).
Define a 'separator' line (column of white for horizontal, row of white for vertical) based on the orientation.
Construct the output grid by repeating the pattern block N+1 times, interleaved with N separators, concatenating horizontally or vertically based on the determined orientation.
"""

def find_markers(grid: np.ndarray, marker_color: int) -> list[tuple[int, int]]:
    """Finds all coordinates of a given marker color."""
    coords = np.argwhere(grid == marker_color)
    return [tuple(coord) for coord in coords]

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by repeating a pattern block based on blue markers.
    """
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape
    marker_color = 1
    separator_color = 0

    # Find blue marker pixels
    marker_coords = find_markers(grid, marker_color)

    if not marker_coords:
        # Handle case with no markers if necessary, though examples suggest markers exist.
        # For now, assume markers are always present as per examples.
        # Returning the input might be a safe default, or raise an error.
        return input_grid 

    # Determine orientation and count markers
    n_markers = len(marker_coords)
    first_marker_row, first_marker_col = marker_coords[0]

    # Check if all markers are in the first row
    is_horizontal = all(r == 0 for r, c in marker_coords)
    # Check if all markers are in the first column
    is_vertical = all(c == 0 for r, c in marker_coords)

    if is_horizontal:
        orientation = 'horizontal'
        # Find the column index where markers start
        marker_start_col = min(c for r, c in marker_coords)
        # Pattern block is columns to the left of the marker column
        pattern_block = grid[:, :marker_start_col]
        # Separator is a column of white pixels
        separator = np.full((height, 1), separator_color, dtype=int)
        # Adjust marker count if needed (examples imply N is count, repetition N+1)
        # N = n_markers 
    elif is_vertical:
        orientation = 'vertical'
        # Find the row index where markers start
        marker_start_row = min(r for r, c in marker_coords)
        # Pattern block is rows above the marker row
        pattern_block = grid[:marker_start_row, :]
        # Separator is a row of white pixels
        separator = np.full((1, width), separator_color, dtype=int)
         # Adjust marker count if needed (examples imply N is count, repetition N+1)
        # N = n_markers
    else:
        # Handle unexpected marker configuration (e.g., scattered blue pixels)
        # Based on examples, this case shouldn't occur. Return input or raise error.
        print("Warning: Unexpected marker configuration.")
        return input_grid

    # N is the number of markers, which dictates N repetitions *after* the initial block
    N = n_markers

    # Construct the output grid
    output_grid = pattern_block.copy()

    for _ in range(N):
        if orientation == 'horizontal':
            # Concatenate separator then pattern block horizontally
            output_grid = np.hstack((output_grid, separator, pattern_block))
        else: # vertical
            # Concatenate separator then pattern block vertically
            output_grid = np.vstack((output_grid, separator, pattern_block))

    # Convert back to list of lists
    return output_grid.tolist()
```