import numpy as np

"""
Recolors specific pixels within an azure-framed area based on their quadrant 
relative to the area's center, using colors defined by a separate 2x2 key.

1.  **Copy Input:** Create a mutable copy of the input grid.
2.  **Locate the Key:** Find the unique 2x2 block where no pixel is white (0) or azure (8). Record the four colors (Key-TL, Key-TR, Key-BL, Key-BR) and the set of key colors.
3.  **Identify Frame Bounds:** Find the min/max row/column indices of all azure (8) pixels.
4.  **Define Target Area:** Calculate the area strictly inside the azure frame boundaries (min_row+1, min_col+1, max_row-1, max_col-1).
5.  **Identify the Source Color:** Find the unique non-white (0) color present both in the Key colors and within the Target Area.
6.  **Determine Quadrants:** Calculate the center dividing lines (rows/columns) of the Target Area.
7.  **Apply Transformation:** Iterate through pixels within the Target Area. If a pixel matches the Source Color, change its color in the copied grid to the Key color corresponding to its quadrant.
8.  **Output:** Return the modified grid.
"""

def find_key(grid):
    """Finds the 2x2 key block (non-0, non-8 colors) and its top-left coordinates."""
    rows, cols = grid.shape
    for r in range(rows - 1):
        for c in range(cols - 1):
            subgrid = grid[r:r+2, c:c+2]
            # Check if all elements are not 0 (white) and not 8 (azure)
            if np.all((subgrid != 0) & (subgrid != 8)):
                return subgrid, (r, c)
    return None, None # Key not found

def find_target_area_by_frame(grid):
    """
    Identifies the target area by finding the bounding box of azure (8) pixels
    and returning the coordinates of the region strictly inside this frame.
    Returns the boundaries (top, left, bottom, right) of the inner area.
    """
    azure_color = 8
    azure_coords = np.argwhere(grid == azure_color)

    if azure_coords.size == 0:
        # print("Debug: No azure pixels found.")
        return None # No frame found

    # Determine the bounding box of azure pixels
    azure_min_r, azure_min_c = azure_coords.min(axis=0)
    azure_max_r, azure_max_c = azure_coords.max(axis=0)

    # Calculate the potential inner area bounds
    target_top = azure_min_r + 1
    target_left = azure_min_c + 1
    target_bottom = azure_max_r - 1
    target_right = azure_max_c - 1

    # Check if the inner area is valid (at least 1x1)
    if target_top > target_bottom or target_left > target_right:
        # print(f"Debug: Invalid inner area derived from frame ({azure_min_r, azure_min_c} to {azure_max_r, azure_max_c}).")
        return None # Frame is too thin or invalid

    # Optional: Add further validation? E.g., check if the frame is solid.
    # For now, assume the bounding box defines the frame.

    return target_top, target_left, target_bottom, target_right

def find_source_color(grid, key_colors, target_area_bounds):
    """
    Finds the unique color present in the key colors and within the target area (non-0).
    """
    if target_area_bounds is None:
        return -1 # Indicate error: target area not defined

    target_top, target_left, target_bottom, target_right = target_area_bounds

    # Ensure bounds are valid before slicing
    if target_top > target_bottom or target_left > target_right:
         return -1 # Invalid target area

    target_area_grid = grid[target_top : target_bottom + 1, target_left : target_right + 1]
    
    # Find unique colors in the target area, excluding white (0)
    target_area_colors = set(np.unique(target_area_grid)) - {0}


    # Find colors present in both the key and the target area (excluding 0)
    valid_source_colors = key_colors.intersection(target_area_colors)

    if len(valid_source_colors) == 1:
        return list(valid_source_colors)[0]
    else:
        # print(f"Debug: Found {len(valid_source_colors)} potential source colors: {valid_source_colors}. Key: {key_colors}, Target: {target_area_colors}")
        return -1 # Indicate error or ambiguous source


def transform(input_grid):
    """
    Transforms the input grid by recoloring pixels based on their quadrant
    within an azure-framed target area, using a 2x2 color key.
    """
    # Convert input to numpy array for easier processing
    grid = np.array(input_grid, dtype=int)
    # 1. Create a mutable copy of the input grid
    output_grid = np.copy(grid)

    # 2. Locate the Key
    key_matrix, key_coords = find_key(grid)
    if key_matrix is None:
        # print("Error: Could not find the 2x2 key.")
        return input_grid # Return original if key is missing

    key_colors = set(key_matrix.flatten())
    key_tl = key_matrix[0, 0]
    key_tr = key_matrix[0, 1]
    key_bl = key_matrix[1, 0]
    key_br = key_matrix[1, 1]

    # 3. Identify Frame Bounds and 4. Define Target Area
    target_area_bounds = find_target_area_by_frame(grid)
    if target_area_bounds is None:
        # print("Error: Could not identify a framed target area.")
        return input_grid # Return original if target area not found

    target_top, target_left, target_bottom, target_right = target_area_bounds
    target_height = target_bottom - target_top + 1
    target_width = target_right - target_left + 1

    # Check for valid dimensions (should be caught by find_target_area_by_frame, but good practice)
    if target_height <= 0 or target_width <= 0:
        # print("Error: Identified target area has invalid dimensions.")
        return input_grid

    # 5. Identify the Source Color
    source_color = find_source_color(grid, key_colors, target_area_bounds)
    if source_color == -1:
        # print("Error: Could not uniquely identify the source color.")
        return input_grid # Return original if source color is ambiguous or missing

    # 6. Determine Quadrants boundaries (midpoints define the split)
    # Rows with index < mid_row_exclusive are Top
    # Cols with index < mid_col_exclusive are Left
    mid_row_exclusive = target_top + target_height // 2
    mid_col_exclusive = target_left + target_width // 2

    # 7. Apply Transformation
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
                    new_color = key_tl
                elif is_top and not is_left:   # Top-Right
                    new_color = key_tr
                elif not is_top and is_left:   # Bottom-Left
                    new_color = key_bl
                elif not is_top and not is_left:# Bottom-Right
                    new_color = key_br

                # Update the output grid if a valid quadrant was found
                if new_color != -1:
                   output_grid[r, c] = new_color
                # No else needed, if pixel isn't source color, it remains unchanged

    # 8. Output: Convert back to list of lists
    return output_grid.tolist()