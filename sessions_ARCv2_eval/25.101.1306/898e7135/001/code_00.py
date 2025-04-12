import numpy as np
from scipy.ndimage import label, find_objects, measurements

"""
Transformation Rule Description:

1.  **Identify Objects**: Find all contiguous blocks of pixels in the input grid that are not the background color (white, 0).
2.  **Determine Background/Fill Color**: Find the top-most, then left-most pixel belonging to any identified object. The color of this pixel becomes the `fill_color` for the output grid. The object containing this pixel is the `background_object`.
3.  **Identify Content Objects**: Create a set of "content objects" consisting of all objects found in step 1, *except* for the `background_object`.
4.  **Calculate Object Properties**: For each content object:
    *   Find its bounding box in the input grid: (row_min, col_min) to (row_max, col_max).
    *   Calculate its height (h = row_max - row_min + 1) and width (w = col_max - col_min + 1).
    *   Determine its characteristic size: `size = min(h, w)`.
    *   Store its color, original top-left corner (row_min, col_min), and its characteristic size `s`.
5.  **Determine Content Canvas**: Calculate the minimal bounding box that encompasses all the *derived square shapes* (size `s` x `s`) if they were placed at their original top-left coordinates (row_min, col_min) from the input grid. Let this overall content bounding box be (`content_R_min`, `content_C_min`) to (`content_R_max`, `content_C_max`).
6.  **Calculate Output Grid Dimensions**:
    *   Content Height: `H = content_R_max - content_R_min + 1`.
    *   Content Width: `W = content_C_max - content_C_min + 1`.
    *   Add a padding of 1 pixel on all sides. Output Height = `H + 2`, Output Width = `W + 2`.
7.  **Create Output Grid**: Initialize a new grid with the calculated output dimensions, filled entirely with the `fill_color`.
8.  **Place Content Objects**: Iterate through the stored properties for each content object (`obj_color`, `r_min`, `c_min`, `s`):
    *   Calculate the top-left position relative to the content canvas: `rel_r = r_min - content_R_min`, `rel_c = c_min - content_C_min`.
    *   Calculate the top-left position in the output grid (adding padding): `out_r = rel_r + 1`, `out_c = rel_c + 1`.
    *   Draw a filled square of size `s x s` with `obj_color` in the output grid, starting at `(out_r, out_c)`.
9.  Return the final output grid.

Note: This interpretation is based on synthesizing observations across examples. The role of marker colors (e.g., orange 7, azure 8) seemed inconsistent or unclear in the examples provided, so this rule focuses on object geometry, relative placement, and background determination by the top-leftmost object. The shape transformation is assumed to be taking the minimal dimension of the object's bounding box to form a square.
"""

def find_all_objects(grid: np.ndarray) -> list[tuple[int, tuple[slice, slice], np.ndarray]]:
    """
    Finds all non-background (color != 0) objects in the grid.

    Args:
        grid: Input numpy array.

    Returns:
        A list of tuples, where each tuple contains:
        (object_color, bounding_box_slices, object_mask_in_bbox)
    """
    objects_data = []
    unique_colors = np.unique(grid)
    
    for color in unique_colors:
        if color == 0: # Skip background
            continue
            
        # Create a binary mask for the current color
        binary_mask = (grid == color)
        
        # Label connected components for this color
        labeled_array, num_features = label(binary_mask)
        
        if num_features > 0:
            # Find the bounding box slices for each component
            slices = find_objects(labeled_array)
            
            for i in range(num_features):
                obj_slice = slices[i]
                # Extract the mask for this specific object within its bounding box
                obj_mask = (labeled_array[obj_slice] == (i + 1))
                objects_data.append((color, obj_slice, obj_mask))
                
    return objects_data

def get_bounding_box_coords(slices: tuple[slice, slice]) -> tuple[int, int, int, int]:
    """Extracts (r_min, c_min, r_max, c_max) from slice tuple."""
    r_slice, c_slice = slices
    r_min, r_max = r_slice.start, r_slice.stop - 1
    c_min, c_max = c_slice.start, c_slice.stop - 1
    return r_min, c_min, r_max, c_max

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.
    """
    input_array = np.array(input_grid, dtype=int)
    
    # 1. Identify Objects
    all_objects = find_all_objects(input_array)
    
    if not all_objects:
        # Handle empty input or input with only background
        # Based on examples, seems unlikely, but good practice.
        # Returning a small grid of a default color (e.g., black) might be one option.
        # Or perhaps return based on input size filled with a default.
        # Let's return input size filled with black (0) if no objects found.
        # Or maybe just return a 1x1 black pixel. Let's choose 1x1 black.
         # Returning a 3x3 grid filled with black (0) as a default guess.
        return [[0,0,0],[0,0,0],[0,0,0]]


    # 2. Determine Background/Fill Color
    top_left_r, top_left_c = float('inf'), float('inf')
    background_object_info = None
    fill_color = -1 # Default invalid color

    object_properties = [] # Store (color, r_min, c_min, r_max, c_max)

    for color, slices, mask in all_objects:
        r_min, c_min, r_max, c_max = get_bounding_box_coords(slices)
        object_properties.append({'color': color, 'r_min': r_min, 'c_min': c_min, 'r_max': r_max, 'c_max': c_max, 'slices': slices})
        
        # Find the first pixel of this object to check for top-leftmost overall
        obj_pixels_r, obj_pixels_c = np.where(mask)
        first_pixel_r = r_min + np.min(obj_pixels_r)
        # Need to find the minimum column index *among* rows equal to first_pixel_r
        min_c_for_min_r = c_min + np.min(obj_pixels_c[obj_pixels_r == np.min(obj_pixels_r)])

        if first_pixel_r < top_left_r:
            top_left_r = first_pixel_r
            top_left_c = min_c_for_min_r
            fill_color = color
            background_object_info = {'color': color, 'slices': slices}
        elif first_pixel_r == top_left_r and min_c_for_min_r < top_left_c:
            top_left_c = min_c_for_min_r
            fill_color = color
            background_object_info = {'color': color, 'slices': slices}

    if fill_color == -1: # Should not happen if objects were found
         return [[0,0,0],[0,0,0],[0,0,0]] # Default error return

    # 3. Identify Content Objects & 4. Calculate Object Properties
    content_objects_props = []
    for props in object_properties:
        # Exclude the background object based on color AND location (slices)
        # This handles cases where multiple objects share the background color.
        is_background = (props['color'] == background_object_info['color'] and 
                         props['slices'] == background_object_info['slices'])
        if not is_background:
            h = props['r_max'] - props['r_min'] + 1
            w = props['c_max'] - props['c_min'] + 1
            s = min(h, w)
            content_objects_props.append({
                'color': props['color'],
                'r_min': props['r_min'],
                'c_min': props['c_min'],
                'size': s
            })

    if not content_objects_props:
         # If only the background object exists, return a minimal grid of its color?
         # Let's return 3x3 grid of the fill color.
         return [[fill_color]*3]*3
         
    # 5. Determine Content Canvas
    content_R_min, content_C_min = float('inf'), float('inf')
    content_R_max, content_C_max = float('-inf'), float('-inf')

    for props in content_objects_props:
        r_min, c_min, s = props['r_min'], props['c_min'], props['size']
        content_R_min = min(content_R_min, r_min)
        content_C_min = min(content_C_min, c_min)
        content_R_max = max(content_R_max, r_min + s - 1)
        content_C_max = max(content_C_max, c_min + s - 1)
        
    # 6. Calculate Output Grid Dimensions
    content_H = content_R_max - content_R_min + 1
    content_W = content_C_max - content_C_min + 1
    padding = 1 # Assume padding of 1 for now
    output_H = content_H + 2 * padding
    output_W = content_W + 2 * padding

    # 7. Create Output Grid
    output_grid = np.full((output_H, output_W), fill_color, dtype=int)

    # 8. Place Content Objects
    for props in content_objects_props:
        obj_color = props['color']
        r_min = props['r_min']
        c_min = props['c_min']
        s = props['size']
        
        # Calculate relative position within the content canvas
        rel_r = r_min - content_R_min
        rel_c = c_min - content_C_min
        
        # Calculate absolute position in the output grid (with padding)
        out_r = rel_r + padding
        out_c = rel_c + padding
        
        # Draw the square
        output_grid[out_r:out_r + s, out_c:out_c + s] = obj_color

    return output_grid.tolist()
