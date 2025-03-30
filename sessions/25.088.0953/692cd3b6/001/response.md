```python
import numpy as np

"""
Identify all non-white pixels in the input grid. 
Calculate the bounding box encompassing all these non-white pixels.
Create an output grid initially identical to the input grid.
Iterate through each pixel within the calculated bounding box. 
If a pixel within the bounding box corresponds to a white pixel (0) in the original input grid, change its color to yellow (4) in the output grid. 
Otherwise, leave the pixel in the output grid unchanged. Pixels outside the bounding box also remain unchanged.
"""

def find_non_white_pixels(grid):
    """Finds the coordinates of all non-white pixels."""
    non_white_coords = np.argwhere(grid != 0)
    # np.argwhere returns coordinates as (row, col) pairs
    return non_white_coords

def calculate_bounding_box(coords):
    """Calculates the bounding box (min_r, min_c, max_r, max_c) from coordinates."""
    if len(coords) == 0:
        return None # No non-white pixels found
    min_r = np.min(coords[:, 0])
    min_c = np.min(coords[:, 1])
    max_r = np.max(coords[:, 0])
    max_c = np.max(coords[:, 1])
    return min_r, min_c, max_r, max_c

def transform(input_grid):
    """
    Fills the bounding box of non-white pixels with yellow (4), 
    only replacing original white (0) pixels within that box.
    """
    # Convert input to numpy array for easier processing
    input_np = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_np)
    
    # 1. Identify all non-white pixels
    non_white_coords = find_non_white_pixels(input_np)
    
    # Handle edge case where there are no non-white pixels
    if len(non_white_coords) == 0:
        return output_grid.tolist() # Return the original grid if no objects found

    # 2. Calculate the bounding box
    min_r, min_c, max_r, max_c = calculate_bounding_box(non_white_coords)
    
    # 4. Iterate through each pixel location (row, column) within the bounding box
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            # 5. Check the color of the corresponding pixel in the *original input* grid
            # 6. If the original input pixel is white (0), change the output pixel to yellow (4)
            if input_np[r, c] == 0:
                output_grid[r, c] = 4
            # 7. If the original input pixel was not white, the output pixel (already copied) remains unchanged.
            
    # 8. Pixels outside the bounding box remain unchanged (as they were copied initially).
    
    # Convert back to list of lists for the expected output format
    return output_grid.tolist()
```