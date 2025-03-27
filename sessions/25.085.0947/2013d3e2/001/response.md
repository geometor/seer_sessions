```python
import numpy as np
from typing import List, Tuple, Optional

"""
Transforms an input grid by extracting a 3x3 subgrid. 
The top-left corner of the subgrid is determined as follows:
1. If the input grid contains any blue pixels (color 1), the top-left corner is the location (row, column) of the uppermost, then leftmost blue pixel.
2. If the input grid does not contain any blue pixels, the top-left corner is the location (row, column) of the uppermost, then leftmost non-white pixel (colors 1-9).
The 3x3 subgrid starting at this determined corner is then returned as the output.
"""

def find_top_left_pixel(grid: np.ndarray, color: int) -> Optional[Tuple[int, int]]:
    """
    Finds the coordinates (row, col) of the first occurrence of a specific color,
    searching row by row, then column by column (top-leftmost).

    Args:
        grid: The input NumPy array representing the grid.
        color: The integer color value to search for.

    Returns:
        A tuple (row, col) if the color is found, otherwise None.
    """
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color:
                return r, c
    return None

def find_non_white_bounding_box_top_left(grid: np.ndarray) -> Optional[Tuple[int, int]]:
    """
    Finds the top-left corner coordinates (min_row, min_col) of the
    bounding box containing all non-white pixels.

    Args:
        grid: The input NumPy array representing the grid.

    Returns:
        A tuple (min_row, min_col) if non-white pixels exist, otherwise None.
    """
    non_white_pixels = np.argwhere(grid != 0) # Find indices where grid is not 0
    if non_white_pixels.size == 0:
        return None # No non-white pixels found
    
    min_row = np.min(non_white_pixels[:, 0])
    min_col = np.min(non_white_pixels[:, 1])
    return min_row, min_col

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the 3x3 extracted output grid.
    """
    # Convert input to numpy array for easier manipulation
    grid_np = np.array(input_grid, dtype=int)
    
    start_row, start_col = -1, -1

    # 1. Check for blue pixels (color 1)
    blue_coords = find_top_left_pixel(grid_np, 1)

    # 2. Determine the starting coordinates for extraction
    if blue_coords is not None:
        # If blue is present, use its top-leftmost coordinates
        start_row, start_col = blue_coords
        # print(f"Blue found at: ({start_row}, {start_col})") # Debugging
    else:
        # If blue is not present, find the top-left of the non-white bounding box
        non_white_coords = find_non_white_bounding_box_top_left(grid_np)
        if non_white_coords is not None:
            start_row, start_col = non_white_coords
            # print(f"Non-white bounding box top-left: ({start_row}, {start_col})") # Debugging
        else:
            # Handle edge case where the grid is entirely white (though unlikely based on task)
            # Defaulting to top-left 0,0 and hoping it fits, or raise error?
            # Based on examples, extraction always seems possible.
            # If this case happens, returning a 3x3 of white might be safest.
            # Let's assume valid inputs mean extraction is always possible based on rules.
            # If we hit this, something is wrong with the assumptions or input.
             print("Warning: Grid has no blue and no non-white pixels. Cannot determine start point.")
             # Returning a default or raising an error might be needed depending on requirements.
             # For now, let's assume valid input means one of the conditions will find coordinates.
             # If start_row/col remain -1, slicing below will fail. Add explicit check.
             if start_row == -1 or start_col == -1:
                 raise ValueError("Could not determine the starting point for extraction.")


    # 3. Extract the 3x3 subgrid
    # Ensure the slice indices are valid
    grid_height, grid_width = grid_np.shape
    end_row = min(start_row + 3, grid_height)
    end_col = min(start_col + 3, grid_width)
    
    # Perform the extraction
    output_grid_np = grid_np[start_row:end_row, start_col:end_col]

    # Check if the extracted grid is indeed 3x3, pad if necessary (though problem implies it fits)
    # Based on problem description, we expect a 3x3 output. If extraction is smaller,
    # it might indicate an issue or require padding, but let's stick to direct extraction first.
    if output_grid_np.shape != (3, 3):
         print(f"Warning: Extracted grid is not 3x3. Actual shape: {output_grid_np.shape}")
         # Consider padding logic here if required by future examples.
         # For now, proceed with the potentially smaller grid.
         # Re-evaluating: The examples strictly show 3x3 output. The slicing should guarantee this
         # unless the start point is too close to the edge. Let's assume valid inputs allow 3x3 extraction.

    # 4. Convert the output numpy array back to a list of lists
    output_grid = output_grid_np.tolist()

    return output_grid
```