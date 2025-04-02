import numpy as np
import collections

"""
Identifies vertical bands of non-background colors in the input grid.
For each band, it determines a primary color (ignoring gray-5) and calculates the bounding box of all non-background pixels within that band.
A color transformation rule is applied to the primary color. This rule depends on whether gray-5 is present anywhere in the *entire* input grid.
  - If gray-5 is present: Blue(1)->Yellow(4), Red(2)->Red(2), Green(3)->Blue(1), Yellow(4)->Green(3).
  - If gray-5 is absent: Red(2)->Orange(7), Yellow(4)->Magenta(6), Magenta(6)->Red(2), Orange(7)->Yellow(4).
The calculated bounding box in the output grid is filled with the transformed color.
"""

def find_vertical_bands(grid):
    """
    Finds contiguous columns containing non-background pixels.

    Args:
        grid (np.array): Input grid.

    Returns:
        list: A list of tuples, where each tuple represents a band
              as (start_column_index, end_column_index_exclusive).
    """
    bands = []
    num_cols = grid.shape[1]
    if num_cols == 0:
        return bands

    # Check which columns contain any non-zero pixels
    has_non_zero = np.any(grid != 0, axis=0)

    in_band = False
    start_col = 0
    for c in range(num_cols):
        if has_non_zero[c] and not in_band:
            in_band = True
            start_col = c
        elif not has_non_zero[c] and in_band:
            in_band = False
            bands.append((start_col, c))

    # Handle case where the last column is part of a band
    if in_band:
        bands.append((start_col, num_cols))

    return bands

def process_band(grid_slice, start_col, color_map):
    """
    Processes a single vertical band slice to find its bounding box,
    primary color, and transformed output color.

    Args:
        grid_slice (np.array): The slice of the input grid corresponding to the band.
        start_col (int): The starting column index of this slice in the original grid.
        color_map (dict): The color transformation map to use.

    Returns:
        tuple: (r_min, r_max, c_min, c_max, output_color) if a primary color is found,
               otherwise None.
    """
    # Find coordinates of all non-background pixels in the slice
    non_zero_coords_local = np.argwhere(grid_slice != 0)
    if non_zero_coords_local.size == 0:
        return None # Band is effectively empty

    # Determine the primary (non-gray, non-background) color within this band
    primary_colors = np.unique(grid_slice[(grid_slice != 0) & (grid_slice != 5)])

    if primary_colors.size == 0:
         # This band might only contain gray or background, ignore for color transformation
         # but still need bbox if only gray exists for shape transformation?
         # The examples suggest output objects correspond to primary colors.
         # If only gray, treat as empty for output object creation.
        return None
    elif primary_colors.size > 1:
        # This case is not expected based on examples, assume one primary color per band
        # print(f"Warning: Multiple primary colors found in band starting at col {start_col}: {primary_colors}")
        # Defaulting to the smallest color number if multiple exist
        input_color = np.min(primary_colors)
    else:
      input_color = primary_colors[0]


    # Apply the color transformation
    output_color = color_map.get(input_color, input_color) # Default to input if not in map

    # Calculate the bounding box using all non-background pixels (including gray)
    rows = non_zero_coords_local[:, 0]
    local_cols = non_zero_coords_local[:, 1]
    global_cols = local_cols + start_col # Convert local column indices to global

    r_min, r_max = np.min(rows), np.max(rows)
    c_min, c_max = np.min(global_cols), np.max(global_cols) # Use global columns for bbox

    return r_min, r_max, c_min, c_max, output_color


def transform(input_grid):
    """
    Transforms the input grid based on vertical bands, bounding boxes,
    and a context-dependent color mapping rule.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed output grid.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    output_grid = np.zeros_like(input_grid_np) # Initialize with background color 0

    # Check if gray (5) is present anywhere in the input grid (excluding background 0)
    unique_colors_non_bg = np.unique(input_grid_np[input_grid_np != 0])
    gray_present = 5 in unique_colors_non_bg

    # Define the color map based on the presence of gray
    if gray_present:
        # Rule from train_1
        color_map = {1: 4, 2: 2, 3: 1, 4: 3}
    else:
        # Rule from train_2
        color_map = {2: 7, 4: 6, 6: 2, 7: 4}

    # Find vertical bands of non-background colors
    bands = find_vertical_bands(input_grid_np)

    # Process each band
    for start_col, end_col in bands:
        # Extract the slice corresponding to the band
        band_slice = input_grid_np[:, start_col:end_col]

        # Process the band to get bounding box and output color
        result = process_band(band_slice, start_col, color_map)

        if result:
            r_min, r_max, c_min, c_max, output_color = result
            # Fill the bounding box in the output grid with the transformed color
            output_grid[r_min : r_max + 1, c_min : c_max + 1] = output_color

    return output_grid.tolist()