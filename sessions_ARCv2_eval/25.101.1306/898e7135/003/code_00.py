import numpy as np
from scipy.ndimage import label, find_objects
from collections import Counter

"""
Transformation Rule Description:

1.  **Define Color Sets:** Identify Marker colors {Orange(7), Azure(8)} and Potential Content colors {Blue(1), Red(2), Green(3), Yellow(4), Gray(5), Magenta(6), Azure(8), Maroon(9)}. Background color is White(0).
2.  **Determine Background Color:**
    *   Check the color `c` at input_grid[0,0].
    *   If `c` is in the Potential Content colors set, use `c` as the `background_color`.
    *   Otherwise (if `c` is 0 or 7), find the Potential Content color that appears most frequently in the input grid. Use this mode color as the `background_color`. Handle ties by choosing the lowest numerical color value among the tied modes.
3.  **Identify All Objects:** Find all distinct contiguous objects in the input grid, ignoring the background color (0). Store their color, pixel coordinates, and bounding box slices.
4.  **Identify Background Object:**
    *   Find the top-most, then left-most pixel in the grid that has the `background_color`.
    *   Identify the specific object instance that contains this pixel. This is the `background_object`.
5.  **Identify Marker Locations:** Find the (row, col) coordinates of all pixels with Marker colors (7 or 8).
6.  **Select Content Objects:**
    *   Initialize an empty list `selected_objects_data`.
    *   Iterate through all objects identified in step 3.
    *   Skip the object if it is the `background_object`.
    *   Skip the object if its color is Orange (7) (since 7 is only a marker, not content).
    *   For the remaining candidate objects (colors 1, 2, 3, 4, 5, 6, 8, 9), check if any of their pixels are adjacent (8-way connectivity) to any marker location found in step 5.
    *   If an object is adjacent to a marker, add its data (color, pixel coordinates list) to `selected_objects_data`.
7.  **Calculate Output Canvas:**
    *   If `selected_objects_data` is empty, return a 3x3 grid filled with `background_color`.
    *   Otherwise, collect all pixel coordinates from all objects in `selected_objects_data`.
    *   Find the minimum bounding box (min_r, min_c, max_r, max_c) that encloses all these collected coordinates.
    *   Calculate canvas dimensions: `H = max_r - min_r + 1`, `W = max_c - min_c + 1`.
8.  **Create and Populate Output Grid:**
    *   Create the output grid with dimensions `(H + 2) x (W + 2)`, filled with `background_color`.
    *   Iterate through each object in `selected_objects_data`. For each pixel `(r, c)` in the object's coordinates list:
        *   Calculate the target coordinates in the output grid: `out_r = r - min_r + 1`, `out_c = c - min_c + 1`.
        *   Set `output_grid[out_r, out_c]` to the object's color.
9.  **Return:** Return the final output grid as a list of lists.
"""

def find_objects_and_pixels(grid: np.ndarray, ignore_color=0) -> list[dict]:
    """Finds all objects, returning their color, slices, and pixel coordinates."""
    objects_data = []
    unique_colors = np.unique(grid)

    for color in unique_colors:
        if color == ignore_color:
            continue

        binary_mask = (grid == color)
        labeled_array, num_features = label(binary_mask)

        if num_features > 0:
            slices = find_objects(labeled_array)
            for i in range(num_features):
                obj_slice = slices[i]
                if obj_slice is None: continue
                
                # Find coordinates relative to the whole grid
                coords = np.argwhere(labeled_array == (i + 1))
                # coords is already Nx2 array of [[r1,c1], [r2,c2], ...]
                
                objects_data.append({
                    'color': color,
                    'slices': obj_slice,
                    'pixels': coords.tolist() # Store as list of [r, c] pairs
                })
    return objects_data

def determine_background_color(grid: np.ndarray, content_colors: set) -> int:
    """Determines the background color based on grid[0,0] or frequency."""
    h, w = grid.shape
    if h == 0 or w == 0: return 0 # Handle empty grid case

    top_left_color = grid[0, 0]

    if top_left_color in content_colors:
        return int(top_left_color)
    else:
        # Flatten grid and count frequencies of content colors
        flat_grid = grid.flatten()
        content_pixels = [p for p in flat_grid if p in content_colors]
        
        if not content_pixels:
            return 0 # Default to white if no content colors found

        counts = Counter(content_pixels)
        max_count = 0
        modes = []
        # Find the highest frequency
        for color, count in counts.items():
             if count > max_count:
                 max_count = count
        # Find all colors with that frequency
        for color, count in counts.items():
             if count == max_count:
                  modes.append(color)

        # Return the smallest color value among modes
        return int(min(modes))


def is_adjacent_to_markers(obj_pixels: list[list[int]], marker_coords_set: set, grid_shape: tuple) -> bool:
    """Checks if any object pixel is adjacent (8-way) to any marker coordinate."""
    rows, cols = grid_shape
    for r, c in obj_pixels:
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    if (nr, nc) in marker_coords_set:
                        return True
    return False

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation logic to the input grid.
    """
    input_array = np.array(input_grid, dtype=int)
    if input_array.size == 0:
        return [[0,0,0],[0,0,0],[0,0,0]] # Handle empty input

    # 1. Define Color Sets
    marker_colors = {7, 8}
    content_colors = {1, 2, 3, 4, 5, 6, 8, 9} # Includes 8

    # 2. Determine Background Color
    background_color = determine_background_color(input_array, content_colors)

    # 3. Identify All Objects
    all_objects = find_objects_and_pixels(input_array, ignore_color=0)
    if not all_objects:
         return [[background_color]*3]*3 # Return 3x3 background if no objects

    # 4. Identify Background Object
    background_object_key = None # Use (color, tuple(slices)) as key? Or just slices? Let's use slices index.
    min_r_bg, min_c_bg = float('inf'), float('inf')
    found_bg_pixel = False
    
    # Find the top-leftmost coordinate of the background color
    bg_coords = np.argwhere(input_array == background_color)
    if bg_coords.size > 0:
        for r, c in bg_coords:
             if r < min_r_bg:
                 min_r_bg = r
                 min_c_bg = c
                 found_bg_pixel = True
             elif r == min_r_bg and c < min_c_bg:
                 min_c_bg = c
                 found_bg_pixel = True
                 
    # Find which object contains this specific pixel
    if found_bg_pixel:
         for i, obj in enumerate(all_objects):
             if obj['color'] == background_color:
                  # Check if the top-left background pixel is in this object's pixel list
                  if [min_r_bg, min_c_bg] in obj['pixels']:
                      background_object_key = i # Store index of background object
                      break # Found it

    # 5. Identify Marker Locations
    marker_coords_list = np.argwhere(np.isin(input_array, list(marker_colors)))
    marker_coords_set = {tuple(coord) for coord in marker_coords_list} # Set for faster lookup

    # 6. Select Content Objects
    selected_objects_data = []
    all_selected_pixels = []

    for i, obj in enumerate(all_objects):
        # Skip if it's the designated background object
        if i == background_object_key:
            continue
        # Skip if it's color 7 (pure marker)
        if obj['color'] == 7:
            continue
        # Check adjacency to markers
        if is_adjacent_to_markers(obj['pixels'], marker_coords_set, input_array.shape):
            selected_objects_data.append(obj)
            all_selected_pixels.extend(obj['pixels']) # Collect pixels for bounding box

    # 7. Calculate Output Canvas
    if not selected_objects_data:
        # Handle cases like only background object exists or no objects selected
        return [[background_color]*3]*3

    # Find bounding box of all selected pixels
    if not all_selected_pixels: # Should not happen if selected_objects_data is not empty
         return [[background_color]*3]*3

    all_selected_pixels_array = np.array(all_selected_pixels)
    min_r = np.min(all_selected_pixels_array[:, 0])
    max_r = np.max(all_selected_pixels_array[:, 0])
    min_c = np.min(all_selected_pixels_array[:, 1])
    max_c = np.max(all_selected_pixels_array[:, 1])

    H = max_r - min_r + 1
    W = max_c - min_c + 1
    padding = 1

    output_H = H + 2 * padding
    output_W = W + 2 * padding

    # 8. Create and Populate Output Grid
    output_grid = np.full((output_H, output_W), background_color, dtype=int)

    for obj in selected_objects_data:
        obj_color = obj['color']
        for r, c in obj['pixels']:
            out_r = r - min_r + padding
            out_c = c - min_c + padding
            # Check bounds just in case (shouldn't be needed with correct logic)
            if 0 <= out_r < output_H and 0 <= out_c < output_W:
                 output_grid[out_r, out_c] = obj_color

    # 9. Return
    return output_grid.tolist()