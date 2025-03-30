```python
import numpy as np
import collections

"""
The transformation identifies horizontal and vertical lines of a single 'divider'
color that partition the input grid into rectangular regions. For each horizontal
band of regions (defined by the horizontal dividers), it identifies the 'source 
color' which is the single non-white, non-divider color present in the leftmost 
region of that band in the input grid. Then, for every region within that same 
horizontal band, it finds all pixels that are neither white nor the divider color 
in the input grid and recolors them to the identified 'source color' in the 
output grid. Divider lines and white background pixels remain unchanged.
"""

def find_divider_color_and_lines(grid):
    """
    Identifies the divider color and the indices of horizontal and vertical divider lines.
    The divider color must be the unique non-white color forming *all* full-width 
    horizontal lines and *all* full-height vertical lines.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        tuple: (divider_color, h_div_indices, v_div_indices)
               divider_color (int): The color used for dividing lines (0-9). Returns None if no clear divider found.
               h_div_indices (list): Sorted list of row indices containing horizontal dividers.
               v_div_indices (list): Sorted list of column indices containing vertical dividers.
    """
    height, width = grid.shape
    h_lines = collections.defaultdict(list)
    v_lines = collections.defaultdict(list)
    all_h_indices = []
    all_v_indices = []

    # Find all horizontal lines and their colors
    for r in range(height):
        unique_colors = np.unique(grid[r, :])
        if len(unique_colors) == 1 and unique_colors[0] != 0:
            color = unique_colors[0]
            h_lines[color].append(r)
            all_h_indices.append(r)

    # Find all vertical lines and their colors
    for c in range(width):
        unique_colors = np.unique(grid[:, c])
        if len(unique_colors) == 1 and unique_colors[0] != 0:
            color = unique_colors[0]
            v_lines[color].append(c)
            all_v_indices.append(c)

    # Determine the divider color
    potential_dividers = []
    
    # Consider colors present in horizontal lines
    for color, rows in h_lines.items():
        # Check if this color forms ALL horizontal lines
        if set(rows) == set(all_h_indices):
             # Check if this color also forms ALL vertical lines (if any exist)
             if not all_v_indices or (color in v_lines and set(v_lines[color]) == set(all_v_indices)):
                 potential_dividers.append(color)

    # Consider colors present in vertical lines (only if no h-lines were found or the h-line color didn't match)
    if not potential_dividers and not all_h_indices:
         for color, cols in v_lines.items():
             # Check if this color forms ALL vertical lines
             if set(cols) == set(all_v_indices):
                  potential_dividers.append(color)

    # If exactly one consistent divider color is found
    if len(potential_dividers) == 1:
        divider_color = potential_dividers[0]
        # Use the found indices for this color, handling cases where one orientation might be empty
        h_divs = sorted(h_lines.get(divider_color, [])) 
        v_divs = sorted(v_lines.get(divider_color, []))
        return divider_color, h_divs, v_divs
    else:
        # No single consistent divider color found
        return None, [], []


def transform(input_grid):
    """
    Transforms the input grid based on the divider and recoloring logic.

    Args:
        input_grid (list): A list of lists representing the input grid.

    Returns:
        list: A list of lists representing the transformed output grid.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_grid_np) # Initialize output as a copy
    height, width = input_grid_np.shape

    # 1. Identify Grid Structure: Find divider color and lines
    divider_color, h_divs, v_divs = find_divider_color_and_lines(input_grid_np)

    # If no clear divider structure is found, return the original grid
    if divider_color is None:
        # print("Warning: No consistent divider color found. Returning input grid.")
        return input_grid 

    # 2. Define Regions: Calculate region boundaries
    row_starts = [0] + [r + 1 for r in h_divs]
    row_ends = [r for r in h_divs] + [height]
    
    col_starts = [0] + [c + 1 for c in v_divs]
    col_ends = [c for c in v_divs] + [width]
    
    num_region_rows = len(row_starts)
    num_region_cols = len(col_starts)

    # 3. Determine Source Colors per Horizontal Band
    source_color_map = {} # Maps row_band_index to source_color
    for i in range(num_region_rows):
        r_start = row_starts[i]
        r_end = row_ends[i]

        # Skip if this band has zero height (e.g., consecutive dividers)
        if r_start >= r_end:
            continue

        # Identify the leftmost region in this band
        # Ensure there are columns defined
        if num_region_cols == 0: 
             continue
        leftmost_c_start = col_starts[0]
        leftmost_c_end = col_ends[0]
        
        # Skip if leftmost region has zero width (e.g., consecutive dividers)
        if leftmost_c_start >= leftmost_c_end:
             continue

        # Extract the leftmost region
        leftmost_region = input_grid_np[r_start:r_end, leftmost_c_start:leftmost_c_end]

        # Find the unique color(s) in the leftmost region, excluding white (0) and the divider color.
        unique_colors_in_region = np.unique(leftmost_region)
        potential_source_colors = [c for c in unique_colors_in_region if c != 0 and c != divider_color]
        
        # Store the source color if exactly one is found
        if len(potential_source_colors) == 1:
            source_color_map[i] = potential_source_colors[0]
        # else:
            # Handle cases with zero or multiple non-background/divider colors if necessary
            # Based on examples, we expect exactly one. If not, this band won't be recolored.
            # print(f"Warning: Found {len(potential_source_colors)} potential source colors in band {i}, region 0: {potential_source_colors}. Skipping recoloring for this band.")
            pass 

    # 4. Recolor Grid based on Source Colors
    for i in range(num_region_rows): # Iterate through horizontal bands
        r_start = row_starts[i]
        r_end = row_ends[i]

        # Skip zero-height bands
        if r_start >= r_end: continue
        
        # Get the source color for this band (if found)
        source_color = source_color_map.get(i)
        
        # If no valid source color was found for this band, skip recoloring it
        if source_color is None:
            continue

        # Iterate through all regions (columns) within this band
        for j in range(num_region_cols):
            c_start = col_starts[j]
            c_end = col_ends[j]

            # Skip zero-width regions
            if c_start >= c_end: continue

            # Iterate through pixels within the current region's boundaries
            for r in range(r_start, r_end):
                for c in range(c_start, c_end):
                    original_color = input_grid_np[r, c]
                    
                    # If the pixel is part of a 'content object' (not white, not divider)
                    if original_color != 0 and original_color != divider_color:
                        # Recolor it in the output grid using the band's source color
                        output_grid[r, c] = source_color
                    # Otherwise (pixel is white or divider), it remains unchanged (already copied)

    # 5. Return Output
    return output_grid.tolist()
```