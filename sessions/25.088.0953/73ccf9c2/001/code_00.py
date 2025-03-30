import numpy as np

"""
The transformation identifies the non-white pixels in the input grid. 
It then determines the smallest rectangular bounding box that encloses all these non-white pixels. 
Finally, it extracts this rectangular subgrid from the input and returns it as the output. 
The color of the non-white pixels is preserved in the output.
"""

def find_bounding_box(grid):
    """Finds the coordinates of the bounding box containing non-white pixels."""
    non_white_pixels = np.argwhere(grid != 0)
    if non_white_pixels.size == 0:
        # Handle cases with no non-white pixels (return empty or original?)
        # Based on examples, there are always non-white pixels.
        # If needed, could return an empty grid or the original grid.
        # For now, assume valid input based on examples.
        return None 
    
    min_row = non_white_pixels[:, 0].min()
    max_row = non_white_pixels[:, 0].max()
    min_col = non_white_pixels[:, 1].min()
    max_col = non_white_pixels[:, 1].max()
    
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    """
    Extracts the rectangular subgrid defined by the bounding box 
    of all non-white pixels in the input grid.
    """
    # Convert input list of lists to a numpy array for efficient processing
    input_array = np.array(input_grid, dtype=int)
    
    # Find the bounding box coordinates
    bounding_box = find_bounding_box(input_array)
    
    if bounding_box is None:
         # Or handle as appropriate if empty inputs are possible
        return np.array([[]], dtype=int) # Return an empty grid

    min_row, max_row, min_col, max_col = bounding_box
    
    # Extract the subgrid using the bounding box coordinates
    # Note: slicing in numpy is exclusive of the end index, so add 1
    output_grid = input_array[min_row : max_row + 1, min_col : max_col + 1]
    
    return output_grid.tolist() # Convert back to list of lists format if required by ARC standard
