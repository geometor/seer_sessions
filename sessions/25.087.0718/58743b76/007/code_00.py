import numpy as np

"""
Recolors pixels of a specific 'source' color based on their quadrant 
within the bounding box of all such source pixels (outside a special 'key' area). 
The new colors are determined by a 2x2 'key' block.

1.  **Initialize:** Create a copy of the input grid.
2.  **Find Key:** Locate the unique 2x2 block with no white(0) or azure(8) pixels. Extract its 4 colors (TL, TR, BL, BR), top-left coordinates (key_r, key_c), and the set of its unique colors.
3.  **Identify Source Color & Coordinates:** Find pixels outside the key's 2x2 area that are not white(0) or azure(8). Identify the unique color among these that is also present in the key's colors (the 'Source Color'). Collect the coordinates of all pixels having the Source Color.
4.  **Define Target Area:** Calculate the bounding box (min_row, min_col, max_row, max_col) enclosing all identified Source Color Pixel coordinates.
5.  **Calculate Quadrant Boundaries:** Determine the row and column indices that divide the Target Area into four quadrants using integer division.
6.  **Apply Transformation:** Iterate through the coordinates of the Source Color Pixels. For each pixel, determine its quadrant within the Target Area and update its color in the output grid using the corresponding color from the Key (TL, TR, BL, BR).
7.  **Output:** Return the modified grid.
"""


def find_key(grid):
    """
    Finds the unique 2x2 key block (non-0, non-8 colors), its top-left coordinates,
    its individual colors (TL, TR, BL, BR), and the set of its unique colors.
    Returns None for all if not found.
    """
    rows, cols = grid.shape
    for r in range(rows - 1):
        for c in range(cols - 1):
            subgrid = grid[r:r+2, c:c+2]
            # Check if all elements are not 0 (white) and not 8 (azure)
            if np.all((subgrid != 0) & (subgrid != 8)):
                key_colors = set(subgrid.flatten())
                key_tl = subgrid[0, 0]
                key_tr = subgrid[0, 1]
                key_bl = subgrid[1, 0]
                key_br = subgrid[1, 1]
                return subgrid, (r, c), key_colors, key_tl, key_tr, key_bl, key_br
    # Key not found
    return None, None, None, None, None, None, None

def find_source_color_and_coords(grid, key_colors_set, key_coords):
    """
    Identifies the source color and the coordinates of all pixels with that color
    located outside the key area.
    Source color is the unique color present in both key_colors_set and among
    non-white, non-azure pixels outside the key.
    Returns (source_color, list_of_source_coords) or (None, None) if ambiguous/not found.
    """
    if key_colors_set is None or key_coords is None:
        return None, None # Cannot proceed without a key

    key_r, key_c = key_coords
    rows, cols = grid.shape
    
    outside_pixels_data = [] # Stores (r, c, color)
    outside_colors = set()

    # Iterate through grid to find potential source pixels
    for r in range(rows):
        for c in range(cols):
            # Check if pixel is outside the key's 2x2 bounding box
            is_outside_key = not (key_r <= r < key_r + 2 and key_c <= c < key_c + 2)
            
            if is_outside_key:
                color = grid[r, c]
                # Check if color is not white (0) and not azure (8)
                if color != 0 and color != 8:
                    outside_pixels_data.append((r, c, color))
                    outside_colors.add(color)

    # Find the unique intersection color
    possible_source_colors = key_colors_set.intersection(outside_colors)

    if len(possible_source_colors) != 1:
        # print(f"Debug: Ambiguous source color. Intersection: {possible_source_colors}")
        return None, None # Source color is not unique or not found

    source_color = list(possible_source_colors)[0]

    # Collect coordinates of actual source pixels
    source_pixel_coords = []
    for r, c, color in outside_pixels_data:
        if color == source_color:
            source_pixel_coords.append((r, c))

    if not source_pixel_coords:
        # print(f"Debug: Source color {source_color} identified, but no pixels found outside key.")
        return source_color, [] # Return color but empty list if no pixels found

    return source_color, source_pixel_coords


def calculate_target_area_bounds(source_pixel_coords):
    """
    Calculates the bounding box (min_row, min_col, max_row, max_col)
    for the given list of coordinates.
    Returns None if the list is empty.
    """
    if not source_pixel_coords:
        return None

    coords_array = np.array(source_pixel_coords)
    min_r, min_c = coords_array.min(axis=0)
    max_r, max_c = coords_array.max(axis=0)

    return min_r, min_c, max_r, max_c


def transform(input_grid):
    """
    Transforms the input grid by recoloring pixels based on their quadrant
    relative to the bounding box of source pixels, using a 2x2 color key.
    """
    # Convert input to numpy array for easier processing
    grid = np.array(input_grid, dtype=int)
    # 1. Initialize output grid as a copy
    output_grid = np.copy(grid)

    # 2. Find Key
    key_matrix, key_coords, key_colors_set, key_tl, key_tr, key_bl, key_br = find_key(grid)
    if key_matrix is None:
        # print("Error: Could not find the 2x2 key.")
        return input_grid # Return original if key is missing

    # 3. Identify Source Color & Coordinates
    source_color, source_pixel_coords = find_source_color_and_coords(grid, key_colors_set, key_coords)

    if source_color is None:
        # print("Error: Could not uniquely identify the source color or no source pixels found.")
        return input_grid # Return original if source color ambiguous or no pixels

    if not source_pixel_coords:
         # print("Info: Source color identified, but no instances found outside the key. No changes needed.")
         return input_grid # No pixels to transform

    # 4. Define Target Area
    target_bounds = calculate_target_area_bounds(source_pixel_coords)
    # This check is technically redundant if source_pixel_coords is not empty, but safe
    if target_bounds is None:
        # print("Error: Could not determine target area bounds.") # Should not happen if source_pixel_coords is populated
        return input_grid

    min_r, min_c, max_r, max_c = target_bounds

    # 5. Calculate Quadrant Boundaries
    target_height = max_r - min_r + 1
    target_width = max_c - min_c + 1

    # Rows with index < mid_row_exclusive are Top
    # Cols with index < mid_col_exclusive are Left
    mid_row_exclusive = min_r + target_height // 2
    mid_col_exclusive = min_c + target_width // 2

    # 6. Apply Transformation
    # Iterate through each source pixel coordinate
    for r, c in source_pixel_coords:
        # Determine quadrant based on the target area's center lines
        is_top = r < mid_row_exclusive
        is_left = c < mid_col_exclusive

        new_color = -1 # Default invalid color
        if is_top and is_left:         # Top-Left
            new_color = key_tl
        elif is_top and not is_left:   # Top-Right
            new_color = key_tr
        elif not is_top and is_left:   # Bottom-Left
            new_color = key_bl
        elif not is_top and not is_left:# Bottom-Right
            new_color = key_br

        # Update the output grid
        if new_color != -1: # Should always be true given the quadrant logic
           output_grid[r, c] = new_color
        # else: print(f"Warning: Could not determine quadrant for pixel at ({r},{c})") # Should not happen

    # 7. Output: Convert back to list of lists
    return output_grid.tolist()