```python
import numpy as np
from scipy.ndimage import label, find_objects
from collections import Counter

"""
Transformation Rule Description:

1.  **Define Color Sets:**
    *   `Marker_Colors = {Orange(7), Azure(8)}`
    *   `Content_Colors = {Blue(1), Red(2), Green(3), Yellow(4), Gray(5), Magenta(6), Maroon(9)}` (Potential colors for background and output objects, excluding markers 0, 7, 8).
2.  **Determine Background Color:**
    *   Check the color `c` at `input_grid[0, 0]`.
    *   If `c` is in `Content_Colors`, use `c` as the `background_color`.
    *   Otherwise (if `c` is 0, 7, or 8), find the color in `Content_Colors` that appears most frequently in the entire `input_grid`. Use this mode color (lowest numerical value in case of ties) as the `background_color`. If no `Content_Colors` exist, default to 0 (White).
3.  **Identify All Objects:** Find all distinct contiguous objects (colors 1-9) in the input grid. Store their color and pixel coordinates list `[(r1, c1), ...]`.
4.  **Identify Background Object:** Find the specific object instance that contains the top-most, then left-most pixel matching the determined `background_color`. Mark this object.
5.  **Identify Marker Locations:** Create a set of `(r, c)` coordinates for all pixels with colors in `Marker_Colors`.
6.  **Select Content Objects:**
    *   Iterate through all identified objects (from step 3).
    *   Skip the marked `background_object`.
    *   Skip objects whose color is in `Marker_Colors` (7 or 8).
    *   For remaining objects (color must be in `Content_Colors`): Check if any of the object's pixels `(r_obj, c_obj)` have a direct neighbor (8-way) `(nr, nc)` such that `(nr, nc)` is in the `marker_locations` set.
    *   If adjacency is found, add the object's data (color, pixel coordinates) to a `selected_objects` list.
7.  **Calculate Output Canvas:**
    *   If `selected_objects` is empty, return a 3x3 grid filled with `background_color`.
    *   Otherwise, find the minimum bounding box (`min_r`, `min_c`, `max_r`, `max_c`) enclosing all pixel coordinates from all `selected_objects`.
    *   Calculate canvas dimensions: `H = max_r - min_r + 1`, `W = max_c - min_c + 1`.
8.  **Create and Populate Output Grid:**
    *   Create the output grid with dimensions `(H + 2) x (W + 2)`, filled with `background_color` (padding = 1).
    *   For each selected object, iterate through its pixel coordinates `(r, c)`. Calculate the target coordinates `out_r = r - min_r + 1`, `out_c = c - min_c + 1` and set `output_grid[out_r, out_c]` to the object's color.
9.  **Return:** Return the final output grid.
"""

# --- Constants ---
MARKER_COLORS = {7, 8}
CONTENT_COLORS = {1, 2, 3, 4, 5, 6, 9}
BACKGROUND_PIXEL = 0

# --- Helper Functions ---

def find_objects_and_pixels(grid: np.ndarray, ignore_color=0) -> list[dict]:
    """
    Finds all contiguous objects for colors not equal to ignore_color.

    Args:
        grid: Input numpy array.
        ignore_color: Color to ignore (typically background).

    Returns:
        A list of dictionaries, where each dict represents an object:
        {'color': int, 'pixels': list[list[int]]} # pixels is list of [r, c]
    """
    objects_data = []
    unique_colors = np.unique(grid)

    for color in unique_colors:
        if color == ignore_color:
            continue

        # Create a binary mask for the current color
        binary_mask = (grid == color)

        # Label connected components for this color
        # Use 8-connectivity (structure=np.ones((3,3))) implicitly by default
        labeled_array, num_features = label(binary_mask)

        if num_features > 0:
            # Find pixel coordinates for each component
            for i in range(1, num_features + 1):
                coords = np.argwhere(labeled_array == i)
                if coords.size > 0:
                    objects_data.append({
                        'color': int(color), # Ensure standard int type
                        'pixels': coords.tolist()
                    })
    return objects_data

def determine_background_color(grid: np.ndarray, content_colors: set) -> int:
    """
    Determines the background color based on grid[0,0] or frequency
    of allowed content colors.
    """
    h, w = grid.shape
    if h == 0 or w == 0: return BACKGROUND_PIXEL # Handle empty grid

    top_left_color = grid[0, 0]

    # Rule 1: If top-left is a valid content color, use it.
    if top_left_color in content_colors:
        return int(top_left_color)
    # Rule 2: Otherwise, find the most frequent content color.
    else:
        flat_grid = grid.flatten()
        # Filter for pixels that are valid content colors
        content_pixels = [p for p in flat_grid if p in content_colors]

        if not content_pixels:
            # Default if no valid content colors are present at all
            return BACKGROUND_PIXEL

        counts = Counter(content_pixels)
        max_count = 0
        modes = []

        # Find the highest frequency count among content colors
        try:
            # most_common returns list of (element, count) tuples
            max_count = counts.most_common(1)[0][1]
        except IndexError:
             # Should not happen if content_pixels is not empty, but safety first
             return BACKGROUND_PIXEL

        # Find all content colors having that maximum frequency
        for color, count in counts.items():
             if count == max_count:
                  modes.append(color)

        # Return the smallest numerical color value among the modes
        return int(min(modes))

def is_object_adjacent_to_markers(obj_pixels: list[list[int]], marker_locations_set: set, grid_shape: tuple) -> bool:
    """
    Checks if any pixel of the object is adjacent (8-way) to any marker location.
    """
    rows, cols = grid_shape
    # Iterate through each pixel belonging to the object
    for r_obj, c_obj in obj_pixels:
        # Check its 8 neighbors
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue # Skip self
                nr, nc = r_obj + dr, c_obj + dc
                # Check if neighbor is within grid bounds
                if 0 <= nr < rows and 0 <= nc < cols:
                    # Check if this neighbor's coordinate is a marker location
                    if (nr, nc) in marker_locations_set:
                        return True # Adjacency found
    return False # No adjacency found after checking all object pixels


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule: selects objects adjacent to markers (7, 8),
    places them on a determined background, preserving shapes and relative positions
    with padding.
    """
    input_array = np.array(input_grid, dtype=int)
    if input_array.size == 0:
        # Default for empty input
        return [[BACKGROUND_PIXEL]*3]*3

    # Step 1: Define Color Sets (already defined as constants)

    # Step 2: Determine Background Color
    background_color = determine_background_color(input_array, CONTENT_COLORS)

    # Step 3: Identify All Objects (colors 1-9)
    all_objects = find_objects_and_pixels(input_array, ignore_color=BACKGROUND_PIXEL)
    if not all_objects:
         # Return 3x3 background if only background color exists
         return [[background_color]*3]*3

    # Step 4: Identify Background Object
    background_object_index = -1 # Use index in all_objects list
    min_r_bg, min_c_bg = float('inf'), float('inf')
    found_bg_pixel = False

    # Find the coordinate of the top-most, left-most pixel with the background color
    bg_coords = np.argwhere(input_array == background_color)
    if bg_coords.size > 0:
        # lexsort sorts by last column first (c), then previous (r)
        sorted_indices = np.lexsort((bg_coords[:, 1], bg_coords[:, 0]))
        min_r_bg, min_c_bg = bg_coords[sorted_indices[0]]
        found_bg_pixel = True

    # Find which object contains this specific pixel
    if found_bg_pixel:
         for i, obj in enumerate(all_objects):
             # Optimization: Could check bounding box first
             if obj['color'] == background_color:
                  # Check if the identified top-left background pixel is in this object's list
                  if [min_r_bg, min_c_bg] in obj['pixels']:
                      background_object_index = i
                      break # Found it

    # Step 5: Identify Marker Locations
    marker_locations_list = np.argwhere(np.isin(input_array, list(MARKER_COLORS)))
    marker_locations_set = {tuple(coord) for coord in marker_locations_list} # Set for faster lookup

    # Step 6: Select Content Objects
    selected_objects = []
    all_selected_pixels = [] # Collect pixels for bounding box calculation

    for i, obj in enumerate(all_objects):
        # Skip if it's the designated background object
        if i == background_object_index:
            continue
        # Skip if its color is a marker color (7 or 8)
        if obj['color'] in MARKER_COLORS:
            continue

        # Check adjacency to markers for remaining objects (color must be in CONTENT_COLORS)
        if is_object_adjacent_to_markers(obj['pixels'], marker_locations_set, input_array.shape):
            selected_objects.append(obj)
            all_selected_pixels.extend(obj['pixels']) # Add pixels to list

    # Step 7: Calculate Output Canvas
    if not selected_objects:
        # Return 3x3 background grid if no objects are selected
        return [[background_color]*3]*3

    # Find bounding box of all selected pixels
    if not all_selected_pixels: # Should not happen if selected_objects is not empty
         return [[background_color]*3]*3 # Safety check

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

    # Step 8: Create and Populate Output Grid
    output_grid = np.full((output_H, output_W), background_color, dtype=int)

    for obj in selected_objects:
        obj_color = obj['color']
        for r, c in obj['pixels']:
            # Calculate position relative to the top-left of the canvas
            rel_r = r - min_r
            rel_c = c - min_c
            # Add padding to get final output coordinates
            out_r = rel_r + padding
            out_c = rel_c + padding
            # Draw the pixel
            # Optional: Add bounds check, though should be correct
            if 0 <= out_r < output_H and 0 <= out_c < output_W:
                 output_grid[out_r, out_c] = obj_color

    # Step 9: Return
    return output_grid.tolist()
```