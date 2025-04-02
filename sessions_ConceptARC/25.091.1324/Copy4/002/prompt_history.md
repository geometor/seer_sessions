
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 4 0 0 0 4 0 0 0 0 0 0 0 4 0 0 0 0
0 4 4 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 4 0 0 0 4 4 4 4 4 0 0 0 4 4 4 4 4
0 4 4 4 4 4 0 0 0 4 4 4 4 4 0 0 0 4 4 4 4 4
0 4 4 4 4 4 0 0 0 4 4 4 4 4 0 0 0 4 4 4 4 4
0 4 4 4 4 4 0 0 0 4 4 4 4 4 0 0 0 4 4 4 4 4
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 6 6 6 0 0 0 0 0 0 0 0
0 0 0 6 6 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 6 6 6 6 6
0 3 3 3 3 0 0 0 6 6 6 6 6 6
0 3 4 4 3 0 0 0 6 6 6 6 6 6
0 3 4 4 3 0 0 0 6 6 6 6 6 6
0 3 3 3 3 0 0 0 6 6 6 6 6 6
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 6 6
0 0 0 0 0 0 0 0 0 0 0 0 6 6
0 0 0 0 0 0 0 3 0 0 0 0 6 6
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 6 6 6 0 0 0 0 0 0 0 0
0 0 0 6 6 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 6 6 6 6 6
0 3 3 3 3 0 0 0 6 6 6 6 6 6
0 3 4 4 3 0 0 0 6 6 6 6 6 6
0 3 4 4 3 0 0 0 6 6 6 6 6 6
0 3 3 3 3 0 0 0 6 6 6 6 6 6
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 0 0 0 0 0 0 0 0
0 0 3 4 4 3 0 0 0 0 0 0 6 6
0 0 3 4 4 3 0 0 0 0 0 0 6 6
0 0 3 3 3 3 0 3 3 3 3 0 6 6
0 0 0 0 0 0 0 3 4 4 3 0 0 0
0 0 0 0 0 0 0 3 4 4 3 0 0 0
0 0 0 0 0 0 0 3 3 3 3 0 0 0
```

## Perception of Task Elements

The task involves identifying patterns within a grid and replicating them based on certain criteria. Each grid contains a background (white) and several distinct objects composed of contiguous pixels of the same color. For each color present, there appears to be a primary "prototype" object, typically the largest one of that color. Other, smaller objects of the same color act as "seeds" or placeholders. The transformation involves copying the pattern associated with the prototype object onto the locations of specific seed objects. The key is to determine which objects are prototypes and which are seeds to be replaced.

Observations across examples:
1.  **Object Identification**: Objects are contiguous blocks of a single color.
2.  **Prototype Identification**: For each color present, the object with the largest area (number of pixels) seems to serve as the prototype.
3.  **Pattern Definition**: The pattern to be copied is the content within the bounding box of the prototype object. This pattern may include multiple colors if they fall within that bounding box (as seen with the green/yellow shape in example 2).
4.  **Seed Identification & Replacement Rule**: Other objects of the same color as the prototype are considered potential seeds. A seed object is replaced by the prototype's pattern if its top-left corner is positioned *after* the prototype's top-left corner in reading order (either lower row, or same row but greater column index).
5.  **Placement**: The copied pattern's top-left corner aligns with the original seed object's top-left corner.
6.  **Overwriting**: The copying process overwrites existing pixels in the target area.

## YAML Facts


```yaml
task_context:
  description: Replace certain objects with copies of the largest object of the same color based on relative position.
  grid_properties:
    - background_color: white (0)
    - objects_are_contiguous: true
    - multiple_colors_per_grid: true

example_1:
  input_objects:
    - color: yellow (4)
      type: rectangle
      size: [4, 5] # height, width
      pixels: 20
      position_top_left: [1, 1]
      role: prototype
    - color: yellow (4)
      type: pixel
      size: [1, 1]
      pixels: 1
      position_top_left: [1, 9]
      role: seed (replace)
    - color: yellow (4)
      type: pixel
      size: [1, 1]
      pixels: 1
      position_top_left: [1, 17]
      role: seed (replace)
    - color: green (3)
      type: rectangle
      size: [3, 5]
      pixels: 15
      position_top_left: [6, 12]
      role: prototype (only one)
  output_description:
    - Single yellow pixels at (1,9) and (1,17) are replaced.
    - Replacement_rule: They are replaced because their top-left coordinates (1,9) and (1,17) come after the prototype's (1,1) in reading order (same row, greater column).
    - Copied_pattern: 4x5 yellow rectangle from bounding box of prototype at (1,1).
    - Placement: Copied pattern starts at (1,9) and (1,17) respectively.
    - Green object remains unchanged as it's the only one of its color.

example_2:
  input_objects:
    - color: magenta (6)
      type: rectangle
      size: [2, 3]
      pixels: 6
      position_top_left: [0, 3]
      role: seed (keep)
    - color: magenta (6)
      type: rectangle
      size: [5, 6]
      pixels: 30
      position_top_left: [2, 8]
      role: prototype
    - color: magenta (6)
      type: rectangle
      size: [3, 2]
      pixels: 6
      position_top_left: [10, 12]
      role: seed (replace)
    - color: green (3)
      type: U-shape
      pixels: 12 # approx, counting green only
      position_top_left: [3, 1] # Top-left of bounding box
      bounding_box_size: [4, 4]
      role: prototype
    - color: green (3)
      type: pixel
      size: [1, 1]
      pixels: 1
      position_top_left: [9, 2]
      role: seed (replace)
    - color: green (3)
      type: pixel
      size: [1, 1]
      pixels: 1
      position_top_left: [12, 7]
      role: seed (replace)
    - color: yellow (4)
      type: square
      size: [2, 2]
      pixels: 4
      position_top_left: [4, 2]
      role: part_of_green_prototype_pattern (no independent role)
  output_description:
    - Magenta object at (10,12) is replaced. Magenta object at (0,3) is kept.
    - Replacement_rule_magenta: Object at (10,12) is replaced because its row (10) > prototype's row (2). Object at (0,3) is kept because its row (0) < prototype's row (2).
    - Copied_pattern_magenta: 5x6 magenta rectangle from bounding box of prototype at (2,8).
    - Placement_magenta: Copied pattern starts at (10,12).
    - Single green pixels at (9,2) and (12,7) are replaced.
    - Replacement_rule_green: They are replaced because their rows (9 and 12) > prototype's row (3).
    - Copied_pattern_green: The 4x4 pattern within the bounding box of the green U-shape prototype (including the yellow square).
    - Placement_green: Copied pattern starts at (9,2) and (12,7) respectively.

```


## Natural Language Program

1.  Initialize the output grid as a copy of the input grid.
2.  Identify all unique colors present in the input grid, excluding the background color (white, 0).
3.  For each unique color `C`:
    a.  Find all distinct connected components (objects) composed solely of color `C`.
    b.  If there is only one component of color `C`, do nothing for this color and proceed to the next color.
    c.  If there are multiple components of color `C`:
        i.  Determine the component with the largest area (number of pixels). If there's a tie for the largest area, select the one whose top-left corner appears earliest in reading order (top-to-bottom, left-to-right). Designate this as the `Prototype Component`.
        ii. Record the top-left coordinate `(proto_r, proto_c)` of the `Prototype Component`.
        iii. Determine the bounding box of the `Prototype Component`.
        iv. Extract the rectangular pattern of pixels within this bounding box from the input grid. This is the `Pattern To Copy`.
        v.  Iterate through all *other* components of color `C` (the `Seed Components`).
        vi. For each `Seed Component`, get its top-left coordinate `(seed_r, seed_c)`.
        vii. Compare the position of the `Seed Component` to the `Prototype Component`: If `seed_r > proto_r` OR (`seed_r == proto_r` AND `seed_c > proto_c`), then this seed needs to be replaced.
        viii. If a `Seed Component` needs replacement, overwrite the area in the output grid starting at `(seed_r, seed_c)` with the `Pattern To Copy`. Ensure the copy respects the grid boundaries.
4.  Return the modified output grid.
```python
import numpy as np
from collections import deque

"""
Identify all distinct objects (contiguous regions of the same color) for each non-background color.
For each color, if there are multiple objects, find the largest one (by pixel count, breaking ties with top-left position) as the prototype.
Extract the pattern within the bounding box of the prototype.
Find all other objects (seeds) of the same color whose top-left corner comes *after* the prototype's top-left corner in reading order (row-major).
Replace each such seed object by pasting the prototype's pattern, aligning the top-left corner of the pattern with the top-left corner of the seed.
"""

def find_objects(grid, color):
    """
    Finds all connected components of a given color in the grid.

    Args:
        grid (np.array): The input grid.
        color (int): The color to search for.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains 'pixels' (set of (r, c) tuples), 'min_r', 'min_c',
              'max_r', 'max_c', 'size', and 'top_left' (tuple (min_r, min_c)).
              Returns an empty list if no objects of the color are found.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    
    for r in range(height):
        for c in range(width):
            if grid[r, c] == color and not visited[r, c]:
                # Start BFS to find a connected component
                component_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c
                
                while q:
                    row, col = q.popleft()
                    component_pixels.add((row, col))
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)
                    
                    # Explore neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                if component_pixels:
                    objects.append({
                        'pixels': component_pixels,
                        'min_r': min_r,
                        'min_c': min_c,
                        'max_r': max_r,
                        'max_c': max_c,
                        'size': len(component_pixels),
                        'top_left': (min_r, min_c)
                    })
                    
    return objects

def get_pattern(grid, bbox):
    """
    Extracts a rectangular pattern from the grid based on the bounding box.

    Args:
        grid (np.array): The grid to extract from.
        bbox (dict): Dictionary containing 'min_r', 'min_c', 'max_r', 'max_c'.

    Returns:
        np.array: The extracted pattern.
    """
    return grid[bbox['min_r']:bbox['max_r']+1, bbox['min_c']:bbox['max_c']+1]

def paste_pattern(grid, pattern, top_left):
    """
    Pastes a pattern onto the grid at the specified top-left position.
    Handles boundary conditions.

    Args:
        grid (np.array): The target grid (mutable).
        pattern (np.array): The pattern to paste.
        top_left (tuple): The (row, column) to start pasting at.
    """
    start_r, start_c = top_left
    pattern_h, pattern_w = pattern.shape
    grid_h, grid_w = grid.shape

    # Calculate the actual region to paste onto, clipping to grid boundaries
    end_r = min(start_r + pattern_h, grid_h)
    end_c = min(start_c + pattern_w, grid_w)

    # Calculate the portion of the pattern to use
    paste_h = end_r - start_r
    paste_w = end_c - start_c

    # Ensure we don't try to paste negative dimensions
    if paste_h <= 0 or paste_w <= 0:
        return

    # Paste the valid portion of the pattern
    grid[start_r:end_r, start_c:end_c] = pattern[0:paste_h, 0:paste_w]


def transform(input_grid):
    """
    Transforms the input grid by finding prototype objects for each color,
    extracting their patterns, and copying these patterns onto specific
    'seed' objects of the same color based on their relative positions.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to numpy array for easier processing
    input_np = np.array(input_grid, dtype=int)
    output_np = np.copy(input_np)
    height, width = input_np.shape

    # Find unique colors present, excluding background (0)
    unique_colors = np.unique(input_np)
    unique_colors = unique_colors[unique_colors != 0]

    # Process each color
    for color in unique_colors:
        # Find all objects of the current color
        objects = find_objects(input_np, color)

        # Skip if only one or zero objects of this color exist
        if len(objects) < 2:
            continue

        # Find the prototype object
        # Sort by size (descending), then by top-left row (ascending), then by top-left col (ascending)
        objects.sort(key=lambda obj: (-obj['size'], obj['top_left'][0], obj['top_left'][1]))
        prototype = objects[0]
        proto_r, proto_c = prototype['top_left']

        # Extract the pattern from the prototype's bounding box in the *original* input grid
        pattern_to_copy = get_pattern(input_np, prototype)
        
        # Identify and replace seed objects
        for i in range(1, len(objects)):
            seed = objects[i]
            seed_r, seed_c = seed['top_left']

            # Check the replacement condition: seed is after prototype in reading order
            if seed_r > proto_r or (seed_r == proto_r and seed_c > proto_c):
                # Replace the seed area with the prototype pattern in the output grid
                paste_pattern(output_np, pattern_to_copy, seed['top_left'])

    # Convert the result back to a list of lists
    return output_np.tolist()
```
