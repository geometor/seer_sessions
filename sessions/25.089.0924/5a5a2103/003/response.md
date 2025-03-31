```python
import numpy as np
from collections import Counter

"""
Transformation Rule Natural Language Description:

1.  Determine the dimensions (height H, width W) of the input grid.
2.  Identify the 'separator color' by finding the most frequent color (excluding white/0) that forms continuous or near-continuous horizontal and vertical lines across the grid. The examples show Azure (8) and Green (3) as separator colors.
3.  Determine the dimensions (comp_h, comp_w) of the compartments formed by the separator lines (e.g., 4x4 in examples).
4.  Select the appropriate 'stamp pattern' based on the identified `separator_color`:
    *   If `separator_color` is Azure (8), use `Pattern_A = [(0, 1), (0, 2), (1, 2), (2, 0), (2, 1), (2, 2), (2, 3), (3, 1)]`.
    *   If `separator_color` is Green (3), use `Pattern_B = [(1, 0), (1, 1), (1, 3), (2, 1), (2, 2), (3, 2)]`.
    *   If the compartment size is not 4x4 or the separator color is not 3 or 8, the behavior is undefined by the examples (assume failure/empty output for now).
5.  Identify the starting coordinates `(r_start, c_start)` for each compartment. Group compartments by their starting row `r_start`.
6.  Initialize an output grid of the same dimensions as the input, filled with white (0).
7.  Copy all pixels matching the `separator_color` from the input grid to the output grid.
8.  Iterate through each unique starting row `r_start` identified for the compartments:
    a.  Scan all pixels within all compartments belonging to this row `r_start` in the *input* grid.
    b.  Identify the single 'significant color' present in these scanned pixels. This color is the most frequent one that is *not* white (0), *not* the `separator_color`, and *not* a noise color (Gray/5, Magenta/6). Store this as the 'row color'. If no such color exists, the 'row color' is white (0).
    c.  For each compartment `(r, c)` starting in this row `r_start`:
        i.  If the determined 'row color' is not white (0):
            1.  For each relative coordinate `(dr, dc)` in the selected 'stamp pattern':
                a.  Calculate the absolute coordinate `(abs_r, abs_c)` = `(r + dr, c + dc)`.
                b.  If `(abs_r, abs_c)` is within the grid bounds and not a separator location, set the pixel at `(abs_r, abs_c)` in the *output* grid to the 'row color'.
9.  Return the completed output grid.
"""

def find_separator_and_dimensions(grid):
    """
    Identifies the separator color, its line indices, and compartment dimensions.
    More robust version based on analysis.
    Args:
        grid (np.array): Input grid.
    Returns:
        tuple: (separator_color, h_sep_indices, v_sep_indices, comp_h, comp_w) or None if failed.
    """
    height, width = grid.shape
    
    # Count non-background colors
    colors, counts = np.unique(grid[grid != 0], return_counts=True)
    if len(colors) == 0:
        return None

    # --- Find Separator Color ---
    potential_separators = {}
    # Prioritize colors forming full lines
    for r in range(height):
        row_colors, row_counts = np.unique(grid[r,:], return_counts=True)
        for c_val, count in zip(row_colors, row_counts):
             if c_val != 0 and count == width: potential_separators[c_val] = potential_separators.get(c_val, 0) + height 
    for c in range(width):
        col_colors, col_counts = np.unique(grid[:,c], return_counts=True)
        for c_val, count in zip(col_colors, col_counts):
             if c_val != 0 and count == height: potential_separators[c_val] = potential_separators.get(c_val, 0) + width

    separator_color = -1
    if potential_separators:
        separator_color = max(potential_separators, key=potential_separators.get)
    else: # Fallback if no full lines - check majority lines (more robustly)
        temp_sep_counts = Counter()
        for r in range(height):
             line_colors, line_counts = np.unique(grid[r,:], return_counts=True)
             for c_val, count in zip(line_colors, line_counts):
                  if c_val != 0 and count > width * 0.5 : # Heuristic for majority line
                       temp_sep_counts[c_val]+=1
        for c in range(width):
             line_colors, line_counts = np.unique(grid[:,c], return_counts=True)
             for c_val, count in zip(line_colors, line_counts):
                  if c_val != 0 and count > height * 0.5 : # Heuristic for majority line
                       temp_sep_counts[c_val]+=1

        if temp_sep_counts:
             separator_color = temp_sep_counts.most_common(1)[0][0]
        else: # Absolute fallback: most frequent non-zero
             if len(colors) > 0:
                 separator_color = colors[np.argmax(counts)]
             else: return None


    if separator_color == -1: return None

    # --- Find Separator Indices ---
    # Use strict definition first, then relax if needed
    h_sep_indices = [r for r in range(height) if np.all(grid[r, :] == separator_color)]
    v_sep_indices = [c for c in range(width) if np.all(grid[:, c] == separator_color)]

    # If few/no full lines found, try majority threshold (useful if grid lines are partial)
    if len(h_sep_indices) < 2 : # Arbitrary threshold, maybe adjust based on grid size?
        h_sep_indices = [r for r in range(height) if np.count_nonzero(grid[r, :] == separator_color) > width * 0.6]
    if len(v_sep_indices) < 2 :
        v_sep_indices = [c for c in range(width) if np.count_nonzero(grid[:, c] == separator_color) > height * 0.6]

    # --- Calculate Compartment Dimensions ---
    # Use contiguous blocks of non-separator rows/cols
    row_indices = sorted([i for i in range(height) if i not in h_sep_indices])
    col_indices = sorted([i for i in range(width) if i not in v_sep_indices])

    comp_h = 0
    if row_indices:
        max_h = 0
        current_h = 0
        for i in range(len(row_indices)):
            if i > 0 and row_indices[i] == row_indices[i-1] + 1:
                current_h += 1
            else:
                max_h = max(max_h, current_h)
                current_h = 0
        comp_h = max(max_h, current_h) + 1 

    comp_w = 0
    if col_indices:
        max_w = 0
        current_w = 0
        for i in range(len(col_indices)):
            if i > 0 and col_indices[i] == col_indices[i-1] + 1:
                current_w += 1
            else:
                 max_w = max(max_w, current_w)
                 current_w = 0
        comp_w = max(max_w, current_w) + 1 

    if comp_h <= 0 or comp_w <= 0:
        # print(f"Warning: Calculated invalid compartment dimensions H:{comp_h}, W:{comp_w}")
        return None # Failed to determine valid dimensions

    return separator_color, h_sep_indices, v_sep_indices, comp_h, comp_w


def get_compartment_locations(height, width, h_sep_indices, v_sep_indices, comp_h, comp_w):
    """
    Calculates the top-left coordinates of each compartment and groups them by starting row.
    """
    compartments_by_row = {}
    row_starts = []
    current_row = 0
    while current_row < height:
        if current_row not in h_sep_indices:
             row_starts.append(current_row)
             # Important: step by actual compartment height, not just 1
             step = comp_h 
             current_row += step
        else:
            current_row += 1 # Skip separator row

    col_starts = []
    current_col = 0
    while current_col < width:
        if current_col not in v_sep_indices:
             col_starts.append(current_col)
             step = comp_w
             current_col += step
        else:
            current_col += 1 # Skip separator col

    # Generate compartment info            
    for r_start in row_starts:
        # Ensure row start is valid
        if r_start + comp_h > height: continue 
        
        row_compartments = []
        for c_start in col_starts:
             # Ensure col start is valid
             if c_start + comp_w > width: continue
             
             # Check if this compartment overlaps with a separator line
             is_valid = True
             # Check horizontal overlap
             # for r in range(r_start, r_start + comp_h):
             #      if r in h_sep_indices: is_valid=False; break
             # if not is_valid: continue
             # # Check vertical overlap
             # for c in range(c_start, c_start + comp_w):
             #      if c in v_sep_indices: is_valid=False; break
             # if not is_valid: continue

             comp_info = ((r_start, c_start), comp_h, comp_w)
             row_compartments.append(comp_info)

        if row_compartments:
             compartments_by_row[r_start] = row_compartments

    return compartments_by_row


def transform(input_grid):
    """
    Transforms the input grid based on the identified rules:
    - Find separator and compartments.
    - Select pattern based on separator color (8 or 3).
    - Determine row color based on significant input pixels (excluding noise 5, 6).
    - Stamp the selected pattern with the row color onto the output grid.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    output_grid = np.zeros_like(input_np) # Start with white

    # 1. Identify Separator and Compartment Dimensions
    sep_info = find_separator_and_dimensions(input_np)
    if sep_info is None:
        # print("Failed to find separator or valid dimensions")
        return output_grid.tolist() # Return empty grid on failure
        
    separator_color, h_sep_indices, v_sep_indices, comp_h, comp_w = sep_info
    
    # 2. Select Stamp Pattern based on separator color and dimensions
    stamp_pattern_relative = None
    # --- Define Known Patterns ---
    patterns = {
        8: [(0, 1), (0, 2), (1, 2), (2, 0), (2, 1), (2, 2), (2, 3), (3, 1)], # Pattern A for separator 8
        3: [(1, 0), (1, 1), (1, 3), (2, 1), (2, 2), (3, 2)]  # Pattern B for separator 3
    }

    if comp_h == 4 and comp_w == 4: # Check dimensions match known patterns
        if separator_color in patterns:
            stamp_pattern_relative = patterns[separator_color]
        else:
            # print(f"Separator color {separator_color} not recognized for 4x4 compartments.")
            return output_grid.tolist() # Unknown separator, return empty
    else:
        # print(f"Compartment size {comp_h}x{comp_w} does not match expected 4x4.")
        return output_grid.tolist() # Non-4x4, return empty
        
    # 3. Copy Separators to Output
    # Create masks for separator locations
    h_mask = np.zeros_like(input_np, dtype=bool)
    v_mask = np.zeros_like(input_np, dtype=bool)
    if h_sep_indices:
        h_mask[h_sep_indices, :] = True
    if v_sep_indices:
        v_mask[:, v_sep_indices] = True
    separator_mask = h_mask | v_mask
    # Apply only where the input actually has the separator color
    output_grid[separator_mask & (input_np == separator_color)] = separator_color

    # 4. Get Compartment Locations
    compartments_by_row = get_compartment_locations(height, width, h_sep_indices, v_sep_indices, comp_h, comp_w)
    if not compartments_by_row:
        # print("Failed to find compartment locations.")
        return output_grid.tolist() # Return grid with only separators if no compartments found

    # 5. Determine Row Colors and Fill Output Grid
    noise_colors = {0, separator_color, 5, 6} # Include 0 and separator explicitly

    for r_start, comps_in_row in compartments_by_row.items():
        # a. Find the significant color for this row
        pixel_colors = []
        for (r, c), h, w in comps_in_row:
            # Extract pixels from the INPUT grid for this compartment
            compartment_slice = input_np[r:min(r + h, height), c:min(c + w, width)]
            pixel_colors.extend(list(compartment_slice.flatten()))

        # Filter colors to find significant ones
        valid_colors = [color for color in pixel_colors if color not in noise_colors]
        
        significant_color_found = 0 # Default to white/background
        if valid_colors:
            color_counts = Counter(valid_colors)
            if color_counts:
                # Assume the most frequent valid color is the significant one
                significant_color_found = color_counts.most_common(1)[0][0]
        
        row_color = significant_color_found

        # b. Apply pattern to compartments in this row on the OUTPUT grid
        if row_color != 0: # Only stamp if a significant color was found
            for (r, c), h, w in comps_in_row:
                 # Apply pattern using the selected relative coordinates
                 for dr, dc in stamp_pattern_relative:
                     abs_r, abs_c = r + dr, c + dc
                     # Check bounds and ensure not overwriting a separator
                     if 0 <= abs_r < height and 0 <= abs_c < width:
                         # Check if the target location is NOT a separator line
                         is_sep_loc = (abs_r in h_sep_indices) or (abs_c in v_sep_indices)
                         if not is_sep_loc: 
                              output_grid[abs_r, abs_c] = row_color
                         # If it IS a separator location, double-check if input had separator color there
                         # This handles cases where pattern might touch a sparse separator line
                         elif input_np[abs_r, abs_c] != separator_color:
                             output_grid[abs_r, abs_c] = row_color


    return output_grid.tolist()
```