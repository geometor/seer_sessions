```python
import numpy as np

"""
Identifies a primary shape (contiguous non-white, non-azure pixels) and a single azure marker pixel (8) in the input grid.
The azure pixel indicates how to extend the primary shape.
If the azure pixel is to the right of the shape's rightmost edge, the shape is extended horizontally to the right. The pattern for extension is taken from the column *at* the rightmost edge (index max_col) of the original shape. This pattern is copied into the columns from the original right edge + 1 up to and including the column of the azure pixel.
If the azure pixel is below the shape's bottom edge, the shape is extended vertically downwards. The pattern for extension is taken from the row *at* the bottom edge (index max_row) of the original shape. This pattern is copied into the rows from the original bottom edge + 1 up to and including the row of the azure pixel.
The azure marker pixel is removed (set to white 0) in the output grid.
"""

def find_marker(grid):
    """Finds the coordinates (row, col) of the first azure (8) pixel."""
    marker_coords = np.where(grid == 8)
    if len(marker_coords[0]) > 0:
        # Return the coordinates of the first marker found
        return int(marker_coords[0][0]), int(marker_coords[1][0])
    return None # No marker found

def find_shape_bounds(grid):
    """Finds the bounding box [min_row, max_row, min_col, max_col] of non-white (0) and non-azure (8) pixels."""
    shape_coords = np.where((grid != 0) & (grid != 8))
    if len(shape_coords[0]) > 0:
        min_row = int(np.min(shape_coords[0]))
        max_row = int(np.max(shape_coords[0]))
        min_col = int(np.min(shape_coords[1]))
        max_col = int(np.max(shape_coords[1]))
        return min_row, max_row, min_col, max_col
    return None # No shape found

def transform(input_grid):
    """
    Extends a shape based on the position of an azure marker pixel, using the
    pattern from the row/column at the relevant edge.
    """
    # Convert input list of lists to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    # 1. Initialize the output_grid as a copy of the input_grid
    output_grid = np.copy(grid)

    # 2. Locate the single azure pixel (color 8) and record its coordinates
    marker_pos = find_marker(grid)

    if marker_pos is None:
        # If no marker exists, return the original input_grid (as list of lists)
        return input_grid

    marker_row, marker_col = marker_pos

    # 3. Set the pixel at (marker_row, marker_col) in the output_grid to white (0).
    output_grid[marker_row, marker_col] = 0

    # 4. Identify the main shape and its bounding box
    shape_bounds = find_shape_bounds(grid)

    if shape_bounds is None:
         # If no shape exists, return the output_grid (with the marker removed)
         return output_grid.tolist()

    min_row, max_row, min_col, max_col = shape_bounds

    # 5. Determine the extension direction and apply the transformation
    # Check for horizontal extension (marker to the right)
    if marker_col > max_col:
        # Define the pattern as the column AT the rightmost edge (max_col)
        pattern = grid[min_row : max_row + 1, max_col]

        # Iterate through columns from edge+1 *up to and including* marker's column
        for c in range(max_col + 1, marker_col + 1):
            # Ensure we don't write out of bounds horizontally
            if c < output_grid.shape[1]:
                # Apply the pattern to the output grid for the relevant rows
                output_grid[min_row : max_row + 1, c] = pattern

    # Check for vertical extension (marker below) - use elif assuming only one direction per task
    elif marker_row > max_row:
        # Define the pattern as the row AT the bottom edge (max_row)
        pattern = grid[max_row, min_col : max_col + 1]

        # Iterate through rows from edge+1 *up to and including* marker's row
        for r in range(max_row + 1, marker_row + 1):
             # Ensure we don't write out of bounds vertically
            if r < output_grid.shape[0]:
                # Apply the pattern to the output grid for the relevant columns
                output_grid[r, min_col : max_col + 1] = pattern

    # 6. Return the modified output_grid as a list of lists
    return output_grid.tolist()
```