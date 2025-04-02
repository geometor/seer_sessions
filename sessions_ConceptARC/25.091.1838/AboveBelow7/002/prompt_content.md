
Previous Code:
```python
import numpy as np
from collections import defaultdict

"""
Identifies distinct groups of pixels based on their non-background color.
Reverses the vertical order of these color groups while maintaining their internal structure, 
horizontal position, and the vertical spacing that originally existed between them.

Workflow:
1. Find all unique non-background colors and the coordinates of pixels for each color.
2. For each color group, determine its vertical bounding box (min_row, max_row).
3. Store information about each group: color, pixel coordinates, min_row, max_row, height.
4. Sort the groups based on their original top row (min_row).
5. Calculate the vertical gaps between consecutive groups in the original sorted order.
6. Determine the starting row for the first group in the output (which is the original starting row of the topmost group).
7. Create a new grid filled with the background color.
8. Reverse the order of the sorted groups list.
9. Reverse the order of the calculated gaps list.
10. Iterate through the reversed groups list:
    a. Calculate the vertical shift required to move the group from its original position to its new target position. The target position depends on the accumulated height of previously placed groups and the gaps between them.
    b. Apply the shift to each pixel coordinate of the current group and draw it onto the output grid.
    c. Update the target starting row for the next group by adding the current group's height and the corresponding gap (if any).
11. Return the modified grid.
"""

def find_color_groups(grid):
    """Finds all pixels belonging to each non-background color."""
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
    """Calculates bounding box and height for a list of coordinates."""
    if not coords:
        return None
    rows = [r for r, c in coords]
    min_row = min(rows)
    max_row = max(rows)
    height = max_row - min_row + 1
    return {'min_row': min_row, 'max_row': max_row, 'height': height}

def transform(input_grid):
    """
    Reverses the vertical order of color groups in the grid.
    """
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    
    # Initialize output_grid with background color
    output_grid = np.zeros_like(input_grid)

    # 1. Find color groups and their pixels
    color_coords, unique_colors = find_color_groups(input_grid)

    if not unique_colors:
        # If no non-background colors, return the original grid
        return input_grid.tolist()

    # 2. & 3. Get properties for each group
    groups = []
    for color in unique_colors:
        coords = color_coords[color]
        properties = get_group_properties(coords)
        if properties:
            groups.append({
                'color': color,
                'pixels': coords,
                'min_row': properties['min_row'],
                'max_row': properties['max_row'],
                'height': properties['height']
            })

    # 4. Sort groups by original vertical position (top to bottom)
    groups.sort(key=lambda g: g['min_row'])

    # Store original min_row for shift calculation later
    for group in groups:
        group['original_min_row'] = group['min_row']

    # 5. Calculate original vertical gaps between consecutive groups
    gaps = []
    if len(groups) > 1:
        for i in range(len(groups) - 1):
            gap = groups[i+1]['min_row'] - groups[i]['max_row'] - 1
            gaps.append(gap)

    # 6. Determine the overall starting row (topmost row of the topmost object)
    original_start_row = groups[0]['min_row'] if groups else 0

    # 8. Reverse the order of groups
    groups.reverse()

    # 9. Reverse the order of gaps
    gaps.reverse()

    # 10. Place groups onto the output grid in the new order
    current_target_row = original_start_row
    for i, group in enumerate(groups):
        # a. Calculate vertical shift
        shift = current_target_row - group['original_min_row']

        # b. Apply shift and draw pixels
        for r, c in group['pixels']:
            new_r = r + shift
            # Ensure the pixel stays within grid bounds (shouldn't be necessary if logic is correct, but safe)
            if 0 <= new_r < rows:
                output_grid[new_r, c] = group['color']

        # c. Update target row for the next group
        current_target_row += group['height']
        if i < len(gaps): # If there's a gap after this group
            current_target_row += gaps[i]
            
    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 4 4 4 4 4 4 4 0 0 0
0 0 0 0 3 3 3 3 3 3 3 3 0 0 0
0 0 0 0 3 0 0 0 0 0 0 3 0 0 0
0 0 0 0 3 0 0 0 0 0 0 3 0 0 0
0 0 0 0 3 0 0 0 0 0 0 3 0 0 0
0 0 0 0 3 3 3 3 3 3 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 3 3 3 3 3 3 0 0 0
0 0 0 0 3 0 0 0 0 0 0 3 0 0 0
0 0 0 0 3 0 0 0 0 0 0 3 0 0 0
0 0 0 0 3 0 0 0 0 0 0 3 0 0 0
0 0 0 0 3 3 3 3 3 3 3 3 0 0 0
0 0 0 0 4 4 4 4 4 4 4 4 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 3 3 3 3 3 3 0 0 0
0 0 0 0 3 0 0 0 0 0 0 3 0 0 0
0 0 0 0 3 0 0 0 0 0 0 3 0 0 0
0 0 0 0 3 0 0 0 0 0 0 3 0 0 0
0 0 0 0 3 3 3 3 3 3 3 3 0 0 0
0 0 0 0 4 4 4 4 4 4 4 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 36
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 24.0

## Example 2:
Input:
```
0 0 0 8 8 0 0 0 0 0 0 0
0 0 8 8 8 8 0 0 0 8 0 0
0 8 8 8 8 8 8 0 8 8 8 0
0 2 2 2 2 2 2 0 2 2 2 0
0 2 0 0 0 0 2 0 2 0 2 0
0 2 0 0 0 0 2 0 2 0 2 0
0 2 0 0 0 0 2 0 2 0 2 0
0 2 0 0 0 0 2 0 2 2 2 0
0 2 2 2 2 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 2 0 2 2 2 0
0 2 0 0 0 0 2 0 2 0 2 0
0 2 0 0 0 0 2 0 2 0 2 0
0 2 0 0 0 0 2 0 2 0 2 0
0 2 0 0 0 0 2 0 2 2 2 0
0 2 2 2 2 2 2 0 0 8 0 0
0 0 0 8 8 0 0 0 8 8 8 0
0 0 8 8 8 8 0 0 0 0 0 0
0 8 8 8 8 8 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 2 2 2 2 2 2 0 2 2 2 0
0 2 0 0 0 0 2 0 2 0 2 0
0 2 0 0 0 0 2 0 2 0 2 0
0 2 0 0 0 0 2 0 2 0 2 0
0 2 0 0 0 0 2 0 2 2 2 0
0 2 2 2 2 2 2 0 0 0 0 0
0 0 0 8 8 0 0 0 0 0 0 0
0 0 8 8 8 8 0 0 0 8 0 0
0 8 8 8 8 8 8 0 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 67
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 39.88095238095239
