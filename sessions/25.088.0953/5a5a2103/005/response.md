```python
import numpy as np
import collections

"""
The transformation identifies horizontal and vertical lines of a single 'divider'
color that partition the input grid into rectangular regions. For each row of 
regions (defined by the horizontal dividers), it identifies the 'source color' 
which is the single non-white, non-divider color present in the leftmost region 
of that row in the input grid. Then, for every region within that same row, it 
finds all pixels that are neither white nor the divider color in the input grid 
and recolors them to the identified 'source color' in the output grid. Divider 
lines and white background pixels remain unchanged.
"""

def find_divider_color_and_lines(grid):
    """
    Identifies the divider color and the indices of horizontal and vertical divider lines.
    A color is considered the divider if it forms all observed full horizontal lines 
    and/or all observed full vertical lines (excluding white color 0).

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        tuple: (divider_color, h_div_indices, v_div_indices)
               divider_color (int): The color used for dividing lines (0-9). Returns None if no clear divider found.
               h_div_indices (list): List of row indices containing horizontal dividers.
               v_div_indices (list): List of column indices containing vertical dividers.
    """
    height, width = grid.shape
    h_divs = []
    v_divs = []
    potential_divider_colors = set()

    # Find all horizontal lines and their colors
    h_line_colors = {}
    for r in range(height):
        unique_colors = np.unique(grid[r, :])
        if len(unique_colors) == 1 and unique_colors[0] != 0:
            color = unique_colors[0]
            h_line_colors[r] = color
            potential_divider_colors.add(color)

    # Find all vertical lines and their colors
    v_line_colors = {}
    for c in range(width):
        unique_colors = np.unique(grid[:, c])
        if len(unique_colors) == 1 and unique_colors[0] != 0:
            color = unique_colors[0]
            v_line_colors[c] = color
            potential_divider_colors.add(color)

    # Determine the divider color
    divider_color = None
    possible_dividers = []

    for color in potential_divider_colors:
        is_sole_h_color = all(c == color for r, c in h_line_colors.items()) if h_line_colors else True
        is_sole_v_color = all(c == color for c, c_val in v_line_colors.items()) if v_line_colors else True
        
        # A color qualifies if it's the *only* color forming horizontal lines (if any exist)
        # AND the *only* color forming vertical lines (if any exist).
        # Or if only one orientation of lines exists, it must be the color for all of them.
        forms_any_h = any(c == color for r, c in h_line_colors.items())
        forms_any_v = any(c == color for c, c_val in v_line_colors.items())

        if (forms_any_h or forms_any_v) and is_sole_h_color and is_sole_v_color:
             possible_dividers.append(color)

    # Expecting only one divider color based on examples
    if len(possible_dividers) == 1:
        divider_color = possible_dividers[0]
        h_divs = [r for r, c in h_line_colors.items() if c == divider_color]
        v_divs = [c for c, c_val in v_line_colors.items() if c_val == divider_color]
    # else: # Ambiguous or no clear divider, handle potentially (e.g., return None)
        # print(f"Warning: Found {len(possible_dividers)} potential divider colors: {possible_dividers}. Cannot proceed reliably.")
        pass 
        
    return divider_color, sorted(list(set(h_divs))), sorted(list(set(v_divs)))


def transform(input_grid):
    """
    Transforms the input grid by recoloring shapes within regions based on the 
    color found in the leftmost region of the same row band.

    Args:
        input_grid (list): A list of lists representing the input grid.

    Returns:
        list: A list of lists representing the transformed output grid.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_grid_np) # Initialize output as a copy
    height, width = input_grid_np.shape

    # 1. Identify the divider color and the locations of divider lines.
    divider_color, h_divs, v_divs = find_divider_color_and_lines(input_grid_np)

    # Handle case where no clear dividers are found 
    if divider_color is None:
        # Strategy fails if dividers aren't identified. Return input as default.
        return input_grid 

    # 2. Define the boundaries of each region (content areas between dividers).
    row_starts = [0] + [r + 1 for r in h_divs]
    row_ends = [r for r in h_divs] + [height]
    
    col_starts = [0] + [c + 1 for c in v_divs]
    col_ends = [c for c in v_divs] + [width]
    
    num_region_rows = len(row_starts)
    num_region_cols = len(col_starts)

    # 3. Iterate through each row of regions (horizontal bands).
    for i in range(num_region_rows):
        r_start = row_starts[i]
        r_end = row_ends[i]

        # Skip if this band has zero height
        if r_start >= r_end:
            continue

        # 4. Identify the leftmost region in this band.
        if not col_starts: # Grid must have width > 0
             continue
        leftmost_c_start = col_starts[0]
        leftmost_c_end = col_ends[0]
        
        # Skip if leftmost region has zero width
        if leftmost_c_start >= leftmost_c_end:
             continue

        # 5. Extract the leftmost region from the input grid.
        leftmost_region = input_grid_np[r_start:r_end, leftmost_c_start:leftmost_c_end]

        # 6. Determine the source color for this band.
        # Find unique colors in the leftmost region, excluding white (0) and the divider color.
        unique_colors = np.unique(leftmost_region)
        source_colors = [c for c in unique_colors if c != 0 and c != divider_color]
        
        source_color = None
        if len(source_colors) == 1:
            source_color = source_colors[0]
        # else: # Handle cases with zero or multiple non-background/divider colors if necessary
            # Based on examples, expect exactly one. If not, maybe default or raise error.
            # For now, if not exactly one, we won't recolor this band.
            # print(f"Warning: Found {len(source_colors)} potential source colors in band {i}, region 0: {source_colors}. Skipping recoloring for this band.")
            # continue # Skip to the next band if source color is ambiguous

        # If no valid source color found (e.g., leftmost region empty or only bg/divider), skip band
        if source_color is None:
            continue

        # 7. Iterate through all regions (columns) within this same band.
        for j in range(num_region_cols):
            c_start = col_starts[j]
            c_end = col_ends[j]

            # Skip if this region has zero width
            if c_start >= c_end:
                 continue

            # 8. Identify target pixels within this region in the input grid.
            # Target pixels are those that are not white (0) and not the divider color.
            for r_local in range(r_end - r_start):
                for c_local in range(c_end - c_start):
                    current_r, current_c = r_start + r_local, c_start + c_local
                    original_color = input_grid_np[current_r, current_c]
                    
                    # 9. Recolor target pixels in the output grid.
                    if original_color != 0 and original_color != divider_color:
                        output_grid[current_r, current_c] = source_color
                    # else: Keep original color (white or divider)

    # 10. Return the modified output grid as a list of lists.
    return output_grid.tolist()
```