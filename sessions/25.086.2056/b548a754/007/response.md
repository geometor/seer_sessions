```python
import numpy as np

"""
Identifies a primary shape (contiguous non-white, non-azure pixels) and a single azure marker pixel (8) in the input grid.
The azure pixel indicates how to extend the primary shape.
If the azure pixel is to the right of the shape's rightmost edge, the shape is extended horizontally to the right. The pattern for extension is taken from the column *just inside* the rightmost edge (index max_col - 1) of the original shape. This pattern is copied into the columns from the original right edge + 1 up to and including the column of the azure pixel.
If the azure pixel is below the shape's bottom edge, the shape is extended vertically downwards. The pattern for extension is taken from the row *just inside* the bottom edge (index max_row - 1) of the original shape. This pattern is copied into the rows from the original bottom edge + 1 up to and including the row of the azure pixel.
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
    pattern from the row/column just inside the relevant edge.
    """
    # Convert input list of lists to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    # 1. Initialize the output_grid as a copy of the input_grid
    output_grid = np.copy(grid)

    # 2. Locate the single azure pixel (color 8) and record its coordinates
    marker_pos = find_marker(grid)

    if marker_pos is None:
        # If no marker exists, return the original input_grid (as list of lists)
        # Ensure conversion to list of lists before returning
        return grid.tolist()

    marker_row, marker_col = marker_pos

    # 3. Set the pixel at (marker_row, marker_col) in the output_grid to white (0).
    # Do this *after* finding the shape to avoid issues if marker is adjacent
    # Update: Do this *before* checking bounds, but after finding marker
    output_grid[marker_row, marker_col] = 0

    # 4. Identify the main shape and its bounding box using the original grid
    shape_bounds = find_shape_bounds(grid) # Use original grid to define shape

    if shape_bounds is None:
         # If no shape exists, return the output_grid (with the marker removed)
         return output_grid.tolist()

    min_row, max_row, min_col, max_col = shape_bounds

    # 5. Determine the extension direction and apply the transformation
    # Check for horizontal extension (marker to the right)
    # We also implicitly assume marker_row is within [min_row, max_row] based on examples
    if marker_col > max_col:
        # Check if shape width allows for index max_col - 1
        if max_col - 1 >= min_col:
            # Define the pattern as the column JUST INSIDE the rightmost edge (max_col - 1)
            pattern = grid[min_row : max_row + 1, max_col - 1]

            # Iterate through columns from edge+1 *up to and including* marker's column
            for c in range(max_col + 1, marker_col + 1):
                # Ensure we don't write out of bounds horizontally
                if c < output_grid.shape[1]:
                    # Apply the pattern to the output grid for the relevant rows
                    output_grid[min_row : max_row + 1, c] = pattern
        else:
             # Handle case where shape is only 1 column wide - unclear from examples what to do.
             # For now, maybe repeat the single column? Let's try repeating max_col itself.
             # Re-evaluating: The pattern logic implies an *inner* pattern. If width=1, there's no inner pattern distinct from the edge.
             # Let's stick to the rule "use max_col-1". If width=1, max_col-1 < min_col, so this block won't execute.
             # This seems safer than guessing an alternative rule.
             pass


    # Check for vertical extension (marker below)
    # We also implicitly assume marker_col is within [min_col, max_col] based on examples
    elif marker_row > max_row:
         # Check if shape height allows for index max_row - 1
        if max_row - 1 >= min_row:
            # Define the pattern as the row JUST INSIDE the bottom edge (max_row - 1)
            pattern = grid[max_row - 1, min_col : max_col + 1]

            # Iterate through rows from edge+1 *up to and including* marker's row
            for r in range(max_row + 1, marker_row + 1):
                 # Ensure we don't write out of bounds vertically
                if r < output_grid.shape[0]:
                    # Apply the pattern to the output grid for the relevant columns
                    output_grid[r, min_col : max_col + 1] = pattern
        else:
             # Handle case where shape is only 1 row tall - similar logic to horizontal.
             # If height=1, max_row-1 < min_row, so this block won't execute.
             pass

    # 6. Return the modified output_grid as a list of lists
    return output_grid.tolist()
```