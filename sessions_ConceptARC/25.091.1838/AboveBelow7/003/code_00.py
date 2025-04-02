import numpy as np
from collections import defaultdict

"""
Identifies distinct groups of pixels based on their non-background color.
Reverses the vertical stacking order of these color groups while maintaining their internal structure, 
horizontal position, and the vertical spacing that originally existed between them. 
The absolute vertical position of the resulting block is determined by placing the group 
that moves to the top at its original starting row.
"""

def find_color_groups(grid):
    """Finds all pixels belonging to each non-background color.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        tuple: A tuple containing:
            - defaultdict: Dictionary mapping color values to lists of (row, col) coordinates.
            - list: A list of unique non-background colors found in the grid.
    """
    color_coords = defaultdict(list)
    rows, cols = grid.shape
    unique_colors = []
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if color != 0: # 0 is background (white)
                color_coords[color].append((r, c))
                if color not in unique_colors:
                    unique_colors.append(color)
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
    input_grid_np = np.array(input_grid, dtype=int)
    rows, cols = input_grid_np.shape
    
    # Initialize output_grid with background color
    output_grid = np.zeros_like(input_grid_np)

    # 1. Identify all unique non-background colors and their pixel coordinates.
    color_coords, unique_colors = find_color_groups(input_grid_np)

    # If no non-background colors, return the original grid (or an empty one of same size)
    if not unique_colors:
        return output_grid.tolist()

    # 2. & 3. For each color group, determine its properties.
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
                'original_min_row': properties['min_row'] # Store original position
            }
            groups.append(group_info)

    # 4. Sort the identified color groups based on their original top row (`min_row`).
    groups.sort(key=lambda g: g['min_row'])

    # 5. Calculate the vertical gaps between consecutive groups in the original order.
    gaps = []
    if len(groups) > 1:
        for i in range(len(groups) - 1):
            # Gap = next group's top - current group's bottom - 1
            gap = groups[i+1]['min_row'] - groups[i]['max_row'] - 1
            gaps.append(max(0, gap)) # Ensure gap is not negative if groups overlap (though not expected here)

    # 7. Reverse the order of the sorted list of color groups.
    reversed_groups = list(reversed(groups))

    # 8. Reverse the order of the list of calculated gaps.
    reversed_gaps = list(reversed(gaps))

    # 6. Create the output grid (already initialized).
    
    # 9. Initialize the target row for placing the first group in the reversed sequence.
    # This is the original starting row of the group that is now at the top.
    if not reversed_groups: # Should not happen if unique_colors exist, but safety check
         return output_grid.tolist()
         
    current_target_row = reversed_groups[0]['original_min_row']

    # 10. Iterate through the reversed list of color groups to place them.
    for i, group in enumerate(reversed_groups):
        # a. Calculate the vertical shift required for the current group.
        shift = current_target_row - group['original_min_row']

        # b. Place all pixels of the current group onto the output grid at the new position.
        for r, c in group['pixels']:
            new_r = r + shift
            # Check bounds just in case, although logic should prevent out-of-bounds
            if 0 <= new_r < rows and 0 <= c < cols:
                output_grid[new_r, c] = group['color']

        # c. Update the `current_target_row` for placing the *next* group: add current group's height.
        current_target_row += group['height']
        
        # d. If there is a gap corresponding to the space *after* the current group, add the gap size + 1.
        if i < len(reversed_gaps):
            current_target_row += reversed_gaps[i] + 1 # +1 because gap is space *between* rows

    # 11. Return the completed output grid.
    return output_grid.tolist()