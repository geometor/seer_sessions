import numpy as np

"""
The transformation identifies the single minimal bounding box that contains all non-white pixels in the input grid. 
It then creates an output grid based on the input grid. 
Within this calculated bounding box, any pixel that was originally white (0) in the input grid is changed to yellow (4) in the output grid. 
Pixels within the bounding box that were not white in the input retain their original color. 
All pixels outside this bounding box retain their original color from the input grid.
"""

def transform(input_grid):
    """
    Fills the overall bounding box of all non-white pixels with yellow (4), 
    only replacing original white (0) pixels within the box.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed grid.
    """
    input_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_np)
    
    # 1. Find coordinates of all non-white pixels (pixels != 0)
    non_white_coords = np.argwhere(input_np != 0)
    
    # 2. Handle the edge case where the grid contains only white pixels.
    #    In this case, no transformation occurs, return the original grid.
    if non_white_coords.shape[0] == 0:
        return output_grid.tolist() 
        
    # 3. Calculate the minimal bounding box encompassing all non-white pixels.
    #    np.min/max on the coordinates array gives the boundaries.
    min_r = np.min(non_white_coords[:, 0])
    max_r = np.max(non_white_coords[:, 0])
    min_c = np.min(non_white_coords[:, 1])
    max_c = np.max(non_white_coords[:, 1])
    
    # 4. Iterate through each pixel location (row r, column c) *within* the bounding box.
    #    The range includes max_r and max_c.
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            # 5. Check if the pixel in the *original* input grid at this location (r, c) is white (0).
            if input_np[r, c] == 0:
                # 6. If it was white in the input, change the corresponding pixel 
                #    in the output grid to yellow (4).
                output_grid[r, c] = 4
            # 7. If the pixel at input_np[r, c] was not white, it retains its 
            #    original color in the output_grid (because output_grid started as a copy).

    # 8. Convert the NumPy array back to a list of lists for the expected output format.
    return output_grid.tolist()