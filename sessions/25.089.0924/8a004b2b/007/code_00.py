import numpy as np
from collections import Counter

"""
Transformation Rule:
1. Identify the primary bounding box defined by yellow (4) pixels in the input grid.
2. Determine the output grid size based on the primary bounding box dimensions.
3. Analyze colors:
    a. Find the set of non-background colors strictly *inside* the primary bounding box (`inside_colors`).
    b. Find the list of all non-background colors *outside* the primary bounding box (`outside_colors_list`).
    c. Determine the `connecting_color`:
        i. Calculate unique colors present outside but not inside (`unique_outside = set(outside_colors_list) - inside_colors`).
        ii. If `len(unique_outside) == 1`, the `connecting_color` is that unique color.
        iii. Otherwise (0 or >1 unique outside colors), find the most frequent color(s) in `outside_colors_list`. The `connecting_color` is the one with the smallest numerical index among the most frequent.
        iv. If `outside_colors_list` is empty, the `connecting_color` is 0.
4. Create the output grid, initially filled with the background color (0).
5. Copy the content strictly *inside* the input primary bounding box to the interior of the output grid (offset by 1 row and 1 column).
6. Identify the bounding box of the *copied content* within the output grid (`content_bounding_box`). Find the minimum and maximum row/column of all non-background pixels in the output grid.
7. Fill Background: If a `connecting_color` > 0 was determined and a `content_bounding_box` exists:
    a. Iterate through all pixels (r, c) within the `content_bounding_box`.
    b. If the pixel `output_grid[r, c]` is currently background (0), change its color to the `connecting_color`.
8. Set the four corner pixels of the output grid to yellow (4).
"""

# --- Helper Functions ---

def find_bounding_box(grid, color_value):
    """Finds the min/max row/col for pixels of a specific color."""
    coordinates = np.argwhere(grid == color_value)
    if coordinates.size == 0:
        return None # Indicate not found
    min_row = np.min(coordinates[:, 0])
    min_col = np.min(coordinates[:, 1])
    max_row = np.max(coordinates[:, 0])
    max_col = np.max(coordinates[:, 1])
    return min_row, min_col, max_row, max_col

def get_colors_in_region(grid, min_r, max_r, min_c, max_c, exclude_zero=True):
    """Gets the set of unique colors within a specified bounding box region."""
    # Ensure indices are valid for slicing (start < end)
    if min_r >= max_r or min_c >= max_c:
        return set()
    region = grid[min_r:max_r, min_c:max_c]
    colors = set(np.unique(region))
    if exclude_zero and 0 in colors:
        colors.remove(0)
    return colors

def get_all_colors_outside_region(grid, min_r, max_r, min_c, max_c, exclude_zero=True):
    """Gets a list of all colors outside the specified bounding box."""
    colors = []
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            # Check if the pixel is outside the bounding box (inclusive bounds)
            is_outside = r < min_r or r > max_r or c < min_c or c > max_c
            if is_outside:
                color = grid[r, c]
                if not exclude_zero or color != 0:
                     colors.append(color)
    return colors

def calculate_connecting_color(inside_colors_set, outside_colors_list):
    """Determines the connecting color based on inside/outside colors."""
    if not outside_colors_list: # No non-zero colors outside
        return 0
        
    outside_colors_set = set(outside_colors_list)
    unique_outside = outside_colors_set - inside_colors_set
    
    if len(unique_outside) == 1:
        return list(unique_outside)[0]
    else:
        # Fallback to most frequent outside color (smallest index tiebreak)
        counts = Counter(outside_colors_list)
        max_freq = 0
        # Find max frequency first
        for count in counts.values():
             if count > max_freq:
                 max_freq = count
                 
        # Collect all colors with max frequency
        most_frequent = [color for color, count in counts.items() if count == max_freq]
        
        # Return the smallest color index among the most frequent
        return min(most_frequent)

def find_content_bounding_box(grid, ignore_value=0):
    """Finds the bounding box of all pixels not matching ignore_value."""
    coords = np.argwhere(grid != ignore_value)
    if coords.size == 0:
        return None # No content found
    min_r = np.min(coords[:, 0])
    min_c = np.min(coords[:, 1])
    max_r = np.max(coords[:, 0])
    max_c = np.max(coords[:, 1])
    return min_r, min_c, max_r, max_c

# --- Main Transform Function ---

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    input_np = np.array(input_grid, dtype=int)
    rows_in, cols_in = input_np.shape

    # 1. Identify Primary Bounding Box (using yellow=4)
    primary_bbox = find_bounding_box(input_np, 4)
    if primary_bbox is None:
         # Cannot proceed without markers, return empty or error?
         # Returning empty list based on common ARC patterns for failure
         return [] 
    min_r_prim, min_c_prim, max_r_prim, max_c_prim = primary_bbox

    # 2. Calculate Output Grid Dimensions
    height = max_r_prim - min_r_prim + 1
    width = max_c_prim - min_c_prim + 1

    # Basic validation for dimensions
    if height <= 0 or width <= 0:
        return []

    # 3. Determine Connecting Color
    # Get colors strictly *inside* the primary box
    inside_colors = get_colors_in_region(input_np, min_r_prim + 1, max_r_prim, min_c_prim + 1, max_c_prim, exclude_zero=True)
    # Get *all* non-zero colors outside the primary box (inclusive borders)
    outside_colors = get_all_colors_outside_region(input_np, min_r_prim, max_r_prim, min_c_prim, max_c_prim, exclude_zero=True)
    # Calculate the color for filling background
    connecting_color = calculate_connecting_color(inside_colors, outside_colors)

    # 4. Create Output Grid
    output_np = np.zeros((height, width), dtype=int)

    # 5. Copy Inner Content
    # Check if there's an inner area to copy (box > 2x2)
    inner_h, inner_w = 0, 0
    if max_r_prim > min_r_prim + 1 and max_c_prim > min_c_prim + 1:
        inner_content = input_np[min_r_prim + 1 : max_r_prim, min_c_prim + 1 : max_c_prim]
        inner_h, inner_w = inner_content.shape
        # Place content starting at [1, 1] in the output grid
        if inner_h > 0 and inner_w > 0:
             # Target region in output: [1:1+inner_h, 1:1+inner_w]
             # Ensure target region fits (it should by definition)
             output_np[1 : 1 + inner_h, 1 : 1 + inner_w] = inner_content

    # 6. Identify Content Bounding Box in the output grid
    content_bbox = find_content_bounding_box(output_np, ignore_value=0)

    # 7. Fill Background within Content Bounding Box
    if connecting_color > 0 and content_bbox:
        content_min_r, content_min_c, content_max_r, content_max_c = content_bbox
        # Iterate through the content bounding box
        for r in range(content_min_r, content_max_r + 1):
             for c in range(content_min_c, content_max_c + 1):
                 # If the pixel is background (0), fill it
                 if output_np[r, c] == 0:
                     output_np[r, c] = connecting_color

    # 8. Set the four corners to yellow (4)
    # Ensure indices are valid before setting
    output_np[0, 0] = 4
    if width > 1:
        output_np[0, width - 1] = 4
    if height > 1:
        output_np[height - 1, 0] = 4
    if height > 1 and width > 1:
        output_np[height - 1, width - 1] = 4
        
    # Convert back to list of lists for the required output format
    output_grid = output_np.tolist()

    return output_grid