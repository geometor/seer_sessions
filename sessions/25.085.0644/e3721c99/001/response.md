```python
import numpy as np
import math
from scipy.ndimage import label, find_objects

"""
Identifies key shapes in the upper part of the grid (above a blue horizontal line) 
and target gray shapes in the lower part. Replaces each gray shape with the 
key shape that is geometrically closest to it. The replacement shape uses the 
color of the closest key shape and is positioned using the top-left corner of 
the original gray shape's bounding box as an anchor.

1.  Create a copy of the input grid for the output.
2.  Find the horizontal blue separator line.
3.  Identify all connected non-white objects (key objects) above the separator. 
    Store their pixels, color, top-left corner, and relative shape.
4.  Identify all connected gray objects (target objects) below the separator. 
    Store their pixels and top-left corner.
5.  For each target object:
    a.  Calculate the minimum distance to every key object.
    b.  Determine the closest key object (using top-left coordinate as a tie-breaker).
    c.  Clear the original gray pixels of the target object in the output grid.
    d.  Draw the shape of the closest key object using its color, anchored at the 
        target object's top-left corner, onto the output grid.
6.  Return the modified output grid.
"""

def find_separator_row(grid):
    """Finds the row index of the horizontal blue line."""
    rows, cols = grid.shape
    for r in range(rows):
        if np.all(grid[r, :] == 1):
            return r
    return -1 # Should not happen based on examples

def get_objects(grid, condition_mask, get_color=False):
    """
    Finds connected components based on a boolean condition mask.
    Returns a list of objects, each with pixels, bbox, top_left, and optionally color and shape.
    """
    labeled_array, num_features = label(condition_mask)
    objects_data = []
    
    # find_objects returns slices, which can include None if the object touches the edge
    # We need to convert these slices to actual bounding box coordinates.
    slices = find_objects(labeled_array) 
    
    for i in range(1, num_features + 1):
        obj_mask = (labeled_array == i)
        pixels = set(tuple(coord) for coord in np.argwhere(obj_mask))
        
        # Get bounding box from slices
        r_slice, c_slice = slices[i-1]
        min_row, max_row = r_slice.start, r_slice.stop
        min_col, max_col = c_slice.start, c_slice.stop
        
        bbox = (min_row, min_col, max_row - 1, max_col - 1) # slices are exclusive at stop
        top_left = (min_row, min_col)
        
        obj_info = {
            "pixels": pixels,
            "bbox": bbox,
            "top_left": top_left
        }

        if get_color:
            # Assuming object has a single non-background color
            color_val = 0
            for r, c in pixels:
                 val = grid[r, c]
                 if val != 0: # Find the first non-background color
                     color_val = val
                     break
            obj_info["color"] = color_val
            
            # Calculate relative shape
            shape = set((r - min_row, c - min_col) for r, c in pixels)
            obj_info["shape"] = shape
            
        objects_data.append(obj_info)
        
    return objects_data

def calculate_min_distance(obj1_pixels, obj2_pixels):
    """Calculates the minimum Euclidean distance between any pair of pixels from two objects."""
    min_dist_sq = float('inf')
    for r1, c1 in obj1_pixels:
        for r2, c2 in obj2_pixels:
            dist_sq = (r1 - r2)**2 + (c1 - c2)**2
            if dist_sq < min_dist_sq:
                min_dist_sq = dist_sq
    return math.sqrt(min_dist_sq)

def draw_shape(grid, top_left, shape, color):
    """Draws a shape onto the grid at the specified anchor point."""
    rows, cols = grid.shape
    anchor_r, anchor_c = top_left
    for dr, dc in shape:
        r, c = anchor_r + dr, anchor_c + dc
        if 0 <= r < rows and 0 <= c < cols:
            grid[r, c] = color

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find the separator row
    separator_row = find_separator_row(output_grid)
    if separator_row == -1:
        # Handle error or return input if no separator found (though unlikely for this task)
        return output_grid 
        
    # --- Identify Key Objects (Above Separator) ---
    key_mask = np.zeros_like(output_grid, dtype=bool)
    # Consider rows 1 to separator_row-1 (excluding row 0 often empty, and the separator itself)
    if separator_row > 1:
         key_mask[1:separator_row, :] = (output_grid[1:separator_row, :] != 0)
    key_objects = get_objects(output_grid, key_mask, get_color=True)

    # --- Identify Target Objects (Below Separator) ---
    target_mask = np.zeros_like(output_grid, dtype=bool)
    if separator_row < rows - 1:
        target_mask[separator_row + 1:, :] = (output_grid[separator_row + 1:, :] == 5) # Gray color
    target_objects = get_objects(output_grid, target_mask, get_color=False)

    # --- Process Each Target Object ---
    if not key_objects: # If no keys, no transformation happens below separator
        return output_grid
        
    for target_obj in target_objects:
        min_distance = float('inf')
        closest_key = None

        # Find the closest key object
        for key_obj in key_objects:
            distance = calculate_min_distance(target_obj["pixels"], key_obj["pixels"])
            
            update_closest = False
            if distance < min_distance:
                update_closest = True
            elif distance == min_distance:
                 # Tie-breaking: prefer key object with smaller top_left row, then smaller top_left col
                 if key_obj["top_left"][0] < closest_key["top_left"][0]:
                     update_closest = True
                 elif key_obj["top_left"][0] == closest_key["top_left"][0] and \
                      key_obj["top_left"][1] < closest_key["top_left"][1]:
                     update_closest = True

            if update_closest:
                min_distance = distance
                closest_key = key_obj

        if closest_key:
            # Clear the original target object pixels
            for r, c in target_obj["pixels"]:
                if r < rows and c < cols: # Boundary check just in case
                   output_grid[r, c] = 0 # Set to background color

            # Draw the closest key's shape at the target's anchor point
            draw_shape(output_grid, 
                       target_obj["top_left"], 
                       closest_key["shape"], 
                       closest_key["color"])

    return output_grid
```