import numpy as np
from scipy.ndimage import label
from collections import Counter

"""
Transformation Rule Description (Hypothesis H6):

1.  **Define Color Sets:**
    *   `Base_Content_Colors = {1, 2, 3, 4, 5, 6, 9}` (Potential background/object colors)
    *   `Orange = 7`, `Azure = 8` (Special roles)
    *   `Background = 0` (Input background)
2.  **Determine Background Color:**
    *   If input[0,0] is in `Base_Content_Colors`, use it.
    *   Else, use the mode (most frequent, lowest value tiebreak) of `Base_Content_Colors` in the input grid.
3.  **Identify All Objects:** Find all contiguous objects (colors 1-9) and their pixel coordinates.
4.  **Identify Background Object:** Find the specific object instance containing the top-most, left-most pixel matching the determined Background_Color.
5.  **Determine Actual Content Colors:** Check if Orange(7) is present in the input. If yes, `Actual_Content_Colors = Base_Content_Colors + {8}`. If no, `Actual_Content_Colors = Base_Content_Colors`.
6.  **Select Content Objects:** Keep objects that are NOT the Background_Object AND whose color IS in `Actual_Content_Colors`.
7.  **Calculate Output Canvas:** Find the minimum bounding box enclosing all pixels of the selected content objects. Handle the case of no selected objects (return 3x3 background).
8.  **Create Output Grid:** Create a grid sized Canvas + 1-pixel padding on all sides, filled with the Background_Color.
9.  **Draw Content:** Copy the exact pixel data of each selected content object onto the output grid relative to the canvas position and padding.
"""

# --- Constants ---
BASE_CONTENT_COLORS = {1, 2, 3, 4, 5, 6, 9}
ORANGE_COLOR = 7
AZURE_COLOR = 8
BACKGROUND_PIXEL = 0
MARKER_COLORS = {ORANGE_COLOR, AZURE_COLOR} # Used for background check

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

        binary_mask = (grid == color)
        # Use 8-connectivity (default structure)
        labeled_array, num_features = label(binary_mask)

        if num_features > 0:
            for i in range(1, num_features + 1): # Labels are 1-based
                coords = np.argwhere(labeled_array == i)
                if coords.size > 0:
                    objects_data.append({
                        'color': int(color),
                        'pixels': coords.tolist()
                    })
    return objects_data

def determine_background_color(grid: np.ndarray, base_content_colors: set) -> int:
    """
    Determines the background color based on grid[0,0] or frequency
    of allowed base content colors.
    """
    h, w = grid.shape
    if h == 0 or w == 0: return BACKGROUND_PIXEL

    top_left_color = grid[0, 0]

    # Use Base_Content_Colors for this rule
    if top_left_color in base_content_colors:
        return int(top_left_color)
    else: # Includes 0, 7, 8 or any other color not in base content
        flat_grid = grid.flatten()
        content_pixels = [p for p in flat_grid if p in base_content_colors]

        if not content_pixels:
            return BACKGROUND_PIXEL # Default if no valid base content colors

        counts = Counter(content_pixels)
        # Find the highest frequency
        try:
            max_count = counts.most_common(1)[0][1]
        except IndexError:
             return BACKGROUND_PIXEL # Should not happen if content_pixels not empty

        # Find all colors with that frequency
        modes = sorted([color for color, count in counts.items() if count == max_count])

        # Return the smallest color value among modes
        return int(modes[0])


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation based on Hypothesis H6.
    """
    input_array = np.array(input_grid, dtype=int)
    if input_array.size == 0:
        return [[BACKGROUND_PIXEL]*3]*3 # Default for empty input

    # Step 2: Determine Background Color (using BASE_CONTENT_COLORS)
    background_color = determine_background_color(input_array, BASE_CONTENT_COLORS)

    # Step 3: Identify All Objects (colors 1-9)
    # Pass background_color to ignore finding it as separate objects if needed,
    # but finding all non-zero is simpler here.
    all_objects = find_objects_and_pixels(input_array, ignore_color=BACKGROUND_PIXEL)
    if not all_objects:
         # Return 3x3 background if only background color exists in input
         return [[background_color]*3]*3

    # Step 4: Identify Background Object
    background_object_index = -1 # Index in all_objects list
    min_r_bg, min_c_bg = float('inf'), float('inf')
    found_bg_pixel = False

    # Find the coordinate of the top-most, left-most pixel with the background color
    bg_coords = np.argwhere(input_array == background_color)
    if bg_coords.size > 0:
        sorted_indices = np.lexsort((bg_coords[:, 1], bg_coords[:, 0]))
        min_r_bg, min_c_bg = bg_coords[sorted_indices[0]]
        found_bg_pixel = True

    # Find which object instance contains this specific pixel
    if found_bg_pixel:
         for i, obj in enumerate(all_objects):
             if obj['color'] == background_color:
                  if [min_r_bg, min_c_bg] in obj['pixels']:
                      background_object_index = i
                      break

    # Step 5: Determine Actual Content Colors based on Orange(7) presence
    orange_present = ORANGE_COLOR in input_array
    if orange_present:
        actual_content_colors = BASE_CONTENT_COLORS.union({AZURE_COLOR})
    else:
        actual_content_colors = BASE_CONTENT_COLORS

    # Step 6: Select Content Objects
    selected_objects = []
    all_selected_pixels = [] # Collect pixels for bounding box

    for i, obj in enumerate(all_objects):
        # Condition 1: Skip if it's the designated background object
        if i == background_object_index:
            continue
        # Condition 2: Keep only if color is in the Actual_Content_Colors set
        if obj['color'] in actual_content_colors:
            selected_objects.append(obj)
            all_selected_pixels.extend(obj['pixels'])

    # Step 7: Calculate Output Canvas
    if not selected_objects:
        # Return 3x3 background grid if no objects are selected
        return [[background_color]*3]*3

    # Find bounding box of all selected pixels
    if not all_selected_pixels:
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

    # Step 9: Draw Content
    for obj in selected_objects:
        obj_color = obj['color']
        for r, c in obj['pixels']:
            # Calculate position relative to the top-left of the canvas
            rel_r = r - min_r
            rel_c = c - min_c
            # Add padding for final output coordinates
            out_r = rel_r + padding
            out_c = rel_c + padding
            # Draw the pixel within bounds
            if 0 <= out_r < output_H and 0 <= out_c < output_W:
                 output_grid[out_r, out_c] = obj_color

    # Convert final numpy array back to list of lists for output
    return output_grid.tolist()