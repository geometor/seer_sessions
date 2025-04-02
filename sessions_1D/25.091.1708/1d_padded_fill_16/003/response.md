```python
import numpy as np
from typing import List, Tuple, Optional

"""
Processes a 2D grid row by row. For each row, it identifies if there are any 
non-background (non-zero) pixels. If non-background pixels exist, it determines 
the unique color of these pixels (assuming only one non-background color per row) 
and finds the horizontal span they occupy by locating the column index of the 
leftmost (minimum index) and rightmost (maximum index) pixel of that color. 
The corresponding row in the output grid is then filled with this non-background 
color between the leftmost and rightmost column indices (inclusive). All other 
pixels in that output row are set to the background color (0). If a row in the 
input grid contains only background pixels, the corresponding row in the output 
grid also contains only background pixels. The output grid has the same dimensions 
as the input grid.
"""

def _find_row_span(row: np.ndarray) -> Optional[Tuple[int, int, int]]:
    """
    Finds the color, min column index, and max column index of non-background pixels in a row.

    Args:
        row: A 1D numpy array representing a row of the grid.

    Returns:
        A tuple (color, min_col, max_col) if non-background pixels are found,
        otherwise None. Returns the single non-background color present.
        Assumes only one non-background color exists per relevant row.
    """
    # Find indices of all non-background (non-zero) pixels
    non_bg_indices = np.where(row != 0)[0]

    # If no non-background pixels are found, return None
    if non_bg_indices.size == 0:
        return None

    # Determine the color (assuming only one non-background color per row)
    # Take the color of the first non-background pixel found
    color = row[non_bg_indices[0]] 
    
    # Find the minimum (leftmost) and maximum (rightmost) column indices
    min_col = np.min(non_bg_indices)
    max_col = np.max(non_bg_indices)
    
    return color, min_col, max_col

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid by filling the horizontal span between the 
    leftmost and rightmost non-background pixels in each row.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input list of lists to a numpy array for efficient processing
    input_np = np.array(input_grid, dtype=int)
    
    # Get the dimensions of the grid
    num_rows, num_cols = input_np.shape
    
    # Initialize the output grid with the same dimensions as the input, 
    # filled entirely with the background color (0)
    output_np = np.zeros_like(input_np)

    # Iterate through each row of the input grid
    for r in range(num_rows):
        # Get the current row from the input grid
        current_row = input_np[r, :]
        
        # Find the color and span (min/max columns) of non-background pixels in the row
        span_info = _find_row_span(current_row)
        
        # If non-background pixels were found in this row
        if span_info is not None:
            color, min_col, max_col = span_info
            
            # Fill the corresponding segment in the output row with the determined color
            # Slicing includes min_col but excludes max_col + 1, achieving inclusive filling
            output_np[r, min_col : max_col + 1] = color
            
        # Else (row contained only background pixels), the output row remains 
        # all background (as initialized with zeros), so no action is needed.

    # Convert the resulting numpy array back to a list of lists format for the output
    return output_np.tolist()

```