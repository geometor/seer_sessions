import numpy as np
from collections import defaultdict

"""
Transforms an input grid by swapping the vertical positions of the two distinct 
non-background color groups present. It identifies the upper and lower groups 
based on their bounding boxes. The lower group remains in its original position. 
The upper group is moved vertically downwards so that it is positioned directly 
below the lower group, while preserving the original vertical gap (number of 
background rows) that existed between their bounding boxes in the input.
"""

def get_color_group_properties(grid: np.ndarray) -> dict:
    """
    Finds non-background colors and properties of their pixel groups.

    Args:
        grid: A numpy array representing the input grid.

    Returns:
        A dictionary where keys are colors (int > 0) and values are 
        dictionaries containing:
          'coords': A set of (row, col) tuples for all pixels of that color.
          'bbox': A tuple (min_r, max_r, min_c, max_c) representing the 
                  bounding box of the color group.
        Returns an empty dictionary if no non-background pixels are found.
    """
    rows, cols = grid.shape
    # Use defaultdict to easily initialize data for each new color found
    color_groups = defaultdict(lambda: {'coords': set(), 'min_r': rows, 'max_r': -1, 'min_c': cols, 'max_c': -1})
    found_non_background = False

    # Iterate through the grid to find pixels and update group properties
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if color != 0:  # Ignore background color
                found_non_background = True
                group = color_groups[color]
                # Add coordinate to the set for this color
                group['coords'].add((r, c))
                # Update bounding box extents
                group['min_r'] = min(group['min_r'], r)
                group['max_r'] = max(group['max_r'], r)
                group['min_c'] = min(group['min_c'], c)
                group['max_c'] = max(group['max_c'], c)

    if not found_non_background:
        return {} # Return empty if only background exists

    # Convert defaultdict to a regular dict and finalize the bbox structure
    result = {}
    for color, group_data in color_groups.items():
         result[color] = {
             'coords': group_data['coords'],
             'bbox': (group_data['min_r'], group_data['max_r'], group_data['min_c'], group_data['max_c'])
         }
    return result


def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    """
    Applies the vertical color group swapping transformation.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    input_array = np.array(input_grid, dtype=int)
    rows, cols = input_array.shape
    
    # Initialize output grid with background color (0)
    output_array = np.zeros_like(input_array)

    # 1. Find the two distinct non-background color groups and their properties
    color_groups = get_color_group_properties(input_array)

    # Check if exactly two non-background colors were found
    if len(color_groups) != 2:
        # Based on examples, we expect exactly two colors.
        # Return the original grid if this condition isn't met.
        print(f"Warning: Expected 2 non-background colors, found {len(color_groups)}. Returning original grid.")
        return input_grid
        
    # 2. Identify the two colors and their corresponding groups
    colors = list(color_groups.keys())
    color1, color2 = colors[0], colors[1]
    group1, group2 = color_groups[color1], color_groups[color2]

    # 3. Determine which group is upper and which is lower based on min_row of bounding box
    if group1['bbox'][0] < group2['bbox'][0]:
        upper_group, lower_group = group1, group2
        upper_color, lower_color = color1, color2
    else:
        upper_group, lower_group = group2, group1
        upper_color, lower_color = color2, color1
        
    # Extract bounding box info for easier access
    upper_min_r, upper_max_r, _, _ = upper_group['bbox']
    lower_min_r, lower_max_r, _, _ = lower_group['bbox']
    
    # 4. Calculate the vertical gap between the bounding boxes
    # gap = top row of lower group's bbox - bottom row of upper group's bbox - 1
    gap = lower_min_r - upper_max_r - 1
    
    # 5. Place the lower group in the output grid at its original position
    for r, c in lower_group['coords']:
        # Check bounds just in case, though coords come from the input grid size
        if 0 <= r < rows and 0 <= c < cols:
            output_array[r, c] = lower_color
        
    # 6. Calculate the vertical shift needed for the upper group's pixels
    # The new top row for the upper group should be below the lower group's bottom row, 
    # separated by the original gap.
    # new_upper_group_start_row = bottom row of lower group's bbox + gap + 1
    new_upper_group_start_row = lower_max_r + gap + 1
    # shift = new starting row - original starting row
    shift = new_upper_group_start_row - upper_min_r
    
    # 7. Place the upper group in the output grid at its new shifted position
    for r, c in upper_group['coords']:
        new_r = r + shift
        # Check if the new position is within grid bounds before placing the pixel
        if 0 <= new_r < rows and 0 <= c < cols:
             output_array[new_r, c] = upper_color
        else:
            # This might indicate an issue if the shifted object goes off-grid
            print(f"Warning: Calculated new row {new_r} for upper group pixel at ({r},{c}) is out of bounds ({rows}x{cols}). Pixel omitted.")

    # Convert the final output NumPy array back to a list of lists
    return output_array.tolist()
