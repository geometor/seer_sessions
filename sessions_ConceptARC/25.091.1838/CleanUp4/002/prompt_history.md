
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 0
8 0 0 0 0 0 0 0 0 3 0 0 0 0 3 0
0 0 3 3 3 3 0 0 0 3 0 0 0 8 3 0
0 0 3 0 0 3 0 0 0 3 0 8 0 0 3 0
0 0 3 0 8 3 0 0 0 3 0 0 0 0 3 0
0 0 3 3 3 3 0 0 0 3 3 3 3 3 3 0
0 0 0 0 0 0 8 0 0 0 0 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 3 3 3 3 3 3 3 0 0 0 0
0 0 0 0 0 3 0 0 0 0 0 3 8 0 0 0
3 8 3 8 0 3 0 0 0 0 0 3 8 0 0 0
8 0 3 8 0 3 0 8 0 8 0 3 0 0 0 0
3 3 3 0 0 3 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 3 3 3 3 3 3 3 0 0 0 0
0 0 0 0 8 0 0 0 0 0 0 0 0 8 0 0
0 0 8 0 0 0 0 0 0 0 0 8 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 0
0 0 0 0 0 0 0 0 0 3 0 0 0 0 3 0
0 0 3 3 3 3 0 0 0 3 0 0 0 0 3 0
0 0 3 0 0 3 0 0 0 3 0 0 0 0 3 0
0 0 3 0 0 3 0 0 0 3 0 0 0 0 3 0
0 0 3 3 3 3 0 0 0 3 3 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 3 3 3 3 3 0 0 0 0
0 0 0 0 0 3 0 0 0 0 0 3 0 0 0 0
3 3 3 0 0 3 0 0 0 0 0 3 0 0 0 0
3 0 3 0 0 3 0 0 0 0 0 3 0 0 0 0
3 3 3 0 0 3 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 3 3 3 3 3 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 7 0 1 0 0 0 0 0 0
6 0 0 0 0 0 8 8 8 8 8
0 2 2 2 2 0 8 6 0 0 8
0 2 0 0 2 0 8 0 0 0 8
0 2 0 4 2 0 8 0 0 4 8
0 2 0 0 2 0 8 8 8 8 8
0 2 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 1 4 4 4 4
0 0 0 1 1 0 4 0 0 0 4
0 1 6 6 6 6 4 0 7 0 4
7 0 6 0 0 6 4 0 6 0 4
0 0 6 0 0 6 4 0 0 0 4
0 0 6 0 4 6 4 0 0 0 4
4 0 6 6 6 6 4 0 0 0 4
0 0 0 0 0 0 4 4 4 4 4
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 8 8 8 8
0 2 2 2 2 0 8 0 0 0 8
0 2 0 0 2 0 8 0 0 0 8
0 2 0 0 2 0 8 0 0 0 8
0 2 0 0 2 0 8 8 8 8 8
0 2 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 4 4 4 4 4
0 0 0 0 0 0 4 0 0 0 4
0 0 6 6 6 6 4 0 0 0 4
0 0 6 0 0 6 4 0 0 0 4
0 0 6 0 0 6 4 0 0 0 4
0 0 6 0 0 6 4 0 0 0 4
0 0 6 6 6 6 4 0 0 0 4
0 0 0 0 0 0 4 4 4 4 4
```


## train_3

**input:**
```
3 4 3 3 3 3
3 3 2 2 2 2
3 3 2 3 4 2
3 4 2 3 3 2
3 3 2 2 2 2
4 3 3 3 3 3
```


**output:**
```
3 3 3 3 3 3
3 3 2 2 2 2
3 3 2 3 3 2
3 3 2 3 3 2
3 3 2 2 2 2
3 3 3 3 3 3
```

Okay, let's break down the task based on the provided examples.

**Perception of Task Elements:**

1.  **Input/Output:** The task takes a grid of colored pixels as input and produces a modified grid as output.
2.  **Colors:** Specific colors seem to trigger actions or are targets of actions: azure (8), green (3), yellow (4), white (0). Other colors (red (2), magenta (6), blue (1), orange (7)) are present but might be part of larger structures or treated as 'noise'.
3.  **Structures/Objects:** The grids contain contiguous blocks of color forming distinct objects. These can be simple spots, lines, or complex shapes like hollow rectangles.
4.  **Key Relationships:**
    *   **Adjacency:** The relationship between adjacent pixels (orthogonal and diagonal) is critical, particularly between azure (8) and green (3) in `train_1`.
    *   **Object Size:** The number of pixels in a contiguous object seems relevant for distinguishing 'major' objects from 'minor' ones or 'noise' in `train_2`.
    *   **Containment:** Some pixels exist 'inside' shapes formed by other colors (e.g., `train_2`), although this might be captured by the object size rule.
5.  **Transformations:** The core transformations observed are:
    *   Changing specific pixels to white (0) based on their color and/or adjacency to other colors (`train_1`, `train_2`).
    *   Changing pixels of one color to another specific color (`train_3`).
    *   Keeping only the largest objects and removing everything else (`train_2`).
6.  **Conditional Logic:** The transformation rule appears to be conditional, depending on the specific content of the input grid. Three distinct rules were identified, applied based on the presence and arrangement of certain colors and object structures.

**Facts (YAML):**


```yaml
task_type: grid_transformation
grid_properties:
  dimensionality: 2
  color_space: 0-9 integer map
  max_size: 30x30
observed_elements:
  - type: pixel
    properties: [color, location]
  - type: object
    definition: contiguous block of same-colored pixels (non-white)
    properties: [color, size (pixel_count), shape, location, pixels]
relationships:
  - type: adjacency
    definition: Orthogonal or diagonal neighboring pixels
    relevance: Used in rule 1 (azure(8) affecting adjacent green(3))
  - type: relative_size
    definition: Comparing pixel counts of different objects
    relevance: Used in rule 2 (selecting the 4 largest objects)
transformations:
  - type: color_change
    details:
      - change_to: white (0) # Removal
        conditions:
          - rule_1: pixel is azure(8) OR pixel is green(3) adjacent to azure(8)
          - rule_2: pixel is not part of the 4 largest objects
      - change_to: green (3)
        conditions:
          - rule_3: pixel is yellow (4)
conditional_rules:
  - condition: Presence of azure(8) AND green(3) pixels, with at least one instance of adjacency (orthogonal or diagonal) between them.
    applies_rule: rule_1
  - condition: Absence of condition_1 AND presence of >= 4 distinct contiguous non-white objects with size >= 10 pixels.
    applies_rule: rule_2
  - condition: Absence of condition_1 and condition_2 AND presence of yellow(4) pixels.
    applies_rule: rule_3
  - default: No change (implied if no conditions met)
```


**Natural Language Program:**

1.  **Analyze the input grid:** Examine the colors and their arrangement.
2.  **Check Rule 1 Condition:** Determine if the grid contains both azure (8) pixels and green (3) pixels, AND if any azure (8) pixel is orthogonally or diagonally adjacent to any green (3) pixel.
    *   **If True (Apply Rule 1):** Create a copy of the input grid. Iterate through the input grid. Change all azure (8) pixels in the copy to white (0). Change all green (3) pixels in the copy that had an azure (8) neighbor (orthogonal or diagonal) in the *original* input grid to white (0). Output the modified copy.
    *   **If False:** Proceed to the next check.
3.  **Check Rule 2 Condition:** Identify all distinct contiguous non-white objects in the grid. Count how many of these objects have a size (pixel count) of 10 or more. Check if this count is 4 or greater.
    *   **If True (Apply Rule 2):** Identify all distinct contiguous non-white objects and calculate their sizes. Select the four objects with the largest sizes (if there's a tie for the 4th position, include all tied objects, potentially resulting in more than 4 being kept). Create a new grid initialized to white (0). Copy only the pixels belonging to these selected largest objects from the input grid to the new grid, maintaining their original colors and positions. Output the new grid.
    *   **If False:** Proceed to the next check.
4.  **Check Rule 3 Condition:** Determine if the grid contains any yellow (4) pixels.
    *   **If True (Apply Rule 3):** Create a copy of the input grid. Change all yellow (4) pixels in the copy to green (3). Output the modified copy.
    *   **If False:** Proceed to the default case.
5.  **Default:** If none of the above conditions were met, output the input grid unchanged.
```python
import numpy as np
from collections import deque

"""
This function transforms an input grid based on one of three conditional rules or returns the grid unchanged if no rule applies.

Rule 1: If the grid contains both azure (8) and green (3) pixels, and at least one azure pixel is adjacent (orthogonally or diagonally) to a green pixel, then change all azure pixels to white (0) and change all green pixels that were adjacent to an azure pixel to white (0).

Rule 2: If Rule 1 does not apply, find all contiguous non-white objects. If there are 4 or more distinct objects with a size (pixel count) of 10 or more, keep only the 4 largest objects (including ties for the 4th position) and set all other pixels to white (0).

Rule 3: If neither Rule 1 nor Rule 2 applies, and the grid contains yellow (4) pixels, change all yellow pixels to green (3).

Default: If none of the above conditions are met, return the input grid unchanged.
"""

def get_neighbors(r, c, height, width, connectivity=8):
    """ Gets valid neighbor coordinates for a given cell (r, c). """
    neighbors = []
    for dr in range(-1, 2):
        for dc in range(-1, 2):
            if dr == 0 and dc == 0:
                continue
            if connectivity == 4 and abs(dr) + abs(dc) != 1: # Skip diagonals for 4-connectivity
                 continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width:
                neighbors.append((nr, nc))
    return neighbors

def find_objects(grid, ignore_color=0):
    """ Finds all contiguous objects of colors other than ignore_color. """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = [] # List to store (color, size, pixel_coords_set)

    for r in range(height):
        for c in range(width):
            if grid[r, c] != ignore_color and not visited[r, c]:
                color = grid[r, c]
                obj_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True
                obj_pixels.add((r, c))

                while q:
                    curr_r, curr_c = q.popleft()
                    # Use 4-connectivity for object definition as per ARC standard
                    for nr, nc in get_neighbors(curr_r, curr_c, height, width, connectivity=4):
                        if grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            obj_pixels.add((nr, nc))
                            q.append((nr, nc))
                
                if obj_pixels:
                    objects.append({'color': color, 'size': len(obj_pixels), 'pixels': obj_pixels})
    return objects


def transform(input_grid):
    """
    Applies the transformation rules to the input grid.
    """
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape
    output_grid = grid.copy() # Start with a copy

    # --- Check Rule 1 Condition ---
    has_azure = np.any(grid == 8)
    has_green = np.any(grid == 3)
    adjacency_found = False
    green_to_remove = set()

    if has_azure and has_green:
        azure_pixels = np.argwhere(grid == 8)
        for r_az, c_az in azure_pixels:
            # Check 8-connectivity neighbors
            for nr, nc in get_neighbors(r_az, c_az, height, width, connectivity=8):
                if grid[nr, nc] == 3:
                    adjacency_found = True
                    green_to_remove.add((nr, nc))
            if adjacency_found: # Optimization: can stop checking neighbors for this azure pixel
                 # but need to continue checking *all* azure pixels to find *all* adjacent greens
                 pass

    # --- Apply Rule 1 if condition met ---
    if adjacency_found:
        # Find all azure pixels again (or use azure_pixels list if kept)
        azure_coords = np.where(grid == 8)
        output_grid[azure_coords] = 0 # Set all azure to white

        # Set adjacent green pixels to white
        for r, c in green_to_remove:
             output_grid[r, c] = 0
        return output_grid.tolist() # Rule 1 applied

    # --- Check Rule 2 Condition ---
    all_objects = find_objects(grid, ignore_color=0)
    large_objects = [obj for obj in all_objects if obj['size'] >= 10]

    if len(large_objects) >= 4:
        # --- Apply Rule 2 ---
        # Sort all non-white objects by size descending
        all_objects.sort(key=lambda x: x['size'], reverse=True)

        # Determine the size threshold (size of the 4th largest object)
        if len(all_objects) >= 4:
             size_threshold = all_objects[3]['size']
        else:
             # Should not happen based on len(large_objects)>=4 check, but handle defensively
             size_threshold = 0 

        # Select objects >= threshold size
        objects_to_keep = [obj for obj in all_objects if obj['size'] >= size_threshold]

        # Create new grid and draw kept objects
        output_grid = np.full_like(grid, 0) # Fill with white
        for obj in objects_to_keep:
            color = obj['color']
            for r, c in obj['pixels']:
                output_grid[r, c] = color
        return output_grid.tolist() # Rule 2 applied

    # --- Check Rule 3 Condition ---
    has_yellow = np.any(grid == 4)

    # --- Apply Rule 3 if condition met ---
    if has_yellow:
        yellow_coords = np.where(grid == 4)
        output_grid[yellow_coords] = 3 # Change yellow to green
        return output_grid.tolist() # Rule 3 applied

    # --- Default Case ---
    # If none of the rules applied, return the original grid (or the initial copy)
    return output_grid.tolist()

```
