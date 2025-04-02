
## train_1

**input:**
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


**output:**
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


## train_2

**input:**
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


**output:**
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

Okay, let's break down the task based on the examples provided.

## Perception

1.  **Input Structure:** The input grids contain distinct shapes made of non-white pixels set against a white background.
2.  **Objects:** In `train_1`, we see two distinct objects: a yellow horizontal line and a green hollow rectangle below it. In `train_2`, we see a complex red shape and multiple disconnected azure shapes located above the red shape. It appears that objects are grouped by color.
3.  **Color Grouping:** All pixels of the same non-white color seem to act as a single unit or group, even if they form disconnected shapes (like the azure pixels in `train_2`).
4.  **Transformation:** The core transformation appears to be a vertical rearrangement of these color groups. In `train_1`, the yellow group (line) and the green group (rectangle) swap their vertical positions. In `train_2`, the azure group (all azure pixels collectively) and the red group swap their vertical positions.
5.  **Spacing:** The relative vertical spacing *between* the bounding boxes of the color groups seems to be preserved during the swap. For instance, in `train_1`, the yellow line is directly above the green rectangle (0 rows gap), and in the output, the green rectangle is directly above the yellow line (0 rows gap). Similarly, in `train_2`, the lowest azure pixel is directly above the highest red pixel, and in the output, the lowest red pixel is directly above the highest azure pixel.
6.  **Internal Structure:** The internal structure and relative positions of pixels within each color group remain unchanged.
7.  **Horizontal Position:** The horizontal position of each color group appears unchanged relative to the grid boundaries.

## Facts


```yaml
task_type: object_manipulation

elements:
  - role: background
    properties:
      color: white
      value: 0
  - role: color_group
    description: A collection of all pixels sharing the same non-background color. Acts as a single unit for transformation.
    properties:
      color: any non-white color (e.g., yellow, green, red, azure)
      value: 1-9
      shape: Can be contiguous or non-contiguous, simple or complex.
      vertical_extent: Defined by the minimum and maximum row indices occupied by pixels of this color.
      horizontal_extent: Defined by the minimum and maximum column indices occupied by pixels of this color.

relationships:
  - type: vertical_ordering
    description: Color groups are ordered vertically based on their topmost pixel row index.
    between: [color_group, color_group]
  - type: vertical_spacing
    description: The number of background rows separating the bounding boxes of vertically adjacent color groups.
    between: [color_group, color_group]

actions:
  - name: identify_color_groups
    input: input_grid
    output: list of color_groups with their properties (pixels, color, vertical_extent)
  - name: determine_vertical_order
    input: list of color_groups
    output: ordered list of color_groups (top to bottom)
  - name: reverse_vertical_order
    input: ordered list of color_groups
    output: list of color_groups in reversed vertical order
  - name: calculate_vertical_shifts
    input: original_order, reversed_order, original_vertical_spacing
    output: vertical shift amount for each color_group
    description: Calculates how many rows each group needs to move up or down to achieve the reversed order while preserving inter-group spacing.
  - name: apply_shifts
    input: input_grid, color_groups, vertical_shifts
    output: output_grid
    description: Creates the output grid by moving pixels of each color group according to the calculated vertical shift.

goal: Reverse the vertical order of the distinct color groups found in the input grid, preserving their internal structure, horizontal positions, and the vertical spacing between them.
```


## Natural Language Program

1.  Identify all unique non-background colors present in the input grid.
2.  For each unique non-background color, determine the set of all pixel coordinates belonging to that color. Treat this set as a single "color group".
3.  For each color group, calculate its vertical bounding box by finding the minimum and maximum row indices occupied by its pixels.
4.  Determine the initial vertical order of the color groups based on their minimum row indices (topmost group first).
5.  Calculate the vertical gaps (number of rows) between the bounding boxes of consecutive groups in the initial order.
6.  Determine the target vertical order by reversing the initial order of the color groups.
7.  Create a new output grid of the same dimensions as the input grid, filled entirely with the background color (white, 0).
8.  Iterate through the color groups in their target vertical order (which is the reversed order). For each group:
    a.  Calculate the target top row for the current group. This will be the row immediately below the bottom row of the previously placed group (or row 0 if it's the first group being placed), plus the original vertical gap that existed *above* this group in the *initial* ordering.
    b.  Calculate the vertical shift required for this group: `shift = target_top_row - original_min_row`.
    c.  For every pixel belonging to the current color group in the input grid, place its color into the output grid at `(original_row + shift, original_column)`.
9.  Return the completed output grid.
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
```python
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
```
