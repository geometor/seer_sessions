
## train_1

**input:**
```
7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7
2 7 7 7 8 7 7 7 7
5 5 5 5 5 5 7 7 7
5 5 5 5 5 5 7 7 7
5 5 5 5 5 5 7 7 7
5 5 5 5 5 5 7 7 7
```


**output:**
```
7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7
7 7 7 7 2 7 7 7 7
5 5 5 5 5 5 7 7 7
5 5 5 5 5 5 7 7 7
5 5 5 5 5 5 7 7 7
5 5 5 5 5 5 8 7 7
```


## train_2

**input:**
```
7 7 7 7 7 7 7
7 7 2 7 8 7 7
7 7 5 5 5 7 7
7 7 5 5 5 7 7
7 7 5 5 5 7 7
7 7 5 5 5 7 7
7 7 5 5 5 7 7
```


**output:**
```
7 7 7 7 7 7 7
7 7 7 7 2 7 7
7 7 5 5 5 7 7
7 7 5 5 5 7 7
7 7 5 5 5 7 7
7 7 5 5 5 7 7
7 7 5 5 5 8 7
```


## train_3

**input:**
```
7 7 7 7 7 7 7 7 7 7 7
7 7 7 8 7 7 2 7 7 7 7
7 7 5 5 5 5 5 5 7 7 7
7 7 5 5 5 5 5 5 7 7 7
7 7 5 5 5 5 5 5 7 7 7
7 7 5 5 5 5 5 5 7 7 7
7 7 5 5 5 5 5 5 7 7 7
7 7 5 5 5 5 5 5 7 7 7
7 7 5 5 5 5 5 5 7 7 7
7 7 5 5 5 5 5 5 7 7 7
7 7 5 5 5 5 5 5 7 7 7
```


**output:**
```
7 7 7 7 7 7 7 7 7 7 7
7 7 7 2 7 7 7 7 7 7 7
7 7 5 5 5 5 5 5 7 7 7
7 7 5 5 5 5 5 5 7 7 7
7 7 5 5 5 5 5 5 7 7 7
7 7 5 5 5 5 5 5 7 7 7
7 7 5 5 5 5 5 5 7 7 7
7 7 5 5 5 5 5 5 7 7 7
7 7 5 5 5 5 5 5 7 7 7
7 7 5 5 5 5 5 5 7 7 7
7 8 5 5 5 5 5 5 7 7 7
```

## Perception

1.  **Grid Structure:** The input and output are grids of varying sizes filled with colors, primarily orange (7), gray (5), red (2), and azure (8).
2.  **Background:** The dominant color is orange (7), acting as the background, which remains static between input and output.
3.  **Key Objects:**
    *   A single red pixel (2).
    *   A single azure pixel (8).
    *   A solid rectangular block of gray pixels (5).
4.  **Transformation:** The core transformation involves changing the positions of the red and azure pixels. The gray block and the orange background remain unchanged.
5.  **Red Pixel Movement:** The red pixel moves from its original location in the input to the location previously occupied by the azure pixel in the input.
6.  **Azure Pixel Movement:** The azure pixel moves from its original location in the input to a new location determined by the position of the gray rectangle. Specifically, it moves to the cell located at the row index of the bottom edge of the gray rectangle and the column index immediately to the right of the right edge of the gray rectangle.
7.  **Interaction:** The movement of the red pixel depends on the initial position of the azure pixel. The final movement of the azure pixel depends on the position (specifically the bottom-right extent) of the gray rectangle.

## Facts


```yaml
task_elements:
  - background:
      color: orange (7)
      shape: grid_fill
      state: static
  - object_1:
      description: Single red pixel
      color: red (2)
      shape: 1x1 pixel
      initial_position: variable (r1_in, c1_in)
      final_position: location of object_2 in input (r2_in, c2_in)
      action: moves
  - object_2:
      description: Single azure pixel
      color: azure (8)
      shape: 1x1 pixel
      initial_position: variable (r2_in, c2_in)
      final_position: calculated based on object_3 (r3_bottom, c3_right + 1)
      action: moves
  - object_3:
      description: Gray rectangle
      color: gray (5)
      shape: rectangle (variable size)
      position: variable (defined by top-left (r3_top, c3_left) and bottom-right (r3_bottom, c3_right))
      state: static
relationships:
  - object_1's final position is determined by object_2's initial position.
  - object_2's final position is determined by object_3's bottom-right boundary.
```


## Natural Language Program

1.  Create the output grid by copying the input grid.
2.  Locate the coordinates of the single red pixel (color 2) in the input grid. Let this be `(red_row_in, red_col_in)`.
3.  Locate the coordinates of the single azure pixel (color 8) in the input grid. Let this be `(azure_row_in, azure_col_in)`.
4.  Identify the gray rectangular block (color 5). Find the maximum row index (`gray_row_bottom`) and maximum column index (`gray_col_right`) occupied by any gray pixel.
5.  Set the pixel at `(red_row_in, red_col_in)` in the output grid to the background color (orange 7).
6.  Set the pixel at `(azure_row_in, azure_col_in)` in the output grid to the color of the red pixel (red 2).
7.  Calculate the target position for the azure pixel: `(gray_row_bottom, gray_col_right + 1)`.
8.  Set the pixel at the calculated target position `(gray_row_bottom, gray_col_right + 1)` in the output grid to the color of the azure pixel (azure 8).
9.  Leave all other pixels (the gray rectangle and the remaining orange background) unchanged from their input values.
```python
"""
The transformation involves relocating two specific pixels, red (2) and azure (8), based on their initial positions and the position of a gray (5) rectangular object, while keeping the gray object and the orange (7) background static.

1.  Identify the initial locations of the single red pixel and the single azure pixel.
2.  Identify the boundaries of the gray rectangular object, specifically its bottom-most row and right-most column.
3.  Create the output grid as a copy of the input grid.
4.  Clear the original position of the red pixel by setting it to the background color (orange).
5.  Move the red pixel to the original position of the azure pixel.
6.  Determine the target position for the azure pixel: it should be in the same row as the bottom edge of the gray rectangle, and in the column immediately to the right of the right edge of the gray rectangle.
7.  Move the azure pixel to this calculated target position.
"""

import numpy as np

def find_pixel(grid, color):
    """Finds the coordinates (row, col) of the first pixel with the specified color."""
    coords = np.argwhere(grid == color)
    if len(coords) > 0:
        return tuple(coords[0])
    return None # Should not happen based on task description

def find_object_boundaries(grid, color):
    """Finds the min/max row/col indices for pixels of the specified color."""
    coords = np.argwhere(grid == color)
    if len(coords) == 0:
        return None # Should not happen for gray object based on task description
    min_row = np.min(coords[:, 0])
    max_row = np.max(coords[:, 0])
    min_col = np.min(coords[:, 1])
    max_col = np.max(coords[:, 1])
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    """
    Transforms the input grid according to the described rules:
    - Moves the red pixel (2) to the original azure pixel's (8) location.
    - Moves the azure pixel (8) relative to the bottom-right of the gray (5) object.
    - Keeps the gray object and orange (7) background static.
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

    if red_pos_in is None or azure_pos_in is None:
        # This case shouldn't occur based on the examples, but handle defensively
        return output_grid.tolist()

    # 2. Find the boundaries of the gray object
    gray_boundaries = find_object_boundaries(grid, gray_color)
    if gray_boundaries is None:
        # This case shouldn't occur based on the examples
        return output_grid.tolist()
    _, gray_row_bottom, _, gray_col_right = gray_boundaries

    # 3. Apply transformations to the output grid
    # Clear the original red pixel location
    output_grid[red_pos_in] = background_color

    # Move the red pixel to the original azure location
    output_grid[azure_pos_in] = red_color

    # Calculate the new azure pixel location
    # Row: bottom edge of gray object
    # Column: one column to the right of the right edge of gray object
    azure_pos_out = (gray_row_bottom, gray_col_right + 1)

    # Ensure the target position is within grid bounds (optional, but good practice)
    # In this specific task, it seems the target is always within bounds or replaces an existing background cell
    if 0 <= azure_pos_out[0] < output_grid.shape[0] and 0 <= azure_pos_out[1] < output_grid.shape[1]:
         # Move the azure pixel to its new location
         output_grid[azure_pos_out] = azure_color
    else:
        # Handle case where calculated position is out of bounds, if necessary
        # Based on examples, this might not happen, but it's a possibility
        # For now, just don't place the pixel if out of bounds
        pass


    # Return the modified grid as a list of lists
    return output_grid.tolist()
```
