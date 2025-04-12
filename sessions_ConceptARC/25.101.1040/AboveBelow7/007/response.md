```python
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
        Returns an empty dictionary if no non-background pixels are found or 
        if grid dimensions are invalid.
    """
    if grid.ndim != 2 or grid.shape[0] == 0 or grid.shape[1] == 0:
        return {} # Handle empty or invalid grid
        
    rows, cols = grid.shape
    # Use defaultdict to easily initialize data for each new color found
    # Initialize min values high and max values low
    color_groups = defaultdict(lambda: {'coords': set(), 'min_r': rows, 'max_r': -1, 'min_c': cols, 'max_c': -1})
    found_non_background = False

    # Iterate through the grid to find pixels and update group properties
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if color != 0:  # Ignore background color (0)
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
    Applies the vertical color group swapping transformation based on bounding boxes.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    input_array = np.array(input_grid, dtype=int)
    
    # Handle potential empty input grid
    if input_array.size == 0:
        return []
        
    rows, cols = input_array.shape
    
    # 5. Initialize an output grid of the same size, filled with background color.
    output_array = np.zeros_like(input_array)

    # 1. Identify the two distinct non-background colors and their properties.
    color_groups = get_color_group_properties(input_array)

    # Check if exactly two non-background colors were found.
    # If not, return the original grid (as per analysis of examples).
    if len(color_groups) != 2:
        # print(f"Warning: Expected 2 non-background colors, found {len(color_groups)}. Returning original grid.")
        return input_grid
        
    # 2. Get the two colors and their group data.
    colors = list(color_groups.keys())
    color1, color2 = colors[0], colors[1]
    group1, group2 = color_groups[color1], color_groups[color2]

    # 3. Designate the 'upper group' and 'lower group' based on bounding box minimum row.
    if group1['bbox'][0] < group2['bbox'][0]:
        upper_group, lower_group = group1, group2
        upper_color, lower_color = color1, color2
    else:
        upper_group, lower_group = group2, group1
        upper_color, lower_color = color2, color1
        
    # Extract specific bounding box values for clarity.
    upper_min_r, upper_max_r, _, _ = upper_group['bbox']
    lower_min_r, lower_max_r, _, _ = lower_group['bbox']
    
    # 4. Calculate the vertical gap between the bounding boxes.
    # gap = top row of lower bbox - bottom row of upper bbox - 1
    gap = lower_min_r - upper_max_r - 1
    
    # Ensure gap is not negative (shouldn't happen if bboxes don't overlap vertically)
    gap = max(0, gap) 

    # 6. Copy all pixels belonging to the 'lower group' to the output grid at original positions.
    for r, c in lower_group['coords']:
        # Basic bounds check (defensive programming)
        if 0 <= r < rows and 0 <= c < cols:
            output_array[r, c] = lower_color
        
    # 7. Calculate the necessary downward vertical shift for the 'upper group' pixels.
    # The new top row for the upper group = bottom row of lower group + gap + 1
    new_upper_group_start_row = lower_max_r + gap + 1
    # shift = difference between new start row and original start row
    shift = new_upper_group_start_row - upper_min_r
    
    # 8. Copy all pixels belonging to the 'upper group' to the output grid at shifted positions.
    for r, c in upper_group['coords']:
        new_r = r + shift
        # Check if the new position is within grid bounds before placing the pixel.
        if 0 <= new_r < rows and 0 <= c < cols:
             output_array[new_r, c] = upper_color
        # else:
            # Optional: Warning if pixels are shifted out of bounds
            # print(f"Warning: Calculated new row {new_r} for upper group pixel at ({r},{c}) is out of bounds ({rows}x{cols}). Pixel omitted.")

    # Convert the final output NumPy array back to a list of lists for the required return type.
    return output_array.tolist()
```