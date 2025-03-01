"""
1. **Identify the foreground shape:** Locate the contiguous region of red (2) pixels within the input grid.
2. **Isolate Input region:** define a region that contains only colors 0 and 2 (white and red).
3. **Crop:**  Create a bounding box around the red shape. I will refer to this box as B.
4. **Remove background:** remove all azure (8) pixels. The box, B, contains only red and white pixels.
5.  **Resize:** reduce the height and width of the bounding box, B, by half, rounding down.
6. **Output:** The resulting cropped, filtered, and resized grid is the output.
"""

import numpy as np

def find_bounding_box(grid, color):
    # Find coordinates of pixels with the specified color
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return None  # Handle cases with no specified color
    # Find minimum and maximum coordinates to define the bounding box
    min_row, min_col = coords.min(axis=0)
    max_row, max_col = coords.max(axis=0)
    return min_row, min_col, max_row, max_col

def transform(input_grid):
    # Convert input grid to a NumPy array
    input_grid = np.array(input_grid)

    # Isolate region with colors 0 and 2
    isolated_grid = np.where((input_grid == 0) | (input_grid == 2), input_grid, -1) #mark other color -1

    # Find the bounding box around the red shape (color 2)
    min_row, min_col, max_row, max_col = find_bounding_box(isolated_grid, 2)

    # Crop the isolated region based on the bounding box.
    cropped_grid = isolated_grid[min_row:max_row+1, min_col:max_col+1]

    # Calculate new dimensions (half, rounded down)
    new_height = cropped_grid.shape[0] // 2
    new_width = cropped_grid.shape[1] // 2

    # Resize using nearest-neighbor interpolation (simplest approach)
    # First, create the indices for the new dimensions.
    rows = np.linspace(0, cropped_grid.shape[0]-1, new_height, dtype=int)
    cols = np.linspace(0, cropped_grid.shape[1]-1, new_width, dtype=int)
    
    # Perform the indexing using meshgrid
    output_grid = cropped_grid[np.ix_(rows,cols)]
    
    
    return output_grid.tolist()