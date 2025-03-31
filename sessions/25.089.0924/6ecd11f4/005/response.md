```python
import numpy as np
from scipy.ndimage import label, find_objects

"""
Transformation Rule:

1. Identify all distinct contiguous regions (objects) of non-background (non-zero) pixels in the input grid.
2. Find the object with the largest number of pixels. This is the `large_shape`. Record its color (`filter_color`).
3. Among the *other* objects, find the one whose bounding box contains more than one distinct non-background color. This is the `key_grid_object`.
4. Determine the rectangular bounding box (slice) that encloses the `key_grid_object`.
5. Extract the sub-grid from the input grid defined by this bounding box. This is the `key_grid`.
6. Define a set of 'target colors' to be replaced with white (0) based on the `filter_color`:
    - If `filter_color` is blue (1), target colors are {blue (1), red (2), yellow (4), maroon (9)}.
    - If `filter_color` is green (3), target colors are {blue (1), azure (8), maroon (9)}.
    - If `filter_color` is azure (8), target colors are {blue (1), green (3), gray (5), orange (7)}.
    - Otherwise, the target color set is empty.
7. Create the output grid by making a copy of the `key_grid`.
8. Iterate through each cell of the output grid. If the cell's color is in the 'target colors' set, change that cell's color to white (0).
9. Return the modified output grid as a list of lists.
"""

def find_objects_data(grid):
    """
    Identifies all connected non-background objects in the grid and returns their properties.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary contains data for one object:
              'label' (int): The unique label assigned by scipy.ndimage.label.
              'size' (int): The number of pixels in the object.
              'color' (int): The color of the object (taken from the first pixel).
              'slice' (tuple): The slice representing the bounding box.
              'bbox_shape' (tuple): The shape (height, width) of the bounding box.
              'num_unique_bbox_non_bg_colors' (int): Count of unique non-background colors within the bounding box.
    """
    background_color = 0
    labeled_array, num_features = label(grid != background_color)
    
    if num_features == 0:
        return []

    object_slices = find_objects(labeled_array)
    object_data = []

    for i in range(1, num_features + 1):
        mask = labeled_array == i
        coords = np.argwhere(mask)
        size = coords.shape[0]
        obj_slice = object_slices[i-1]
        bounding_box_grid = grid[obj_slice]
        
        # Count unique non-background colors within the bounding box
        bbox_unique_colors = np.unique(bounding_box_grid)
        num_bbox_unique_non_bg = len(bbox_unique_colors[bbox_unique_colors != background_color])
        
        # Get the color of the object itself (from the first pixel)
        color = grid[coords[0, 0], coords[0, 1]]

        object_data.append({
            "label": i,
            "size": size,
            "color": color,
            "slice": obj_slice,
            "bbox_shape": bounding_box_grid.shape,
            "num_unique_bbox_non_bg_colors": num_bbox_unique_non_bg
        })
        
    # Sort objects by size, largest first
    object_data.sort(key=lambda x: x["size"], reverse=True)
    return object_data


def transform(input_grid):
    """
    Applies the transformation logic: identifies a large single-color object and a multi-color key grid,
    then filters the key grid based on the large object's color.
    """
    grid = np.array(input_grid, dtype=int)
    background_color = 0

    # 1. Identify all non-background objects and their properties
    all_objects = find_objects_data(grid)

    if not all_objects:
        return [[]] # No objects found

    # 2. Find the largest object and its color
    large_shape = all_objects[0]
    filter_color = large_shape['color']

    # 3. Find the key_grid_object among the *other* objects
    key_grid_object = None
    for obj in all_objects[1:]: # Skip the largest object
        # Criterion: Bounding box contains more than one distinct non-background color
        if obj['num_unique_bbox_non_bg_colors'] > 1:
            key_grid_object = obj
            break # Assume only one key grid object per example

    if key_grid_object is None:
        # Fallback if only one object exists or no object fits the multi-color bbox criteria
        # Check if the largest object *itself* could be the key grid (if its bbox has multiple colors)
        # This might happen if the 'large shape' is small or absent, and the key grid is the dominant feature.
        if large_shape['num_unique_bbox_non_bg_colors'] > 1:
             key_grid_object = large_shape
             # If the key grid is the largest, what's the filter color? Maybe default to no filter?
             filter_color = None # Indicate no specific filter color found from a separate large object
        else:
             return [[]] # No suitable key grid object found

    # 4. Get the bounding box slice of the key_grid_object
    key_grid_slice = key_grid_object['slice']
    
    # 5. Extract the key_grid
    key_grid = grid[key_grid_slice]

    # 6. Define target colors based on filter_color
    target_colors = set()
    if filter_color == 1: # Blue
        target_colors = {1, 2, 4, 9}
    elif filter_color == 3: # Green
        target_colors = {1, 8, 9}
    elif filter_color == 8: # Azure
        target_colors = {1, 3, 5, 7}
    # Add more rules here if needed for other filter colors

    # 7. Create output grid as a copy
    output_grid = key_grid.copy()

    # 8. Iterate and apply filtering
    rows, cols = output_grid.shape
    for r in range(rows):
        for c in range(cols):
            if output_grid[r, c] in target_colors:
                output_grid[r, c] = background_color

    # 9. Return as list of lists
    return output_grid.tolist()
```