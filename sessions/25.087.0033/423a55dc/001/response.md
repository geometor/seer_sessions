```python
"""
This program identifies a single contiguous non-white object in the input grid 
and translates it so that its top-leftmost point aligns with the top-left corner (0, 0) 
of the output grid. The output grid has the same dimensions as the input grid 
and is initially filled with the background color (white, 0).
"""

import numpy as np

def find_object_pixels(grid):
    """
    Identifies all non-background (non-zero) pixels in the grid.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of tuples, where each tuple contains (row, column, color) 
              for a non-background pixel. Returns an empty list if no object is found.
    """
    object_pixels = []
    height, width = grid.shape
    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            if color != 0:
                object_pixels.append((r, c, color))
    return object_pixels

def calculate_bounding_box_top_left(object_pixels):
    """
    Calculates the minimum row and column indices (top-left corner) 
    of the bounding box containing the object pixels.

    Args:
        object_pixels (list): A list of (row, column, color) tuples.

    Returns:
        tuple: A tuple (min_row, min_col), or None if object_pixels is empty.
    """
    if not object_pixels:
        return None
    
    min_row = min(r for r, c, color in object_pixels)
    min_col = min(c for r, c, color in object_pixels)
    return min_row, min_col

def transform(input_grid):
    """
    Transforms the input grid by translating the single non-white object 
    to the top-left corner.

    Args:
        input_grid (list or np.array): The input grid represented as a list of lists or numpy array.

    Returns:
        np.array: The transformed output grid as a numpy array.
    """
    # Convert input to numpy array for easier manipulation
    input_grid_np = np.array(input_grid)
    height, width = input_grid_np.shape

    # 1. Initialize the output grid with the background color (white, 0).
    output_grid = np.zeros_like(input_grid_np)

    # 2. Identify all non-white pixels forming the object.
    object_pixels = find_object_pixels(input_grid_np)

    # If no object is found, return the empty grid
    if not object_pixels:
        return output_grid

    # 3. Find the minimum row and column indices of the object.
    min_row, min_col = calculate_bounding_box_top_left(object_pixels)

    # 4. Translate each object pixel to the new location in the output grid.
    for r, c, color in object_pixels:
        # a. Calculate the corresponding output coordinates.
        new_r = r - min_row
        new_c = c - min_col
        
        # Ensure the new coordinates are within the grid bounds (should always be true if logic is correct)
        if 0 <= new_r < height and 0 <= new_c < width:
             # b. Set the pixel at the new coordinates in the output grid.
            output_grid[new_r, new_c] = color

    # 5. Return the completed output grid.
    return output_grid
```