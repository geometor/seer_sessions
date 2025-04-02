"""
Transforms the input grid by identifying the single non-background foreground color, 
determining the bounding box (minimum and maximum row and column indices) containing 
all pixels of that color, and then filling this entire rectangular area in the 
output grid with the foreground color. Pixels outside this bounding box remain 
the background color (0).
"""

import numpy as np

def find_foreground_color(grid: np.ndarray) -> int:
    """
    Finds the single non-background (non-zero) color in the grid.
    Assumes exactly one non-background color exists if any.
    Returns 0 if only the background color is present.
    """
    unique_colors = np.unique(grid)
    for color in unique_colors:
        if color != 0:
            return int(color) # Return the first non-zero color found
    return 0 # Return 0 if only background color (0) is found

def find_bounding_box(grid: np.ndarray, color: int) -> tuple | None:
    """
    Finds the min row, max row, min col, max col for a given color.
    Returns None if the color is not found in the grid.
    """
    # Find all row and column indices where the grid matches the color
    rows, cols = np.where(grid == color)
    
    # Check if any pixels of the specified color were found
    if rows.size == 0: 
        return None # Color not found
        
    # Determine the min/max row and column indices
    min_row = np.min(rows)
    max_row = np.max(rows)
    min_col = np.min(cols)
    max_col = np.max(cols)
    
    # Return the bounding box coordinates as integers
    return int(min_row), int(max_row), int(min_col), int(max_col)

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the bounding box fill transformation to the input grid.
    
    Args:
        input_grid: A list of lists representing the input grid.
        
    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input list of lists to numpy array for efficient processing
    input_array = np.array(input_grid, dtype=int)
    
    # Create an output grid with the same dimensions as the input, 
    # initialized entirely with the background color (0).
    output_array = np.zeros_like(input_array)
    
    # 1. Identify the single non-white color (C)
    foreground_color = find_foreground_color(input_array)
    
    # Proceed only if a foreground color exists (is not 0)
    if foreground_color != 0:
        # 2. Find the bounding box of the foreground color
        bounding_box = find_bounding_box(input_array, foreground_color)
        
        # 3. If a bounding box was found (which it should be if foreground_color != 0)
        if bounding_box is not None:
            min_row, max_row, min_col, max_col = bounding_box
            
            # 4. Fill the rectangular region defined by the bounding box 
            #    in the output grid with the foreground color.
            #    Numpy slicing is [start_row:end_row, start_col:end_col]
            #    where end_row and end_col are *exclusive*. Add 1 to max_row/max_col
            #    to make the slice inclusive of the max indices.
            output_array[min_row : max_row + 1, min_col : max_col + 1] = foreground_color
            
    # 5. Convert the output numpy array back to a list of lists and return
    return output_array.tolist()