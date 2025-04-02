
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

Okay, let's analyze the provided examples.

**Perception of Elements:**

*   **Example 1:** The input grid contains two distinct objects on a white background: a yellow horizontal line segment (1x8) and a green hollow rectangle (5x8) located directly below the yellow line. In the output grid, the green rectangle remains in the same position, but the yellow line has moved to the position directly below the green rectangle.
*   **Example 2:** The input grid contains two distinct color groups on a white background: several azure shapes clustered together at the top and a red shape (resembling a 'C') located below the azure shapes. In the output grid, the red 'C' shape remains in its original position, while the entire cluster of azure shapes has moved to occupy the space directly below the red 'C' shape. The relative arrangement of the azure shapes within their cluster is preserved.

**Common Pattern:** In both examples, there are two distinct non-background color objects (or groups of objects treated as one). One object/group is positioned vertically above the other. The transformation involves moving the *upper* object/group to the position directly *below* the *lower* object/group, while the lower object/group remains stationary. The horizontal position of the moved object/group is maintained.

**YAML Facts:**


```yaml
task_description: Swap the vertical positions of two distinct colored objects/groups, moving the upper one below the lower one.

examples:
  - id: train_1
    input:
      grid_size: [10, 15]
      background_color: white (0)
      objects:
        - color: yellow (4)
          shape: horizontal line segment
          bounding_box: [row_start: 3, row_end: 3, col_start: 4, col_end: 11]
          position: Above the green object
        - color: green (3)
          shape: hollow rectangle
          bounding_box: [row_start: 4, row_end: 8, col_start: 4, col_end: 11]
          position: Below the yellow object
    output:
      grid_size: [10, 15]
      background_color: white (0)
      objects:
        - color: green (3)
          shape: hollow rectangle
          bounding_box: [row_start: 4, row_end: 8, col_start: 4, col_end: 11]
          position: Remains stationary (now above the yellow object)
        - color: yellow (4)
          shape: horizontal line segment
          bounding_box: [row_start: 9, row_end: 9, col_start: 4, col_end: 11]
          position: Moved below the green object
    transformation:
      action: Vertical repositioning
      moved_object_color: yellow (4)
      stationary_object_color: green (3)
      rule: The yellow object moves from row 3 to row 9 (row 8 of green object + 1).

  - id: train_2
    input:
      grid_size: [14, 12]
      background_color: white (0)
      objects:
        - color: azure (8)
          shape: multiple disconnected shapes forming a cluster
          bounding_box: [row_start: 0, row_end: 2, col_start: 2, col_end: 10] # Approximate bounding box of the group
          position: Above the red object
        - color: red (2)
          shape: hollow 'C' shape
          bounding_box: [row_start: 3, row_end: 8, col_start: 1, col_end: 10] # Approximate bounding box
          position: Below the azure object group
    output:
      grid_size: [14, 12]
      background_color: white (0)
      objects:
        - color: red (2)
          shape: hollow 'C' shape
          bounding_box: [row_start: 3, row_end: 8, col_start: 1, col_end: 10]
          position: Remains stationary (now above the azure group)
        - color: azure (8)
          shape: multiple disconnected shapes forming a cluster
          bounding_box: [row_start: 9, row_end: 11, col_start: 2, col_end: 10] # Approximate bounding box of the moved group
          position: Moved below the red object
    transformation:
      action: Vertical repositioning
      moved_object_color: azure (8)
      stationary_object_color: red (2)
      rule: The azure group moves down. Its top row moves from 0 to 9 (row 8 of red object + 1). The relative positions within the azure group are preserved.

general_properties:
  - The input grid contains exactly two non-background colors.
  - Pixels of the same color form one or more potentially disconnected components, treated collectively as a single group for positioning.
  - One color group is located entirely above the other color group (their row ranges do not overlap).
  - The transformation swaps the vertical order: the upper group moves below the lower group.
  - The lower group's position remains unchanged.
  - The upper group is translated vertically downwards. Its new top boundary is one row below the original bottom boundary of the lower group.
  - Horizontal positions are preserved for all pixels.
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid.
2.  Identify all non-background pixels and determine the two distinct colors present (Color A, Color B).
3.  Find the set of all coordinates for pixels of Color A and the set of all coordinates for pixels of Color B.
4.  Determine the minimum and maximum row indices for each color set (defining their vertical extents).
5.  Identify the 'Upper Group' as the color set with the smaller minimum row index, and the 'Lower Group' as the other color set. Let the color of the Upper Group be `Upper_Color` and the color of the Lower Group be `Lower_Color`.
6.  Find the maximum row index (`Lower_Max_Row`) of the Lower Group.
7.  Find the minimum row index (`Upper_Min_Row`) of the Upper Group.
8.  Calculate the vertical shift distance: `Shift = Lower_Max_Row + 1 - Upper_Min_Row`.
9.  Iterate through all pixel coordinates `(r, c)` belonging to the Upper Group in the input grid:
    a.  Set the pixel at `(r, c)` in the output grid to the background color (white, 0).
    b.  Set the pixel at the new coordinate `(r + Shift, c)` in the output grid to `Upper_Color`.
10. Return the final output grid.
```python
import numpy as np

"""
Identifies two distinct non-background colored objects/groups in the input grid.
One group is positioned vertically above the other.
The transformation moves the upper object/group vertically downwards, positioning it directly below the lower object/group.
The lower object/group remains stationary.
Horizontal positions are preserved for all pixels.
"""

def find_colored_pixels(grid):
    """Finds pixels of non-background colors and groups them by color."""
    pixels_by_color = {}
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if color != 0:  # Assuming 0 is the background color
                if color not in pixels_by_color:
                    pixels_by_color[color] = []
                pixels_by_color[color].append((r, c))
    return pixels_by_color

def get_bounding_box(pixels):
    """Calculates the bounding box for a set of pixel coordinates."""
    if not pixels:
        return None
    rows = [r for r, c in pixels]
    cols = [c for r, c in pixels]
    return min(rows), max(rows), min(cols), max(cols)

def transform(input_grid):
    """
    Transforms the input grid by identifying two colored groups (upper and lower)
    and moving the upper group below the lower group.
    """
    # Convert input list of lists to numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_grid_np)
    
    # Find all non-background pixels grouped by color
    pixels_by_color = find_colored_pixels(input_grid_np)
    
    # Ensure there are exactly two non-background colors
    colors = list(pixels_by_color.keys())
    if len(colors) != 2:
        # If not exactly two colors, return the original grid or handle error
        # Based on the examples, we assume exactly two colors exist.
        return input_grid # Or raise an error

    color1, color2 = colors
    pixels1 = pixels_by_color[color1]
    pixels2 = pixels_by_color[color2]

    # Determine the bounding boxes
    min_row1, max_row1, _, _ = get_bounding_box(pixels1)
    min_row2, max_row2, _, _ = get_bounding_box(pixels2)

    # Identify the upper and lower groups based on minimum row index
    if min_row1 < min_row2:
        upper_color = color1
        upper_pixels = pixels1
        upper_min_row = min_row1
        # lower_color = color2 # Not explicitly needed but good for clarity
        # lower_pixels = pixels2 # Not explicitly needed
        lower_max_row = max_row2
    else:
        upper_color = color2
        upper_pixels = pixels2
        upper_min_row = min_row2
        # lower_color = color1 # Not explicitly needed
        # lower_pixels = pixels1 # Not explicitly needed
        lower_max_row = max_row1

    # Calculate the vertical shift distance
    # The new top row of the upper object should be one row below the bottom row of the lower object
    shift = (lower_max_row + 1) - upper_min_row

    # Modify the output grid:
    # 1. Erase the upper group from its original position
    for r, c in upper_pixels:
        output_grid[r, c] = 0 # Set to background color

    # 2. Draw the upper group in its new position
    for r, c in upper_pixels:
        new_r = r + shift
        # Check bounds just in case, though ARC examples usually fit
        if 0 <= new_r < output_grid.shape[0]:
             output_grid[new_r, c] = upper_color

    # Convert back to list of lists for the expected output format
    return output_grid.tolist()
```
