import numpy as np
from scipy.ndimage import label, find_objects
import math

"""
Identifies all distinct objects (contiguous blocks of the same color, including diagonals) in the input grid.
For each color:
  - Finds objects that are single pixels ("markers").
  - Finds objects that are larger than one pixel ("potential sources").
  - If there is exactly one marker and at least one potential source of the same color:
    - Identifies the potential source object with the largest number of pixels (the "largest source object").
    - Determines the coordinates of the single marker pixel.
    - Calculates the bounding box of the largest source object.
    - Calculates the conceptual center of the bounding box (using floor division on dimensions).
    - Calculates the placement position for a copy of the largest source object so that its conceptual center aligns with the marker pixel's position.
    - Iterates through ONLY the actual pixel coordinates of the largest source object. For each source pixel, calculates its corresponding target position on the output grid based on the alignment.
    - Places the source object's color at these calculated target coordinates on an output grid, overwriting existing pixels (including the original marker). Pixels within the calculated placement area but NOT part of the original source object's shape are NOT drawn.
Repeats this process for all applicable colors. Pixels not involved in any copy/placement operation retain their original values from the input grid.
"""

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
    # Find unique non-background colors present in the grid
    unique_colors = np.unique(grid[grid > 0])
    if unique_colors.size == 0:
        return {} # Return empty if only background color exists

    for color in unique_colors:
        # Create a binary mask for the current color
        mask = (grid == color)
        
        # Label connected components in the mask. 
        # structure=np.ones((3,3)) ensures diagonal connectivity is considered.
        labeled_array, num_features = label(mask, structure=np.ones((3,3)))

        if num_features > 0:
            # find_objects returns a list of slices corresponding to the bounding box of each feature
            coords_slices = find_objects(labeled_array)
            color_objects = []
            
            # Iterate through each found feature (object) for this color
            for i in range(num_features):
                # Get the slice defining the bounding box for the current feature
                loc = coords_slices[i]
                
                # Basic validation for the slice object
                if loc is None or not isinstance(loc, tuple) or len(loc) != 2:
                    continue 
                
                # Extract the portion of the labeled array corresponding to this object's bounding box
                object_slice = labeled_array[loc]
                
                # Find the coordinates *within the slice* where the label matches the current feature index + 1
                # This identifies the pixels belonging to this specific object within its bounding box
                obj_mask_in_slice = (object_slice == (i + 1))
                obj_coords_in_slice = np.argwhere(obj_mask_in_slice)

                # If no coordinates were found (e.g., issues with labeling), skip
                if obj_coords_in_slice.size == 0:
                    continue

                # Convert slice-relative coordinates (r, c) to absolute grid coordinates
                # by adding the starting row and column of the slice.
                obj_coords_global = set(
                    (r + loc[0].start, c + loc[1].start)
                    for r, c in obj_coords_in_slice
                )
                
                # Add the set of global coordinates for this object to the list
                if obj_coords_global: # Ensure we don't add empty sets
                    color_objects.append(obj_coords_global)
            
            # If any objects were found for this color, add them to the main dictionary
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
    # Return the min/max row and column values
    return (min(rows), min(cols), max(rows), max(cols))

# --- Main Transformation Function ---

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # 1. Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape
    
    # 2. Identify all distinct contiguous objects for each non-white color.
    objects_by_color = find_all_objects_by_color(input_grid)

    # 3. Iterate through each color found.
    for color, objects in objects_by_color.items():
        markers = []
        potential_sources = []
        
        # 3a. Separate objects into markers (size 1) and potential sources (size > 1).
        for obj_coords in objects:
            if len(obj_coords) == 1:
                markers.append(obj_coords)
            elif len(obj_coords) > 1:
                potential_sources.append(obj_coords)

        # 3b. Check if the condition is met: exactly one marker and at least one source.
        if len(markers) == 1 and len(potential_sources) >= 1:
            
            # 3c.i. Get the coordinate of the single marker pixel.
            marker_coord = list(markers[0])[0] # markers[0] is a set like {(r, c)}
            marker_r, marker_c = marker_coord

            # 3c.ii. Find the largest source object by pixel count.
            largest_source_obj_coords = max(potential_sources, key=len)

            # 3c.iii. Determine the bounding box of the largest source object.
            source_bbox = get_bounding_box(largest_source_obj_coords)
            if source_bbox is None:
                continue # Should not happen if largest_source_obj_coords is valid
            src_min_r, src_min_c, src_max_r, src_max_c = source_bbox

            # 3c.iv. Calculate the dimensions of the source bounding box.
            src_height = src_max_r - src_min_r + 1
            src_width = src_max_c - src_min_c + 1

            # 3c.v. Calculate the center offset relative to the source bounding box's top-left.
            center_offset_r = math.floor((src_height - 1) / 2)
            center_offset_c = math.floor((src_width - 1) / 2)

            # 3c.vi. Calculate the top-left anchor coordinate for placing the object.
            # This is the coordinate where the source object's bounding box's top-left
            # would be placed so that its center aligns with the marker.
            anchor_r = marker_r - center_offset_r
            anchor_c = marker_c - center_offset_c

            # 3c.vii. Iterate through each coordinate *actually belonging* to the largest source object.
            for src_r, src_c in largest_source_obj_coords:
                # 1. Calculate the pixel's relative offset from the source bounding box's top-left.
                relative_r = src_r - src_min_r
                relative_c = src_c - src_min_c

                # 2. Calculate the final target coordinate on the output grid.
                target_r = anchor_r + relative_r
                target_c = anchor_c + relative_c

                # 3. If the target coordinate is within the grid bounds, place the color.
                if 0 <= target_r < height and 0 <= target_c < width:
                    output_grid[target_r, target_c] = color

    # 4. Return the modified output grid.
    return output_grid