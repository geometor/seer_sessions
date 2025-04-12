
## train_1

**input:**
```
0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 4
0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 4 4 4 4 4 4 4
0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
7 0 7 0 7 0 7 0 7 0 7 0 7 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
7 0 7 0 7 0 7 0 7 0 7 0 7 0
0 0 0 0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 3 0 0 0 0
```


**output:**
```
3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 3 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 3 0 0 0 0
```

**Perception**

1.  **Input/Output Structure:** Both input and output are grids of colored pixels (represented by integers 0-9). White (0) acts as the background.
2.  **Key Elements:** The grids contain distinct types of non-background elements:
    *   A single "agent" pixel: This pixel seems to initiate the transformation. In the examples, it's often identified by being the only pixel of its color (yellow in train_1, red in train_3) or being spatially isolated from other pixels of the same color (the single orange pixel in train_2, distinct from the orange pixels in the top row).
    *   A set of "obstacle" pixels: These are the other non-background pixels. They seem to define boundaries or stopping points for the action initiated by the agent. They can form structures like lines (gray vertical line in train_1, orange horizontal line in train_2) or be scattered points (green diagonal points in train_3).
3.  **Transformation:** The core transformation is drawing a line segment originating from the agent pixel, using the agent pixel's color.
4.  **Line Direction:** The direction of the line appears determined by the agent's position relative to the grid boundaries. Agents near an edge or corner seem to draw lines moving away from that edge/corner (e.g., right edge -> move left, bottom edge -> move up, bottom-left corner -> move up-right).
5.  **Stopping Condition:** The line segment stops based on interaction with the obstacle pixels. The specific rule seems to depend on the arrangement of the obstacles:
    *   If obstacles form a solid line (like train_1, train_2), the drawn line stops exactly one pixel *before* reaching the row or column occupied by the obstacle line.
    *   If obstacles are scattered points (like train_3), the drawn line stops *at* the first pixel whose row OR column contains any obstacle pixel.

**Facts (YAML)**


```yaml
task_description: Draw a line from a single 'agent' pixel, using its color, until the line reaches a boundary defined by 'obstacle' pixels. The stopping rule depends on the obstacle configuration.

definitions:
  - name: background_pixel
    value: 0 # white
  - name: agent_pixel
    description: A unique non-background pixel, identified either by its unique color or spatial isolation.
    properties:
      - color: C
      - position: (r0, c0)
  - name: obstacle_pixels
    description: All non-background pixels excluding the agent pixel.
    properties:
      - positions: Set of (r, c) coordinates.
      - occupied_rows: R_O (Set of row indices containing obstacles).
      - occupied_cols: C_O (Set of column indices containing obstacles).
      - structure: Derived property, either 'solid_line' (if obstacles form a contiguous horizontal or vertical line) or 'scattered'.

parameters:
  - name: line_direction
    description: Vector (dr, dc) determined by agent position relative to grid boundaries.
    values:
      - (-1, 0) # Up
      - (1, 0)  # Down
      - (0, -1) # Left
      - (0, 1)  # Right
      - (-1, -1) # Up-Left
      - (-1, 1)  # Up-Right
      - (1, -1)  # Down-Left
      - (1, 1)   # Down-Right
    determination: Move away from the nearest grid edge/corner.

transformations:
  - step: Identify agent (C, (r0, c0)) and obstacles (O, R_O, C_O).
  - step: Classify obstacle structure ('solid_line' or 'scattered').
  - step: Determine line_direction (dr, dc).
  - step: Initialize current position (r, c) = (r0, c0).
  - step: Draw line segment based on obstacle structure:
      - if structure == 'solid_line':
          - Loop:
              - Calculate next position (nr, nc) = (r + dr, c + dc).
              - Check grid bounds for (nr, nc). If out, stop loop.
              - Check if (nr, nc) hits the obstacle line boundary (e.g., nr is in R_O if obstacle is horizontal line, nc is in C_O if obstacle is vertical line). If yes, stop loop.
              - If not stopped: color pixel (nr, nc) with C, update (r, c) = (nr, nc).
      - if structure == 'scattered':
          - Loop:
              - Calculate next position (nr, nc) = (r + dr, c + dc).
              - Check grid bounds for (nr, nc). If out, stop loop.
              - Check stop condition: Is row `nr` in R_O OR column `nc` in C_O?
              - If stop condition is TRUE: color pixel (nr, nc) with C, then stop loop.
              - If stop condition is FALSE: color pixel (nr, nc) with C, update (r, c) = (nr, nc).

output_grid: The input grid modified by coloring the pixels along the drawn line segment.
```


**Natural Language Program**

1.  Identify the agent pixel, which is the unique non-background pixel (either by color or spatial isolation). Note its color (C) and position (r0, c0).
2.  Identify all other non-background pixels as obstacles. Record the set of rows (R_O) and columns (C_O) they occupy.
3.  Analyze the obstacle positions to determine if they form a 'solid\_line' (horizontal or vertical) or are 'scattered'.
4.  Determine the drawing direction (dr, dc) by finding the nearest grid edge or corner to the agent pixel and selecting the direction moving away from it (e.g., if nearest is bottom-left corner, direction is up-right (-1, 1)).
5.  Initialize the current drawing position (r, c) to the agent's position (r0, c0).
6.  If the obstacle structure is 'solid\_line':
    *   Repeatedly calculate the next position (nr, nc) = (r + dr, c + dc).
    *   If (nr, nc) is outside the grid, stop drawing.
    *   If the obstacles form a horizontal line, check if the row `nr` is in R_O. If yes, stop drawing.
    *   If the obstacles form a vertical line, check if the column `nc` is in C_O. If yes, stop drawing.
    *   If not stopped, color the pixel at (nr, nc) with C, update (r, c) = (nr, nc), and repeat.
7.  If the obstacle structure is 'scattered':
    *   Repeatedly calculate the next position (nr, nc) = (r + dr, c + dc).
    *   If (nr, nc) is outside the grid, stop drawing.
    *   Check if the row `nr` is in R_O OR the column `nc` is in C_O.
    *   If this condition is TRUE, color the pixel at (nr, nc) with C, and then stop drawing.
    *   If this condition is FALSE, color the pixel at (nr, nc) with C, update (r, c) = (nr, nc), and repeat.
8.  Output the resulting grid.
```python
import numpy as np
from collections import Counter

"""
Transformation Rule Description:

The transformation identifies a single 'agent' pixel and multiple 'obstacle' pixels within the input grid. The agent pixel is determined first by checking for a non-background color that appears only once in the grid. If no such unique color exists, the agent is identified as the first non-background pixel found that is spatially isolated (has no neighbors of the same color). All other non-background pixels are considered obstacles.

Based on the agent pixel's position relative to the grid boundaries (specifically, the nearest edge or corner), a drawing direction (up, down, left, right, or diagonal) is determined, always moving away from that nearest boundary.

A line is then drawn starting from the agent's position, moving step-by-step in the determined direction, and coloring the pixels with the agent's color.

The stopping condition for the line depends on the spatial arrangement of the obstacle pixels:
1.  If all obstacle pixels lie entirely within a single row OR a single column ('solid_line' structure), the line stops *just before* drawing a pixel that would enter that obstacle row or column.
2.  If the obstacle pixels are dispersed across multiple rows and columns ('scattered' structure), the line stops *immediately after* drawing the first pixel whose row OR column contains any obstacle pixel.

The final output grid includes the newly drawn line segment.
"""

# Helper Functions

def find_non_background_pixels(grid: np.ndarray) -> list[tuple[int, int, int]]:
    """Finds all non-background (non-zero) pixels.

    Args:
        grid: The input numpy array representation of the grid.

    Returns:
        A list of tuples, where each tuple is (row, column, color).
    """
    pixels = []
    height, width = grid.shape
    for r in range(height):
        for c in range(width):
            if grid[r, c] != 0:
                pixels.append((r, c, int(grid[r, c])))
    return pixels

def get_neighbors(r: int, c: int, shape: tuple[int, int]) -> list[tuple[int, int]]:
    """Gets the coordinates of the 8 neighboring pixels (Moore neighborhood).

    Args:
        r: The row index of the center pixel.
        c: The column index of the center pixel.
        shape: A tuple (height, width) representing the grid dimensions.

    Returns:
        A list of (row, column) tuples for valid neighbors within grid bounds.
    """
    neighbors = []
    height, width = shape
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue # Skip self
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width:
                neighbors.append((nr, nc))
    return neighbors

def identify_agent_and_obstacles(grid: np.ndarray) -> tuple[tuple[int, int, int] | None, list[tuple[int, int, int]]]:
    """
    Identifies the agent pixel and obstacle pixels based on uniqueness rules.

    Agent criteria precedence:
    1. Pixel with a color that appears only once in the grid.
    2. If no unique color, the first spatially isolated pixel found
       (no neighbors of the same color).

    Args:
        grid: The input numpy array grid.

    Returns:
        A tuple containing:
        - agent_info: A tuple (row, col, color) for the agent, or None if no agent found.
        - obstacle_list: A list of (row, col, color) tuples for all obstacles.
    """
    non_bg_pixels = find_non_background_pixels(grid)
    if not non_bg_pixels:
        return None, []

    # Count color frequencies
    color_counts = Counter(p[2] for p in non_bg_pixels)
    unique_colors = [color for color, count in color_counts.items() if count == 1]

    agent_pixel_info = None
    obstacle_pixels = []

    # Criterion 1: Unique color
    if len(unique_colors) == 1:
        agent_color = unique_colors[0]
        for r, c, color in non_bg_pixels:
            if color == agent_color:
                agent_pixel_info = (r, c, color)
            else:
                obstacle_pixels.append((r, c, color))
        return agent_pixel_info, obstacle_pixels
    elif len(unique_colors) > 1:
         # Ambiguous case not present in examples, treat all as obstacles for now
         return None, non_bg_pixels


    # Criterion 2: Spatial isolation (if no unique color was found)
    if not agent_pixel_info:
        pixel_map = {(p[0], p[1]): p[2] for p in non_bg_pixels}
        for r, c, color in non_bg_pixels:
            is_isolated = True
            neighbors = get_neighbors(r, c, grid.shape)
            for nr, nc in neighbors:
                if pixel_map.get((nr, nc)) == color:
                    is_isolated = False
                    break
            if is_isolated:
                agent_pixel_info = (r, c, color)
                # Rebuild obstacle list excluding the found agent
                obstacle_pixels = [p for p in non_bg_pixels if (p[0], p[1]) != (r, c)]
                return agent_pixel_info, obstacle_pixels

    # If no agent identified by either criterion
    return None, non_bg_pixels


def get_obstacle_info(obstacle_pixels: list[tuple[int, int, int]]) -> tuple[set[int], set[int]]:
    """Extracts the sets of rows and columns occupied by obstacles.

    Args:
        obstacle_pixels: A list of (row, col, color) tuples for obstacles.

    Returns:
        A tuple containing (set_of_occupied_rows, set_of_occupied_columns).
    """
    occupied_rows = set(r for r, c, color in obstacle_pixels)
    occupied_cols = set(c for r, c, color in obstacle_pixels)
    return occupied_rows, occupied_cols

def classify_obstacle_structure(obstacle_pixels: list[tuple[int, int, int]]) -> str:
    """Classifies obstacle arrangement as 'solid_line' or 'scattered'.

    'solid_line' means all obstacles fall within a single row OR a single column.
    'scattered' means obstacles occupy multiple rows AND multiple columns.

    Args:
        obstacle_pixels: A list of (row, col, color) tuples for obstacles.

    Returns:
        'solid_line' or 'scattered'.
    """
    if not obstacle_pixels:
        return 'scattered' # Treat no obstacles as scattered for stopping logic

    occupied_rows, occupied_cols = get_obstacle_info(obstacle_pixels)

    # Check if all obstacles are confined to a single row or single column
    if len(occupied_rows) == 1 or len(occupied_cols) == 1:
        return 'solid_line'
    else:
        return 'scattered'

def determine_direction(agent_pos: tuple[int, int], grid_shape: tuple[int, int]) -> tuple[int, int]:
    """Determines the drawing direction (dr, dc) away from the nearest grid edge/corner.

    Args:
        agent_pos: A tuple (row, col) of the agent's position.
        grid_shape: A tuple (height, width) of the grid dimensions.

    Returns:
        A tuple (dr, dc) representing the change in row and column for the next step.
        Example: (-1, 0) is Up, (1, 1) is Down-Right.
    """
    r, c = agent_pos
    h, w = grid_shape

    # Calculate distances to edges
    dist_top = r
    dist_bottom = h - 1 - r
    dist_left = c
    dist_right = w - 1 - c

    # Find the minimum distance to any edge
    min_dist = min(dist_top, dist_bottom, dist_left, dist_right)

    # Determine direction components (move away from the closest edge)
    dr, dc = 0, 0
    if dist_top == min_dist:
        dr = 1  # Move Down
    if dist_bottom == min_dist:
        dr = -1 # Move Up
    if dist_left == min_dist:
        dc = 1  # Move Right
    if dist_right == min_dist:
        dc = -1 # Move Left

    # Adjust if multiple edges are equidistant (corners / exact centers)
    # If tied for closest vertical edge, dr might be +/-1. If tied for horizontal, dc might be +/-1.
    # If tied between a vertical and horizontal edge (corner case):
    is_top = dist_top == min_dist
    is_bottom = dist_bottom == min_dist
    is_left = dist_left == min_dist
    is_right = dist_right == min_dist

    # Explicitly set corner directions
    if is_top and is_left: dr, dc = 1, 1      # Away from Top-Left
    elif is_top and is_right: dr, dc = 1, -1     # Away from Top-Right
    elif is_bottom and is_left: dr, dc = -1, 1    # Away from Bottom-Left
    elif is_bottom and is_right: dr, dc = -1, -1   # Away from Bottom-Right
    # If tied top/bottom or left/right, the individual assignments above handle it.
    # e.g., if tied top/bottom only, dr might be set twice, ending as -1 (up).
    # e.g., if tied left/right only, dc might be set twice, ending as -1 (left).
    # Let's rethink the tie logic slightly: set direction based on *first* hit minimum.
    dr_final, dc_final = 0, 0
    if dist_top == min_dist: dr_final = 1
    elif dist_bottom == min_dist: dr_final = -1

    if dist_left == min_dist: dc_final = 1
    elif dist_right == min_dist: dc_final = -1

    # Ensure diagonals are captured if both vertical and horizontal are min_dist
    if (is_top or is_bottom) and (is_left or is_right):
         # Use the individually determined components
         dr, dc = dr_final, dc_final
    elif is_top or is_bottom: # Only vertical edge is closest
         dr, dc = dr_final, 0
    elif is_left or is_right: # Only horizontal edge is closest
         dr, dc = 0, dc_final
    # If agent is perfectly centered and h,w > 1, min_dist > 0.
    # This logic might result in (0,0) if perfectly centered. Add default.
    if dr == 0 and dc == 0 and (h > 1 or w > 1):
         # Default: try moving away from top-left? (arbitrary consistent choice)
         if h > 1 : dr = 1
         if w > 1 : dc = 1
         if dr == 0 and dc == 0 : # if h=1 and w=1
             pass # direction remains (0,0)

    return dr, dc

# Main Transformation Function

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the described transformation to the input grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Initialize grid using numpy for easier manipulation
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy()
    h, w = grid.shape

    # --- Step 1: Identify agent and obstacles ---
    agent_info, obstacles = identify_agent_and_obstacles(grid)

    # If no agent identified, return the original grid
    if agent_info is None:
        return input_grid

    agent_r, agent_c, agent_color = agent_info

    # --- Step 2: Get obstacle information ---
    obstacle_rows, obstacle_cols = get_obstacle_info(obstacles)

    # --- Step 3: Classify obstacle structure ---
    structure = classify_obstacle_structure(obstacles)

    # --- Step 4: Determine drawing direction ---
    dr, dc = determine_direction((agent_r, agent_c), (h, w))

    # If direction is (0,0) (e.g., 1x1 grid or error), no drawing needed
    if dr == 0 and dc == 0:
        return input_grid

    # --- Step 5 & 6/7: Draw line with appropriate stopping condition ---
    curr_r, curr_c = agent_r, agent_c

    while True:
        # Calculate the *next* potential position
        next_r, next_c = curr_r + dr, curr_c + dc

        # Check if next position is within grid bounds
        if not (0 <= next_r < h and 0 <= next_c < w):
            break # Stop drawing if out of bounds

        # Check stopping conditions based on obstacle structure
        stop_drawing = False
        if structure == 'solid_line':
            # Stop *before* drawing on the obstacle row/column
            if dr != 0 and next_r in obstacle_rows: # Moving vertically into obstacle row
                 stop_drawing = True
            elif dc != 0 and next_c in obstacle_cols: # Moving horizontally into obstacle col
                 stop_drawing = True
            # Handle diagonal moves towards a line (stop if either row or col matches)
            elif dr != 0 and dc != 0 and (next_r in obstacle_rows or next_c in obstacle_cols):
                 stop_drawing = True

            if stop_drawing:
                break # Break before coloring next_r, next_c

        elif structure == 'scattered':
            # Stop *after* drawing on the first row/column that contains an obstacle
            if next_r in obstacle_rows or next_c in obstacle_cols:
                output_grid[next_r, next_c] = agent_color # Color the stopping pixel
                stop_drawing = True                     # Set flag to break after coloring
                # Note: coloring happens below if not stopping yet

        # If we determined to stop *before* coloring (solid_line case hit), exit loop
        # (Already handled by the 'break' inside the 'solid_line' block)

        # Color the next pixel if we haven't decided to stop yet
        if not stop_drawing:
             output_grid[next_r, next_c] = agent_color

        # If we determined to stop *after* coloring (scattered case hit), exit loop now
        if stop_drawing and structure == 'scattered':
            break

        # Update current position for the next iteration
        curr_r, curr_c = next_r, next_c

    # --- Step 8: Return the modified grid ---
    return output_grid.tolist()
```
