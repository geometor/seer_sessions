import numpy as np

"""
Recolors pixels within a bounded area based on their quadrant, using a 2x2 color key found elsewhere.

1.  **Locate the Key:** Find the unique 2x2 block of pixels in the input grid where none of the four pixels are white (0) or azure (8). Record the four colors (Key-TL, Key-TR, Key-BL, Key-BR) and the key's location.
2.  **Identify the Target Area:** Determine the rectangular region where modifications occur. This area is typically enclosed by a single-pixel-thick frame of azure (8) pixels. Find the bounding box of all non-azure (8) pixels; if it's framed by azure (8), the Target Area consists of all pixels strictly *inside* this frame. Record its boundaries (top, bottom, left, right) and dimensions (height, width).
3.  **Identify the Source Color:** Find the single color value that is present both within the 2x2 Key and also appears at least once within the identified Target Area in the input grid (excluding white (0)). This is the Source Color.
4.  **Determine Quadrants:** Calculate the center of the Target Area. The midpoint row is `top + height // 2` and the midpoint column is `left + width // 2`. Pixels with row index `< midpoint_row` are in the top half; pixels with column index `< midpoint_col` are in the left half. This divides the Target Area into four quadrants: Top-Left (TL), Top-Right (TR), Bottom-Left (BL), Bottom-Right (BR).
5.  **Apply Transformation:** Create a copy of the input grid. Iterate through each pixel within the Target Area's boundaries. If a pixel in the input grid has the Source Color:
    *   Determine which quadrant it falls into (TL, TR, BL, BR).
    *   Change the color of this pixel in the copied grid to the corresponding Key color: Key-TL for TL quadrant, Key-TR for TR, Key-BL for BL, Key-LR for BR.
6.  **Output:** The modified grid.
"""

def find_key(grid):
    """Finds the 2x2 key block (non-0, non-8 colors) and its top-left coordinates."""
    rows, cols = grid.shape
    for r in range(rows - 1):
        for c in range(cols - 1):
            subgrid = grid[r:r+2, c:c+2]
            # Check if all elements are not 0 and not 8
            if np.all((subgrid != 0) & (subgrid != 8)):
                return subgrid, (r, c)
    return None, None # Key not found

def find_target_area(grid):
    """
    Identifies the target area, assuming it's framed by azure (8) pixels.
    Returns the boundaries (top, left, bottom, right) of the area *inside* the frame.
    """
    rows, cols = grid.shape
    azure_color = 8

    # Find coordinates of all non-azure pixels
    non_azure_coords = np.argwhere(grid != azure_color)

    if non_azure_coords.size == 0:
        return None # No non-azure pixels found

    # Determine the bounding box of non-azure pixels
    min_r, min_c = non_azure_coords.min(axis=0)
    max_r, max_c = non_azure_coords.max(axis=0)

    # Define potential frame coordinates
    frame_top_r = min_r - 1
    frame_bottom_r = max_r + 1
    frame_left_c = min_c - 1
    frame_right_c = max_c + 1

    # Check if frame coordinates are within grid bounds
    if frame_top_r < 0 or frame_bottom_r >= rows or frame_left_c < 0 or frame_right_c >= cols:
        # print(f"Warning: Bounding box touches grid edge ({min_r, min_c} to {max_r, max_c}). Cannot confirm frame.")
        # Fallback: maybe the target area IS the bounding box? Let's return the bbox for now.
        # Based on examples, a frame seems required. Returning None indicates failure.
        return None 


    # Check if the surrounding 1-pixel border is entirely azure
    is_framed = True
    # Check top row of frame
    if not np.all(grid[frame_top_r, frame_left_c : frame_right_c + 1] == azure_color):
        is_framed = False
    # Check bottom row of frame
    if is_framed and not np.all(grid[frame_bottom_r, frame_left_c : frame_right_c + 1] == azure_color):
         is_framed = False
    # Check left column of frame (excluding corners already checked)
    if is_framed and not np.all(grid[frame_top_r + 1 : frame_bottom_r, frame_left_c] == azure_color):
        is_framed = False
    # Check right column of frame (excluding corners already checked)
    if is_framed and not np.all(grid[frame_top_r + 1 : frame_bottom_r, frame_right_c] == azure_color):
        is_framed = False

    if is_framed:
        # Target area is inside the frame
        target_top = min_r
        target_left = min_c
        target_bottom = max_r
        target_right = max_c
        return target_top, target_left, target_bottom, target_right
    else:
        # print("Warning: Non-azure bounding box is not fully framed by azure.")
        # If no frame, the logic fails based on examples.
        return None

def find_source_color(grid, key_colors, target_area_bounds):
    """
    Finds the unique color present in the key and within the target area (non-0).
    """
    if target_area_bounds is None:
        return -1 # Indicate error

    target_top, target_left, target_bottom, target_right = target_area_bounds
    
    target_area_colors = set()
    # Iterate only within the target area
    for r in range(target_top, target_bottom + 1):
        for c in range(target_left, target_right + 1):
             pixel_color = grid[r, c]
             if pixel_color != 0: # Exclude white background
                 target_area_colors.add(pixel_color)

    # Find colors present in both the key and the target area (excluding 0)
    valid_source_colors = key_colors.intersection(target_area_colors)

    if len(valid_source_colors) == 1:
        return list(valid_source_colors)[0]
    else:
        # print(f"Warning: Found {len(valid_source_colors)} potential source colors: {valid_source_colors}")
        return -1 # Indicate error or ambiguous source


def transform(input_grid):
    """
    Transforms the input grid by recoloring pixels based on their quadrant
    within a framed target area, using a 2x2 color key.
    """
    # Convert input to numpy array for easier processing
    grid = np.array(input_grid, dtype=int)
    # Create a copy to modify and return
    output_grid = np.copy(grid)

    # 1. Locate the Key
    key_matrix, key_coords = find_key(grid)
    if key_matrix is None:
        # print("Error: Could not find the 2x2 key.")
        return input_grid # Return original if key is missing

    key_colors = set(key_matrix.flatten())
    key_ul = key_matrix[0, 0]
    key_ur = key_matrix[0, 1]
    key_ll = key_matrix[1, 0]
    key_lr = key_matrix[1, 1]

    # 2. Identify the Target Area (inside the azure frame)
    target_area_bounds = find_target_area(grid)
    if target_area_bounds is None:
        # print("Error: Could not identify a framed target area.")
        return input_grid # Return original if target area is not found as expected

    target_top, target_left, target_bottom, target_right = target_area_bounds
    target_height = target_bottom - target_top + 1
    target_width = target_right - target_left + 1

    # Check for valid dimensions
    if target_height <= 0 or target_width <= 0:
        # print("Error: Identified target area has invalid dimensions.")
        return input_grid

    # 3. Identify the Source Color
    source_color = find_source_color(grid, key_colors, target_area_bounds)
    if source_color == -1:
        # print("Error: Could not uniquely identify the source color.")
        return input_grid # Return original if source color is ambiguous or missing

    # 4. Determine Quadrants boundaries (midpoints are exclusive)
    # Pixels with row index < mid_row_exclusive are Top
    # Pixels with col index < mid_col_exclusive are Left
    mid_row_exclusive = target_top + target_height // 2
    mid_col_exclusive = target_left + target_width // 2

    # 5. Apply Transformation
    # Iterate through each pixel *only* within the identified Target Area
    for r in range(target_top, target_bottom + 1):
        for c in range(target_left, target_right + 1):
            # Check if the pixel in the original grid is the source color
            if grid[r, c] == source_color:
                # Determine quadrant
                is_top = r < mid_row_exclusive
                is_left = c < mid_col_exclusive

                new_color = -1 # Default invalid color
                if is_top and is_left:         # Top-Left
                    new_color = key_ul
                elif is_top and not is_left:   # Top-Right
                    new_color = key_ur
                elif not is_top and is_left:   # Bottom-Left
                    new_color = key_ll
                elif not is_top and not is_left:# Bottom-Right
                    new_color = key_lr

                if new_color != -1:
                   output_grid[r, c] = new_color
                # No else needed, if quadrant determination failed somehow, pixel remains unchanged

    # 6. Output: Convert back to list of lists
    return output_grid.tolist()