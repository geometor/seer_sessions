
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
6 0 0 3 3 3 3 3 3 3 0 0
6 0 3 3 0 0 0 0 3 0 0 6
0 0 3 0 0 6 0 0 3 0 0 0
0 0 3 3 0 6 0 6 3 0 6 0
0 0 0 3 0 0 0 0 3 0 0 0
6 0 0 3 0 0 6 0 0 3 0 0
0 0 3 3 0 0 0 0 0 3 0 0
0 0 0 3 3 3 0 0 0 3 0 0
0 0 0 0 0 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0 0 0 6
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 0 0 4 4 0 0
0 0 4 4 0 0 1 0 0 0 4 0 4 0 0
0 0 4 0 4 0 0 0 0 0 0 0 4 0 0
0 4 0 0 4 0 0 0 0 4 0 0 0 4 0
4 0 1 0 4 4 0 0 0 4 0 0 0 4 0
4 4 0 0 0 4 4 4 4 0 0 0 4 4 0
0 4 4 0 0 0 0 0 0 0 0 0 4 0 0
0 0 4 4 0 1 0 0 0 0 0 4 4 0 0
0 0 0 4 4 0 0 1 0 0 0 4 0 0 0
0 0 0 0 4 0 0 0 0 0 4 4 0 0 0
0 0 0 0 4 0 0 0 0 4 0 0 0 1 0
0 1 0 0 0 0 4 4 4 4 0 1 0 0 0
0 0 0 0 1 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 1 0
0 1 0 0 0 0 0 0 0 0 0 1 0 0 0
0 0 0 0 1 0 0 0 0 0 0 0 0 0 0
```

*   **Perception:**
    *   The input grids contain a background color (white - 0), a primary structure color (green - 3 in example 1, yellow - 4 in example 2), and a target color (magenta - 6 in example 1, blue - 1 in example 2).
    *   The primary structure color forms connected shapes that act as boundaries or containers.
    *   The target color pixels appear both inside and outside these container structures.
    *   The output grids retain only the background color (white - 0) and the target color pixels that were originally located *outside* the container structures.
    *   All pixels of the container color and all target color pixels located *inside* the containers are replaced with the background color in the output.
    *   The core transformation involves identifying regions enclosed by the primary structure color and removing everything within those regions, including the structure itself, while preserving target color pixels located outside these regions. The "outside" region can be defined as the area reachable from the grid boundaries without crossing the container color.

*   **Facts:**
    
```yaml
    background_color: 0 # white
    elements:
      - role: container
        properties:
          - forms connected components
          - color varies (e.g., green (3), yellow (4))
          - encloses areas within the grid
      - role: target
        properties:
          - often appear as individual pixels or small groups
          - color varies (e.g., magenta (6), blue (1))
          - location relative to container (inside or outside) is critical
    transformation:
      - identifies the container color and target color.
      - determines the 'outside' region: cells reachable from the grid boundary without crossing the container color.
      - removes container color pixels.
      - removes target color pixels not in the 'outside' region (i.e., 'inside' pixels).
      - preserves target color pixels located in the 'outside' region.
    output:
      - contains only background color and preserved target color pixels.
      - dimensions match the input grid.

    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid, filled entirely with the background color (white - 0).
    2.  Identify the 'container' color: the color that forms the largest connected component, excluding the background color.
    3.  Identify the 'target' color: the non-background, non-container color present in the input grid.
    4.  Perform a flood fill (or similar connectivity analysis like Breadth-First Search) starting from all pixels on the boundary of the input grid.
    5.  During the flood fill:
        *   Mark visited cells.
        *   Do not enter cells containing the 'container' color.
        *   Only traverse into adjacent (including diagonals) cells that have not been visited and do not contain the 'container' color.
    6.  Iterate through all cells in the input grid.
    7.  If a cell contains the 'target' color AND was visited during the flood fill (meaning it's reachable from the boundary without crossing the container color), copy its 'target' color to the corresponding cell in the output grid.
    8.  All other cells in the output grid remain the background color (white - 0).
    9.  Return the modified output grid.
```python
import numpy as np
from collections import deque, Counter

"""
Identify the background color (assumed to be 0), the container color (the most frequent non-background color forming enclosing structures), and the target color (the other non-background color). 
Perform a flood fill (or Breadth-First Search - BFS) starting from the grid boundaries, avoiding cells with the container color. 
Mark all reachable cells ('outside' region). 
Create an output grid initialized with the background color. 
Copy the target color to the output grid only for cells that originally contained the target color and were marked as reachable ('outside') during the flood fill.
"""

def _identify_colors(grid):
    """Identifies background, container, and target colors."""
    unique_colors, counts = np.unique(grid, return_counts=True)
    color_counts = dict(zip(unique_colors, counts))

    # Assume background is 0
    background_color = 0
    if background_color in color_counts:
        del color_counts[background_color]

    if not color_counts: # Only background color present
        return background_color, None, None

    # Find the most frequent non-background color as the potential container
    # Sort by count descending, then by color value ascending as tie-breaker
    sorted_colors = sorted(color_counts.items(), key=lambda item: (-item[1], item[0]))
    
    container_color = sorted_colors[0][0]
    target_color = None
    
    if len(sorted_colors) > 1:
        # Find the first color that isn't the container
        for color, _ in sorted_colors[1:]:
            target_color = color
            break
    elif len(sorted_colors) == 1:
         # If only one non-background color, it acts as the target, no container blocking
         target_color = container_color
         container_color = -1 # Indicate no container effectively blocks flood fill


    # A better heuristic might be needed if frequency isn't always the best indicator
    # of the container, but it works for the provided examples.

    return background_color, container_color, target_color

def transform(input_grid):
    """
    Filters the input grid to keep only target color pixels located outside
    of regions enclosed by the container color.
    """
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape

    # Identify the key colors
    background_color, container_color, target_color = _identify_colors(input_np)

    # Initialize output grid with background color
    output_grid = np.full_like(input_np, background_color)

    # If there's no target color, return the background grid
    if target_color is None:
        return output_grid.tolist()
        
    # If there's effectively no container (either only background and target,
    # or identified container color is -1), all target pixels are kept.
    if container_color is None or container_color == -1:
         for r in range(rows):
            for c in range(cols):
                 if input_np[r, c] == target_color:
                     output_grid[r, c] = target_color
         return output_grid.tolist()


    # Perform flood fill (BFS) from boundaries to find 'outside' cells
    q = deque()
    visited = np.zeros_like(input_np, dtype=bool)

    # Add boundary cells to queue if they are not the container color
    for r in range(rows):
        for c in [0, cols - 1]:
            if input_np[r, c] != container_color and not visited[r, c]:
                q.append((r, c))
                visited[r, c] = True
    for c in range(cols): # Use range(cols) instead of range(1, cols - 1) to include corners twice, which is fine
        for r in [0, rows - 1]:
             if input_np[r, c] != container_color and not visited[r, c]:
                q.append((r, c))
                visited[r, c] = True
                
    # Define 8 directions for neighbors (including diagonals)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    # Start BFS
    while q:
        r, c = q.popleft()

        # Explore neighbors
        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            # Check bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if neighbor is not visited and not the container color
                if not visited[nr, nc] and input_np[nr, nc] != container_color:
                    visited[nr, nc] = True
                    q.append((nr, nc))

    # Populate the output grid
    for r in range(rows):
        for c in range(cols):
            # If the cell in the input grid has the target color AND was visited (is outside)
            if input_np[r, c] == target_color and visited[r, c]:
                # Set the corresponding cell in the output grid to the target color
                output_grid[r, c] = target_color

    return output_grid.tolist()
```
```python
import numpy as np
from collections import deque

"""
Identifies the background color (0), the container color (most frequent non-background color), and the target color (other non-background color).
Performs a Breadth-First Search (BFS) starting only from background-colored cells on the grid boundary, exploring only through adjacent background cells, to identify the 'outside' background region.
Creates an output grid initialized with the background color.
Copies the target color to the output grid only for cells that originally contained the target color AND are adjacent (8-way) to at least one cell marked as belonging to the 'outside' background region.
"""

def _identify_colors(grid):
    """
    Identifies background, container, and target colors based on frequency.
    Assumes background is 0.
    Container is the most frequent non-background color.
    Target is the other non-background color.
    Handles cases with 0, 1, or 2 non-background colors.
    """
    unique_colors, counts = np.unique(grid, return_counts=True)
    color_counts = dict(zip(unique_colors, counts))

    # Assume background is 0
    background_color = 0
    if background_color in color_counts:
        del color_counts[background_color]

    if not color_counts: # Only background color present
        return background_color, None, None

    # Sort by count descending, then by color value ascending as tie-breaker
    sorted_colors = sorted(color_counts.items(), key=lambda item: (-item[1], item[0]))

    container_color = None
    target_color = None

    if len(sorted_colors) >= 2:
        container_color = sorted_colors[0][0]
        target_color = sorted_colors[1][0] # The next most frequent is assumed target
        # If there are more than 2 non-bg colors, this heuristic might fail.
        # For this specific task, it seems there are only ever 2 non-bg colors.
    elif len(sorted_colors) == 1:
         # If only one non-background color, it acts as the target, no container blocking
         target_color = sorted_colors[0][0]
         container_color = -1 # Use -1 to signify no effective container barrier

    return background_color, container_color, target_color


def transform(input_grid):
    """
    Filters the input grid based on reachability from the outer background.
    """
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape

    # 1. Identify the key colors
    background_color, container_color, target_color = _identify_colors(input_np)

    # 2. Initialize output grid with background color
    output_grid = np.full_like(input_np, background_color)

    # 3. Handle edge cases: no target color
    if target_color is None:
        return output_grid.tolist()

    # 4. Handle edge case: no container color (only background and target)
    # In this case, all target pixels are effectively 'outside'.
    if container_color == -1:
        output_grid[input_np == target_color] = target_color
        return output_grid.tolist()

    # 5. Perform flood fill (BFS) from boundary *background* cells
    # This identifies the 'outside' background region.
    q = deque()
    visited_background = np.zeros_like(input_np, dtype=bool)

    # Add boundary background cells to queue and mark as visited
    for r in range(rows):
        for c in [0, cols - 1]:
            if input_np[r, c] == background_color and not visited_background[r, c]:
                q.append((r, c))
                visited_background[r, c] = True
    for c in range(cols): # Cover top/bottom rows, including corners again (fine)
        for r in [0, rows - 1]:
            if input_np[r, c] == background_color and not visited_background[r, c]:
                q.append((r, c))
                visited_background[r, c] = True

    # Define 8 directions for neighbors (including diagonals)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    # Start BFS, exploring only through background cells
    while q:
        r, c = q.popleft()

        # Explore neighbors
        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            # Check bounds and if the neighbor is background and not visited
            if (0 <= nr < rows and 0 <= nc < cols and
                    input_np[nr, nc] == background_color and
                    not visited_background[nr, nc]):
                visited_background[nr, nc] = True
                q.append((nr, nc))

    # 6. Populate the output grid
    # Iterate through all input cells
    for r in range(rows):
        for c in range(cols):
            # If the cell contains the target color
            if input_np[r, c] == target_color:
                # Check its 8 neighbors
                keep_target = False
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    # Check bounds
                    if 0 <= nr < rows and 0 <= nc < cols:
                        # Check if the neighbor is background AND part of the 'outside' region
                        if input_np[nr, nc] == background_color and visited_background[nr, nc]:
                            keep_target = True
                            break # Found a connection to the outside, no need to check further neighbors

                # If connected to the outside background, copy target color to output
                if keep_target:
                    output_grid[r, c] = target_color

    # 7. Return the modified output grid as a list of lists
    return output_grid.tolist()
```
