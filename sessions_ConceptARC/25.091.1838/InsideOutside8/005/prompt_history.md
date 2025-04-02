
## train_1

**input:**
```
0 0 0 0 0 3 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 4 0
0 0 4 0 0 0 0 0 0 0 4 0
0 0 4 0 3 0 0 0 0 0 4 0
0 0 4 0 0 0 0 0 0 0 4 0
0 0 4 0 0 0 0 0 0 0 4 0
0 0 4 0 0 0 0 0 0 0 4 3
0 0 4 0 0 0 0 0 0 0 4 0
0 0 4 0 0 0 0 0 3 0 4 0
0 0 4 0 0 0 0 0 0 0 4 0
0 0 4 4 4 4 4 4 4 4 4 0
3 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 0 0
6 0 0 0 0 0 0 0 0 0 6
0 6 0 0 8 0 0 0 0 6 0
0 0 6 0 0 8 0 0 6 0 0
0 0 0 6 0 0 0 6 0 0 0
0 0 0 0 6 0 6 0 0 0 0
0 0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 0 0 0
0 0 0 8 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

Okay, let's break down this task.

## Perception of Elements

1.  **Grid Structure:** Both input and output are 2D grids of pixels with different colors. The grid dimensions remain constant between input and output for each example.
2.  **Colors:** Each example uses three colors: white (0) as the background, one color forming a prominent shape or boundary (yellow/4 in train_1, magenta/6 in train_2), and another color representing points or small objects (green/3 in train_1, azure/8 in train_2).
3.  **Boundary Shape:** In both examples, one color (yellow or magenta) forms a structure that seems to enclose or delineate a region within the grid. In train_1, it's a clear 'U' shape. In train_2, it's a more scattered but still somewhat containing shape.
4.  **Target Points:** The other color (green or azure) appears as scattered individual pixels or very small clusters.
5.  **Transformation:** The core transformation involves selectively keeping some of the 'target points' based on their relationship to the 'boundary shape'. Specifically, target points that appear to be *inside* the region defined by the boundary shape are retained in the output, while target points *outside* this region are removed (turned to white). The boundary shape itself is also removed in the output, replaced by the background color (white).
6.  **Defining 'Inside':** The concept of 'inside' seems related to connectivity. Points are 'inside' if they are in an area that is separated from the grid's outer border by the boundary shape. A flood fill starting from the outside (grid edges) and stopping at the boundary color would likely fail to reach the 'inside' points.

## YAML Facts


```yaml
task_description: Keep only the target-colored pixels that are located inside the region defined by the boundary-colored shape. Replace everything else, including the boundary shape itself, with the background color.

elements:
  - object: Grid
    properties:
      - type: 2D array
      - pixels: contain color values (0-9)
      - dimensions: consistent between input and output

  - object: Background
    properties:
      - color: white (0)
      - role: fills most of the output grid and areas outside the boundary in the input

  - object: Boundary Shape
    properties:
      - color: distinct non-background color (e.g., yellow/4, magenta/6)
      - shape: forms a connected or semi-connected structure
      - role: defines an 'inside' and 'outside' region within the grid
      - persistence: removed in the output

  - object: Target Points
    properties:
      - color: distinct non-background color, different from boundary color (e.g., green/3, azure/8)
      - shape: typically individual pixels or small clusters
      - location: scattered across the grid
      - role: points to be selectively kept or removed
      - persistence: kept only if located 'inside' the boundary region, otherwise removed

relationships:
  - type: containment
    description: Target points are classified as either 'inside' or 'outside' the region defined by the Boundary Shape.
  - type: transformation_rule
    description: The output grid retains only the 'inside' Target Points at their original locations, set against the Background color. The Boundary Shape is removed.

determination_of_inside:
  - method: Flood Fill Inversion
    steps:
      - Identify Boundary Color pixels.
      - Perform a flood fill starting from all Background pixels on the grid's border.
      - The fill propagates to adjacent Background pixels but cannot cross Boundary Color pixels.
      - Mark all pixels reached by the flood fill as 'outside'.
      - Any non-Boundary, non-Background pixel *not* marked as 'outside' is considered 'inside'.
```


## Natural Language Program

1.  Create an output grid with the same dimensions as the input grid, initially filled entirely with the background color (white, 0).
2.  Identify the 'boundary color' (the color forming the main enclosing shape, e.g., yellow in train_1, magenta in train_2) and the 'target color(s)' (the color(s) of the scattered points, e.g., green in train_1, azure in train_2).
3.  Determine the 'outside' region of the input grid:
    a.  Create a boolean grid (or marker set) of the same size as the input, initialized to `false`.
    b.  Initialize a queue with the coordinates of all background-colored (white, 0) pixels located on the outermost border (row 0, last row, column 0, last column) of the input grid. Mark these initial coordinates as `true` in the boolean grid.
    c.  While the queue is not empty:
        i.  Dequeue a coordinate `(r, c)`.
        ii. For each neighbor `(nr, nc)` (adjacent horizontally or vertically) of `(r, c)`:
            - If `(nr, nc)` is within the grid bounds, is *not* the 'boundary color' in the input grid, and is marked `false` in the boolean grid:
                - Mark `(nr, nc)` as `true` in the boolean grid.
                - Enqueue `(nr, nc)`.
    d.  The pixels marked `true` in the boolean grid now represent the 'outside' region reachable from the border without crossing the boundary shape.
4.  Iterate through each pixel `(r, c)` of the input grid:
    a.  If the color of the input pixel `input[r][c]` is a 'target color' AND the corresponding location `(r, c)` is marked `false` in the boolean grid (meaning it's *not* 'outside', therefore it's 'inside'):
        i.  Set the corresponding pixel in the output grid `output[r][c]` to the 'target color' found in `input[r][c]`.
5.  Return the completed output grid.
```python
import numpy as np
from collections import deque, Counter

"""
Keep only the target-colored pixels that are located inside the region defined 
by the boundary-colored shape. Replace everything else, including the boundary 
shape itself, with the background color (0).

The 'inside' region is determined by performing a flood fill starting from the 
background pixels (0) on the grid's border. Pixels reachable by this flood fill 
without crossing the boundary color are considered 'outside'. Target-colored 
pixels not marked as 'outside' are considered 'inside' and are kept in the 
output grid. The boundary color is identified as the non-background color with 
the highest pixel count in the input grid. All other non-background colors are 
considered target colors.
"""

def find_colors(input_grid_np):
    """Identifies background, boundary, and target colors."""
    unique_colors, counts = np.unique(input_grid_np, return_counts=True)
    color_counts = dict(zip(unique_colors, counts))
    
    background_color = 0
    non_background_colors = {c: count for c, count in color_counts.items() if c != background_color}
    
    boundary_color = None
    target_colors = set()
    
    if not non_background_colors:
        # Only background color present
        return background_color, boundary_color, target_colors
        
    # Heuristic: Boundary color is the non-background color with the most pixels
    boundary_color = max(non_background_colors, key=non_background_colors.get)
    
    # All other non-background colors are targets
    target_colors = set(non_background_colors.keys()) - {boundary_color}
    
    return background_color, boundary_color, target_colors

def transform(input_grid):
    """
    Transforms the input grid based on the containment rule.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list.

    Returns:
        list of lists: The transformed output grid.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape
    
    # Initialize output grid with background color
    background_color = 0
    output_grid_np = np.full_like(input_grid_np, background_color)
    
    # Identify the boundary and target colors
    _, boundary_color, target_colors = find_colors(input_grid_np)

    # If there's no boundary or no targets, return the background grid
    if boundary_color is None or not target_colors:
         return output_grid_np.tolist()

    # Determine the 'outside' region using flood fill from borders
    visited = np.zeros_like(input_grid_np, dtype=bool)
    q = deque()

    # Add border pixels that are NOT the boundary color to the queue
    for r in range(height):
        for c in [0, width - 1]:
            if input_grid_np[r, c] != boundary_color and not visited[r, c]:
                visited[r, c] = True
                q.append((r, c))
    for c in range(1, width - 1): # Avoid double-adding corners
        for r in [0, height - 1]:
             if input_grid_np[r, c] != boundary_color and not visited[r, c]:
                visited[r, c] = True
                q.append((r, c))

    # Perform flood fill (Breadth-First Search)
    while q:
        r, c = q.popleft()
        
        # Check neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            
            # Check bounds
            if 0 <= nr < height and 0 <= nc < width:
                # If neighbor is not boundary color and not visited
                if input_grid_np[nr, nc] != boundary_color and not visited[nr, nc]:
                    visited[nr, nc] = True
                    q.append((nr, nc))

    # Populate the output grid
    # Iterate through each pixel of the input grid
    for r in range(height):
        for c in range(width):
            pixel_color = input_grid_np[r, c]
            # If the pixel has a target color AND it was NOT visited by the flood fill (i.e., it's 'inside')
            if pixel_color in target_colors and not visited[r, c]:
                # Keep this pixel in the output grid
                output_grid_np[r, c] = pixel_color
                
    # Convert back to list of lists and return
    return output_grid_np.tolist()
```
```python
import numpy as np
from collections import deque

"""
Keep only the target-colored pixels that are located inside the region defined 
by the boundary-colored shape. Replace everything else, including the boundary 
shape itself, with the background color (white, 0).

The boundary color is identified as the non-background color with the highest 
pixel count. Target colors are all other non-background colors.

The 'inside' region is determined by performing a flood fill starting *only* from 
the background pixels (0) located on the grid's border. Pixels reachable by this 
flood fill without crossing the boundary color are marked as 'outside'. 
Target-colored pixels *not* marked as 'outside' are considered 'inside' and 
are kept in the output grid at their original positions.
"""

def find_colors(input_grid_np):
    """
    Identifies background, boundary (most frequent non-0), and target 
    (other non-0) colors.

    Args:
        input_grid_np (np.ndarray): The input grid as a NumPy array.

    Returns:
        tuple: (background_color, boundary_color, target_colors)
               boundary_color is None if only background exists.
               target_colors is an empty set if no targets exist.
    """
    unique_colors, counts = np.unique(input_grid_np, return_counts=True)
    color_counts = dict(zip(unique_colors, counts))
    
    background_color = 0
    non_background_colors = {c: count for c, count in color_counts.items() if c != background_color}
    
    boundary_color = None
    target_colors = set()
    
    if not non_background_colors:
        # Only background color present
        return background_color, boundary_color, target_colors
        
    # Heuristic: Boundary color is the non-background color with the most pixels
    boundary_color = max(non_background_colors, key=non_background_colors.get)
    
    # All other non-background colors are targets
    target_colors = set(non_background_colors.keys()) - {boundary_color}
    
    return background_color, boundary_color, target_colors

def transform(input_grid):
    """
    Transforms the input grid based on the containment rule.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list.

    Returns:
        list of lists: The transformed output grid.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape
    
    # 1. Identify colors
    background_color, boundary_color, target_colors = find_colors(input_grid_np)

    # Initialize output grid with background color
    output_grid_np = np.full_like(input_grid_np, background_color)

    # Handle edge cases: If no boundary or no targets, return the background grid
    if boundary_color is None or not target_colors:
         return output_grid_np.tolist()

    # 2. Determine the 'outside' region using flood fill
    is_outside = np.zeros_like(input_grid_np, dtype=bool)
    q = deque()

    # Initialize queue with background pixels on the border
    for r in range(height):
        for c in [0, width - 1]:
            if input_grid_np[r, c] == background_color and not is_outside[r, c]:
                is_outside[r, c] = True
                q.append((r, c))
    for c in range(1, width - 1): # Avoid double-adding corners
        for r in [0, height - 1]:
             if input_grid_np[r, c] == background_color and not is_outside[r, c]:
                is_outside[r, c] = True
                q.append((r, c))

    # Perform flood fill (Breadth-First Search)
    while q:
        r, c = q.popleft()
        
        # Check neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            
            # Check bounds
            if 0 <= nr < height and 0 <= nc < width:
                # Check if neighbor is NOT boundary color AND NOT already marked as outside
                if input_grid_np[nr, nc] != boundary_color and not is_outside[nr, nc]:
                    is_outside[nr, nc] = True
                    q.append((nr, nc))

    # 3. Populate the output grid
    # Iterate through each pixel of the input grid
    for r in range(height):
        for c in range(width):
            pixel_color = input_grid_np[r, c]
            # If the pixel has a target color AND it was NOT marked as outside (i.e., it's 'inside')
            if pixel_color in target_colors and not is_outside[r, c]:
                # Keep this pixel in the output grid
                output_grid_np[r, c] = pixel_color
                
    # Convert back to list of lists and return
    return output_grid_np.tolist()
```

Previous Code:
```python
import numpy as np
from collections import deque

"""
Keep only the target-colored pixels that are located inside the region defined 
by the boundary-colored shape. Replace everything else, including the boundary 
shape itself, with the background color (white, 0).

The boundary color is identified as the non-background color with the highest 
pixel count. Target colors are all other non-background colors.

The 'inside' region is determined by performing a flood fill starting *only* from 
the background pixels (0) located on the grid's border. Pixels reachable by this 
flood fill without crossing the boundary color are marked as 'outside'. 
Target-colored pixels *not* marked as 'outside' are considered 'inside' and 
are kept in the output grid at their original positions.
"""

def find_colors(input_grid_np):
    """
    Identifies background, boundary (most frequent non-0), and target 
    (other non-0) colors.

    Args:
        input_grid_np (np.ndarray): The input grid as a NumPy array.

    Returns:
        tuple: (background_color, boundary_color, target_colors)
               boundary_color is None if only background exists.
               target_colors is an empty set if no targets exist.
    """
    unique_colors, counts = np.unique(input_grid_np, return_counts=True)
    color_counts = dict(zip(unique_colors, counts))
    
    background_color = 0
    non_background_colors = {c: count for c, count in color_counts.items() if c != background_color}
    
    boundary_color = None
    target_colors = set()
    
    if not non_background_colors:
        # Only background color present
        return background_color, boundary_color, target_colors
        
    # Heuristic: Boundary color is the non-background color with the most pixels
    boundary_color = max(non_background_colors, key=non_background_colors.get)
    
    # All other non-background colors are targets
    target_colors = set(non_background_colors.keys()) - {boundary_color}
    
    return background_color, boundary_color, target_colors

def transform(input_grid):
    """
    Transforms the input grid based on the containment rule.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list.

    Returns:
        list of lists: The transformed output grid.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape
    
    # 1. Identify colors
    background_color, boundary_color, target_colors = find_colors(input_grid_np)

    # Initialize output grid with background color
    output_grid_np = np.full_like(input_grid_np, background_color)

    # Handle edge cases: If no boundary or no targets, return the background grid
    if boundary_color is None or not target_colors:
         return output_grid_np.tolist()

    # 2. Determine the 'outside' region using flood fill
    is_outside = np.zeros_like(input_grid_np, dtype=bool)
    q = deque()

    # Initialize queue with background pixels on the border
    for r in range(height):
        for c in [0, width - 1]:
            if input_grid_np[r, c] == background_color and not is_outside[r, c]:
                is_outside[r, c] = True
                q.append((r, c))
    for c in range(1, width - 1): # Avoid double-adding corners
        for r in [0, height - 1]:
             if input_grid_np[r, c] == background_color and not is_outside[r, c]:
                is_outside[r, c] = True
                q.append((r, c))

    # Perform flood fill (Breadth-First Search)
    while q:
        r, c = q.popleft()
        
        # Check neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            
            # Check bounds
            if 0 <= nr < height and 0 <= nc < width:
                # Check if neighbor is NOT boundary color AND NOT already marked as outside
                if input_grid_np[nr, nc] != boundary_color and not is_outside[nr, nc]:
                    is_outside[nr, nc] = True
                    q.append((nr, nc))

    # 3. Populate the output grid
    # Iterate through each pixel of the input grid
    for r in range(height):
        for c in range(width):
            pixel_color = input_grid_np[r, c]
            # If the pixel has a target color AND it was NOT marked as outside (i.e., it's 'inside')
            if pixel_color in target_colors and not is_outside[r, c]:
                # Keep this pixel in the output grid
                output_grid_np[r, c] = pixel_color
                
    # Convert back to list of lists and return
    return output_grid_np.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 3 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 4 0
0 0 4 0 0 0 0 0 0 0 4 0
0 0 4 0 3 0 0 0 0 0 4 0
0 0 4 0 0 0 0 0 0 0 4 0
0 0 4 0 0 0 0 0 0 0 4 0
0 0 4 0 0 0 0 0 0 0 4 3
0 0 4 0 0 0 0 0 0 0 4 0
0 0 4 0 0 0 0 0 3 0 4 0
0 0 4 0 0 0 0 0 0 0 4 0
0 0 4 4 4 4 4 4 4 4 4 0
3 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 2
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 2.564102564102541

## Example 2:
Input:
```
0 8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 0 0
6 0 0 0 0 0 0 0 0 0 6
0 6 0 0 8 0 0 0 0 6 0
0 0 6 0 0 8 0 0 6 0 0
0 0 0 6 0 0 0 6 0 0 0
0 0 0 0 6 0 6 0 0 0 0
0 0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 0 0 0
0 0 0 8 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 2
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 3.3057851239669276
## General Assessment

The previous code failed because the flood fill logic used to determine the 'outside' region incorrectly included the 'inside' target pixels. The flood fill propagated through any non-boundary pixel, allowing it to "leak" into the intended inner region via background or target pixels connected to the border region.

The core idea is to keep target-colored pixels that are *not* connected to the grid's border if we are only allowed to move through non-boundary-colored pixels.

The strategy is to use a connected components approach. For each target pixel encountered that hasn't been visited yet, perform a search (like BFS or DFS) to find all connected non-boundary pixels. During the search, check if any pixel in the component touches the grid border. If the component does not touch the border, then all target pixels found within that component are considered 'inside' and should be kept in the output.

## Metrics

**Train Example 1:**
*   Input Grid Size: 13 rows x 12 columns = 156 pixels
*   Output Grid Size: 13 rows x 12 columns = 156 pixels
*   Colors Present (Input):
    *   0 (white): 123 pixels (Background)
    *   3 (green): 6 pixels (Target)
    *   4 (yellow): 27 pixels (Boundary - most frequent non-background)
*   Colors Present (Output):
    *   0 (white): 154 pixels
    *   3 (green): 2 pixels
*   Target Pixels Kept: `(4, 4)`, `(9, 8)`
*   Target Pixels Removed: `(0, 5)`, `(0, 8)`, `(7, 11)`, `(12, 0)`
*   Boundary Pixels: Removed (turned to white).
*   Previous Code Output: All 0s. Failed.

**Train Example 2:**
*   Input Grid Size: 11 rows x 11 columns = 121 pixels
*   Output Grid Size: 11 rows x 11 columns = 121 pixels
*   Colors Present (Input):
    *   0 (white): 104 pixels (Background)
    *   6 (magenta): 11 pixels (Boundary - most frequent non-background)
    *   8 (azure): 6 pixels (Target)
*   Colors Present (Output):
    *   0 (white): 119 pixels
    *   8 (azure): 2 pixels
*   Target Pixels Kept: `(3, 4)`, `(4, 5)`
*   Target Pixels Removed: `(0, 1)`, `(1, 8)`, `(9, 7)`, `(10, 3)`
*   Boundary Pixels: Removed (turned to white).
*   Previous Code Output: All 0s. Failed.

## YAML Facts


```yaml
task_description: Isolate and keep only the target-colored pixels that belong to connected regions of non-boundary-colored pixels which do not touch the grid border. All other pixels, including the boundary color itself and target pixels in regions connected to the border, become background color.

elements:
  - object: Grid
    properties:
      - type: 2D array
      - pixels: contain color values (0-9)
      - dimensions: consistent between input and output (H x W)

  - object: Background
    properties:
      - color: white (0)
      - role: fills the output grid except for 'inside' target pixels

  - object: Boundary Color
    properties:
      - determination: the non-background (non-0) color with the highest frequency in the input grid
      - role: acts as a barrier separating potential 'inside' regions from the 'outside'
      - persistence: removed in the output (becomes background color)

  - object: Target Color(s)
    properties:
      - determination: all non-background colors that are not the boundary color
      - role: pixels to be potentially kept in the output
      - persistence: kept only if they belong to a component of non-boundary pixels disconnected from the grid border

  - object: Connected Component
    properties:
      - definition: a set of pixels connected horizontally or vertically
      - constraint: all pixels within the component must NOT have the boundary color
      - property: border_touching (boolean) - true if any pixel in the component is located at row 0, row H-1, col 0, or col W-1

relationships:
  - type: connectivity
    description: Pixels are connected if adjacent horizontally or vertically.
  - type: containment (implicit)
    description: A target pixel is 'inside' if its connected component of non-boundary pixels is not border_touching.
  - type: transformation_rule
    description: Create an output grid filled with the background color. Find all connected components of non-boundary pixels. For each component that is *not* border_touching, identify all target-colored pixels within it and place them at their original coordinates in the output grid.

actions:
  - action: identify_colors
    inputs: input_grid
    outputs: background_color, boundary_color, target_colors
    description: Count pixel frequencies to determine boundary (most frequent non-0) and target (other non-0) colors.
  - action: find_connected_components
    inputs: input_grid, boundary_color
    outputs: list of components, where each component notes if it touches the border and lists its target pixels
    description: Use BFS or DFS starting from unvisited non-boundary pixels to find connected components, tracking border contact and contained target pixels.
  - action: filter_and_render
    inputs: output_grid_dimensions, background_color, components_data
    outputs: final_output_grid
    description: Create a background grid. For each component that is *not* border-touching, place its associated target pixels onto the output grid.

```


## Natural Language Program

1.  **Analyze Input:**
    a.  Determine the dimensions (height H, width W) of the input grid.
    b.  Count the occurrences of each non-background (non-zero) color.
    c.  Identify the `boundary_color` as the non-background color with the highest count.
    d.  Identify the `target_colors` as the set of all non-background colors *except* the `boundary_color`.
2.  **Initialize:**
    a.  Create an output grid of the same dimensions (H x W), filled entirely with the background color (0).
    b.  Create a `visited` grid (boolean, H x W), initialized to all `false`.
3.  **Process Components:**
    a.  Iterate through each cell `(r, c)` from `(0, 0)` to `(H-1, W-1)` of the input grid.
    b.  If the current cell `(r, c)` has not been `visited` AND its color `input[r][c]` is NOT the `boundary_color`:
        i.  Start a search (e.g., Breadth-First Search) from `(r, c)` to find the connected component of non-`boundary_color` pixels.
        ii. Initialize for this component: `touches_border = false`, `component_pixels = empty list`, `component_targets = empty list`.
        iii. Use a queue for the search, initially containing `(r, c)`. Mark `visited[r][c] = true`.
        iv. While the search queue is not empty:
            1.  Dequeue a pixel `(curr_r, curr_c)`.
            2.  Add `(curr_r, curr_c)` to `component_pixels`.
            3.  If `input[curr_r][curr_c]` is in `target_colors`, add `(curr_r, curr_c)` to `component_targets`.
            4.  Check if `(curr_r, curr_c)` is on the border (i.e., `curr_r == 0` or `curr_r == H-1` or `curr_c == 0` or `curr_c == W-1`). If yes, set `touches_border = true`.
            5.  For each valid neighbor `(nr, nc)` (within grid bounds, adjacent horizontally/vertically):
                *   If `visited[nr, nc]` is `false` AND `input[nr, nc]` is NOT the `boundary_color`:
                    *   Mark `visited[nr, nc] = true`.
                    *   Enqueue `(nr, nc)`.
        v.  After the search for this component is complete: If `touches_border` is `false`:
            1.  For each target pixel coordinate `(tr, tc)` in `component_targets`:
                *   Set `output[tr][tc] = input[tr][tc]`.
4.  **Return:** Return the final output grid.


```python
import numpy as np
from collections import deque

"""
Keep only the target-colored pixels that belong to connected regions of 
non-boundary-colored pixels which do not touch the grid border. All other 
pixels, including the boundary color itself and target pixels in regions 
connected to the border, become background color (0).

The boundary color is identified as the non-background color with the highest 
pixel count. Target colors are all other non-background colors.

A connected component search (BFS) is performed starting from each unvisited, 
non-boundary pixel. If a component is found to not touch the border, any 
target-colored pixels within that component are placed onto the output grid.
"""

def find_colors(input_grid_np):
    """
    Identifies background, boundary (most frequent non-0), and target 
    (other non-0) colors.
    """
    unique_colors, counts = np.unique(input_grid_np, return_counts=True)
    color_counts = dict(zip(unique_colors, counts))
    
    background_color = 0
    non_background_colors = {c: count for c, count in color_counts.items() if c != background_color}
    
    boundary_color = None
    target_colors = set()
    
    if not non_background_colors:
        return background_color, boundary_color, target_colors
        
    boundary_color = max(non_background_colors, key=non_background_colors.get)
    target_colors = set(non_background_colors.keys()) - {boundary_color}
    
    return background_color, boundary_color, target_colors

def transform(input_grid):
    """
    Transforms the input grid based on the border-connected component rule.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape
    
    # 1. Identify colors
    background_color, boundary_color, target_colors = find_colors(input_grid_np)

    # Initialize output grid with background color
    output_grid_np = np.full_like(input_grid_np, background_color)

    # Handle edge cases: If no boundary or no targets, return background grid
    if boundary_color is None: # No boundary means everything non-bg is target
        target_colors = set(np.unique(input_grid_np)) - {background_color}
        # If no targets either, result is all background anyway
        if not target_colors:
             return output_grid_np.tolist()
        # Treat the problem as if there's a dummy boundary - effectively check connectivity to border for all non-bg pixels
        # Or simplify: if no boundary, maybe keep all targets? Let's stick to component logic.
        # If no boundary color identified (e.g. only bg and one other color)
        # consider all non-bg colors as targets and proceed, boundary effectively doesn't block anything.
        boundary_color = -1 # Use a dummy value not in 0-9
    
    if not target_colors: # Only background and boundary exist
         return output_grid_np.tolist()


    # 2. Initialize visited grid
    visited = np.zeros_like(input_grid_np, dtype=bool)

    # 3. Process Components
    for r in range(height):
        for c in range(width):
            # Start BFS from unvisited non-boundary cells
            if not visited[r, c] and input_grid_np[r, c] != boundary_color:
                q = deque([(r, c)])
                visited[r, c] = True
                component_pixels = []
                component_targets = []
                touches_border = False
                
                while q:
                    curr_r, curr_c = q.popleft()
                    component_pixels.append((curr_r, curr_c))
                    pixel_color = input_grid_np[curr_r, curr_c]

                    if pixel_color in target_colors:
                        component_targets.append((curr_r, curr_c, pixel_color)) # Store color too

                    # Check border contact
                    if not touches_border and (curr_r == 0 or curr_r == height - 1 or curr_c == 0 or curr_c == width - 1):
                        touches_border = True
                        
                    # Explore neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        
                        if 0 <= nr < height and 0 <= nc < width:
                            if not visited[nr, nc] and input_grid_np[nr, nc] != boundary_color:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                                
                # After BFS for component is done, check border contact
                if not touches_border:
                    # Place targets from this component onto the output grid
                    for tr, tc, t_color in component_targets:
                        output_grid_np[tr, tc] = t_color

    # Convert back to list of lists and return
    return output_grid_np.tolist()
```
