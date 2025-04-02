
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

Previous Code:
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
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
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
Expected Output:
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
Transformed Output:
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
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0

## Example 2:
Input:
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
Expected Output:
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
Transformed Output:
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
0 0 0 0 0 0 0 3 4 4 3 0 6 6
0 0 0 0 0 0 0 3 4 4 3 0 6 6
0 0 0 0 0 0 0 3 3 3 3 0 0 0
```
Match: False
Pixels Off: 4
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 3.5714285714285836
## General Assessment and Strategy

The initial code successfully solved Example 1 but failed on Example 2. The failure occurred because the rule for deciding *which* objects (seeds) to replace was too broad. The original rule replaced any object of the same color whose top-left corner appeared *after* the prototype's top-left corner in reading order.

Comparing the `Transformed Output` and `Expected Output` for Example 2 revealed that a magenta object `(10, 12)` which appeared after the magenta prototype `(2, 8)` was *not* replaced in the expected output, contrary to the initial rule. However, two single-pixel green objects `(9, 2)` and `(12, 7)` which appeared after the green prototype `(3, 1)` *were* replaced.

This led to the revised hypothesis: **Replacement only occurs if the seed object is exactly 1x1 pixel in size AND its top-left coordinate comes after the prototype's top-left coordinate in reading order.** This revised rule correctly explains the outcomes for both examples.

The strategy is to update the natural language program and the subsequent code implementation to incorporate this more specific condition for identifying which seeds get replaced.

## Metrics Gathering (Example 2 Analysis)


*code_execution:*
```python
import numpy as np
from collections import deque

def find_objects(grid, color):
    # (Using the same find_objects function as provided in the thought process)
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    obj_id = 0
    for r in range(height):
        for c in range(width):
            if grid[r, c] == color and not visited[r, c]:
                obj_id += 1
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

                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                if component_pixels:
                    objects.append({
                        'id': f"{color}-{obj_id}",
                        'color': color,
                        'pixels': component_pixels,
                        'min_r': min_r,
                        'min_c': min_c,
                        'max_r': max_r,
                        'max_c': max_c,
                        'size': len(component_pixels),
                        'top_left': (min_r, min_c),
                        'is_1x1': len(component_pixels) == 1
                    })
    return objects

# Example 2 Input Grid
grid_ex2_input = np.array([
    [0, 0, 0, 6, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 6, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 6, 6, 6, 6, 6, 6],
    [0, 3, 3, 3, 3, 0, 0, 0, 6, 6, 6, 6, 6, 6],
    [0, 3, 4, 4, 3, 0, 0, 0, 6, 6, 6, 6, 6, 6],
    [0, 3, 4, 4, 3, 0, 0, 0, 6, 6, 6, 6, 6, 6],
    [0, 3, 3, 3, 3, 0, 0, 0, 6, 6, 6, 6, 6, 6],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6],
    [0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 6, 6],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
], dtype=int)

print("--- Example 2 Analysis ---")
unique_colors = np.unique(grid_ex2_input)
unique_colors = unique_colors[unique_colors != 0] # Exclude background

report = {}

for color in unique_colors:
    objects = find_objects(grid_ex2_input, color)
    report[color] = {'count': len(objects), 'objects': []}
    if len(objects) >= 1:
        objects.sort(key=lambda obj: (-obj['size'], obj['top_left'][0], obj['top_left'][1]))
        prototype = objects[0]
        report[color]['prototype'] = {'id': prototype['id'], 'top_left': prototype['top_left'], 'size': prototype['size']}
        proto_r, proto_c = prototype['top_left']
        for i, obj in enumerate(objects):
            obj_info = {
                'id': obj['id'],
                'top_left': obj['top_left'],
                'size': obj['size'],
                'is_1x1': obj['is_1x1'],
                'role': 'prototype' if i == 0 else 'seed'
            }
            if i > 0: # It's a seed
                seed_r, seed_c = obj['top_left']
                is_after = seed_r > proto_r or (seed_r == proto_r and seed_c > proto_c)
                obj_info['is_after_prototype'] = is_after
                # Apply the REVISED rule
                if obj['is_1x1'] and is_after:
                    obj_info['action'] = 'replace'
                else:
                    obj_info['action'] = 'keep'
            else: # Prototype
                 obj_info['action'] = 'keep (prototype)'

            report[color]['objects'].append(obj_info)
    else: # Handle cases with 0 objects of a color (e.g. yellow in this case after finding objects by primary color)
        # Color 4 (yellow) exists but only as part of the green prototype's pattern, not as a standalone object.
        # find_objects only finds objects of the specified color.
         report[color]['prototype'] = None

# Special handling for yellow (color 4) as it's part of the green pattern
if 4 in unique_colors and 4 not in report:
     objects_4 = find_objects(grid_ex2_input, 4)
     report[4] = {'count': len(objects_4), 'objects': []}
     if len(objects_4) > 0:
          objects_4.sort(key=lambda obj: (-obj['size'], obj['top_left'][0], obj['top_left'][1]))
          for i, obj in enumerate(objects_4):
               obj_info = {
                   'id': obj['id'],
                   'top_left': obj['top_left'],
                   'size': obj['size'],
                   'is_1x1': obj['is_1x1'],
                   'role': 'part_of_other_pattern', # Indicate it's not a primary object here
                   'action': 'keep (part of green pattern)'
               }
               report[4]['objects'].append(obj_info)
     else:
          report[4]['prototype'] = None


import json
print(json.dumps(report, indent=2))
```

*code_execution_result:*
outcome: OUTCOME_OK
```
--- Example 2 Analysis ---

```

*code_execution_result:*
outcome: OUTCOME_FAILED
```
Traceback (most recent call last):
  File "<string>", line 131, in <module>
  File "__init__.py", line 238, in dumps
    **kw).encode(obj)
          ^^^^^^^^^^^
  File "encoder.py", line 202, in encode
    chunks = list(chunks)
             ^^^^^^^^^^^^
  File "encoder.py", line 432, in _iterencode
    yield from _iterencode_dict(o, _current_indent_level)
  File "encoder.py", line 377, in _iterencode_dict
    raise TypeError(f'keys must be str, int, float, bool or None, '
TypeError: keys must be str, int, float, bool or None, not int64

```
Ran into a json serialization error because numpy integers (like the color keys `3`, `4`, `6`) are not directly supported. Let's fix that by converting keys to strings.


*code_execution:*
```python
import numpy as np
from collections import deque
import json # Import json here

def find_objects(grid, color):
    # (Using the same find_objects function as provided in the thought process)
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    obj_id = 0
    for r in range(height):
        for c in range(width):
            if grid[r, c] == color and not visited[r, c]:
                obj_id += 1
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

                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                if component_pixels:
                    objects.append({
                        'id': f"{color}-{obj_id}",
                        'color': color,
                        'pixels': component_pixels,
                        'min_r': min_r,
                        'min_c': min_c,
                        'max_r': max_r,
                        'max_c': max_c,
                        'size': len(component_pixels),
                        'top_left': (min_r, min_c),
                        'is_1x1': len(component_pixels) == 1
                    })
    return objects

# Example 2 Input Grid
grid_ex2_input = np.array([
    [0, 0, 0, 6, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 6, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 6, 6, 6, 6, 6, 6],
    [0, 3, 3, 3, 3, 0, 0, 0, 6, 6, 6, 6, 6, 6],
    [0, 3, 4, 4, 3, 0, 0, 0, 6, 6, 6, 6, 6, 6],
    [0, 3, 4, 4, 3, 0, 0, 0, 6, 6, 6, 6, 6, 6],
    [0, 3, 3, 3, 3, 0, 0, 0, 6, 6, 6, 6, 6, 6],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6],
    [0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 6, 6],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
], dtype=int)

print("--- Example 2 Analysis ---")
unique_colors = np.unique(grid_ex2_input)
unique_colors = unique_colors[unique_colors != 0] # Exclude background

# Use string keys for the report dictionary
report = {}

for color in unique_colors:
    color_key = str(color) # Use string key
    objects = find_objects(grid_ex2_input, color)
    report[color_key] = {'count': len(objects), 'objects': []}
    if len(objects) >= 1:
        objects.sort(key=lambda obj: (-obj['size'], obj['top_left'][0], obj['top_left'][1]))
        prototype = objects[0]
        report[color_key]['prototype'] = {'id': prototype['id'], 'top_left': prototype['top_left'], 'size': prototype['size']}
        proto_r, proto_c = prototype['top_left']
        for i, obj in enumerate(objects):
            obj_info = {
                'id': obj['id'],
                'top_left': obj['top_left'],
                'size': obj['size'],
                'is_1x1': obj['is_1x1'],
                'role': 'prototype' if i == 0 else 'seed'
            }
            if i > 0: # It's a seed
                seed_r, seed_c = obj['top_left']
                is_after = seed_r > proto_r or (seed_r == proto_r and seed_c > proto_c)
                obj_info['is_after_prototype'] = is_after
                # Apply the REVISED rule
                if obj['is_1x1'] and is_after:
                    obj_info['action'] = 'replace'
                else:
                    obj_info['action'] = 'keep'
            else: # Prototype
                 obj_info['action'] = 'keep (prototype)'

            # Store pixels as list of lists for JSON compatibility
            obj_info['pixels'] = [list(p) for p in sorted(list(obj['pixels']))]
            report[color_key]['objects'].append(obj_info)
    else:
         report[color_key]['prototype'] = None


# Check for yellow again, ensure key is string
color4_key = str(4)
if color4_key in report and report[color4_key]['count'] > 0:
     # Update role/action for yellow objects found
     for obj_info in report[color4_key]['objects']:
          obj_info['role'] = 'part_of_other_pattern'
          obj_info['action'] = 'keep (part of green pattern)'
elif color4_key not in report and 4 in unique_colors:
     # Handle case where yellow exists but wasn't processed as primary color
     objects_4 = find_objects(grid_ex2_input, 4)
     report[color4_key] = {'count': len(objects_4), 'objects': []}
     if len(objects_4) > 0:
          objects_4.sort(key=lambda obj: (-obj['size'], obj['top_left'][0], obj['top_left'][1]))
          for i, obj in enumerate(objects_4):
               obj_info = {
                   'id': obj['id'],
                   'top_left': obj['top_left'],
                   'size': obj['size'],
                   'is_1x1': obj['is_1x1'],
                   'role': 'part_of_other_pattern',
                   'action': 'keep (part of green pattern)',
                   'pixels': [list(p) for p in sorted(list(obj['pixels']))] # Add pixels
               }
               report[color4_key]['objects'].append(obj_info)
     else:
        report[color4_key]['prototype'] = None


print(json.dumps(report, indent=2))
```

*code_execution_result:*
outcome: OUTCOME_OK
```
--- Example 2 Analysis ---
{
  "3": {
    "count": 3,
    "objects": [
      {
        "id": "3-1",
        "top_left": [
          3,
          1
        ],
        "size": 12,
        "is_1x1": false,
        "role": "prototype",
        "action": "keep (prototype)",
        "pixels": [
          [
            3,
            1
          ],
          [
            3,
            2
          ],
          [
            3,
            3
          ],
          [
            3,
            4
          ],
          [
            4,
            1
          ],
          [
            4,
            4
          ],
          [
            5,
            1
          ],
          [
            5,
            4
          ],
          [
            6,
            1
          ],
          [
            6,
            2
          ],
          [
            6,
            3
          ],
          [
            6,
            4
          ]
        ]
      },
      {
        "id": "3-2",
        "top_left": [
          9,
          2
        ],
        "size": 1,
        "is_1x1": true,
        "role": "seed",
        "is_after_prototype": true,
        "action": "replace",
        "pixels": [
          [
            9,
            2
          ]
        ]
      },
      {
        "id": "3-3",
        "top_left": [
          12,
          7
        ],
        "size": 1,
        "is_1x1": true,
        "role": "seed",
        "is_after_prototype": true,
        "action": "replace",
        "pixels": [
          [
            12,
            7
          ]
        ]
      }
    ],
    "prototype": {
      "id": "3-1",
      "top_left": [
        3,
        1
      ],
      "size": 12
    }
  },
  "4": {
    "count": 1,
    "objects": [
      {
        "id": "4-1",
        "top_left": [
          4,
          2
        ],
        "size": 4,
        "is_1x1": false,
        "role": "part_of_other_pattern",
        "action": "keep (part of green pattern)",
        "pixels": [
          [
            4,
            2
          ],
          [
            4,
            3
          ],
          [
            5,
            2
          ],
          [
            5,
            3
          ]
        ]
      }
    ],
    "prototype": {
      "id": "4-1",
      "top_left": [
        4,
        2
      ],
      "size": 4
    }
  },
  "6": {
    "count": 3,
    "objects": [
      {
        "id": "6-2",
        "top_left": [
          2,
          8
        ],
        "size": 30,
        "is_1x1": false,
        "role": "prototype",
        "action": "keep (prototype)",
        "pixels": [
          [
            2,
            8
          ],
          [
            2,
            9
          ],
          [
            2,
            10
          ],
          [
            2,
            11
          ],
          [
            2,
            12
          ],
          [
            2,
            13
          ],
          [
            3,
            8
          ],
          [
            3,
            9
          ],
          [
            3,
            10
          ],
          [
            3,
            11
          ],
          [
            3,
            12
          ],
          [
            3,
            13
          ],
          [
            4,
            8
          ],
          [
            4,
            9
          ],
          [
            4,
            10
          ],
          [
            4,
            11
          ],
          [
            4,
            12
          ],
          [
            4,
            13
          ],
          [
            5,
            8
          ],
          [
            5,
            9
          ],
          [
            5,
            10
          ],
          [
            5,
            11
          ],
          [
            5,
            12
          ],
          [
            5,
            13
          ],
          [
            6,
            8
          ],
          [
            6,
            9
          ],
          [
            6,
            10
          ],
          [
            6,
            11
          ],
          [
            6,
            12
          ],
          [
            6,
            13
          ]
        ]
      },
      {
        "id": "6-1",
        "top_left": [
          0,
          3
        ],
        "size": 6,
        "is_1x1": false,
        "role": "seed",
        "is_after_prototype": false,
        "action": "keep",
        "pixels": [
          [
            0,
            3
          ],
          [
            0,
            4
          ],
          [
            0,
            5
          ],
          [
            1,
            3
          ],
          [
            1,
            4
          ],
          [
            1,
            5
          ]
        ]
      },
      {
        "id": "6-3",
        "top_left": [
          10,
          12
        ],
        "size": 6,
        "is_1x1": false,
        "role": "seed",
        "is_after_prototype": true,
        "action": "keep",
        "pixels": [
          [
            10,
            12
          ],
          [
            10,
            13
          ],
          [
            11,
            12
          ],
          [
            11,
            13
          ],
          [
            12,
            12
          ],
          [
            12,
            13
          ]
        ]
      }
    ],
    "prototype": {
      "id": "6-2",
      "top_left": [
        2,
        8
      ],
      "size": 30
    }
  }
}

```
The generated report confirms the analysis:
*   **Green (3):** Prototype `3-1` (size 12, top-left `(3,1)`). Seeds `3-2` (size 1, top-left `(9,2)`) and `3-3` (size 1, top-left `(12,7)`). Both seeds are 1x1 and appear after the prototype, so their `action` is correctly identified as `replace`.
*   **Yellow (4):** Only one object `4-1` (size 4, top-left `(4,2)`). It's correctly identified as `part_of_other_pattern` (the green prototype's pattern) and its action is `keep`.
*   **Magenta (6):** Prototype `6-2` (size 30, top-left `(2,8)`). Seed `6-1` (size 6, top-left `(0,3)`) is not 1x1 and appears before the prototype; action is `keep`. Seed `6-3` (size 6, top-left `(10,12)`) appears after the prototype but is not 1x1; action is `keep`.

## Updated YAML Facts


```yaml
task_context:
  description: Replace specific single-pixel objects with copies of the largest object (prototype) of the same color, based on relative position.
  grid_properties:
    - background_color: white (0)
    - objects_are_contiguous: true
    - multiple_colors_per_grid: true

object_identification:
  - method: Find connected components (4-connectivity) of the same non-background color.
  - properties: size (pixel count), bounding_box, top-left coordinate.

prototype_identification:
  - rule: For each color with multiple objects, the prototype is the object with the largest size (pixel count).
  - tie_breaking: If sizes are equal, the prototype is the one with the top-left corner earliest in reading order (top-to-bottom, left-to-right).

seed_identification:
  - rule: A seed is any object of a given color that is not the prototype for that color.

pattern_extraction:
  - source: The rectangular region defined by the bounding box of the prototype object.
  - content: All pixels (including potentially different colors or background) within the prototype's bounding box in the original input grid.

replacement_rule:
  - condition_1: The seed object must be exactly 1x1 pixel in size.
  - condition_2: The seed object's top-left coordinate `(seed_r, seed_c)` must be *after* the prototype's top-left coordinate `(proto_r, proto_c)` in reading order (i.e., `seed_r > proto_r` OR (`seed_r == proto_r` AND `seed_c > proto_c`)).
  - action: If both conditions are met, replace the seed. Otherwise, keep the seed.

replacement_action:
  - method: Paste the extracted prototype pattern onto the output grid.
  - placement: Align the top-left corner of the pattern with the top-left corner of the seed object being replaced.
  - overwrite: Yes, overwrite existing pixels in the target area. Handles grid boundaries (clipping).

example_analysis_summary:
  - example_1: Yellow prototype (4x5 at (1,1)). Seeds at (1,9) and (1,17) are 1x1 and after prototype -> replaced. Green object is unique -> kept.
  - example_2:
      - Magenta prototype (5x6 at (2,8)). Seeds at (0,3) and (10,12) are NOT 1x1 -> kept.
      - Green prototype (U-shape, bbox 4x4 at (3,1)). Seeds at (9,2) and (12,7) ARE 1x1 and after prototype -> replaced with 4x4 pattern.
      - Yellow object (2x2 at (4,2)) is unique (as a yellow object) and part of green prototype pattern -> kept.

```


## Updated Natural Language Program

1.  Initialize the output grid as a copy of the input grid.
2.  Identify all unique colors present in the input grid, excluding the background color (white, 0).
3.  For each unique color `C`:
    a.  Find all distinct connected components (objects) composed solely of color `C`.
    b.  If there is only one component of color `C`, do nothing for this color and proceed to the next color.
    c.  If there are multiple components of color `C`:
        i.  Determine the `Prototype Component`: Find the component with the largest area (number of pixels). Break ties by selecting the component whose top-left corner appears earliest in reading order (top-to-bottom, left-to-right).
        ii. Record the top-left coordinate `(proto_r, proto_c)` of the `Prototype Component`.
        iii. Determine the bounding box of the `Prototype Component`.
        iv. Extract the rectangular pattern of pixels within this bounding box from the *original input grid*. This is the `Pattern To Copy`.
        v.  Iterate through all *other* components of color `C` (the `Seed Components`).
        vi. For each `Seed Component`:
            1. Check if the `Seed Component` consists of exactly one pixel (size is 1).
            2. Get the `Seed Component`'s top-left coordinate `(seed_r, seed_c)`.
            3. Check if the `Seed Component` is positioned after the `Prototype Component` in reading order: (`seed_r > proto_r` OR (`seed_r == proto_r` AND `seed_c > proto_c`)).
            4. **Replacement Condition:** If the `Seed Component` is exactly 1x1 pixel in size AND it is positioned after the `Prototype Component`, then this seed needs to be replaced.
            5. **Replacement Action:** If the `Replacement Condition` is met, overwrite the area in the output grid starting at `(seed_r, seed_c)` with the `Pattern To Copy`. Ensure the copy respects the grid boundaries (clipping if necessary). Otherwise, leave the `Seed Component` unchanged.
4.  Return the modified output grid.
