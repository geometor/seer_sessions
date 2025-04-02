```python
"""
Transforms the input grid by identifying the single non-background foreground color, 
finding all rows containing this color, determining the overall horizontal extent 
(minimum and maximum columns) of the color across these rows, and then filling 
this horizontal extent with the foreground color *only* on those specific rows 
in the output grid. The rest of the output grid remains the background color (0).
"""

import numpy as np

def find_foreground_locations(grid: np.ndarray) -> tuple | None:
    """
    Finds the foreground color, the rows it appears in, and its min/max column extent.

    Args:
        grid: The input grid as a numpy array.

    Returns:
        A tuple containing:
        - foreground_color (int): The non-zero color found.
        - unique_rows (list[int]): Sorted list of unique row indices containing the color.
        - min_col (int): The minimum column index where the color appears.
        - max_col (int): The maximum column index where the color appears.
        Returns None if no non-zero color is found.
    """
    unique_colors = np.unique(grid)
    foreground_color = 0
    for color in unique_colors:
        if color != 0:
            foreground_color = int(color)
            break
            
    if foreground_color == 0:
        return None # No foreground color found

    rows, cols = np.where(grid == foreground_color)
    
    if rows.size == 0: # Should not happen if foreground_color != 0, but safety check
        return None
        
    unique_rows = sorted(list(np.unique(rows)))
    min_col = int(np.min(cols))
    max_col = int(np.max(cols))
    
    return foreground_color, unique_rows, min_col, max_col

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.
    
    Args:
        input_grid: A list of lists representing the input grid.
        
    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input list of lists to numpy array for efficient processing
    input_array = np.array(input_grid, dtype=int)
    
    # Initialize output grid with the same shape, filled with background color (0)
    output_array = np.zeros_like(input_array)
    
    # Find the foreground color, its rows, and its horizontal extent
    locations = find_foreground_locations(input_array)
    
    # If a foreground color and its locations were found
    if locations:
        foreground_color, unique_rows, min_col, max_col = locations
        
        # Iterate through only the rows where the foreground color was originally present
        for r in unique_rows:
            # Fill the horizontal span (min_col to max_col) on this specific row
            # Numpy slicing is [start:end], where end is exclusive, so add 1 to max_col
            output_array[r, min_col:max_col + 1] = foreground_color
            
    # Convert the output numpy array back to a list of lists and return
    return output_array.tolist()
```