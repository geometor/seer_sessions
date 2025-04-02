
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 0 2 2 0 4 4 0 3 3 0
0 1 1 0 2 2 0 4 4 0 5 5 0
0 1 1 0 5 5 0 4 4 0 3 3 0
0 1 1 0 2 2 0 5 5 0 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 0 2 2 0 3 3 0 1 1 0
0 4 4 0 2 2 0 3 3 0 1 1 0
0 4 4 0 2 2 0 3 3 0 1 1 0
0 4 4 0 2 2 0 3 3 0 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
4 4 4 0 2 2 2 0 6 6 6 0 7 7 7
4 0 4 0 2 2 2 0 6 6 6 0 7 7 7
4 4 4 0 2 2 2 0 6 6 6 0 7 7 7
4 4 4 0 2 2 2 0 6 6 6 0 7 7 7
4 4 4 0 2 0 2 0 6 6 6 0 7 7 7
4 4 4 0 2 2 2 0 6 6 6 0 7 0 7
4 4 4 0 2 2 2 0 6 0 6 0 7 7 7
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
6 6 6 0 7 7 7 0 2 2 2 0 4 4 4
6 6 6 0 7 7 7 0 2 2 2 0 4 4 4
6 6 6 0 7 7 7 0 2 2 2 0 4 4 4
6 6 6 0 7 7 7 0 2 2 2 0 4 4 4
6 6 6 0 7 7 7 0 2 2 2 0 4 4 4
6 6 6 0 7 7 7 0 2 2 2 0 4 4 4
6 6 6 0 7 7 7 0 2 2 2 0 4 4 4
```

Okay, let's break down the transformation logic for this task.

**Perception of the Elements:**

1.  **Grid Structure:** Both input and output grids maintain the same dimensions. The background color, white (0), remains unchanged and acts as a separator between distinct shapes or objects.
2.  **Objects:** The core elements are distinct objects composed of connected non-white pixels. These objects are separated horizontally by columns of the white background color.
3.  **Object Types:** There appear to be two categories of objects based on their composition across the examples:
    *   **Type 1 (Train_1):** Objects contain exactly two non-white colors: gray (5) and one other 'primary' color (blue, red, yellow, or green). The shape is relatively solid.
    *   **Type 2 (Train_2):** Objects contain only one non-white color (yellow, red, magenta, or orange) but may contain internal "holes" represented by the white (0) background color.
4.  **Transformation:** The transformation modifies the colors of the pixels *within* each object, while preserving the object's overall shape, position, and any internal holes (white pixels within the object's boundary). The specific color change depends on the type of object.
5.  **Conditional Logic:** The presence or absence of the gray (5) color within an object dictates which color transformation rule is applied.

**Facts:**


```yaml
Grid:
  Properties:
    - Size: Unchanged between input and output.
    - Background: Color white (0) is preserved. Acts as a separator.
Objects:
  Definition: Connected components of non-white pixels (pixels with value > 0).
  Properties:
    - Pixels: The set of coordinates belonging to the component.
    - Has_Gray: Boolean flag, true if any pixel in the component has value gray (5).
    - Primary_Color:
        - If Has_Gray is true: The non-gray, non-white color within the component (assuming one primary color exists besides gray based on examples).
        - If Has_Gray is false: The single non-white color of the component.
    - Shape: Defined by the `Pixels` coordinates. Preserved in the output (including internal white/0 pixels).
Transformation:
  Type: Color substitution within objects.
  Rule: Conditional based on the `Has_Gray` property of the object.
  Mappings:
    - Rule_Gray_Present: # Applied if Has_Gray is true
        Input_Color: Blue (1) -> Output_Color: Yellow (4)
        Input_Color: Red (2) -> Output_Color: Red (2)
        Input_Color: Yellow (4) -> Output_Color: Green (3)
        Input_Color: Green (3) -> Output_Color: Blue (1)
    - Rule_Gray_Absent: # Applied if Has_Gray is false
        Input_Color: Yellow (4) -> Output_Color: Magenta (6)
        Input_Color: Red (2) -> Output_Color: Orange (7)
        Input_Color: Magenta (6) -> Output_Color: Red (2)
        Input_Color: Orange (7) -> Output_Color: Yellow (4)
Action:
  - Iterate through each identified object in the input grid.
  - Determine `Has_Gray` and `Primary_Color` for the object.
  - Select the appropriate transformation mapping (Rule_Gray_Present or Rule_Gray_Absent).
  - Determine the `Output_Color` by applying the selected mapping to the `Primary_Color`.
  - For every pixel coordinate within the object's `Pixels` set, change the color in the output grid at that coordinate to the determined `Output_Color`.
  - Pixels that were originally white (0), whether background or internal holes, remain white (0).
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid.
2.  Identify all distinct objects in the input grid. An object is a group of connected pixels with colors other than white (0).
3.  For each identified object:
    a.  Examine all pixels belonging to the object to check if any of them are gray (5).
    b.  Determine the object's 'primary color'. If gray (5) is present, the primary color is the *other* non-white color in the object. If gray (5) is absent, the primary color is the single non-white color composing the object.
    c.  Select the appropriate color transformation rule based on whether gray (5) was found:
        i.  **If gray (5) is present:** Use the mapping: Blue (1) becomes Yellow (4), Red (2) becomes Red (2), Yellow (4) becomes Green (3), Green (3) becomes Blue (1).
        ii. **If gray (5) is absent:** Use the mapping: Yellow (4) becomes Magenta (6), Red (2) becomes Orange (7), Magenta (6) becomes Red (2), Orange (7) becomes Yellow (4).
    d.  Apply the selected transformation rule to the object's primary color to find the target output color.
    e.  For every pixel coordinate that belongs to the current object in the input grid, update the corresponding pixel in the output grid to the calculated target output color. (This ensures both the primary color and the gray color pixels, if present, are updated).
4.  Return the modified output grid.
```python
import numpy as np
from collections import deque

"""
This program transforms an input grid into an output grid based on the colors within connected objects.

1.  Identifies distinct objects in the input grid. An object is a contiguous group of non-white (non-zero) pixels.
2.  For each object, it determines if the color gray (5) is present among its pixels.
3.  Based on the presence or absence of gray (5), it identifies a 'primary' color for the object:
    - If gray (5) is present, the primary color is the other non-white color in the object.
    - If gray (5) is absent, the primary color is the single non-white color composing the object.
4.  Applies a color transformation rule to the primary color to get a target output color. There are two separate rules: one for objects containing gray, and one for objects without gray.
    - Rule (Gray Present): Blue (1) -> Yellow (4), Red (2) -> Red (2), Yellow (4) -> Green (3), Green (3) -> Blue (1).
    - Rule (Gray Absent): Yellow (4) -> Magenta (6), Red (2) -> Orange (7), Magenta (6) -> Red (2), Orange (7) -> Yellow (4).
5.  Updates all pixels belonging to the original object in the output grid to this single target output color, preserving the object's shape and position.
6.  White (0) pixels (background or internal holes) remain unchanged.
"""

def find_objects(grid):
    """
    Finds connected components of non-background (non-zero) pixels in the grid.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains 'coords' (a set of (row, col) tuples) and 'colors'
              (a set of color values present in the object).
    """
    height, width = grid.shape
    visited = set()
    objects = []
    for r in range(height):
        for c in range(width):
            if grid[r, c] != 0 and (r, c) not in visited:
                # Found the start of a new object
                current_object_coords = set()
                current_object_colors = set()
                q = deque([(r, c)])
                visited.add((r, c))

                while q:
                    row, col = q.popleft()
                    current_object_coords.add((row, col))
                    current_object_colors.add(grid[row, col])

                    # Check 4-directional neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] != 0 and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            q.append((nr, nc))

                if current_object_coords:
                    objects.append({
                        'coords': current_object_coords,
                        'colors': current_object_colors
                    })
    return objects

def transform(input_grid):
    """
    Transforms the input grid based on object colors and presence of gray.

    Args:
        input_grid (np.ndarray): The input grid.

    Returns:
        np.ndarray: The transformed output grid.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Define the color transformation maps
    map_gray_present = {
        1: 4,  # Blue -> Yellow
        2: 2,  # Red -> Red
        4: 3,  # Yellow -> Green
        3: 1   # Green -> Blue
    }
    map_gray_absent = {
        4: 6,  # Yellow -> Magenta
        2: 7,  # Red -> Orange
        6: 2,  # Magenta -> Red
        7: 4   # Orange -> Yellow
    }

    # Find all objects in the input grid
    objects = find_objects(input_grid)

    # Process each object
    for obj in objects:
        coords = obj['coords']
        colors = obj['colors']
        
        # Check if gray (5) is present
        has_gray = 5 in colors

        primary_color = -1
        target_color = -1

        if has_gray:
            # Find the primary color (the one that's not 0 or 5)
            # Assuming exactly one primary color exists alongside gray based on examples
            primary_colors = [c for c in colors if c != 0 and c != 5]
            if primary_colors: # Should always be true if has_gray and object exists
                 primary_color = primary_colors[0]
                 # Apply the transformation rule for objects with gray
                 target_color = map_gray_present.get(primary_color, primary_color) # Default to itself if not in map
            else:
                # Handle edge case? E.g., an object made *only* of gray?
                # Based on examples, this doesn't seem to happen. Assume we find a primary.
                # If only gray existed, maybe it maps to itself? For now, stick to observed rules.
                # Let's assume primary_color must be found if gray is present. If not, something is wrong.
                # If object was ONLY gray, target_color would remain -1. We can add a fallback.
                if not primary_colors and colors == {5}:
                     target_color = 5 # Map gray-only object to gray? Or maybe another rule applies? Let's keep gray.
                     # However, based on task, this scenario doesn't occur.
                else:
                     # This case signifies an unexpected object composition (e.g. {0, 5})
                     # Defaulting to keep original color might be safest if primary unclear
                     # For now, assume the primary color is always identifiable per rules.
                     pass # target_color remains -1 initially

        else: # No gray color (5) in the object
            # Find the primary color (the single non-zero color)
            primary_colors = [c for c in colors if c != 0]
            if len(primary_colors) == 1: # Should be true for non-gray objects based on examples
                primary_color = primary_colors[0]
                # Apply the transformation rule for objects without gray
                target_color = map_gray_absent.get(primary_color, primary_color) # Default to itself if not in map
            else:
                # Handle edge case: multiple non-gray colors without gray present?
                # Not observed in examples. Assume single primary color if no gray.
                pass # target_color remains -1

        # Update the output grid for all pixels in this object
        if target_color != -1: # Ensure we found a valid transformation
            for r, c in coords:
                 # Check bounds just in case, though coords should be valid
                if 0 <= r < height and 0 <= c < width:
                    output_grid[r, c] = target_color
        # If target_color remained -1 (due to unexpected object composition),
        # the original colors in output_grid (copied from input) are preserved for that object.

    return output_grid
```
