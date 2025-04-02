
## train_1

**input:**
```
0 0 9 9 9 0 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 9 9 9 0 0 9 9 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 2 2 2 0 0 0 2 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 2 2 2 0 0 2 2 2 0 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 8 8 8 0 0 0 0 8 0 0 0 0 0 8 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 8 8 8 0 0 0 8 8 8 0 0 0 8 8 8 0 8 8 8 0 0 0 0 0 0 0 0 0 0 0
```

*   **Perception:**
    *   The task involves modifying input grids containing various colored shapes on a white background.
    *   The primary colors observed are maroon (9), red (2), and azure (8), always on a white (0) background.
    *   Shapes appear as contiguous blocks of non-white pixels.
    *   The transformation specifically targets isolated, single non-white pixels.
    *   Larger shapes (composed of more than one pixel) remain unchanged in the output.
    *   Isolated single pixels are expanded horizontally to the right, forming a 1x3 line of the original pixel's color. The original pixel becomes the leftmost pixel of this new line.
    *   The background remains white, except where overwritten by the expanded pixels.

*   **YAML Facts:**
    
```yaml
    task_description: Modify grid based on the size of colored objects.
    background_color: white (0)
    objects:
      - type: shape
        properties:
          - color: non-white (e.g., maroon, red, azure)
          - connectivity: contiguous pixels (including diagonals)
          - size: number of pixels in the shape
    actions:
      - name: identify_objects
        description: Find all connected components of non-white pixels.
      - name: filter_objects
        criteria: Identify objects composed of exactly one pixel.
      - name: transform_single_pixel_objects
        description: Replace the single pixel with a 1x3 horizontal line of the same color, starting at the original pixel's location and extending rightwards.
        constraints: Respect grid boundaries; do not extend beyond the right edge.
      - name: preserve_larger_objects
        description: Copy objects composed of more than one pixel directly from input to output without change.
      - name: preserve_background
        description: Maintain white background pixels unless overwritten by the transformation.
    relationships:
      - The transformation rule depends solely on the size (pixel count) of each distinct colored object.
      - Single-pixel objects trigger expansion.
      - Multi-pixel objects are preserved.
    ```


*   **Natural Language Program:**
    1.  Initialize an output grid identical in size and background color (white) to the input grid.
    2.  Identify all distinct objects in the input grid. An object is a group of one or more contiguous pixels (sharing a side or corner) of the same non-white color.
    3.  For each identified object:
        a.  Count the number of pixels that make up the object.
        b.  If the object consists of exactly one pixel:
            i.  Determine the row `r`, column `c`, and color `clr` of this pixel.
            ii. In the output grid, color the pixel at `(r, c)` with `clr`.
            iii. If column `c+1` is within the grid bounds, color the pixel at `(r, c+1)` with `clr`.
            iv. If column `c+2` is within the grid bounds, color the pixel at `(r, c+2)` with `clr`.
        c.  If the object consists of more than one pixel:
            i.  Copy all pixels belonging to this object from their original positions in the input grid to the corresponding positions in the output grid.
    4.  Return the final output grid.
```python
import numpy as np
from collections import deque

"""
Transforms an input grid by identifying objects (connected non-white pixels).
If an object consists of exactly one pixel, it is expanded into a 1x3 horizontal line 
of the same color, starting at the original pixel's position and extending to the right 
(within grid bounds). Objects consisting of more than one pixel are left unchanged.
The background remains white unless overwritten by the expansion.
"""

def find_objects(grid):
    """
    Finds all connected objects of non-white pixels in the grid.
    Connectivity includes diagonals.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains 'pixels' (a set of (row, col) tuples) and 'color'.
    """
    height, width = grid.shape
    visited = set()
    objects = []
    
    for r in range(height):
        for c in range(width):
            # Check if pixel is non-white and not visited
            if grid[r, c] != 0 and (r, c) not in visited:
                object_color = grid[r, c]
                current_object_pixels = set()
                queue = deque([(r, c)])
                visited.add((r, c))
                
                # Start Breadth-First Search (BFS) to find connected pixels of the same color
                while queue:
                    curr_r, curr_c = queue.popleft()
                    current_object_pixels.add((curr_r, curr_c))
                    
                    # Check all 8 neighbors (including diagonals)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue # Skip self
                                
                            nr, nc = curr_r + dr, curr_c + dc
                            
                            # Check bounds
                            if 0 <= nr < height and 0 <= nc < width:
                                # Check if neighbor is part of the same object (same color) and not visited
                                if grid[nr, nc] == object_color and (nr, nc) not in visited:
                                    visited.add((nr, nc))
                                    queue.append((nr, nc))
                                    
                objects.append({'pixels': current_object_pixels, 'color': object_color})
                
    return objects

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (np.array): The input grid.

    Returns:
        np.array: The transformed output grid.
    """
    # Initialize output_grid as a copy of the input_grid.
    # This handles background preservation and ensures larger objects are initially copied.
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Find all distinct objects in the input grid.
    objects = find_objects(input_grid)

    # Iterate through each identified object.
    for obj in objects:
        # Count the number of pixels in the object.
        num_pixels = len(obj['pixels'])
        
        # If the object consists of exactly one pixel:
        if num_pixels == 1:
            # Get the coordinates and color of the single pixel.
            # The 'pixels' set contains only one tuple, so we can get it using next(iter(...)).
            r, c = next(iter(obj['pixels'])) 
            color = obj['color']
            
            # In the output grid, color the pixel at (r, c) with its color. 
            # This is already done by the initial copy, but explicit for clarity.
            # output_grid[r, c] = color 
            
            # If column c+1 is within bounds, color the pixel at (r, c+1).
            if c + 1 < width:
                output_grid[r, c + 1] = color
                
            # If column c+2 is within bounds, color the pixel at (r, c+2).
            if c + 2 < width:
                output_grid[r, c + 2] = color
                
        # If the object consists of more than one pixel, do nothing.
        # These pixels are already correctly placed in the output_grid due to the initial copy.
        # else: # num_pixels > 1
        #     pass # No change needed for larger objects

    return output_grid
```
