```python
import numpy as np
from collections import defaultdict

"""
Identifies distinct groups of pixels based on their non-background color.
Reverses the vertical stacking order of these color groups while maintaining their internal structure, 
horizontal position, and the vertical spacing that originally existed between them. 
The absolute vertical position of the resulting stack is determined by placing the new top group 
(originally the bottom group) such that its top row (`min_row`) equals the `min_row` of the 
original top group plus the height of the original top group.
"""

def find_color_groups(grid):
    """Finds all pixels belonging to each non-background color.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        tuple: A tuple containing:
            - defaultdict: Dictionary mapping color values to lists of (row, col) coordinates.
            - list: A list of unique non-background colors found in the grid, preserving 
                    order of appearance roughly top-to-bottom, left-to-right.
    """
    color_coords = defaultdict(list)
    rows, cols = grid.shape
    unique_colors = []
    color_set = set() # Keep track of colors added to unique_colors
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if color != 0: # 0 is background (white)
                color_coords[color].append((r, c))
                if color not in color_set:
                    unique_colors.append(color)
                    color_set.add(color)
    return color_coords, unique_colors

def get_group_properties(coords):
    """Calculates bounding box and height for a list of coordinates.

    Args:
        coords (list): A list of (row, col) coordinates for a color group.

    Returns:
        dict or None: A dictionary with 'min_row', 'max_row', 'height' 
                      if coordinates exist, otherwise None.
    """
    if not coords:
        return None
    rows = [r for r, c in coords]
    min_row = min(rows)
    max_row = max(rows)
    height = max_row - min_row + 1
    return {'min_row': min_row, 'max_row': max_row, 'height': height}

def transform(input_grid):
    """
    Reverses the vertical order of color groups in the grid according to the specified rules.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert to numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    rows, cols = input_grid_np.shape
    
    # Initialize output_grid with background color (0)
    output_grid = np.zeros_like(input_grid_np)

    # --- Workflow ---

    # 1. Identify Color Groups: Find unique non-background colors and their pixels.
    color_coords, unique_colors = find_color_groups(input_grid_np)

    # If no non-background colors, return the empty grid.
    if not unique_colors:
        return output_grid.tolist()

    # 2. Calculate Group Properties: Get bounding box and height for each group.
    groups = []
    for color in unique_colors:
        coords = color_coords[color]
        properties = get_group_properties(coords)
        if properties:
            group_info = {
                'color': color,
                'pixels': coords,
                'min_row': properties['min_row'],
                'max_row': properties['max_row'],
                'height': properties['height'],
                'original_min_row': properties['min_row'] # Store original top position
            }
            groups.append(group_info)

    # Handle case where no valid groups were formed (e.g., only background pixels)
    if not groups:
         return output_grid.tolist()

    # 3. Determine Initial Order and Gaps: Sort groups top-to-bottom, calculate gaps.
    groups.sort(key=lambda g: g['min_row'])
    
    # Remember the original top group's properties
    original_top_group_min_row = groups[0]['min_row']
    original_top_group_height = groups[0]['height']

    # Calculate vertical gaps between consecutive groups in the original sorted order.
    gaps = []
    if len(groups) > 1:
        for i in range(len(groups) - 1):
            # Gap = next group's top - current group's bottom - 1
            gap = groups[i+1]['min_row'] - groups[i]['max_row'] - 1
            gaps.append(max(0, gap)) # Ensure gap is not negative

    # 4. Reverse Order: Reverse the groups list and the gaps list for placement.
    reversed_groups = list(reversed(groups))
    reversed_gaps = list(reversed(gaps))

    # 5. Calculate Target Starting Row: Determine where the new top group starts.
    current_target_row = original_top_group_min_row + original_top_group_height

    # 6. Create Output Grid: Already initialized above.

    # 7. Place Groups: Iterate through reversed groups and place them in the output grid.
    for i, group in enumerate(reversed_groups):
        # a. Calculate the vertical shift needed for the current group.
        shift = current_target_row - group['original_min_row']

        # b. Place all pixels of the current group onto the output grid at the new position.
        for r, c in group['pixels']:
            new_r = r + shift
            # Check bounds just in case, although logic should prevent out-of-bounds
            if 0 <= new_r < rows and 0 <= c < cols:
                output_grid[new_r, c] = group['color']

        # c. Update the `current_target_row` for placing the *next* group.
        #    The next group starts below the current one, accounting for the relevant gap.
        #    Update happens *after* placing the current group.
        #    Next row = current target row + current group height + gap
        gap_to_add = 0
        if i < len(reversed_gaps):
             gap_to_add = reversed_gaps[i] + 1 # +1 because gap is space *between* rows
        
        current_target_row += group['height'] + gap_to_add


    # 8. Return Result: Convert the numpy array back to a list of lists.
    return output_grid.tolist()
```