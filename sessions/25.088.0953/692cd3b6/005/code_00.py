import numpy as np

"""
Identify all non-white pixels in the input grid.
Calculate the minimal bounding box that encompasses *all* these non-white pixels (the overall bounding box).
Create an output grid initialized as a copy of the input grid.
Iterate through each pixel location (row, column) within this overall bounding box.
If the corresponding pixel in the original input grid at this location is white (0), change the corresponding pixel in the output grid to yellow (4).
Otherwise (if the original pixel is not white), the pixel in the output grid retains its original color from the input grid.
Pixels outside the overall bounding box remain unchanged from the input grid.
"""

def transform(input_grid):
    """
    Fills the overall bounding box of all non-white pixels with yellow (4), 
    only replacing original white (0) pixels within the box.
    """
    input_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_np)
    
    # 1. Find coordinates of all non-white pixels
    non_white_coords = np.argwhere(input_np != 0)
    
    # 2. Handle case where there are no non-white pixels
    if non_white_coords.shape[0] == 0:
        return output_grid.tolist() # Return the original grid
        
    # 3. Calculate the overall bounding box
    min_r = np.min(non_white_coords[:, 0])
    max_r = np.max(non_white_coords[:, 0])
    min_c = np.min(non_white_coords[:, 1])
    max_c = np.max(non_white_coords[:, 1])
    
    # 4. Iterate through each pixel within the overall bounding box
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            # 5. Check if the pixel in the *original* input grid is white (0)
            if input_np[r, c] == 0:
                # 6. If it's white, change the corresponding pixel in the output grid to yellow (4)
                output_grid[r, c] = 4
            # 7. If it's not white, it retains its original color (already copied)

    # Convert back to list of lists for the expected output format
    return output_grid.tolist()
