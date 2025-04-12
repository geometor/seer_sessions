```python
import numpy as np
from collections import defaultdict

"""
Identifies the two distinct non-background color groups in the input grid.
Determines which group is vertically above the other based on their bounding boxes.
Calculates the vertical gap between their bounding boxes.
Creates an output grid where the original lower color group maintains its position,
and the original upper color group is moved directly below the lower group, 
preserving the original vertical gap between their bounding boxes.
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
    color_groups = defaultdict(lambda: {'coords': set(), 'min_r': rows, 'max_r': -1, 'min_c': cols, 'max_c': -1})
    found_non_background = False

    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if color != 0:
                found_non_background = True
                group = color_groups[color]
                group['coords'].add((r, c))
                # Update bounding box extents
                group['min_r'] = min(group['min_r'], r)
                group['max_r'] = max(group['max_r'], r)
                group['min_c'] = min(group['min_c'], c)
                group['max_c'] = max(group['max_c'], c)

    if not found_non_background:
        return {}

    # Convert defaultdict to regular dict and finalize bbox structure
    result = {}
    for color, group_data in color_groups.items():
         result[color] = {
             'coords': group_data['coords'],
             'bbox': (group_data['min_r'], group_data['max_r'], group_data['min_c'], group_data['max_c'])
         }
    return result


def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    """
    Transforms the input grid by swapping the vertical positions of the two 
    non-background color groups, keeping the lower one fixed and moving the 
    upper one below it, preserving the gap.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    input_array = np.array(input_grid, dtype=int)
    rows, cols = input_array.shape
    
    # Initialize output grid with background color (0)
    output_array = np.zeros_like(input_array)

    # Find the color groups and their properties
    color_groups = get_color_group_properties(input_array)

    # Check if exactly two non-background colors were found
    if len(color_groups) != 2:
        # If not 2 colors, return the original grid (or handle as error)
        # Based on examples, we expect exactly two colors.
        # Returning input grid might be safest for unexpected test cases.
        print(f"Warning: Expected 2 non-background colors, found {len(color_groups)}. Returning original grid.")
        return input_grid
        
    # Identify the two colors
    colors = list(color_groups.keys())
    color1 = colors[0]
    color2 = colors[1]
    group1 = color_groups[color1]
    group2 = color_groups[color2]

    # Determine which group is upper and which is lower based on min_row
    if group1['bbox'][0] < group2['bbox'][0]:
        upper_group = group1
        lower_group = group2
        upper_color = color1
        lower_color = color2
    else:
        upper_group = group2
        lower_group = group1
        upper_color = color2
        lower_color = color1
        
    # Extract bounding box info for easier access
    upper_min_r, upper_max_r, _, _ = upper_group['bbox']
    lower_min_r, lower_max_r, _, _ = lower_group['bbox']
    
    # Calculate the vertical gap between the bounding boxes of the groups
    # gap = top row of lower group - bottom row of upper group - 1
    gap = lower_min_r - upper_max_r - 1
    
    # Place the lower group in the output grid at its original position
    for r, c in lower_group['coords']:
        # Basic boundary check (shouldn't be necessary if input is valid)
        if 0 <= r < rows and 0 <= c < cols:
            output_array[r, c] = lower_color
        
    # Determine the new starting row for the top of the upper group's bbox
    # It should start below the lower group's bbox, maintaining the gap
    # new_upper_top_row = bottom row of lower group + gap + 1
    new_upper_group_start_row = lower_max_r + gap + 1
    
    # Calculate the vertical shift needed for the upper group's pixels
    shift = new_upper_group_start_row - upper_min_r
    
    # Place the upper group in the output grid at its new shifted position
    for r, c in upper_group['coords']:
        new_r = r + shift
        # Check if the new position is within grid bounds
        if 0 <= new_r < rows and 0 <= c < cols:
             output_array[new_r, c] = upper_color
        else:
            # This might indicate an issue if the shifted object goes off-grid
            print(f"Warning: Calculated new row {new_r} for upper group pixel at ({r},{c}) is out of bounds ({rows}x{cols}). Pixel omitted.")

    # Convert the output NumPy array back to a list of lists
    return output_array.tolist()
```