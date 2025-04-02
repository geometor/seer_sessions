```python
import numpy as np
from collections import Counter

"""
Identify primary horizontal and vertical structures based on dominant colors in rows and columns, respectively. 
Remove specific vertical structures based on the count of horizontal structures.

1. Identify the two non-background colors present (H_Color for horizontal, V_Color for vertical).
2. Determine which color dominates which rows/columns.
3. Count the number of rows dominated by H_Color (H_Count).
4. Identify the columns dominated by V_Color (V_Indices).
5. Select target column(s) based on H_Count:
    - H_Count >= 3: Middle column index from V_Indices.
    - H_Count == 2: Leftmost (minimum) column index from V_Indices.
    - H_Count == 1: Rightmost (maximum) column index from V_Indices.
6. Modify the grid: Change pixels with V_Color in the target column(s) to the background color (white, 0).
"""

def _get_dominant_color_info(grid):
    """
    Identifies dominant colors in rows/columns and determines H/V roles.

    Args:
        grid (np.array): The input grid.

    Returns:
        dict: Information about colors, counts, and indices, or None if the pattern is not met.
              Keys: "H_Color", "H_Count", "V_Color", "V_Indices"
    """
    height, width = grid.shape
    non_bg_colors = np.unique(grid[grid != 0])

    # Expect exactly two non-background colors for this pattern
    if len(non_bg_colors) != 2:
        return None 

    color1, color2 = non_bg_colors

    rows_dominated_by_c1 = []
    rows_dominated_by_c2 = []
    for r in range(height):
        row = grid[r, :]
        counts = Counter(c for c in row if c != 0)
        if not counts: continue
        # Find the most common non-zero color
        mc = counts.most_common(1)
        if mc:
            dominant_color = mc[0][0]
            if dominant_color == color1:
                rows_dominated_by_c1.append(r)
            elif dominant_color == color2:
                rows_dominated_by_c2.append(r)

    cols_dominated_by_c1 = []
    cols_dominated_by_c2 = []
    for c in range(width):
        col = grid[:, c]
        counts = Counter(p for p in col if p != 0)
        if not counts: continue
        # Find the most common non-zero color
        mc = counts.most_common(1)
        if mc:
             dominant_color = mc[0][0]
             if dominant_color == color1:
                 cols_dominated_by_c1.append(c)
             elif dominant_color == color2:
                 cols_dominated_by_c2.append(c)

    # Determine H_Color and V_Color. The color defining the structures to be removed (vertical)
    # is likely the one dominating fewer columns in the observed examples.
    # If counts are equal, use a fallback heuristic (fewer structures overall).
    if len(cols_dominated_by_c1) < len(cols_dominated_by_c2):
        v_color, h_color = color1, color2
        v_indices = cols_dominated_by_c1
        h_count = len(rows_dominated_by_c2)
    elif len(cols_dominated_by_c2) < len(cols_dominated_by_c1):
        v_color, h_color = color2, color1
        v_indices = cols_dominated_by_c2
        h_count = len(rows_dominated_by_c1)
    # Fallback heuristic for ties or ambiguity
    elif (len(cols_dominated_by_c1)+len(rows_dominated_by_c1)) < (len(cols_dominated_by_c2)+len(rows_dominated_by_c2)):
            v_color, h_color = color1, color2
            v_indices = cols_dominated_by_c1
            h_count = len(rows_dominated_by_c2)
    elif (len(cols_dominated_by_c1)+len(rows_dominated_by_c1)) > (len(cols_dominated_by_c2)+len(rows_dominated_by_c2)):
            v_color, h_color = color2, color1
            v_indices = cols_dominated_by_c2
            h_count = len(rows_dominated_by_c1)
    else:
        # If still tied, perhaps default based on color index or return None
        # Let's assume based on examples that vertical structures are 'less numerous'
        # If column counts are equal, maybe check row counts?
        if len(rows_dominated_by_c1) > len(rows_dominated_by_c2): # c1 is more horizontal
             v_color, h_color = color2, color1
             v_indices = cols_dominated_by_c2
             h_count = len(rows_dominated_by_c1)
        else: # c2 is more horizontal (or equal)
             v_color, h_color = color1, color2
             v_indices = cols_dominated_by_c1
             h_count = len(rows_dominated_by_c2)


    if not v_indices: # Need vertical structures to modify
        return None

    v_indices.sort() # Ensure consistent order for selection

    return {
        "H_Color": h_color,
        "H_Count": h_count,
        "V_Color": v_color,
        "V_Indices": v_indices,
    }


def _select_target_indices(v_indices, h_count):
    """
    Selects the target column indices based on the horizontal count.

    Args:
        v_indices (list): Sorted list of vertical structure column indices.
        h_count (int): Count of horizontal structures.

    Returns:
        list: The target column indices to modify.
    """
    target_indices = []
    num_v_lines = len(v_indices)

    if num_v_lines == 0:
        return []

    if h_count >= 3:
        # Select the middle index. Index at position N // 2
        middle_idx_pos = num_v_lines // 2
        target_indices.append(v_indices[middle_idx_pos])
    elif h_count == 2:
        # Select the minimum (leftmost) index
        target_indices.append(min(v_indices))
    elif h_count == 1:
        # Select the maximum (rightmost) index
        target_indices.append(max(v_indices))
        
    return target_indices


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    # Initialize output grid as a copy of the input
    output_np = np.copy(input_np)

    # 1. Identify dominant colors, structures, counts, and indices
    color_info = _get_dominant_color_info(input_np)

    # If the expected pattern (2 non-bg colors, distinct structures) isn't found, return the original grid
    if color_info is None:
        return input_grid

    h_count = color_info["H_Count"]
    v_color = color_info["V_Color"]
    v_indices = color_info["V_Indices"]

    # 2. Determine the target column index/indices to modify based on H_Count
    target_indices = _select_target_indices(v_indices, h_count)

    # 3. Modify the output grid
    if target_indices:
        for col_index in target_indices:
            # In the target column(s), find pixels with V_Color
            mask = output_np[:, col_index] == v_color
            # Change those pixels to background color (0)
            output_np[mask, col_index] = 0

    # Convert the result back to a list of lists
    return output_np.tolist()
```