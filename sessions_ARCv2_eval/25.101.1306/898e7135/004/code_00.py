import numpy as np
from scipy.ndimage import label, find_objects
from collections import Counter
import sys
from io import StringIO

# --- Helper Functions (Copied from previous code) ---
def find_objects_and_pixels(grid: np.ndarray, ignore_color=0) -> list[dict]:
    objects_data = []
    unique_colors = np.unique(grid)
    for color in unique_colors:
        if color == ignore_color: continue
        binary_mask = (grid == color)
        labeled_array, num_features = label(binary_mask)
        if num_features > 0:
            slices = find_objects(labeled_array)
            for i in range(num_features):
                obj_slice = slices[i]
                if obj_slice is None: continue
                coords = np.argwhere(labeled_array == (i + 1))
                if coords.size == 0: continue # Skip if no pixels found for label
                objects_data.append({
                    'color': color,
                    'slices': obj_slice,
                    'pixels': coords.tolist()
                })
    return objects_data

def determine_background_color(grid: np.ndarray, content_colors: set) -> int:
    h, w = grid.shape
    if h == 0 or w == 0: return 0
    top_left_color = grid[0, 0]
    if top_left_color in content_colors:
        return int(top_left_color)
    else:
        flat_grid = grid.flatten()
        content_pixels = [p for p in flat_grid if p in content_colors]
        if not content_pixels: return 0
        counts = Counter(content_pixels)
        max_count = 0
        modes = []
        # Find the highest frequency
        try:
            max_count = counts.most_common(1)[0][1]
        except IndexError: # Handle case where counts is empty
             return 0
        # Find all colors with that frequency
        for color, count in counts.items():
             if count == max_count:
                  modes.append(color)
        return int(min(modes))

def is_adjacent_to_markers(obj_pixels: list[list[int]], marker_coords_set: set, grid_shape: tuple) -> bool:
    rows, cols = grid_shape
    # Optimization: Convert obj_pixels to set for faster checking later if needed
    # obj_pixels_set = {tuple(p) for p in obj_pixels}

    for r_marker, c_marker in marker_coords_set:
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0: continue
                nr, nc = r_marker + dr, c_marker + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    # Check if this neighbor pixel belongs to the object
                    if [nr, nc] in obj_pixels: # Check against list directly
                    # if tuple([nr, nc]) in obj_pixels_set: # Check against set
                        return True # Found an object pixel adjacent to this marker pixel
    return False # No object pixel was adjacent to any marker pixel

# --- Debugging Function ---
def debug_transform_steps(input_grid_str: str, name: str):
    print(f"\n--- Debugging {name} ---")
    input_array = np.array([list(map(int, row.split())) for row in input_grid_str.strip().split('\n')])
    if input_array.size == 0:
        print("Input grid is empty.")
        return

    # 1. Define Color Sets
    marker_colors = {7, 8}
    content_colors = {1, 2, 3, 4, 5, 6, 8, 9}
    print(f"Marker Colors: {marker_colors}")
    print(f"Content Colors: {content_colors}")

    # 2. Determine Background Color
    background_color = determine_background_color(input_array, content_colors)
    print(f"Determined Background Color: {background_color}")

    # 3. Identify All Objects
    all_objects = find_objects_and_pixels(input_array, ignore_color=0)
    if not all_objects:
        print("No objects found.")
        return
    print(f"Total objects found (excluding background 0): {len(all_objects)}")
    # for i, obj in enumerate(all_objects):
    #     print(f"  Obj {i}: Color={obj['color']}, Slice={obj['slices']}, NumPixels={len(obj['pixels'])}")


    # 4. Identify Background Object
    background_object_key = None
    min_r_bg, min_c_bg = float('inf'), float('inf')
    found_bg_pixel = False
    bg_coords = np.argwhere(input_array == background_color)

    if bg_coords.size > 0:
         # Find the actual top-leftmost pixel of the background color
         first_bg_pixel_coord = tuple(bg_coords[np.lexsort((bg_coords[:,1], bg_coords[:,0]))[0]])
         min_r_bg, min_c_bg = first_bg_pixel_coord
         found_bg_pixel = True
         print(f"Top-left pixel of background color ({background_color}) found at: ({min_r_bg}, {min_c_bg})")
    else:
        print(f"Background color ({background_color}) not found in grid.")


    if found_bg_pixel:
         for i, obj in enumerate(all_objects):
             if obj['color'] == background_color:
                 # Check if the top-left background pixel is in this object's pixel list
                 if [min_r_bg, min_c_bg] in obj['pixels']:
                     background_object_key = i
                     print(f"Background object identified: Index={i}, Color={obj['color']}, Slice={obj['slices']}")
                     break
         if background_object_key is None:
              print(f"Could not associate top-left background pixel ({min_r_bg}, {min_c_bg}) with a found object.")
    else:
        print("Cannot identify background object as background color not found.")


    # 5. Identify Marker Locations
    marker_coords_list = np.argwhere(np.isin(input_array, list(marker_colors)))
    marker_coords_set = {tuple(coord) for coord in marker_coords_list}
    print(f"Marker locations found ({len(marker_coords_set)}): {marker_coords_set if len(marker_coords_set)<20 else '...too many to list...'}")


    # 6. Select Content Objects (Debugging Checks)
    print("Checking object selection:")
    selected_count = 0
    for i, obj in enumerate(all_objects):
        print(f"  Checking Obj {i}: Color={obj['color']}, Slice={obj['slices']}")
        if i == background_object_key:
            print(f"    -> Skipping: Is background object.")
            continue
        if obj['color'] == 7:
            print(f"    -> Skipping: Is marker color 7.")
            continue

        # Perform adjacency check
        is_adj = is_adjacent_to_markers(obj['pixels'], marker_coords_set, input_array.shape)
        print(f"    -> Is adjacent to any marker? {is_adj}")
        if is_adj:
            selected_count += 1
            print(f"    -> SELECTED")

    print(f"Total objects selected based on adjacency check: {selected_count}")


# --- Input Data ---
grid1_str = """
2 2 2 2 2 2 0 0 7 0 0 0 0 0 0
2 0 0 2 0 2 0 0 0 0 0 0 0 0 0
2 0 2 2 2 2 0 0 0 0 0 0 0 0 0
2 2 2 2 0 2 0 0 0 8 8 0 0 7 0
2 2 0 0 0 2 0 0 0 8 8 0 0 0 0
2 2 2 2 2 2 0 8 8 8 8 0 0 0 0
0 0 0 0 0 0 0 8 8 8 8 0 0 0 0
0 7 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 0 0 0 0 0 3 3 3 3 0 0
0 0 0 0 0 7 0 0 0 3 3 3 3 0 0
0 0 0 0 0 0 0 0 0 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 3 3 0 0 0 0
0 0 7 0 0 0 0 0 0 3 3 0 0 0 7
0 0 0 0 0 0 0 0 0 3 3 0 0 0 0
0 0 0 0 0 0 7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 7 0 0
"""

grid2_str = """
0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 0 3 3 3 3
0 0 0 0 0 1 1 1 1 1 1 1 1 0 0 0 5 5 0 0 3 0 3 3 3 0 0 0 0 3
0 8 0 0 0 1 1 1 1 1 1 1 1 0 0 0 5 5 0 0 3 3 3 3 3 3 3 3 0 3
0 0 0 0 0 0 0 1 1 0 0 1 1 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3
0 0 0 0 0 0 0 1 1 0 0 1 1 0 0 0 0 0 0 0 3 3 3 3 3 0 3 3 3 3
0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 0 0 0 3 3 3
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 0 3 3 3 3
0 0 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 4 4 0 3 3 3 3 3 3 3 3 3 3
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 4 0 3 0 0 3 3 3 3 3 3 3
0 0 0 0 6 6 0 0 0 0 0 4 4 4 4 4 4 4 4 0 3 0 3 3 3 3 3 3 3 3
0 0 0 0 6 6 0 0 0 0 0 4 4 4 4 4 4 4 4 0 3 0 0 3 3 3 3 0 3 3
0 0 6 6 6 6 6 6 0 0 0 4 4 0 0 0 0 0 0 0 3 0 3 3 3 3 3 3 3 3
0 0 6 6 6 6 6 6 0 0 0 4 4 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3
0 0 0 0 6 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 6 0 0 0 0 0 0 0 0 0 5 5 0 0 0 8 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0
"""

# --- Execute Debugging ---
debug_transform_steps(grid1_str, "Example 1")
debug_transform_steps(grid2_str, "Example 2")
