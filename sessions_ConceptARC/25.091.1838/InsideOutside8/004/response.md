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