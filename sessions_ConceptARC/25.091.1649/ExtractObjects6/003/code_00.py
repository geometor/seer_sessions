import numpy as np
from collections import Counter
import math

"""
Processes an input grid by performing the following steps:

1.  **Find Separator:** Locates a solid horizontal or vertical line of yellow (4) pixels that divides the grid. Records the orientation (horizontal/vertical) and index.
2.  **Divide Input:** Splits the input grid into two subgrids based on the separator, discarding the separator line itself. Notes the original relative orientation (top/bottom or left/right).
3.  **Process Each Subgrid:** For each subgrid:
    a.  **Check for Special Case:** Determines if the subgrid contains both green (3) and gray (5) pixels.
    b.  **Extract Feature Pixels:**
        i.  **If Special Case (Green and Gray):** Identifies green (3) pixels adjacent (sharing an edge) to *any* non-green pixel within that subgrid. Collects these 'perimeter' green pixel coordinates. The feature color is green (3).
        ii. **If General Case:** Identifies the primary object color(s) (non-background, non-yellow). Finds the background (most frequent non-yellow). Collects coordinates of all non-background, non-yellow pixels. If multiple object colors, picks the most frequent one as the feature color and filters coordinates accordingly.
    c.  **Create Output Subgrid:** Calculates the minimal bounding box of the collected feature pixels. Creates a new grid (filled with white 0) of the bounding box size. Places the feature pixels (using the determined feature color) into this new grid at relative positions. If no feature pixels are found, returns a 1x1 white grid. Records the output subgrid's dimensions.
4.  **Standardize Dimensions:** Compares the dimensions of the two processed subgrids.
    a.  **If Separator was Horizontal (Row):** Finds the maximum width. Pads the narrower subgrid with white (0) columns (centered horizontally) to match the maximum width.
    b.  **If Separator was Vertical (Column):** Finds the maximum height. Pads the shorter subgrid with white (0) rows (centered vertically) to match the maximum height.
5.  **Combine Results:** Concatenates the two standardized subgrids based on the original separator orientation (vertically for row separator, horizontally for column separator).
"""

def find_separator(grid):
    """Finds a horizontal or vertical solid line of yellow (4)."""
    h, w = grid.shape
    # Check for horizontal separator
    for r in range(h):
        if np.all(grid[r, :] == 4):
            return 'h', r # Horizontal line at row r
    # Check for vertical separator
    for c in range(w):
        if np.all(grid[:, c] == 4):
            return 'v', c # Vertical line at column c
    return None, -1 # No separator found

def get_bounding_box(coords):
    """Calculates the bounding box for a list of coordinates."""
    if not coords:
        return 0, -1, 0, -1 # Indicate empty box
    rows = [r for r, c in coords]
    cols = [c for r, c in coords]
    min_r, max_r = min(rows), max(rows)
    min_c, max_c = min(cols), max(cols)
    return min_r, max_r, min_c, max_c

def find_green_perimeter_refined(subgrid):
    """Finds green pixels adjacent to any non-green pixel within the subgrid."""
    h, w = subgrid.shape
    perimeter_coords = []
    green_coords = np.argwhere(subgrid == 3)

    for r, c in green_coords:
        is_perimeter = False
        # Check 4 neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < h and 0 <= nc < w:
                # If neighbor is NOT green (could be gray, background, etc.)
                if subgrid[nr, nc] != 3:
                    is_perimeter = True
                    break
        if is_perimeter:
            perimeter_coords.append((r, c))

    # Return coordinates and the feature color (always green for this case)
    return perimeter_coords, 3

def extract_feature(subgrid):
    """Extracts the main feature/object from a subgrid."""
    h, w = subgrid.shape
    unique_colors = np.unique(subgrid)
    feature_coords = []
    feature_color = 0 # Default to 0 (white)

    # Handle empty or single-color subgrids early
    if h == 0 or w == 0:
         return np.zeros((1, 1), dtype=int), (1, 1)
    non_yellow_colors = [c for c in unique_colors if c != 4]
    if len(non_yellow_colors) <= 1: # Only background or only yellow separator remnants
         return np.zeros((1, 1), dtype=int), (1, 1)


    # Check for the special green (3) and gray (5) case
    if 3 in unique_colors and 5 in unique_colors:
        feature_coords, feature_color = find_green_perimeter_refined(subgrid)
    else:
        # General case: extract non-background, non-yellow pixels
        counts = Counter(subgrid.flatten())
        
        # Find likely background (most frequent, non-yellow)
        bg_color = -1
        max_count = -1
        sorted_counts = sorted(counts.items(), key=lambda item: item[1], reverse=True)
        for color, count in sorted_counts:
             if color != 4: # ignore yellow separator remnants if any
                 bg_color = color
                 break
        # If calculation failed (e.g., only yellow?), default background to white?
        if bg_color == -1: bg_color = 0 # Fallback

        object_colors = set()
        temp_feature_coords = [] # Store potential feature coords before filtering by color
        for r in range(h):
            for c in range(w):
                color = subgrid[r, c]
                if color != bg_color and color != 4:
                    temp_feature_coords.append((r, c))
                    object_colors.add(color)

        if not object_colors: # No object pixels found
            pass # feature_coords remains empty
        elif len(object_colors) == 1:
             feature_color = object_colors.pop()
             feature_coords = temp_feature_coords # All collected coords belong to the single object color
        else: # Multiple object colors found
             # Heuristic: pick the most frequent non-background, non-yellow color
             obj_counts = {c: counts[c] for c in object_colors}
             feature_color = max(obj_counts, key=obj_counts.get)
             # Filter coords to only include the chosen feature color
             feature_coords = [(r,c) for r,c in temp_feature_coords if subgrid[r,c] == feature_color]


    # Create the output subgrid based on bounding box
    if not feature_coords:
        # Return a minimal 1x1 white grid if no feature was extracted
        return np.zeros((1, 1), dtype=int), (1, 1)

    min_r, max_r, min_c, max_c = get_bounding_box(feature_coords)
    # Check for invalid bounding box (e.g., from empty coords)
    if max_r < min_r or max_c < min_c:
         return np.zeros((1, 1), dtype=int), (1, 1)

    out_h = max_r - min_r + 1
    out_w = max_c - min_c + 1
    output_subgrid = np.zeros((out_h, out_w), dtype=int) # Fill with white (0)

    # Place feature pixels into the output subgrid
    for r, c in feature_coords:
        # Make sure the pixel being placed belongs to the designated feature_color
        # This handles the case where multiple object colors existed initially
        if subgrid[r,c] == feature_color:
             output_subgrid[r - min_r, c - min_c] = feature_color

    return output_subgrid, (out_h, out_w)


def pad_grid(grid, target_h, target_w, bg_color=0):
    """Pads a grid to target dimensions, centering the content."""
    h, w = grid.shape
    
    # Ensure target dimensions are at least the current dimensions
    target_h = max(h, target_h)
    target_w = max(w, target_w)

    pad_h = target_h - h
    pad_w = target_w - w

    pad_top = pad_h // 2
    pad_bottom = pad_h - pad_top
    pad_left = pad_w // 2
    pad_right = pad_w - pad_left
    
    # np.pad requires non-negative padding amounts
    if pad_top < 0 or pad_bottom < 0 or pad_left < 0 or pad_right < 0:
         # This should not happen with max() check above, but as safety:
         print(f"Warning: Negative padding calculated unexpectedly. Grid shape: ({h},{w}), Target: ({target_h},{target_w})")
         return grid # Return original grid if something went wrong

    padded_grid = np.pad(
        grid,
        ((pad_top, pad_bottom), (pad_left, pad_right)),
        mode='constant',
        constant_values=bg_color
    )
    return padded_grid


def transform(input_grid):
    """
    Applies the transformation logic to the input grid.
    """
    input_array = np.array(input_grid, dtype=int)

    # 1. Find Separator
    orientation, index = find_separator(input_array)
    if orientation is None:
        # If no separator, maybe return input or handle as error?
        # Based on task structure, separator is expected.
        # Returning input for safety, though it likely indicates an issue.
        print("Warning: No separator found.")
        return input_grid

    # 2. Divide Input
    subgrids = []
    split_orientation = None # Determines how to standardize and combine
    if orientation == 'h': # Horizontal separator (row) -> top/bottom regions
        if index > 0:
            subgrids.append(input_array[:index, :])
        if index < input_array.shape[0] - 1:
            subgrids.append(input_array[index+1:, :])
        split_orientation = 'vertical' # Regions are top/bottom -> stack vertically
    elif orientation == 'v': # Vertical separator (column) -> left/right regions
        if index > 0:
            subgrids.append(input_array[:, :index])
        if index < input_array.shape[1] - 1:
             subgrids.append(input_array[:, index+1:])
        split_orientation = 'horizontal' # Regions are left/right -> stack horizontally

    # Handle cases where splitting might yield fewer than 2 grids (e.g., separator at edge)
    if len(subgrids) == 0:
         print("Warning: Splitting resulted in zero subgrids.")
         return [[]] # Return empty grid
    elif len(subgrids) == 1:
         # If only one region, process it and return (no standardization/combination needed)
         processed, (h, w) = extract_feature(subgrids[0])
         return processed.tolist()

    # 3. Process Each Subgrid (expecting 2 subgrids now)
    processed_subgrids = []
    dimensions = []
    for subgrid in subgrids:
        processed, (h, w) = extract_feature(subgrid)
        processed_subgrids.append(processed)
        dimensions.append((h, w))

    if not processed_subgrids or len(processed_subgrids) != 2:
         print("Warning: Incorrect number of processed subgrids.")
         return [[]] # Return empty

    # 4. Standardize Dimensions
    standardized_subgrids = []
    grid1, grid2 = processed_subgrids[0], processed_subgrids[1]
    (h1, w1), (h2, w2) = dimensions[0], dimensions[1]

    if split_orientation == 'vertical': # Row separator -> standardize width
        max_w = max(w1, w2)
        std1 = pad_grid(grid1, h1, max_w)
        std2 = pad_grid(grid2, h2, max_w)
        standardized_subgrids = [std1, std2]

    elif split_orientation == 'horizontal': # Column separator -> standardize height
        max_h = max(h1, h2)
        std1 = pad_grid(grid1, max_h, w1)
        std2 = pad_grid(grid2, max_h, w2)
        standardized_subgrids = [std1, std2]

    # 5. Combine Results
    if not standardized_subgrids:
        print("Warning: Standardization failed.")
        return [[]] # Return empty grid if processing failed

    output_array = None
    if split_orientation == 'vertical':
        output_array = np.vstack(standardized_subgrids)
    elif split_orientation == 'horizontal':
        output_array = np.hstack(standardized_subgrids)

    if output_array is None:
         print("Warning: Combination failed.")
         return [[]]

    # Convert final numpy array back to list of lists
    output_grid = output_array.tolist()
    return output_grid