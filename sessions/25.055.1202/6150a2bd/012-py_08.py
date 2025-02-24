"""
The transformation involves these steps:

1.  **Identify Objects:** Find all contiguous regions of the same color. Consider single pixels as objects, too.
2.  **Background Identification**: The background is identified as the color filling most of the input grid except for a single pixel.
3.  **Identify Single Pixel Object:** The input grid contains a single pixel object that is different than the background.
4.  **Move Single Pixel:** If the input grid contains a single pixel of a color different from the background, move it to the diagonally opposite corner. The coordinate spaces appear transposed.
5.  **Background Preservation:** The background, identified in step 2, remains unchanged.
"""

import numpy as np
from skimage import measure

def find_objects(grid):
    """Finds contiguous regions of the same color (objects) in a grid."""
    arr = np.array(grid)
    unique_colors = np.unique(arr)
    objects = []
    for color in unique_colors:
        color_arr = (arr == color).astype(int)
        labeled_arr, num_labels = measure.label(color_arr, connectivity=1, return_num=True)
        for i in range(1, num_labels + 1):
            obj_coords = np.where(labeled_arr == i)
            objects.append({
                'color': color,
                'coords': list(zip(obj_coords[0], obj_coords[1]))
            })
    return objects

def identify_background(grid):
    """Identifies the background color based on the largest object."""
    objects = find_objects(grid)
    if not objects:
        return None  # Empty grid case

    largest_object = max(objects, key=lambda obj: len(obj['coords']))
    return largest_object['color']


def transform(input_grid):
    """Transforms the input grid according to the rules."""
    # initialize output_grid
    output_grid = [row[:] for row in input_grid] # Create a deep copy
    input_array = np.array(input_grid)

    # Identify background and objects
    background_color = identify_background(input_grid)
    objects = find_objects(input_grid)

    # Find single-pixel objects
    single_pixel_objects = [obj for obj in objects if len(obj['coords']) == 1 and obj['color'] != background_color]

    # Move single pixel object
    for obj in single_pixel_objects:
            y, x = obj['coords'][0]
            height, width = input_array.shape

            # Transpose coordinates for the new position
            new_y, new_x = x, y # bottom right becomes top right, etc.

            output_grid[y][x] = background_color          # remove from original location

            output_grid[new_y][new_x] = obj['color']  # set new location


    return output_grid