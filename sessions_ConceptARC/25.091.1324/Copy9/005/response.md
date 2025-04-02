```python
"""
For each non-white color present in the input grid:
1. Identify all distinct contiguous objects (pixels connected horizontally, vertically, or diagonally).
2. Check if there is exactly one object of size 1 (a "marker") and at least one object of size > 1 (a "potential source").
3. If these conditions are met for a color:
    a. Select the potential source object with the largest number of pixels (the "largest source").
    b. Determine the bounding box of the largest source object.
    c. Extract the rectangular region defined by this bounding box directly from the *input* grid (this region includes all pixels within the box, regardless of color).
    d. Find the coordinates of the single marker pixel.
    e. Calculate the top-left coordinate (anchor) required to paste the extracted region onto the output grid such that the region's center aligns with the marker pixel's coordinates. Center calculation uses floor division on the region's dimensions.
    f. Paste the extracted region onto an output grid (initially a copy of the input) at the calculated anchor position, overwriting any existing pixels within that target area. Ensure pasting stays within the grid boundaries.
4. Repeat for all colors meeting the conditions.
5. Return the final modified output grid.
"""

import numpy as np
from scipy.ndimage import label, find_objects
import math

# --- Helper Functions ---

def find_all_objects_by_color(grid):
    """
    Finds all contiguous objects (connected components including diagonals) 
    of non-background colors in the grid.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        dict: A dictionary where keys are colors (int > 0) and values are lists
              of objects. Each object is represented as a set of coordinates
              {(r1, c1), (r2, c2), ...}. Returns an empty dict if no 
              non-background objects are found.
    """
    objects_by_color = {}
    unique_colors = np.unique(grid[grid > 0])
    if unique_colors.size == 0:
        return {} 

    for color in unique_colors:
        mask = (grid == color)
        labeled_array, num_features = label(mask, structure=np.ones((3,3)))

        if num_features > 0:
            coords_slices = find_objects(labeled_array)
            color_objects = []
            
            for i in range(num_features):
                loc = coords_slices[i]
                if loc is None or not isinstance(loc, tuple) or len(loc) != 2:
                    continue 
                
                object_slice = labeled_array[loc]
                obj_mask_in_slice = (object_slice == (i + 1))
                obj_coords_in_slice = np.argwhere(obj_mask_in_slice)

                if obj_coords_in_slice.size == 0:
                    continue

                obj_coords_global = set(
                    (r + loc[0].start, c + loc[1].start)
                    for r, c in obj_coords_in_slice
                )
                
                if obj_coords_global: 
                    color_objects.append(obj_coords_global)
            
            if color_objects: 
                 objects_by_color[color] = color_objects
                 
    return objects_by_color

def get_bounding_box(obj_coords):
    """
    Calculates the bounding box (min_row, min_col, max_row, max_col) 
    for a set of object coordinates.

    Args:
        obj_coords (set): A set of (row, col) tuples representing the object's pixels.

    Returns:
        tuple: (min_row, min_col, max_row, max_col) or None if obj_coords is empty.
    """
    if not obj_coords:
        return None
    rows = [r for r, c in obj_coords]
    cols = [c for r, c in obj_coords]
    return (min(rows), min(cols), max(rows), max(cols))

# --- Main Transformation Function ---

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # 1. Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape
    
    # 2. Find all distinct contiguous objects for each non-white color.
    objects_by_color = find_all_objects_by_color(input_grid)

    # 3. Iterate through each color found.
    for color, objects in objects_by_color.items():
        markers = []
        potential_sources = []
        
        # 3a & 3b. Separate objects into markers (size 1) and potential sources (size > 1).
        for obj_coords in objects:
            if len(obj_coords) == 1:
                markers.append(obj_coords)
            elif len(obj_coords) > 1:
                potential_sources.append(obj_coords)

        # 3c. Check if conditions are met: exactly one marker and at least one source.
        if len(markers) == 1 and len(potential_sources) >= 1:
            
            # --- Conditions met, proceed with transformation for this color ---
            
            # 3d.i. Select the largest source object by pixel count.
            largest_source_obj_coords = max(potential_sources, key=len)

            # 3d.ii. Determine the bounding box of the largest source object.
            source_bbox = get_bounding_box(largest_source_obj_coords)
            if source_bbox is None: 
                continue # Safety check, should not happen here
            src_min_r, src_min_c, src_max_r, src_max_c = source_bbox

            # 3d.iii. Extract the rectangular source patch from the *input* grid.
            source_patch = input_grid[src_min_r : src_max_r + 1, src_min_c : src_max_c + 1]
            patch_h, patch_w = source_patch.shape

            # 3d.iv. Get the coordinate of the single marker pixel.
            marker_coord = list(markers[0])[0] # markers[0] is a set like {(r, c)}
            marker_r, marker_c = marker_coord

            # 3d.v. Calculate the target top-left anchor coordinate for pasting.
            # Center offset within the patch (relative to its top-left)
            center_offset_r = math.floor((patch_h - 1) / 2)
            center_offset_c = math.floor((patch_w - 1) / 2)
            # Anchor coordinate on the output grid
            anchor_r = marker_r - center_offset_r
            anchor_c = marker_c - center_offset_c

            # 3d.vi. Paste the source_patch onto the output grid.
            for dr in range(patch_h): # dr is row offset within the patch
                for dc in range(patch_w): # dc is col offset within the patch
                    # Calculate target coordinates on the output grid
                    target_r = anchor_r + dr
                    target_c = anchor_c + dc

                    # Check if target coordinates are within grid bounds
                    if 0 <= target_r < height and 0 <= target_c < width:
                        # Overwrite the output grid pixel with the corresponding patch pixel
                        output_grid[target_r, target_c] = source_patch[dr, dc]

    # 5. Return the final modified output grid.
    return output_grid
```