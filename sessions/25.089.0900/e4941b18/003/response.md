```python
"""
The transformation involves relocating two specific pixels, red (2) and azure (8), based on their initial positions and the position of a gray (5) rectangular object, while keeping the gray object and the orange (7) background static.

1.  Identify the initial locations of the single red pixel (2) and the single azure pixel (8).
2.  Identify the boundaries of the gray rectangular object (5), specifically its bottom-most row, left-most column, and right-most column.
3.  Create the output grid as a copy of the input grid.
4.  Clear the original position of the red pixel by setting it to the background color (orange 7).
5.  Move the red pixel to the original position of the azure pixel.
6.  Determine the target row for the azure pixel: this is the same row as the bottom edge of the gray rectangle.
7.  Determine the target column for the azure pixel:
    - If the red pixel's initial column is less than or equal to the gray rectangle's left-most column, the target column is one column to the right of the gray rectangle's right-most column.
    - Otherwise, the target column is one column to the left of the gray rectangle's left-most column.
8.  Move the azure pixel to this calculated target position, ensuring it's within the grid boundaries.
"""

import numpy as np

def find_pixel(grid, color):
    """Finds the coordinates (row, col) of the first pixel with the specified color."""
    coords = np.argwhere(grid == color)
    if len(coords) > 0:
        # Return coordinates as standard Python integers
        return (int(coords[0][0]), int(coords[0][1]))
    return None

def find_object_boundaries(grid, color):
    """Finds the min/max row/col indices for pixels of the specified color."""
    coords = np.argwhere(grid == color)
    if len(coords) == 0:
        return None
    # Return boundaries as standard Python integers
    min_row = int(np.min(coords[:, 0]))
    max_row = int(np.max(coords[:, 0]))
    min_col = int(np.min(coords[:, 1]))
    max_col = int(np.max(coords[:, 1]))
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    """
    Transforms the input grid according to the described rules.
    """
    # Convert input list of lists to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy() # Initialize output grid as a copy

    # Define colors
    background_color = 7
    red_color = 2
    azure_color = 8
    gray_color = 5

    # 1. Locate the red and azure pixels in the input
    red_pos_in = find_pixel(grid, red_color)
    azure_pos_in = find_pixel(grid, azure_color)

    # 2. Find the boundaries of the gray object
    gray_boundaries = find_object_boundaries(grid, gray_color)

    # Defensive check: ensure all required elements were found
    if red_pos_in is None or azure_pos_in is None or gray_boundaries is None:
        # If any required element is missing, return the original grid unchanged
        # (or handle error appropriately based on broader context)
        print("Warning: Could not find red, azure, or gray elements as expected.")
        return output_grid.tolist()

    _, gray_row_bottom, gray_col_left, gray_col_right = gray_boundaries
    red_row_in, red_col_in = red_pos_in

    # 3. Apply transformations to the output grid
    # Clear the original red pixel location
    output_grid[red_pos_in] = background_color

    # Move the red pixel to the original azure location
    output_grid[azure_pos_in] = red_color

    # Calculate the target row for the azure pixel
    azure_row_out = gray_row_bottom

    # Calculate the target column for the azure pixel based on red's initial column
    if red_col_in <= gray_col_left:
        azure_col_out = gray_col_right + 1
    else: # red_col_in > gray_col_left
        azure_col_out = gray_col_left - 1

    # Form the final target position for the azure pixel
    azure_pos_out = (azure_row_out, azure_col_out)

    # Get grid dimensions for boundary check
    grid_height, grid_width = output_grid.shape

    # Ensure the target position is within grid bounds before placing the azure pixel
    if 0 <= azure_pos_out[0] < grid_height and 0 <= azure_pos_out[1] < grid_width:
         # Move the azure pixel to its new location
         output_grid[azure_pos_out] = azure_color
    else:
        # Handle case where calculated position is out of bounds, if necessary
        # Based on examples, this might not happen, but it's good practice
        print(f"Warning: Calculated azure position {azure_pos_out} is out of bounds for grid size ({grid_height}x{grid_width}).")
        pass

    # Return the modified grid as a list of lists
    return output_grid.tolist()
```