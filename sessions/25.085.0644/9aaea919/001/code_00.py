import numpy as np
from scipy.ndimage import label, find_objects
from collections import Counter

"""
Transformation Rule Natural Language Description:

1.  Identify the background color (most frequent color in the grid).
2.  Create an output grid initialized as a copy of the input grid.
3.  Find all distinct contiguous objects in the input grid that are not the background color.
4.  For each object:
    a.  Determine its shape, size (bounding box), location, and color.
    b.  **Rule 1 (Bottom Line Removal):** If the object is a 1x5 horizontal line located entirely within the bottom-most row of the grid, change all pixels belonging to this object in the output grid to the background color.
    c.  **Rule 2 (Plus Sign Color Change):** If the object forms a 3x3 "plus" shape (5 pixels: center and 4 orthogonal neighbors), check its color:
        i.  If the color is Maroon (9), Magenta (6), or Green (3), change the 5 pixels forming the plus sign in the output grid to Gray (5).
        ii. If the color is any other color (White 0, Blue 1, Red 2, Yellow 4, Orange 7, Azure 8), leave the object pixels unchanged in the output grid.
    d.  Objects that do not match Rule 1 or Rule 2 are left unchanged.
5.  Return the modified output grid.
"""

def find_background_color(grid):
    """Finds the most frequent color in the grid."""
    colors, counts = np.unique(grid, return_counts=True)
    return colors[np.argmax(counts)]

def transform(input_grid):
    """
    Applies the transformation rules to the input grid.
    Removes 1x5 horizontal lines from the bottom row.
    Changes the color of specific 3x3 plus-shaped objects (Maroon, Magenta, Green -> Gray).
    """
    # Convert input list of lists to a numpy array for easier processing
    input_array = np.array(input_grid, dtype=int)
    output_array = np.copy(input_array)
    height, width = input_array.shape

    # 1. Identify the background color
    background_color = find_background_color(input_array)

    # 2. Create a mask for non-background pixels
    object_mask = input_array != background_color

    # 3. Find connected components (objects) using the mask
    # structure=np.array([[0,1,0],[1,1,1],[0,1,0]]) ensures 4-connectivity (orthogonal)
    labeled_array, num_objects = label(object_mask, structure=np.array([[0,1,0],[1,1,1],[0,1,0]]))

    # 4. Iterate through each found object
    object_slices = find_objects(labeled_array)
    for i in range(num_objects):
        obj_label = i + 1
        slices = object_slices[i]
        # Get coordinates of the current object within the original array
        obj_coords = np.argwhere(labeled_array[slices] == obj_label) + np.array([slices[0].start, slices[1].start])
        
        # Check if coordinates are valid before accessing color
        if obj_coords.size == 0:
            continue
            
        # Get the color of the object (all pixels in a component have the same color)
        obj_color = input_array[obj_coords[0, 0], obj_coords[0, 1]]

        # Calculate bounding box properties
        min_row, min_col = obj_coords.min(axis=0)
        max_row, max_col = obj_coords.max(axis=0)
        obj_height = max_row - min_row + 1
        obj_width = max_col - min_col + 1
        num_pixels = obj_coords.shape[0]

        # a. Rule 1: Check for 1x5 horizontal line at the bottom row
        is_bottom_row = (min_row == height - 1) and (max_row == height - 1)
        if obj_height == 1 and obj_width == 5 and num_pixels == 5 and is_bottom_row:
            # Replace object pixels with background color in the output
            for r, c in obj_coords:
                output_array[r, c] = background_color
            continue # Move to the next object

        # b. Rule 2: Check for 3x3 plus sign shape
        # A 3x3 plus sign has 5 pixels and a 3x3 bounding box.
        if obj_height == 3 and obj_width == 3 and num_pixels == 5:
            # More specific check: Ensure center pixel exists and matches object
            center_r, center_c = min_row + 1, min_col + 1
            # Check if the center pixel belongs to this object (basic check)
            if labeled_array[center_r, center_c] == obj_label:
                 # Check if this specific object color needs changing
                if obj_color in [9, 6, 3]: # Maroon, Magenta, Green
                    # Change the 5 pixels to Gray (5)
                    for r, c in obj_coords:
                         output_array[r, c] = 5
                # Otherwise (color is 0, 1, 2, 4, 7, 8), do nothing, color remains as copied initially.

    # Convert the final numpy array back to a list of lists
    output_grid = output_array.tolist()
    return output_grid
