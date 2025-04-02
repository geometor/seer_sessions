import numpy as np
from collections import defaultdict

"""
Identifies distinct groups of pixels based on their non-background color.
Reverses the vertical stacking order of these color groups while maintaining their internal structure, 
horizontal position, and the vertical spacing that originally existed between them. 
The absolute vertical position of the resulting block is determined by placing the group 
that moves to the top (originally the bottom group) such that its top row aligns with the 
original top row of the entire object collection.
"""

def find_color_groups(grid):
    """Finds all pixels belonging to each non-background color.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        tuple: A tuple containing:
            - defaultdict: Dictionary mapping color values to lists of (row, col) coordinates.
            - list: A list of unique non-background colors found in the grid, preserving order of appearance roughly top-to-bottom, left-to-right.
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

    # 1. Identify all unique non-background colors and their pixel coordinates.
    color_coords, unique_colors = find_color_groups(input_grid_np)

    # If no non-background colors, return the empty grid.
    if not unique_colors:
        return output_grid.tolist()

    # 2. & 3. For each color group, determine its properties (pixels, bounding box, height).
    #    Also store the original minimum row for later shift calculation.
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

    # 4. Sort the identified color groups based on their original top row (`min_row`).
    groups.sort(key=lambda g: g['min_row'])
    
    # Store the original top row of the entire collection of objects
    if not groups: # Should not happen if unique_colors exist, but safety check
         return output_grid.tolist()
    original_overall_min_row = groups[0]['min_row']


    # 5. Calculate the vertical gaps between consecutive groups in the original sorted order.
    #    Gap is the number of background rows between the max_row of one group and the min_row of the next.
    gaps = []
    if len(groups) > 1:
        for i in range(len(groups) - 1):
            # Gap = next group's top - current group's bottom - 1
            gap = groups[i+1]['min_row'] - groups[i]['max_row'] - 1
            gaps.append(max(0, gap)) # Ensure gap is not negative

    # 6. Reverse the order of the sorted list of color groups. This is the target placement order.
    reversed_groups = list(reversed(groups))

    # 7. Reverse the order of the list of calculated gaps. These gaps will be used between the reversed groups.
    reversed_gaps = list(reversed(gaps))

    # 8. Determine the starting row for placing the first group in the reversed sequence.
    #    This will be the original minimum row of the topmost object in the input grid.
    current_target_row = original_overall_min_row

    # 9. Iterate through the reversed list of color groups to place them onto the output grid.
    for i, group in enumerate(reversed_groups):
        # a. Calculate the vertical shift required for the current group.
        #    Shift = target top row - original top row
        shift = current_target_row - group['original_min_row']

        # b. Place all pixels of the current group onto the output grid at the new position.
        for r, c in group['pixels']:
            new_r = r + shift
            # Check bounds just in case, although logic should prevent out-of-bounds
            if 0 <= new_r < rows and 0 <= c < cols:
                output_grid[new_r, c] = group['color']

        # c. Update the `current_target_row` for placing the *next* group.
        #    The next group starts below the current one, considering the relevant gap.
        #    New target row = current group's new max row + gap + 1
        #    Current group's new max row = group['original_min_row'] + shift + group['height'] - 1
        
        new_max_row_current_group = group['original_min_row'] + shift + group['height'] - 1
        
        # Add the corresponding gap (if one exists after this group)
        if i < len(reversed_gaps):
            current_target_row = new_max_row_current_group + reversed_gaps[i] + 1
        else:
            # If this is the last group, we don't need to calculate the next start row,
            # but we could set it just past the current group for consistency (though unused).
            current_target_row = new_max_row_current_group + 1

    # 10. Return the completed output grid as a list of lists.
    return output_grid.tolist()