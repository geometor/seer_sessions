import numpy as np
from scipy.ndimage import label, find_objects

"""
Transforms an input grid based on the locations of blue (1), green (3), and yellow (4) pixels.
1. Initialize a new grid (output) with the same dimensions as the input grid, filling it entirely with the background color azure (8).
2. Identify all distinct contiguous shapes in the input grid that are composed of blue (1) or green (3) pixels. Count the number of shapes found.
3. Locate the single yellow (4) pixel in the input grid and note its column index.
4. Conditional Step: If the total number of blue/green shapes found is greater than one:
    a. For each individual blue/green shape identified:
        i. Determine the minimum bounding box enclosing that specific shape.
        ii. Fill the rectangular area defined by this bounding box with red (2) pixels in the output grid.
5. Fill the entire column corresponding to the yellow pixel's column index with red (2) pixels in the output grid. This overwrites any pixels previously set in that column.
6. Return the modified output grid.
"""

def transform(input_grid):
    """
    Applies the described transformation to the input grid.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    # Convert input_grid to numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    rows, cols = input_grid_np.shape
    background_color = 8
    fill_color = 2
    shape_colors = [1, 3] # blue, green
    marker_color = 4 # yellow

    # 1. Initialize output_grid with background color
    output_grid = np.full_like(input_grid_np, background_color)

    # 2. Identify all distinct contiguous blue (1) or green (3) shapes and count them
    shape_mask = np.isin(input_grid_np, shape_colors)
    # Use 8-connectivity (diagonal included) which seems standard for ARC shapes
    labeled_array, num_features = label(shape_mask, structure=np.ones((3,3), dtype=bool)) 
    # find_objects returns a list of slice tuples for each feature
    object_slices = find_objects(labeled_array) 

    # 3. Locate the single yellow (4) pixel and its column index
    marker_pixel_coords = np.argwhere(input_grid_np == marker_color)
    marker_col = -1 # Initialize with invalid value
    if marker_pixel_coords.size > 0:
        # Assuming there's only one yellow pixel as per observation
        marker_col = marker_pixel_coords[0, 1]

    # 4. Conditional Step: If more than one shape, draw bounding boxes
    if num_features > 1:
        # For each individual shape's bounding box slice
        for obj_slice in object_slices:
            # Fill the bounding box area with the fill color
            output_grid[obj_slice] = fill_color

    # 5. Fill the entire column identified by the marker with red (2)
    if marker_col != -1: # Check if marker was found
        output_grid[:, marker_col] = fill_color

    # 6. Return the modified output grid as list of lists
    return output_grid.tolist()