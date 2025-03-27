```python
import numpy as np

"""
Identify the non-white pixels in the input grid. Determine the minimal bounding box 
that encloses all these non-white pixels. Extract (crop) this rectangular region 
from the input grid to form the output grid.
"""

def find_bounding_box(grid):
    """
    Finds the coordinates of the minimal bounding box containing non-zero pixels.
    
    Args:
        grid (np.array): The input grid.
    
    Returns:
        tuple: (min_row, min_col, max_row, max_col) if non-zero pixels are found,
               otherwise None.
    """
    non_white_pixels = np.argwhere(grid != 0)
    if non_white_pixels.size == 0:
        return None  # No non-white pixels found
    
    min_row = np.min(non_white_pixels[:, 0])
    min_col = np.min(non_white_pixels[:, 1])
    max_row = np.max(non_white_pixels[:, 0])
    max_col = np.max(non_white_pixels[:, 1])
    
    return min_row, min_col, max_row, max_col

def transform(input_grid):
    """
    Extracts the minimal bounding box containing the non-white object.
    
    Args:
        input_grid (list of list of int): The input grid.
        
    Returns:
        list of list of int: The cropped output grid.
    """
    # Convert input list of lists to a numpy array for efficient processing
    grid_np = np.array(input_grid, dtype=int)
    
    # Find the coordinates of the non-white pixels
    # and determine the bounding box
    bounding_box = find_bounding_box(grid_np)
    
    # If no non-white object is found, return an empty grid or handle as appropriate
    # Based on examples, assume an object always exists.
    if bounding_box is None:
        # Or perhaps return the original grid? Or raise an error?
        # For now, returning an empty list to signify no object found.
        return [] 
        
    min_row, min_col, max_row, max_col = bounding_box
    
    # Extract the subgrid defined by the bounding box
    # Note: Slicing in numpy is exclusive for the end index, so add 1
    output_grid_np = grid_np[min_row : max_row + 1, min_col : max_col + 1]
    
    # Convert the resulting numpy array back to a list of lists
    output_grid = output_grid_np.tolist()
    
    return output_grid
```