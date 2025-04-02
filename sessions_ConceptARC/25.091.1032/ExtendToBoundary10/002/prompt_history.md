
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 4 4 4 4 0
0 0 4 0 0 0 0 0 4 0
0 0 4 0 0 0 0 0 4 0
7 0 0 0 0 0 0 0 4 0
0 0 4 0 0 0 0 0 4 0
0 0 4 0 0 0 0 0 4 0
0 0 4 4 4 4 4 4 4 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 4 4 4 4 0
0 0 4 0 0 0 0 0 4 0
0 0 4 0 0 0 0 0 4 0
7 7 7 7 7 7 7 7 4 0
0 0 4 0 0 0 0 0 4 0
0 0 4 0 0 0 0 0 4 0
0 0 4 4 4 4 4 4 4 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 4 4 4 4 4 4 4 4 0
0 0 4 0 0 0 0 0 0 0 0 0 4 0
0 0 4 0 0 0 0 0 0 0 0 0 4 0
0 0 4 0 0 0 0 0 0 0 0 0 4 0
0 0 4 0 0 0 0 0 0 0 0 0 4 0
0 0 4 0 0 0 0 0 0 0 0 0 4 0
0 0 4 0 0 0 0 0 0 0 0 0 4 0
0 0 4 0 4 4 4 4 4 0 4 4 4 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 7 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 4 4 4 4 4 4 4 4 0
0 0 4 7 0 0 0 0 0 7 0 0 4 0
0 0 4 7 0 0 0 0 0 7 0 0 4 0
0 0 4 7 0 0 0 0 0 7 0 0 4 0
0 0 4 7 0 0 0 0 0 7 0 0 4 0
0 0 4 7 0 0 0 0 0 7 0 0 4 0
0 0 4 7 0 0 0 0 0 7 0 0 4 0
0 0 4 7 4 4 4 4 4 7 4 4 4 0
0 0 0 7 0 0 0 0 0 7 0 0 0 0
0 0 0 7 0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0 0 7 0 0 0 0
```

Okay, let's analyze the provided examples to understand the transformation.

**Perception of Elements and Transformation**

1.  **Colors:** The grids primarily use white (0) for the background, yellow (4) for static structures, and orange (7) for dynamic elements that initiate a change.
2.  **Objects:**
    *   **Background:** The white space (0) acts as the area where changes can occur.
    *   **Boundary Structure:** The yellow (4) pixels form a static structure, typically a shape like a hollow rectangle, sometimes with internal features. This structure seems to define boundaries for the transformation but remains unchanged itself. In train_2, there's a large yellow rectangle and a smaller internal yellow line.
    *   **Seed Pixels:** The orange (7) pixels are the starting points or 'seeds' for the transformation. Their initial positions are key.
3.  **Transformation:** The core transformation involves the orange (7) seed pixels 'painting' or filling adjacent white (0) pixels along a specific axis (either horizontally or vertically).
4.  **Determining Fill Direction:** The direction of filling seems to depend on the position of the orange seed pixel relative to the main yellow boundary structure.
    *   In train_1, the orange pixel is at (5,0). The main yellow rectangle spans rows 2-8. Since the orange pixel's row (5) is *within* the vertical span of the yellow structure, the fill occurs *horizontally* along row 5.
    *   In train_2, the orange pixels are at (10,3) and (11,9). The main yellow rectangle spans rows 1-8. Since the orange pixels' rows (10 and 11) are *outside* the vertical span of the yellow structure, the fill occurs *vertically* along their respective columns (3 and 9).
5.  **Fill Mechanism:** The fill radiates outwards from the seed pixel along the determined axis (row or column). It colors all contiguous white (0) pixels along that line until it encounters a pixel belonging to the main yellow (4) boundary structure or the edge of the grid. Importantly, internal features of the boundary structure (like the horizontal yellow line inside the rectangle in train_2) seem to be ignored by the fill; the fill continues until it hits the *outermost* boundary defined by that structure along the fill axis. The original seed pixel's location is also colored orange in the output.

**Facts YAML**


```yaml
elements:
  - color: 0
    name: white
    role: background
    property: fillable_area
  - color: 4
    name: yellow
    role: boundary_structure
    property: static
    observation: Forms shapes, defines limits for filling. The largest connected component seems to be the primary boundary. Internal parts might be ignored by the fill.
  - color: 7
    name: orange
    role: seed_and_fill
    property: dynamic
    observation: Initiates filling process. Final fill color.

grid_properties:
  - size: variable height and width

transformation:
  - name: ray_cast_fill
    input_elements:
      - seed_pixels (orange)
      - boundary_structure (yellow)
      - background (white)
    output_elements:
      - filled_pixels (orange)
      - original_boundary_structure (yellow)
      - remaining_background (white)
    process:
      - step: Identify the largest connected component of boundary (yellow) pixels.
      - step: Determine the row-wise bounding box [min_row, max_row] of this component.
      - step: For each seed (orange) pixel at (r, c):
          - determine_direction: Check if `r` is within [min_row, max_row]. If yes, direction=horizontal. Else, direction=vertical.
          - ray_cast: From (r, c), cast rays in both directions along the determined axis.
          - fill: Change all white pixels along the ray paths to orange until a pixel from the largest boundary component or grid edge is hit. Ensure (r,c) is orange.
    notes: The fill process seems to treat only the pixels of the largest yellow component as stopping points, ignoring other yellow pixels or potentially other orange pixels created by the fill process itself.

examples_summary:
  - train_1: Seed row is inside boundary bbox rows -> horizontal fill.
  - train_2: Seed rows are outside boundary bbox rows -> vertical fill. Fill ignores internal yellow line, stops at top boundary.
```


**Natural Language Program**

1.  Create a copy of the input grid, which will become the output grid.
2.  Identify all yellow (4) pixels in the input grid. Determine the largest connected component formed by these yellow pixels (this is the 'main boundary structure').
3.  Calculate the minimum and maximum row indices occupied by this main boundary structure.
4.  Identify all orange (7) 'seed' pixels in the input grid.
5.  For each orange seed pixel located at row `r` and column `c`:
    a.  Determine the fill direction: If the seed pixel's row `r` falls within the minimum and maximum row indices of the main boundary structure (inclusive), the direction is horizontal. Otherwise, the direction is vertical.
    b.  If the direction is horizontal (fill along row `r`):
        i.  Starting from the column `c-1` and moving left towards column 0, examine each pixel `(r, j)`. If the pixel `(r, j)` in the *input* grid is white (0), change the corresponding pixel `(r, j)` in the *output* grid to orange (7). Stop this leftward scan if a pixel belonging to the main boundary structure (identified in step 2) is encountered at `(r, j)`, or if the grid edge is reached.
        ii. Starting from the column `c+1` and moving right towards the last column, examine each pixel `(r, j)`. If the pixel `(r, j)` in the *input* grid is white (0), change the corresponding pixel `(r, j)` in the *output* grid to orange (7). Stop this rightward scan if a pixel belonging to the main boundary structure is encountered at `(r, j)`, or if the grid edge is reached.
        iii. Ensure the pixel at `(r, c)` in the output grid is set to orange (7).
    c.  If the direction is vertical (fill along column `c`):
        i.  Starting from the row `r-1` and moving up towards row 0, examine each pixel `(i, c)`. If the pixel `(i, c)` in the *input* grid is white (0), change the corresponding pixel `(i, c)` in the *output* grid to orange (7). Stop this upward scan if a pixel belonging to the main boundary structure is encountered at `(i, c)`, or if the grid edge is reached.
        ii. Starting from the row `r+1` and moving down towards the last row, examine each pixel `(i, c)`. If the pixel `(i, c)` in the *input* grid is white (0), change the corresponding pixel `(i, c)` in the *output* grid to orange (7). Stop this downward scan if a pixel belonging to the main boundary structure is encountered at `(i, c)`, or if the grid edge is reached.
        iii. Ensure the pixel at `(r, c)` in the output grid is set to orange (7).
6.  Return the final output grid.
```python
import numpy as np
from collections import deque

"""
Transformation rule:
1. Identify the largest connected component of yellow (4) pixels, which forms the main boundary structure.
2. Calculate the vertical span (minimum and maximum row indices) of this main boundary structure.
3. Find all orange (7) 'seed' pixels.
4. For each orange seed pixel at (r, c):
    a. Determine the fill direction based on its row 'r' relative to the boundary's vertical span. If 'r' is within the span (inclusive), fill horizontally. Otherwise, fill vertically.
    b. Perform a 'ray cast' fill along the determined axis (row 'r' or column 'c').
    c. Starting from the seed pixel's location, change adjacent white (0) pixels in the input grid to orange (7) in the output grid along the determined axis (in both directions).
    d. Stop the fill in a given direction when a pixel belonging to the main yellow boundary component is encountered or the grid edge is reached.
    e. The original seed pixel location is also colored orange (7) in the output grid.
5. All other pixels retain their original colors.
"""

def find_largest_connected_component(grid, target_color):
    """Finds the largest connected component of a given color in the grid."""
    height, width = grid.shape
    visited = set()
    largest_component = set()

    for r in range(height):
        for c in range(width):
            if grid[r, c] == target_color and (r, c) not in visited:
                current_component = set()
                q = deque([(r, c)])
                visited.add((r, c))
                current_component.add((r, c))

                while q:
                    row, col = q.popleft()
                    # Check 8 neighbors (including diagonals for connectivity)
                    # Although ARC usually uses 4-way adjacency for objects,
                    # let's use 4-way (von Neumann) for finding the component itself.
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] == target_color and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            current_component.add((nr, nc))
                            q.append((nr, nc))

                if len(current_component) > len(largest_component):
                    largest_component = current_component

    return largest_component

def get_bounding_box_rows(component_coords):
    """Calculates the min and max row indices for a set of coordinates."""
    if not component_coords:
        return -1, -1 # Indicate no component found or empty component
    rows = [r for r, c in component_coords]
    return min(rows), max(rows)

def transform(input_grid):
    """
    Applies the ray-cast fill transformation based on orange seeds and a yellow boundary.
    """
    input_arr = np.array(input_grid, dtype=int)
    output_arr = np.copy(input_arr)
    height, width = input_arr.shape

    # Define colors
    WHITE = 0
    YELLOW = 4
    ORANGE = 7

    # 1. Identify the largest connected component of yellow (4) pixels
    main_boundary_coords = find_largest_connected_component(input_arr, YELLOW)

    # Handle case where no boundary is found (though unlikely based on examples)
    if not main_boundary_coords:
         # If no boundary, maybe default behavior? Or just return copy?
         # For now, assume boundary exists. If needed, add logic here.
         # Let's proceed assuming boundary exists. Find seeds first anyway.
         min_boundary_row, max_boundary_row = -1, -1 # Indicate no boundary impact
    else:
       # 2. Calculate the vertical span (min/max rows) of the main boundary
       min_boundary_row, max_boundary_row = get_bounding_box_rows(main_boundary_coords)


    # 3. Find all orange (7) seed pixels
    seed_coords = []
    for r in range(height):
        for c in range(width):
            if input_arr[r, c] == ORANGE:
                seed_coords.append((r, c))

    # 4. Process each seed pixel
    for r_seed, c_seed in seed_coords:
        # Set the seed pixel itself to orange in the output
        output_arr[r_seed, c_seed] = ORANGE

        # 4a. Determine fill direction
        # If no boundary was found, default to vertical? Or horizontal? Let's default to vertical.
        is_horizontal = False
        if min_boundary_row != -1 : # Check if boundary exists
             is_horizontal = (min_boundary_row <= r_seed <= max_boundary_row)


        # 4b/c/d. Perform ray cast fill
        if is_horizontal:
            # Fill left
            for c in range(c_seed - 1, -1, -1):
                if (r_seed, c) in main_boundary_coords:
                    break # Stop at boundary
                if input_arr[r_seed, c] == WHITE:
                    output_arr[r_seed, c] = ORANGE
                # Optional: Should it stop if it hits *any* non-white pixel?
                # Based on examples, it seems to only stop at the *main* boundary yellow.
                # Let's stick to stopping only at main boundary or grid edge.

            # Fill right
            for c in range(c_seed + 1, width):
                if (r_seed, c) in main_boundary_coords:
                    break # Stop at boundary
                if input_arr[r_seed, c] == WHITE:
                    output_arr[r_seed, c] = ORANGE

        else: # Vertical fill
            # Fill up
            for r in range(r_seed - 1, -1, -1):
                if (r, c_seed) in main_boundary_coords:
                    break # Stop at boundary
                if input_arr[r, c_seed] == WHITE:
                    output_arr[r, c_seed] = ORANGE

            # Fill down
            for r in range(r_seed + 1, height):
                if (r, c_seed) in main_boundary_coords:
                    break # Stop at boundary
                if input_arr[r, c_seed] == WHITE:
                    output_arr[r, c_seed] = ORANGE

    # Convert back to list of lists for the required output format
    return output_arr.tolist()
```
