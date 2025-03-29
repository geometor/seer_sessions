```python
import numpy as np

"""
Draws the perimeter of the bounding box encompassing the unique red (2), green (3), and yellow (4) pixels found in the input grid.

1.  Identify the locations (row, column) of the single red, green, and yellow pixels.
2.  Determine the minimum and maximum row and column indices (min_row, max_row, min_col, max_col) to define the bounding box containing these three pixels.
3.  Create a copy of the input grid.
4.  Iterate through the cells forming the perimeter of this bounding box.
5.  For each perimeter cell, if its original color in the input grid is white (0), change its color in the copied grid to gray (5). If the perimeter cell contains one of the original marker pixels (red, green, or yellow), leave it unchanged.
6.  Return the modified grid.
"""

def find_pixel_coordinates(grid, color):
    """Finds the coordinates of the first pixel with the specified color."""
    coords = np.argwhere(grid == color)
    if len(coords) > 0:
        return coords[0] # Return row, col
    return None

def transform(input_grid):
    """
    Draws the gray perimeter of the bounding box enclosing the red, green, and yellow pixels.
    """
    input_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_np)
    rows, cols = input_np.shape

    # 1. Identify the locations of the marker pixels
    coord_red = find_pixel_coordinates(input_np, 2)
    coord_green = find_pixel_coordinates(input_np, 3)
    coord_yellow = find_pixel_coordinates(input_np, 4)

    # Ensure all three pixels are found
    if coord_red is None or coord_green is None or coord_yellow is None:
        # Handle cases where not all required pixels are present, maybe return input?
        # For this specific task based on examples, we assume they always exist.
        print("Warning: Not all marker pixels (2, 3, 4) found.")
        return input_grid # Or raise an error

    all_coords = np.array([coord_red, coord_green, coord_yellow])

    # 2. Determine the bounding box
    min_row = np.min(all_coords[:, 0])
    max_row = np.max(all_coords[:, 0])
    min_col = np.min(all_coords[:, 1])
    max_col = np.max(all_coords[:, 1])

    # 3. Create a copy (already done)
    # output_grid = np.copy(input_np)

    # 4. Iterate through the perimeter cells
    # 5. Check original color and update output grid if white
    
    # Top edge
    for c in range(min_col, max_col + 1):
        if input_np[min_row, c] == 0:
            output_grid[min_row, c] = 5
            
    # Bottom edge
    for c in range(min_col, max_col + 1):
         # Check bounds just in case max_row is out of grid range (shouldn't happen if pixels are valid)
        if max_row < rows and input_np[max_row, c] == 0:
             output_grid[max_row, c] = 5

    # Left edge (excluding corners already done)
    for r in range(min_row + 1, max_row):
        # Check bounds
         if min_col < cols and input_np[r, min_col] == 0:
            output_grid[r, min_col] = 5

    # Right edge (excluding corners already done)
    for r in range(min_row + 1, max_row):
        # Check bounds
        if max_col < cols and input_np[r, max_col] == 0:
            output_grid[r, max_col] = 5

    # 6. Return the modified grid
    return output_grid.tolist()
```