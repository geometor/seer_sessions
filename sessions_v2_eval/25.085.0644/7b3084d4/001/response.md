```python
import numpy as np

def find_bounding_box(grid):
    """
    Finds the minimum bounding box containing all non-white pixels.
    
    Args:
        grid (np.array): The input grid.
        
    Returns:
        tuple: (min_row, max_row, min_col, max_col) or None if no non-white pixels.
    """
    non_white_pixels = np.argwhere(grid != 0)
    if non_white_pixels.size == 0:
        return None  # No non-white pixels found
        
    min_row = np.min(non_white_pixels[:, 0])
    max_row = np.max(non_white_pixels[:, 0])
    min_col = np.min(non_white_pixels[:, 1])
    max_col = np.max(non_white_pixels[:, 1])
    
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    """
    Extracts the smallest rectangular subgrid containing all non-white pixels 
    from the input grid.
    
    1. Convert the input list of lists to a numpy array.
    2. Find the coordinates of all pixels that are not white (value != 0).
    3. If no non-white pixels exist, return a 1x1 grid containing white (0).
    4. Determine the minimum and maximum row and column indices (bounding box) 
       that enclose all these non-white pixels.
    5. Extract the subgrid defined by this bounding box from the input array.
    6. Convert the resulting numpy array back to a list of lists.
    """
    # Convert input to numpy array for efficient processing
    grid_np = np.array(input_grid, dtype=int)
    
    # Find the bounding box of non-white pixels
    bbox = find_bounding_box(grid_np)
    
    # Handle case where input is all white
    if bbox is None:
        return [[0]] # Return a 1x1 white grid as per observation refinement
        
    min_row, max_row, min_col, max_col = bbox
    
    # Extract the subgrid using the bounding box coordinates
    # Slicing is [start_row:end_row+1, start_col:end_col+1]
    output_grid_np = grid_np[min_row : max_row + 1, min_col : max_col + 1]
    
    # Convert the resulting numpy array back to a list of lists
    output_grid = output_grid_np.tolist()
    
    return output_grid

```