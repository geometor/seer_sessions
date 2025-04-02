
## train_1

**input:**
```
0 2 2 2 0 0 0 0 0 0
0 2 0 2 0 0 0 0 0 0
0 2 0 2 0 0 0 0 0 0
0 2 0 2 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 4 4 0 0
0 0 0 4 0 0 0 4 0 0
0 0 0 4 4 4 4 4 0 0
```


**output:**
```
0 2 2 2 0 0 0 0 0 0
0 2 3 2 0 0 0 0 0 0
0 2 3 2 0 0 0 0 0 0
0 2 3 2 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 4 4 0 0
0 0 0 4 7 7 7 4 0 0
0 0 0 4 4 4 4 4 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 4 4 4
0 0 0 0 0 0 0 0 0 0 0 4 0 4
0 0 0 0 0 0 0 0 0 0 0 4 0 4
0 2 2 2 2 2 2 2 2 0 0 4 0 4
0 2 0 0 0 0 0 0 2 0 0 4 0 4
0 2 0 0 0 0 0 0 2 0 0 4 4 4
0 2 2 2 2 2 2 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 7 7 7
0 0 0 0 0 0 0 0 0 0 0 7 0 7
0 0 7 7 7 7 7 7 7 0 0 7 0 7
0 0 7 0 0 0 0 0 7 0 0 7 0 7
0 0 7 7 7 7 7 7 7 0 0 7 0 7
0 0 0 0 0 0 0 0 0 0 0 7 0 7
0 0 0 0 0 0 0 0 0 0 0 7 7 7
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 4 4 4
0 0 0 0 0 0 0 0 0 0 0 4 3 4
0 0 0 0 0 0 0 0 0 0 0 4 3 4
0 2 2 2 2 2 2 2 2 0 0 4 3 4
0 2 7 7 7 7 7 7 2 0 0 4 3 4
0 2 7 7 7 7 7 7 2 0 0 4 4 4
0 2 2 2 2 2 2 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 7 7 7
0 0 0 0 0 0 0 0 0 0 0 7 3 7
0 0 7 7 7 7 7 7 7 0 0 7 3 7
0 0 7 7 7 7 7 7 7 0 0 7 3 7
0 0 7 7 7 7 7 7 7 0 0 7 3 7
0 0 0 0 0 0 0 0 0 0 0 7 3 7
0 0 0 0 0 0 0 0 0 0 0 7 7 7
```

Okay, let's analyze the task based on the provided examples.

## Perception of Task Elements

1.  **Input/Output Structure**: Both input and output are grids of pixels with different colors. The overall grid dimensions remain unchanged.
2.  **Objects**: The grids contain distinct shapes formed by contiguous pixels of a single non-white color (Red, Yellow, Orange). These shapes are placed on a white background (color 0).
3.  **Shape Types**: The shapes appear to be either closed loops (like rectangles or 'O' shapes) or partially open loops (like 'C' shapes).
4.  **Transformation**: The core transformation involves filling certain white areas within or adjacent to the colored shapes with a new color. The original colored shapes remain unchanged.
5.  **Filling Logic**:
    *   Only white areas (color 0) that are enclosed or partially enclosed by a *single* colored shape are affected.
    *   The color used for filling depends on both the color of the enclosing shape and whether the white area is fully enclosed ('O' type) or partially enclosed ('C' type, connected to the outside background).
    *   Specifically:
        *   White areas partially enclosed by a C-shape (any color: Red, Yellow, Orange observed) are filled with Green (3).
        *   White areas fully enclosed by an O-shape/Rectangle depend on the boundary color:
            *   If the boundary is Red (2) or Yellow (4), the area is filled with Orange (7).
            *   If the boundary is Orange (7), the area is filled with Green (3).

## YAML Fact Documentation


```yaml
task_description: Fill internal white areas of colored shapes based on boundary color and shape topology.

definitions:
  - object: A contiguous block of pixels of the same non-white color (1-9).
  - background_region: The main contiguous area of white pixels (0) connected to the grid borders.
  - internal_white_region: A contiguous area of white pixels (0) not part of the background_region.
  - boundary_color: The color of the object pixels immediately adjacent to a white region.
  - shape_topology: Classification of how a shape encloses a white region.
      - C-like: Encloses a white region that IS connected to the background_region.
      - O-like: Encloses a white region that IS NOT connected to the background_region.

examples:
  train_1:
    input_grid_size: [10, 10]
    output_grid_size: [10, 10]
    objects:
      - color: Red (2)
        shape_topology: C-like
        action: Fill internal white region with Green (3).
      - color: Yellow (4)
        shape_topology: O-like
        action: Fill internal white region with Orange (7).
  train_2:
    input_grid_size: [14, 14]
    output_grid_size: [14, 14]
    objects:
      - color: Yellow (4)
        shape_topology: C-like
        action: Fill internal white region with Green (3).
      - color: Red (2)
        shape_topology: O-like
        action: Fill internal white region with Orange (7).
      - color: Orange (7)
        shape_topology: O-like
        action: Fill internal white region with Green (3).
      - color: Orange (7)
        shape_topology: C-like
        action: Fill internal white region with Green (3).

derived_rules:
  - rule: Identify all contiguous white regions.
  - rule: Determine the background_region (white region connected to grid borders).
  - rule: Identify internal_white_regions (all other white regions).
  - rule: For each internal_white_region:
      - Check if all adjacent non-white pixels belong to a single object and have the same boundary_color.
      - If yes:
          - Determine shape_topology by checking connectivity of the internal_white_region to the background_region.
          - Apply fill color based on shape_topology and boundary_color:
              - If C-like: Fill with Green (3).
              - If O-like:
                  - If boundary_color is Red (2) or Yellow (4): Fill with Orange (7).
                  - If boundary_color is Orange (7): Fill with Green (3).
                  - (Potentially other rules for unobserved boundary colors).
```


## Natural Language Program

1.  Identify all contiguous regions of white pixels (color 0) in the input grid.
2.  Identify the largest white region that touches the grid borders; designate this as the "background region". All other white regions are considered "internal regions".
3.  For each internal region:
    a.  Examine all pixels immediately adjacent (horizontally or vertically) to this internal region.
    b.  Check if all these adjacent pixels that are *not* white belong to a *single* contiguous non-white object (i.e., they all share the same non-white color and are connected to each other directly or through other pixels of the same color). Let this color be the `boundary_color`.
    c.  If such a single, uniformly colored boundary exists:
        i.  Determine if the internal region is "partially enclosed" (C-like) or "fully enclosed" (O-like). An internal region is "partially enclosed" if any of its pixels are adjacent to a pixel belonging to the "background region". Otherwise, it is "fully enclosed".
        ii. Select the fill color based on the enclosure type and the `boundary_color`:
            *   If the region is "partially enclosed" (C-like), the fill color is Green (3).
            *   If the region is "fully enclosed" (O-like):
                *   If the `boundary_color` is Red (2) or Yellow (4), the fill color is Orange (7).
                *   If the `boundary_color` is Orange (7), the fill color is Green (3).
        iii. Change the color of all pixels within this internal region to the determined fill color.
4.  Leave all pixels belonging to the original non-white shapes and the background region unchanged. The final grid is the output.
```python
import numpy as np
from collections import deque

"""
Identifies contiguous regions of white pixels (0) that are not connected to the grid border (internal regions).
For each such internal region, it checks if it is bounded by a single, uniform non-white color.
If it is, it determines if the region is partially enclosed (connected to the border white region via adjacency, C-like) or fully enclosed (O-like).
Based on the boundary color and enclosure type, it fills the internal region with a new color:
- Partially enclosed (C-like): Fill with Green (3).
- Fully enclosed (O-like):
    - Boundary Red (2) or Yellow (4): Fill with Orange (7).
    - Boundary Orange (7): Fill with Green (3).
The original non-white shapes and the background white region remain unchanged.
"""

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the output grid.
    """
    input_grid = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape
    
    # Keep track of visited pixels during flood fills
    visited = np.zeros_like(input_grid, dtype=bool)
    # Keep track of pixels belonging to the background white region
    is_background = np.zeros_like(input_grid, dtype=bool)

    q = deque()

    # 1. Identify the background white region (connected to borders) using BFS
    for r in range(height):
        for c in [0, width - 1]: # Left and right borders
            if input_grid[r, c] == 0 and not visited[r, c]:
                visited[r, c] = True
                is_background[r, c] = True
                q.append((r, c))
    for c in range(width):
        for r in [0, height - 1]: # Top and bottom borders
             if input_grid[r, c] == 0 and not visited[r, c]:
                visited[r, c] = True
                is_background[r, c] = True
                q.append((r, c))

    while q:
        r, c = q.popleft()
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]: # 4-directional neighbors
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width and \
               input_grid[nr, nc] == 0 and not visited[nr, nc]:
                visited[nr, nc] = True
                is_background[nr, nc] = True
                q.append((nr, nc))

    # 2. Iterate through the grid to find internal white regions
    for r in range(height):
        for c in range(width):
            # If it's a white pixel and hasn't been visited (i.e., not background)
            if input_grid[r, c] == 0 and not visited[r, c]:
                
                # Start a BFS for this potential internal region
                internal_q = deque([(r, c)])
                visited[r, c] = True
                current_region_pixels = [(r, c)]
                boundary_neighbors = set() # Store (nr, nc, color) tuples
                is_partially_enclosed = False 

                while internal_q:
                    curr_r, curr_c = internal_q.popleft()

                    # Check neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc

                        if 0 <= nr < height and 0 <= nc < width:
                            neighbor_color = input_grid[nr, nc]
                            
                            if neighbor_color == 0:
                                # Check if adjacent to known background
                                if is_background[nr, nc]:
                                    is_partially_enclosed = True
                                
                                # If this white neighbor hasn't been visited, add to queue
                                if not visited[nr, nc]:
                                    visited[nr, nc] = True
                                    internal_q.append((nr, nc))
                                    current_region_pixels.append((nr, nc))
                            else:
                                # It's a non-white boundary neighbor
                                boundary_neighbors.add((nr, nc, neighbor_color))
                        # else: neighbor is out of bounds, implicitly connected to 'outside'
                        # This doesn't directly make it partially enclosed by our definition,
                        # which relies on connection to the *white* background region.
                        
                # 3. Analyze the found region
                boundary_colors = set(color for _, _, color in boundary_neighbors)

                # Check if bounded by a single color
                if len(boundary_colors) == 1:
                    boundary_color = list(boundary_colors)[0]
                    fill_color = -1 # Use -1 to indicate no fill initially

                    # Determine fill color based on rules
                    if is_partially_enclosed:
                        # C-like shape rule
                        fill_color = 3 # Green
                    else:
                        # O-like shape rule
                        if boundary_color == 2 or boundary_color == 4: # Red or Yellow
                            fill_color = 7 # Orange
                        elif boundary_color == 7: # Orange
                            fill_color = 3 # Green
                            
                    # 4. Apply fill if a color was determined
                    if fill_color != -1:
                        for pr, pc in current_region_pixels:
                            output_grid[pr, pc] = fill_color

    return output_grid
```
