"""
Transforms the input grid by identifying each distinct non-background colored object 
and repositioning it vertically. The object's internal pattern is preserved (not flipped).
The new vertical position is determined by placing the object such that its bottom edge 
in the output grid is mirrored across the horizontal center relative to its original 
bottom edge position. Specifically, the new top row of the object's bounding box is 
calculated as grid_height - original_bottom_row_exclusive (original r_max). 
The horizontal position remains unchanged. The background remains white (0).
"""

import numpy as np
from scipy.ndimage import label, find_objects

def transform(input_grid):
    """
    Applies a vertical repositioning transformation to each non-background object 
    without altering the object's internal pattern.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape
    background_color = 0

    # Initialize the output grid with the background color
    output_array = np.full_like(input_array, background_color)

    # Find all unique non-background colors
    unique_colors = np.unique(input_array)
    non_background_colors = unique_colors[unique_colors != background_color]

    # Process objects for each color independently to handle overlaps correctly if needed,
    # though in this task objects seem distinct.
    for color in non_background_colors:
        # Create a mask for the current color
        color_mask = (input_array == color)

        # Label connected components (objects) for the current color
        # Use a structure that connects diagonally as well
        structure = np.array([[1,1,1], [1,1,1], [1,1,1]], dtype=bool)
        labeled_mask, num_features = label(color_mask, structure=structure)

        # If no objects of this color are found, continue
        if num_features == 0:
            continue

        # Find the bounding boxes for each distinct object of this color
        object_slices = find_objects(labeled_mask)

        # Process each object found
        for i, obj_slice in enumerate(object_slices):
            object_label = i + 1 # Labels start from 1

            # Get bounding box coordinates and dimensions from the slice
            r_slice, c_slice = obj_slice
            r_min, r_max = r_slice.start, r_slice.stop
            c_min, c_max = c_slice.start, c_slice.stop
            bbox_height = r_max - r_min
            bbox_width = c_max - c_min

            # Calculate the new top row position for the object
            # The new top position is H - old_bottom_exclusive (r_max)
            target_r_start = height - r_max
            target_c_start = c_min # Horizontal position remains the same

            # Iterate through the bounding box of the object in the input grid
            for r_sub in range(bbox_height):
                for c_sub in range(bbox_width):
                    # Get the original coordinates in the input grid
                    original_r = r_min + r_sub
                    original_c = c_min + c_sub

                    # Check if the pixel at this original coordinate belongs to the *current* labeled object
                    if labeled_mask[original_r, original_c] == object_label:
                        # Get the pixel color from the input grid
                        pixel_color = input_array[original_r, original_c]

                        # Calculate target coordinates in the output grid
                        target_row = target_r_start + r_sub
                        target_col = target_c_start + c_sub

                        # Ensure target coordinates are within bounds (should be, but safe check)
                        if 0 <= target_row < height and 0 <= target_col < width:
                           output_array[target_row, target_col] = pixel_color

    # Convert the NumPy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid
