```python
"""
Extracts a 3x3 subgrid from the input grid. The extraction anchor point depends on the presence of a blue pixel (color 1).
1. Search for the top-leftmost blue pixel (minimum row, then minimum column).
2. If a blue pixel is found, its coordinates (r, c) become the anchor point.
3. If no blue pixel is found, find the top-left corner (min_r, min_c) of the bounding box containing all non-white pixels (color > 0). This corner becomes the anchor point.
4. Extract the 3x3 subgrid starting at the determined anchor point (anchor_r, anchor_c), covering input[anchor_r : anchor_r + 3, anchor_c : anchor_c + 3].
"""

import numpy as np

def find_top_left_color(grid, color):
    """
    Finds the row and column of the top-leftmost pixel with the specified color.
    Scans row by row, then column by column.

    Args:
        grid (np.array): The input grid.
        color (int): The color value to search for.

    Returns:
        tuple or None: A tuple (row, col) if the color is found, otherwise None.
    """
    height, width = grid.shape
    for r in range(height):
        for c in range(width):
            if grid[r, c] == color:
                return (r, c)
    return None

def find_non_white_bbox_top_left(grid):
    """
    Finds the minimum row and minimum column index of any non-white pixel.

    Args:
        grid (np.array): The input grid.

    Returns:
        tuple or None: A tuple (min_row, min_col) if non-white pixels exist,
                       otherwise None.
    """
    non_white_indices = np.argwhere(grid != 0) # Find indices where color is not 0 (white)
    if non_white_indices.size == 0:
        return None  # Grid contains only white pixels (or is empty)
    min_row = non_white_indices[:, 0].min() # Minimum row index among non-white pixels
    min_col = non_white_indices[:, 1].min() # Minimum column index among non-white pixels
    return (min_row, min_col)

def transform(input_grid):
    """
    Extracts a 3x3 subgrid from the input grid based on the anchor point rules.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        np.array: A 3x3 numpy array representing the extracted output grid.
                  Returns a 3x3 grid of zeros if no anchor point can be determined
                  (e.g., input is all white).
    """
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape
    blue_color = 1
    start_row, start_col = -1, -1 # Initialize with invalid values

    # 1. Search for the top-leftmost blue pixel
    blue_pixel_loc = find_top_left_color(input_grid_np, blue_color)

    # 2. If blue pixel found, use its location as anchor
    if blue_pixel_loc is not None:
        start_row, start_col = blue_pixel_loc
        # print(f"Blue pixel found at: ({start_row}, {start_col})") # Debug info

    # 3. Else (no blue pixel), use non-white bounding box top-left as anchor
    else:
        bbox_top_left = find_non_white_bbox_top_left(input_grid_np)
        if bbox_top_left is not None:
            # Use the bounding box top-left directly as the anchor
            start_row, start_col = bbox_top_left
            # print(f"No blue pixel. Bbox TL: {bbox_top_left}. Start: ({start_row}, {start_col})") # Debug info
        else:
            # Handle case where no blue pixel AND no non-white pixels are found
            # (e.g., input is all white). Return a 3x3 white grid.
            # print("Warning: No blue pixel and no non-white pixels found. Returning 3x3 white grid.") # Debug info
            return np.zeros((3, 3), dtype=int)

    # Basic check if calculated anchor is somehow invalid (should not happen based on ARC task examples)
    # An anchor point should always allow for a 3x3 extraction if found according to rules.
    if start_row < 0 or start_col < 0 or start_row + 3 > height or start_col + 3 > width:
         # print(f"Warning: Calculated extraction start ({start_row}, {start_col}) leads to out-of-bounds for input size ({height}x{width}). Returning 3x3 white grid.") # Debug info
         # Returning a default; this suggests an issue either with the input violating assumptions or a flaw in the logic if it occurs.
         return np.zeros((3, 3), dtype=int)

    # 4. Extract the 3x3 subgrid using the determined anchor point
    output_grid = input_grid_np[start_row : start_row + 3, start_col : start_col + 3]

    # Final check to ensure output is 3x3 (numpy slicing should handle this correctly if anchor is valid)
    if output_grid.shape != (3, 3):
         # print(f"Warning: Extracted grid shape is {output_grid.shape}, expected (3, 3). Problem with start indices ({start_row}, {start_col}) or input size. Returning 3x3 white grid.") # Debug info
         # Fallback for unexpected slicing results
         return np.zeros((3, 3), dtype=int)

    return output_grid
```