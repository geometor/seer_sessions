
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

Previous Code:
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
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
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
Expected Output:
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
Transformed Output:
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
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0.0

## Example 2:
Input:
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
Expected Output:
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
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
7 7 7 0 7 0 7 0 7 0 7 0 7 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 6
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 9.523809523809547

## Example 3:
Input:
```
3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 3 0 0 0 0
```
Expected Output:
```
3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 3 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 3 0 0 0 0
```
Transformed Output:
```
3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 3 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 3 0 0 0 0
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0.0
**General Assessment**

The initial analysis correctly identified the core mechanism (drawing a line from an agent pixel) and the two distinct stopping behaviors ('solid_line' vs 'scattered'). However, the code failed on `train_2`, revealing an issue in the agent identification logic. The initial logic prioritized unique color, then spatial isolation, but incorrectly handled the case in `train_2` where multiple pixels of the same color were spatially isolated.

The `code_output` from the metric gathering confirms this. The refined identification logic (unique color -> unique isolation) still failed on `train_2` because multiple pixels were isolated. This necessitates a revised hypothesis for agent identification.

**Strategy for Resolution**

The new hypothesis prioritizes structural patterns:
1.  Look for a dominant line structure (multiple pixels of the same color in a single row or column). If found, these are the obstacles, and the single remaining non-background pixel (if one exists) is the agent.
2.  If the above doesn't apply, revert to the previous logic: unique color identifies the agent.
3.  If neither applies, unique spatial isolation identifies the agent.
4.  All non-agent, non-background pixels become obstacles.

This strategy correctly identifies the agent and obstacles in all three training examples:
*   `train_1`: Unique color (yellow) identifies agent. Gray pixels form a line and are obstacles. Fits both rules.
*   `train_2`: Orange pixels in row 1 form a line (obstacles). Single remaining orange pixel (7,8) is the agent. Fits the new primary rule.
*   `train_3`: Unique color (red) identifies agent. Green pixels are scattered obstacles. Fits the secondary rule.

The drawing direction and stopping logic based on 'solid_line' vs 'scattered' obstacles seem correct and do not need revision based on the analysis.

**Metrics Analysis**

Based on the refined understanding ("line structure first" or "unique characteristic"):

*   **train_1:**
    *   Agent Identification: Yellow (4) at (5, 11) identified by unique color.
    *   Obstacles: Gray (5) pixels at (0,1), (2,1), (4,1), (6,1), (8,1), (10,1).
    *   Structure: `solid_line` (all obstacles in column 1).
    *   Agent Location: Near right edge (row 5, col 11 in 12x12).
    *   Direction: Away from right edge -> Left (0, -1).
    *   Stopping Rule: Stop before column 1.
    *   Result: Correct.

*   **train_2:**
    *   Agent Identification: Orange (7) pixels in row 1 form a line structure. The single other orange pixel at (7, 8) is the agent.
    *   Obstacles: Orange (7) pixels at (1,0), (1,2), (1,4), (1,6), (1,8), (1,10), (1,12).
    *   Structure: `solid_line` (all obstacles in row 1).
    *   Agent Location: Near bottom edge (row 7, col 8 in 9x14).
    *   Direction: Away from bottom edge -> Up (-1, 0).
    *   Stopping Rule: Stop before row 1.
    *   Result: Initial code failed due to incorrect agent ID. Refined logic should work.

*   **train_3:**
    *   Agent Identification: Red (2) at (6, 0) identified by unique color.
    *   Obstacles: Green (3) pixels at (0,0), (2,2), (4,4), (6,6).
    *   Structure: `scattered` (obstacles in multiple rows and columns).
    *   Agent Location: Near bottom-left corner (row 6, col 0 in 7x11).
    *   Direction: Away from bottom-left -> Up-Right (-1, 1).
    *   Stopping Rule: Stop after drawing on first pixel whose row OR column contains an obstacle.
    *   Result: Correct.

**Facts (YAML)**


```yaml
task_description: Draw a line from a single 'agent' pixel, using its color, until the line reaches a boundary defined by 'obstacle' pixels. The agent is identified primarily by being separate from a line structure, or secondarily by color/isolation uniqueness. The stopping rule depends on the obstacle configuration.

definitions:
  - name: background_pixel
    value: 0 # white
  - name: non_background_pixels
    description: All pixels with color != 0.
    properties:
      - positions: List of (r, c, color) tuples.
  - name: line_structure_pixels
    description: The largest set of non-background pixels sharing the same color AND lying on a single row OR single column. Can be empty.
  - name: agent_pixel
    description: The single pixel initiating the line draw. Identified via prioritized rules.
    properties:
      - color: C
      - position: (r0, c0)
    identification_rules: # Priority Order
      - 1: If line_structure_pixels exist AND exactly one non-background pixel remains outside this structure, that remaining pixel is the agent.
      - 2: If rule 1 doesn't apply, find pixels with a color appearing only once grid-wide. If exactly one such pixel exists, it's the agent.
      - 3: If rules 1 & 2 don't apply, find pixels with no neighbors (Moore neighborhood) of the same color. If exactly one such pixel exists, it's the agent.
      - 4: Otherwise, no agent is identified.
  - name: obstacle_pixels
    description: All non-background pixels excluding the identified agent pixel.
    properties:
      - positions: Set of (r, c) coordinates.
      - occupied_rows: R_O (Set of row indices containing obstacles).
      - occupied_cols: C_O (Set of column indices containing obstacles).
      - structure: Derived property, either 'solid_line' (if obstacles occupy only one row OR only one column) or 'scattered'.

parameters:
  - name: line_direction
    description: Vector (dr, dc) determined by agent position relative to grid boundaries.
    values: # Examples
      - (-1, 0) # Up
      - (1, 0)  # Down
      - (0, -1) # Left
      - (0, 1)  # Right
      - (-1, 1) # Up-Right
    determination: Move away from the nearest grid edge/corner. Ties favor Up/Left components.

transformations:
  - step: Identify all non_background_pixels.
  - step: Attempt to identify agent using rule 1 (line structure separation).
  - step: If no agent yet, attempt using rule 2 (unique color).
  - step: If no agent yet, attempt using rule 3 (unique spatial isolation).
  - step: If an agent (C, (r0, c0)) was identified, define all other non-background pixels as obstacles. If no agent, stop.
  - step: Analyze obstacles to determine structure ('solid_line' or 'scattered') and get occupied rows (R_O) and columns (C_O).
  - step: Determine line_direction (dr, dc) based on agent position (r0, c0) and grid dimensions.
  - step: Initialize current position (r, c) = (r0, c0).
  - step: Draw line segment based on obstacle structure:
      - if structure == 'solid_line':
          - Loop:
              - Calculate next position (nr, nc) = (r + dr, c + dc).
              - Check grid bounds for (nr, nc). If out, stop loop.
              - Check if (nr, nc) hits the obstacle boundary (nr in R_O or nc in C_O). If yes, stop loop.
              - If not stopped: color pixel (nr, nc) with C, update (r, c) = (nr, nc).
      - if structure == 'scattered':
          - Loop:
              - Calculate next position (nr, nc) = (r + dr, c + dc).
              - Check grid bounds for (nr, nc). If out, stop loop.
              - Check stop condition: Is row `nr` in R_O OR column `nc` in C_O?
              - If stop condition is TRUE: color pixel (nr, nc) with C, then stop loop.
              - If stop condition is FALSE: color pixel (nr, nc) with C, update (r, c) = (nr, nc).

output_grid: The input grid modified by coloring the pixels along the drawn line segment. If no agent was identified, the output is identical to the input.
```


**Natural Language Program**

1.  Find all non-background pixels in the input grid. If none exist, return the input grid.
2.  **Identify the Agent:**
    *   a. Check if there's a set of pixels forming the largest possible line (sharing the same color and all in the same single row or same single column).
    *   b. If such a line structure exists and there is *exactly one* other non-background pixel remaining, designate that single pixel as the **agent**.
    *   c. If step (b) did not identify an agent, check if there is *exactly one* pixel whose color is unique across the entire grid. If so, designate that pixel as the **agent**.
    *   d. If steps (b) and (c) did not identify an agent, check if there is *exactly one* pixel that has no neighbors (including diagonals) of the same color. If so, designate that pixel as the **agent**.
    *   e. If no agent was identified by steps (b), (c), or (d), return the input grid unchanged.
3.  Designate all non-background pixels that are *not* the agent as **obstacles**. Note the agent's color (C) and position (r0, c0).
4.  Analyze the obstacle positions: Determine if they occupy only a single row OR a single column (structure is 'solid\_line'), or if they occupy multiple rows AND columns (structure is 'scattered'). Record the set of rows (R\_O) and columns (C\_O) occupied by any obstacle.
5.  Determine the drawing direction (dr, dc) based on the agent's position (r0, c0). The direction moves away from the nearest grid edge or corner. (e.g., nearest = bottom-left corner -> direction = up-right (-1, 1)).
6.  Initialize the current drawing position (r, c) to the agent's position (r0, c0).
7.  **Draw the Line:**
    *   Repeatedly calculate the next potential position (nr, nc) = (r + dr, c + dc).
    *   Stop drawing if (nr, nc) is outside the grid boundaries.
    *   **If the obstacle structure is 'solid\_line':**
        *   Check if the next position (nr, nc) would fall into a row present in R\_O or a column present in C\_O.
        *   If YES, stop drawing *before* coloring (nr, nc).
        *   If NO, color the pixel at (nr, nc) with the agent's color C, update (r, c) = (nr, nc), and continue the loop.
    *   **If the obstacle structure is 'scattered':**
        *   Check if the next position's row `nr` is in R\_O OR its column `nc` is in C\_O.
        *   If YES, color the pixel at (nr, nc) with C, and then stop drawing *after* coloring this pixel.
        *   If NO, color the pixel at (nr, nc) with C, update (r, c) = (nr, nc), and continue the loop.
8.  Output the resulting grid.
```python
import numpy as np
from collections import Counter, defaultdict

"""
Transformation Rule Description:

The transformation identifies a single 'agent' pixel and multiple 'obstacle' pixels within the input grid. The agent pixel is identified using a prioritized set of rules:
1.  Structural Separation: If the largest group of same-colored pixels forming a line (horizontal or vertical) can be identified, and there is exactly one other non-background pixel remaining, that single remaining pixel is the agent.
2.  Unique Color: If rule 1 doesn't apply, if there's exactly one pixel whose color appears only once in the entire grid, that pixel is the agent.
3.  Unique Spatial Isolation: If rules 1 and 2 don't apply, if there's exactly one non-background pixel with no neighbors (Moore neighborhood) of the same color, that pixel is the agent.
If no agent is identified, the grid remains unchanged.

All non-background pixels that are not the agent are considered 'obstacles'.

Based on the agent pixel's position relative to the grid boundaries (specifically, the nearest edge or corner), a drawing direction (up, down, left, right, or diagonal) is determined, always moving away from that nearest boundary.

A line is then drawn starting one step away from the agent's position, moving step-by-step in the determined direction, and coloring the pixels with the agent's color.

The stopping condition for the line depends on the spatial arrangement of the obstacle pixels:
1.  Solid Line Obstacles: If all obstacle pixels lie entirely within a single row OR a single column ('solid_line' structure), the line stops *just before* drawing a pixel that would enter that obstacle row or column.
2.  Scattered Obstacles: If the obstacle pixels are dispersed across multiple rows and columns ('scattered' structure), the line stops *immediately after* drawing the first pixel whose row OR column contains any obstacle pixel.

The final output grid includes the newly drawn line segment.
"""

# Imports
import numpy as np
from collections import Counter, defaultdict

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

def find_largest_line_structure(non_bg_pixels: list[tuple[int, int, int]]) -> list[tuple[int, int, int]]:
    """Finds the largest group of same-colored pixels in a single row or column.

    Args:
        non_bg_pixels: List of (r, c, color) tuples for all non-background pixels.

    Returns:
        A list of (r, c, color) tuples representing the pixels in the largest line found,
        or an empty list if no line structure (at least 2 pixels) is found or multiple
        lines have the same maximum size.
    """
    if not non_bg_pixels:
        return []

    pixels_by_color = defaultdict(list)
    for r, c, color in non_bg_pixels:
        pixels_by_color[color].append((r, c, color))

    largest_line = []
    max_len = 0

    for color, pixels in pixels_by_color.items():
        if len(pixels) < 2: # A line needs at least 2 points
            continue

        rows = set(r for r, c, _ in pixels)
        cols = set(c for r, c, _ in pixels)

        # Check for horizontal line
        if len(rows) == 1:
            if len(pixels) > max_len:
                max_len = len(pixels)
                largest_line = pixels
            elif len(pixels) == max_len:
                 # Tie case - invalidate by returning empty? Or pick first? Let's invalidate for now.
                 # If ties are allowed, this might need adjusting based on examples.
                 # For now, assume a unique largest line is required for Rule 1.
                 # Revisit if examples contradict this. Let's stick with picking the first for now.
                 # If we stick with the first, the condition 'len(pixels) > max_len' handles it.
                 pass


        # Check for vertical line
        elif len(cols) == 1: # Use elif to avoid counting grids of single points as both
            if len(pixels) > max_len:
                max_len = len(pixels)
                largest_line = pixels
            elif len(pixels) == max_len:
                 # Tie case - see above comment.
                 pass

    # Return only if a line structure was found (max_len >= 2)
    return largest_line if max_len >= 2 else []


def identify_agent_and_obstacles_refined(grid: np.ndarray) -> tuple[tuple[int, int, int] | None, list[tuple[int, int, int]]]:
    """
    Identifies the agent pixel and obstacle pixels using refined, prioritized rules.

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

    agent_pixel_info = None
    obstacle_pixels = []
    non_bg_pixel_set = set((p[0], p[1]) for p in non_bg_pixels) # For quick lookup

    # Rule 1: Structural Separation
    line_pixels = find_largest_line_structure(non_bg_pixels)
    if line_pixels:
        line_pixel_coords = set((p[0], p[1]) for p in line_pixels)
        potential_agent_coords = non_bg_pixel_set - line_pixel_coords
        if len(potential_agent_coords) == 1:
            agent_coord = potential_agent_coords.pop()
            # Find the full agent info (r, c, color)
            for r, c, color in non_bg_pixels:
                if (r, c) == agent_coord:
                    agent_pixel_info = (r, c, color)
                    break
            obstacle_pixels = line_pixels # Obstacles are the line pixels
            return agent_pixel_info, obstacle_pixels

    # Rule 2: Unique Color
    if not agent_pixel_info:
        color_counts = Counter(p[2] for p in non_bg_pixels)
        unique_colors = [color for color, count in color_counts.items() if count == 1]
        if len(unique_colors) == 1:
            agent_color = unique_colors[0]
            temp_obstacles = []
            for r, c, color in non_bg_pixels:
                if color == agent_color:
                    agent_pixel_info = (r, c, color)
                else:
                    temp_obstacles.append((r, c, color))
            obstacle_pixels = temp_obstacles
            return agent_pixel_info, obstacle_pixels

    # Rule 3: Unique Spatial Isolation
    if not agent_pixel_info:
        isolated_pixels = []
        pixel_map = {(p[0], p[1]): p[2] for p in non_bg_pixels}
        for r, c, color in non_bg_pixels:
            is_isolated = True
            neighbors = get_neighbors(r, c, grid.shape)
            for nr, nc in neighbors:
                if pixel_map.get((nr, nc)) == color:
                    is_isolated = False
                    break
            if is_isolated:
                isolated_pixels.append((r, c, color))

        if len(isolated_pixels) == 1:
            agent_pixel_info = isolated_pixels[0]
            # Rebuild obstacle list excluding the found agent
            obstacle_pixels = [p for p in non_bg_pixels if (p[0], p[1]) != (agent_pixel_info[0], agent_pixel_info[1])]
            return agent_pixel_info, obstacle_pixels

    # If no agent identified by any rule
    # Assign obstacles as all non-bg pixels if no agent found.
    # This ensures obstacle info is available even if drawing doesn't happen.
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
    if len(occupied_rows) <= 1 or len(occupied_cols) <= 1: # Allow single point "lines"
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

    # Handle 1x1 grid case
    if h == 1 and w == 1:
        return (0, 0)

    # Calculate distances to edges
    dist_top = r
    dist_bottom = h - 1 - r
    dist_left = c
    dist_right = w - 1 - c

    # Find the minimum distance to any edge
    min_dist = min(dist_top, dist_bottom, dist_left, dist_right)

    # Determine potential directions (away from closest edges)
    dr, dc = 0, 0
    if dist_top == min_dist:
        dr = 1  # Move Down (away from top)
    if dist_bottom == min_dist:
        # If dr is already 1 (meaning top was also min_dist), bottom wins (move Up)
        dr = -1 # Move Up (away from bottom)
    if dist_left == min_dist:
        dc = 1  # Move Right (away from left)
    if dist_right == min_dist:
        # If dc is already 1 (meaning left was also min_dist), right wins (move Left)
        dc = -1 # Move Left (away from right)

    # Check if exactly centered in one dimension (e.g., r = (h-1)/2)
    # If centered vertically and only vertical edges are minimal
    if h > 1 and dist_top == dist_bottom == min_dist and dist_left > min_dist and dist_right > min_dist:
         dr = -1 # Prioritize Up if centered vertically
         dc = 0
    # If centered horizontally and only horizontal edges are minimal
    elif w > 1 and dist_left == dist_right == min_dist and dist_top > min_dist and dist_bottom > min_dist:
         dc = -1 # Prioritize Left if centered horizontally
         dr = 0
    # If perfectly centered in both dimensions (and grid > 1x1)
    elif h > 1 and w > 1 and dist_top == dist_bottom == dist_left == dist_right == min_dist:
         dr, dc = -1, -1 # Prioritize Up-Left if perfectly centered

    # Ensure direction is non-zero if grid > 1x1 (should be covered above, but as fallback)
    if dr == 0 and dc == 0 and (h > 1 or w > 1):
        # Default: move away from top-left corner
        if dist_top <= dist_bottom: dr = 1
        else: dr = -1
        if dist_left <= dist_right: dc = 1
        else: dc = -1

    return dr, dc


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

    # --- Step 1-3: Identify agent and obstacles using refined rules ---
    agent_info, obstacles = identify_agent_and_obstacles_refined(grid)

    # If no agent identified, return the original grid
    if agent_info is None:
        return input_grid # Return as list of lists

    agent_r, agent_c, agent_color = agent_info

    # --- Step 4: Get obstacle information and classify structure ---
    obstacle_rows, obstacle_cols = get_obstacle_info(obstacles)
    structure = classify_obstacle_structure(obstacles)

    # --- Step 5: Determine drawing direction ---
    dr, dc = determine_direction((agent_r, agent_c), (h, w))

    # If direction is (0,0) (e.g., 1x1 grid), no drawing needed
    if dr == 0 and dc == 0:
        return output_grid.tolist() # Return current grid as list of lists

    # --- Step 6 & 7: Draw line with appropriate stopping condition ---
    curr_r, curr_c = agent_r, agent_c

    while True:
        # Calculate the *next* potential position
        next_r, next_c = curr_r + dr, curr_c + dc

        # Check if next position is within grid bounds
        if not (0 <= next_r < h and 0 <= next_c < w):
            break # Stop drawing if out of bounds

        # Check stopping conditions based on obstacle structure
        stop_drawing_after_color = False
        stop_drawing_before_color = False

        if structure == 'solid_line':
            # Stop *before* drawing on the obstacle row/column
            if next_r in obstacle_rows or next_c in obstacle_cols:
                 stop_drawing_before_color = True

            if stop_drawing_before_color:
                break # Break before coloring next_r, next_c

        elif structure == 'scattered':
            # Stop *after* drawing on the first row/column that contains an obstacle
            if next_r in obstacle_rows or next_c in obstacle_cols:
                stop_drawing_after_color = True
                # Action: Color this pixel, then stop.

        # Color the next pixel (unless stopping before coloring)
        output_grid[next_r, next_c] = agent_color

        # If we determined to stop *after* coloring (scattered case hit), exit loop now
        if stop_drawing_after_color:
            break

        # Update current position for the next iteration
        curr_r, curr_c = next_r, next_c

    # --- Step 8: Return the modified grid ---
    return output_grid.tolist()
```

Previous Code:
```python
import numpy as np
from collections import Counter, defaultdict

"""
Transformation Rule Description:

The transformation identifies a single 'agent' pixel and multiple 'obstacle' pixels within the input grid. The agent pixel is identified using a prioritized set of rules:
1.  Structural Separation: If the largest group of same-colored pixels forming a line (horizontal or vertical) can be identified, and there is exactly one other non-background pixel remaining, that single remaining pixel is the agent.
2.  Unique Color: If rule 1 doesn't apply, if there's exactly one pixel whose color appears only once in the entire grid, that pixel is the agent.
3.  Unique Spatial Isolation: If rules 1 and 2 don't apply, if there's exactly one non-background pixel with no neighbors (Moore neighborhood) of the same color, that pixel is the agent.
If no agent is identified, the grid remains unchanged.

All non-background pixels that are not the agent are considered 'obstacles'.

Based on the agent pixel's position relative to the grid boundaries (specifically, the nearest edge or corner), a drawing direction (up, down, left, right, or diagonal) is determined, always moving away from that nearest boundary.

A line is then drawn starting one step away from the agent's position, moving step-by-step in the determined direction, and coloring the pixels with the agent's color.

The stopping condition for the line depends on the spatial arrangement of the obstacle pixels:
1.  Solid Line Obstacles: If all obstacle pixels lie entirely within a single row OR a single column ('solid_line' structure), the line stops *just before* drawing a pixel that would enter that obstacle row or column.
2.  Scattered Obstacles: If the obstacle pixels are dispersed across multiple rows and columns ('scattered' structure), the line stops *immediately after* drawing the first pixel whose row OR column contains any obstacle pixel.

The final output grid includes the newly drawn line segment.
"""

# Imports
import numpy as np
from collections import Counter, defaultdict

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

def find_largest_line_structure(non_bg_pixels: list[tuple[int, int, int]]) -> list[tuple[int, int, int]]:
    """Finds the largest group of same-colored pixels in a single row or column.

    Args:
        non_bg_pixels: List of (r, c, color) tuples for all non-background pixels.

    Returns:
        A list of (r, c, color) tuples representing the pixels in the largest line found,
        or an empty list if no line structure (at least 2 pixels) is found or multiple
        lines have the same maximum size.
    """
    if not non_bg_pixels:
        return []

    pixels_by_color = defaultdict(list)
    for r, c, color in non_bg_pixels:
        pixels_by_color[color].append((r, c, color))

    largest_line = []
    max_len = 0

    for color, pixels in pixels_by_color.items():
        if len(pixels) < 2: # A line needs at least 2 points
            continue

        rows = set(r for r, c, _ in pixels)
        cols = set(c for r, c, _ in pixels)

        # Check for horizontal line
        if len(rows) == 1:
            if len(pixels) > max_len:
                max_len = len(pixels)
                largest_line = pixels
            elif len(pixels) == max_len:
                 # Tie case - invalidate by returning empty? Or pick first? Let's invalidate for now.
                 # If ties are allowed, this might need adjusting based on examples.
                 # For now, assume a unique largest line is required for Rule 1.
                 # Revisit if examples contradict this. Let's stick with picking the first for now.
                 # If we stick with the first, the condition 'len(pixels) > max_len' handles it.
                 pass


        # Check for vertical line
        elif len(cols) == 1: # Use elif to avoid counting grids of single points as both
            if len(pixels) > max_len:
                max_len = len(pixels)
                largest_line = pixels
            elif len(pixels) == max_len:
                 # Tie case - see above comment.
                 pass

    # Return only if a line structure was found (max_len >= 2)
    return largest_line if max_len >= 2 else []


def identify_agent_and_obstacles_refined(grid: np.ndarray) -> tuple[tuple[int, int, int] | None, list[tuple[int, int, int]]]:
    """
    Identifies the agent pixel and obstacle pixels using refined, prioritized rules.

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

    agent_pixel_info = None
    obstacle_pixels = []
    non_bg_pixel_set = set((p[0], p[1]) for p in non_bg_pixels) # For quick lookup

    # Rule 1: Structural Separation
    line_pixels = find_largest_line_structure(non_bg_pixels)
    if line_pixels:
        line_pixel_coords = set((p[0], p[1]) for p in line_pixels)
        potential_agent_coords = non_bg_pixel_set - line_pixel_coords
        if len(potential_agent_coords) == 1:
            agent_coord = potential_agent_coords.pop()
            # Find the full agent info (r, c, color)
            for r, c, color in non_bg_pixels:
                if (r, c) == agent_coord:
                    agent_pixel_info = (r, c, color)
                    break
            obstacle_pixels = line_pixels # Obstacles are the line pixels
            return agent_pixel_info, obstacle_pixels

    # Rule 2: Unique Color
    if not agent_pixel_info:
        color_counts = Counter(p[2] for p in non_bg_pixels)
        unique_colors = [color for color, count in color_counts.items() if count == 1]
        if len(unique_colors) == 1:
            agent_color = unique_colors[0]
            temp_obstacles = []
            for r, c, color in non_bg_pixels:
                if color == agent_color:
                    agent_pixel_info = (r, c, color)
                else:
                    temp_obstacles.append((r, c, color))
            obstacle_pixels = temp_obstacles
            return agent_pixel_info, obstacle_pixels

    # Rule 3: Unique Spatial Isolation
    if not agent_pixel_info:
        isolated_pixels = []
        pixel_map = {(p[0], p[1]): p[2] for p in non_bg_pixels}
        for r, c, color in non_bg_pixels:
            is_isolated = True
            neighbors = get_neighbors(r, c, grid.shape)
            for nr, nc in neighbors:
                if pixel_map.get((nr, nc)) == color:
                    is_isolated = False
                    break
            if is_isolated:
                isolated_pixels.append((r, c, color))

        if len(isolated_pixels) == 1:
            agent_pixel_info = isolated_pixels[0]
            # Rebuild obstacle list excluding the found agent
            obstacle_pixels = [p for p in non_bg_pixels if (p[0], p[1]) != (agent_pixel_info[0], agent_pixel_info[1])]
            return agent_pixel_info, obstacle_pixels

    # If no agent identified by any rule
    # Assign obstacles as all non-bg pixels if no agent found.
    # This ensures obstacle info is available even if drawing doesn't happen.
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
    if len(occupied_rows) <= 1 or len(occupied_cols) <= 1: # Allow single point "lines"
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

    # Handle 1x1 grid case
    if h == 1 and w == 1:
        return (0, 0)

    # Calculate distances to edges
    dist_top = r
    dist_bottom = h - 1 - r
    dist_left = c
    dist_right = w - 1 - c

    # Find the minimum distance to any edge
    min_dist = min(dist_top, dist_bottom, dist_left, dist_right)

    # Determine potential directions (away from closest edges)
    dr, dc = 0, 0
    if dist_top == min_dist:
        dr = 1  # Move Down (away from top)
    if dist_bottom == min_dist:
        # If dr is already 1 (meaning top was also min_dist), bottom wins (move Up)
        dr = -1 # Move Up (away from bottom)
    if dist_left == min_dist:
        dc = 1  # Move Right (away from left)
    if dist_right == min_dist:
        # If dc is already 1 (meaning left was also min_dist), right wins (move Left)
        dc = -1 # Move Left (away from right)

    # Check if exactly centered in one dimension (e.g., r = (h-1)/2)
    # If centered vertically and only vertical edges are minimal
    if h > 1 and dist_top == dist_bottom == min_dist and dist_left > min_dist and dist_right > min_dist:
         dr = -1 # Prioritize Up if centered vertically
         dc = 0
    # If centered horizontally and only horizontal edges are minimal
    elif w > 1 and dist_left == dist_right == min_dist and dist_top > min_dist and dist_bottom > min_dist:
         dc = -1 # Prioritize Left if centered horizontally
         dr = 0
    # If perfectly centered in both dimensions (and grid > 1x1)
    elif h > 1 and w > 1 and dist_top == dist_bottom == dist_left == dist_right == min_dist:
         dr, dc = -1, -1 # Prioritize Up-Left if perfectly centered

    # Ensure direction is non-zero if grid > 1x1 (should be covered above, but as fallback)
    if dr == 0 and dc == 0 and (h > 1 or w > 1):
        # Default: move away from top-left corner
        if dist_top <= dist_bottom: dr = 1
        else: dr = -1
        if dist_left <= dist_right: dc = 1
        else: dc = -1

    return dr, dc


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

    # --- Step 1-3: Identify agent and obstacles using refined rules ---
    agent_info, obstacles = identify_agent_and_obstacles_refined(grid)

    # If no agent identified, return the original grid
    if agent_info is None:
        return input_grid # Return as list of lists

    agent_r, agent_c, agent_color = agent_info

    # --- Step 4: Get obstacle information and classify structure ---
    obstacle_rows, obstacle_cols = get_obstacle_info(obstacles)
    structure = classify_obstacle_structure(obstacles)

    # --- Step 5: Determine drawing direction ---
    dr, dc = determine_direction((agent_r, agent_c), (h, w))

    # If direction is (0,0) (e.g., 1x1 grid), no drawing needed
    if dr == 0 and dc == 0:
        return output_grid.tolist() # Return current grid as list of lists

    # --- Step 6 & 7: Draw line with appropriate stopping condition ---
    curr_r, curr_c = agent_r, agent_c

    while True:
        # Calculate the *next* potential position
        next_r, next_c = curr_r + dr, curr_c + dc

        # Check if next position is within grid bounds
        if not (0 <= next_r < h and 0 <= next_c < w):
            break # Stop drawing if out of bounds

        # Check stopping conditions based on obstacle structure
        stop_drawing_after_color = False
        stop_drawing_before_color = False

        if structure == 'solid_line':
            # Stop *before* drawing on the obstacle row/column
            if next_r in obstacle_rows or next_c in obstacle_cols:
                 stop_drawing_before_color = True

            if stop_drawing_before_color:
                break # Break before coloring next_r, next_c

        elif structure == 'scattered':
            # Stop *after* drawing on the first row/column that contains an obstacle
            if next_r in obstacle_rows or next_c in obstacle_cols:
                stop_drawing_after_color = True
                # Action: Color this pixel, then stop.

        # Color the next pixel (unless stopping before coloring)
        output_grid[next_r, next_c] = agent_color

        # If we determined to stop *after* coloring (scattered case hit), exit loop now
        if stop_drawing_after_color:
            break

        # Update current position for the next iteration
        curr_r, curr_c = next_r, next_c

    # --- Step 8: Return the modified grid ---
    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
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
Expected Output:
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
Transformed Output:
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
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0.0

## Example 2:
Input:
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
Expected Output:
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
Transformed Output:
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
Match: False
Pixels Off: 5
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 7.9365079365079225

## Example 3:
Input:
```
3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 3 0 0 0 0
```
Expected Output:
```
3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 3 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 3 0 0 0 0
```
Transformed Output:
```
3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 3 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 3 0 0 0 0
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0.0
**General Assessment**

The previous iteration successfully identified the agent and obstacle structures for all examples, including the challenging `train_2` case, by introducing prioritized agent identification rules (structural separation first). However, the code execution revealed that `train_2` still failed.

The error lies in the stopping condition logic for the 'solid\_line' obstacle structure. The code incorrectly stopped the line drawing immediately if the *next* pixel's column was occupied by an obstacle, even when moving vertically towards a horizontal obstacle line. The stopping condition for a solid line needs to be more specific: the line should only stop when the next step would cross into the specific row (for a horizontal line) or column (for a vertical line) occupied by the obstacles, considering the direction of movement. The 'scattered' obstacle stopping logic appears correct.

**Strategy for Resolution**

1.  **Refine 'solid\_line' Stopping Logic:** Modify the drawing loop. When the obstacle structure is 'solid\_line', the stopping check must depend on the direction of movement (`dr`, `dc`):
    *   If moving purely vertically (`dc == 0`), stop only if `next_r` is in `obstacle_rows`.
    *   If moving purely horizontally (`dr == 0`), stop only if `next_c` is in `obstacle_cols`.
    *   If moving diagonally (`dr != 0` and `dc != 0`), stop if `next_r` is in `obstacle_rows` OR `next_c` is in `obstacle_cols`.
2.  **Verify Agent Identification and Direction:** Double-check that the agent identification and direction logic remain correct for all examples with the refined understanding. (The previous analysis indicated they were correct).
3.  **Update Documentation:** Update the YAML definitions and Natural Language Program to reflect the precise stopping logic for 'solid\_line' obstacles based on movement direction.

**Metrics Analysis**

*   **train\_1:**
    *   Agent: Yellow (4) at (5, 11). Rule: Unique Color. Correct.
    *   Obstacles: Gray (5) line in column 1. Structure: `solid_line`. Correct.
    *   Direction: (0, -1) (Left). Correct.
    *   Stopping: Obstacle column = {1}. Moving horizontally (`dr=0, dc=-1`). Should stop *before* `next_c` is 1. `classify_obstacle_structure` correctly identifies `solid_line` (since `len(occupied_cols) == 1`). The refined logic will check `if dr == 0: stop if next_c in obstacle_cols`. This is correct. Expected output matches.
*   **train\_2:**
    *   Agent: Orange (7) at (7, 8). Rule: Structural Separation. Correct.
    *   Obstacles: Orange (7) line in row 1. Structure: `solid_line`. Correct.
    *   Direction: (-1, 0) (Up). Correct.
    *   Stopping: Obstacle row = {1}. Moving vertically (`dr=-1, dc=0`). Should stop *before* `next_r` is 1. `classify_obstacle_structure` correctly identifies `solid_line` (since `len(occupied_rows) == 1`). The refined logic will check `if dc == 0: stop if next_r in obstacle_rows`. This corrects the previous error. Expected output should now match.
*   **train\_3:**
    *   Agent: Red (2) at (6, 0). Rule: Unique Color. Correct.
    *   Obstacles: Green (3) scattered points. Structure: `scattered`. Correct.
    *   Direction: (-1, 1) (Up-Right). Correct.
    *   Stopping: Obstacle rows = {0, 2, 4, 6}, Obstacle cols = {0, 2, 4, 6}. Moving diagonally. Should stop *after* drawing on the first pixel where `next_r` is in {0, 2, 4, 6} OR `next_c` is in {0, 2, 4, 6}.
        *   Start: (6, 0)
        *   Step 1: Draw at (5, 1). `5 not in R_O`, `1 not in C_O`. Continue.
        *   Step 2: Draw at (4, 2). `4 in R_O`, `2 in C_O`. Draw here and stop.
    *   This matches the expected output. The 'scattered' logic is correct.

**Facts (YAML)**


```yaml
task_description: Draw a line from a single 'agent' pixel, using its color, until the line reaches a boundary defined by 'obstacle' pixels. The agent is identified via prioritized rules (structural separation, unique color, unique isolation). The stopping rule depends on the obstacle configuration ('solid_line' vs 'scattered') and the direction of movement.

definitions:
  - name: background_pixel
    value: 0 # white
  - name: non_background_pixels
    description: All pixels with color != 0.
    properties:
      - positions: List of (r, c, color) tuples.
  - name: line_structure_pixels
    description: The largest set of non-background pixels sharing the same color AND lying on a single row OR single column (minimum 2 pixels). Can be empty.
  - name: agent_pixel
    description: The single pixel initiating the line draw. Identified via prioritized rules.
    properties:
      - color: C
      - position: (r0, c0)
    identification_rules: # Priority Order
      - 1: If line_structure_pixels exist AND exactly one non-background pixel remains outside this structure, that remaining pixel is the agent.
      - 2: If rule 1 doesn't apply, find pixels with a color appearing only once grid-wide. If exactly one such pixel exists, it's the agent.
      - 3: If rules 1 & 2 don't apply, find pixels with no neighbors (Moore neighborhood) of the same color. If exactly one such pixel exists, it's the agent.
      - 4: Otherwise, no agent is identified.
  - name: obstacle_pixels
    description: All non-background pixels excluding the identified agent pixel.
    properties:
      - positions: Set of (r, c) coordinates.
      - occupied_rows: R_O (Set of row indices containing obstacles).
      - occupied_cols: C_O (Set of column indices containing obstacles).
      - structure: Derived property, either 'solid_line' (if obstacles occupy only one row OR only one column, allowing single-pixel obstacles) or 'scattered'.

parameters:
  - name: line_direction
    description: Vector (dr, dc) determined by agent position relative to grid boundaries.
    values: # Examples
      - (-1, 0) # Up
      - (1, 0)  # Down
      - (0, -1) # Left
      - (0, 1)  # Right
      - (-1, 1) # Up-Right
    determination: Move away from the nearest grid edge/corner. Ties favor Up/Left components.

transformations:
  - step: Identify all non_background_pixels.
  - step: Attempt to identify agent using rule 1 (line structure separation).
  - step: If no agent yet, attempt using rule 2 (unique color).
  - step: If no agent yet, attempt using rule 3 (unique spatial isolation).
  - step: If an agent (C, (r0, c0)) was identified, define all other non-background pixels as obstacles. If no agent, stop and return input grid.
  - step: Analyze obstacles to determine structure ('solid_line' or 'scattered') and get occupied rows (R_O) and columns (C_O).
  - step: Determine line_direction (dr, dc) based on agent position (r0, c0) and grid dimensions.
  - step: Initialize current position (r, c) = (r0, c0).
  - step: Draw line segment:
      - Loop:
          - Calculate next position (nr, nc) = (r + dr, c + dc).
          - Check grid bounds for (nr, nc). If out, stop loop.
          - Define stop_before_coloring = False, stop_after_coloring = False.
          - if structure == 'solid_line':
              - if dr != 0 and dc == 0: # Pure vertical move
                  if nr in R_O: stop_before_coloring = True
              - elif dr == 0 and dc != 0: # Pure horizontal move
                  if nc in C_O: stop_before_coloring = True
              - elif dr != 0 and dc != 0: # Diagonal move
                  if nr in R_O or nc in C_O: stop_before_coloring = True
          - elif structure == 'scattered':
              - if nr in R_O or nc in C_O:
                  stop_after_coloring = True
          - If stop_before_coloring: break loop.
          - Color pixel (nr, nc) with C.
          - If stop_after_coloring: break loop.
          - Update (r, c) = (nr, nc).

output_grid: The input grid modified by coloring the pixels along the drawn line segment. If no agent was identified, the output is identical to the input.
```


**Natural Language Program**

1.  Find all non-background pixels in the input grid. If none exist, return the input grid.
2.  **Identify the Agent:**
    *   a. Check if there's a largest group of same-colored pixels (minimum 2) forming a single horizontal or vertical line.
    *   b. If such a line structure exists and there is *exactly one* other non-background pixel remaining, designate that single pixel as the **agent**.
    *   c. If step (b) did not identify an agent, check if there is *exactly one* pixel whose color is unique across the entire grid. If so, designate that pixel as the **agent**.
    *   d. If steps (b) and (c) did not identify an agent, check if there is *exactly one* pixel that has no neighbors (including diagonals) of the same color. If so, designate that pixel as the **agent**.
    *   e. If no agent was identified, return the input grid unchanged.
3.  Designate all non-background pixels that are *not* the agent as **obstacles**. Note the agent's color (C) and position (r0, c0).
4.  Analyze the obstacle positions: Determine if they occupy only a single row OR a single column (structure is 'solid\_line'), or if they occupy multiple rows AND columns (structure is 'scattered'). Record the set of rows (R\_O) and columns (C\_O) occupied by any obstacle.
5.  Determine the drawing direction vector (dr, dc) based on the agent's position (r0, c0). The direction moves away from the nearest grid edge or corner (ties favor Up and/or Left components).
6.  Initialize the current drawing position (r, c) to the agent's position (r0, c0).
7.  **Draw the Line:**
    *   Repeatedly calculate the next potential position (nr, nc) = (r + dr, c + dc).
    *   Stop drawing if (nr, nc) is outside the grid boundaries.
    *   **Check Stopping Conditions:**
        *   If the obstacle structure is 'solid\_line':
            *   If moving vertically (`dc == 0`) and the next row `nr` is in R\_O, stop drawing *before* coloring (nr, nc).
            *   If moving horizontally (`dr == 0`) and the next column `nc` is in C\_O, stop drawing *before* coloring (nr, nc).
            *   If moving diagonally (`dr != 0` and `dc != 0`) and the next row `nr` is in R\_O OR the next column `nc` is in C\_O, stop drawing *before* coloring (nr, nc).
        *   If the obstacle structure is 'scattered':
            *   If the next row `nr` is in R\_O OR the next column `nc` is in C\_O, plan to stop drawing *after* coloring this pixel (nr, nc).
    *   If the decision was made to stop *before* coloring, exit the drawing loop now.
    *   Color the pixel at (nr, nc) with the agent's color C.
    *   If the decision was made to stop *after* coloring (in the 'scattered' case), exit the drawing loop now.
    *   Update the current position (r, c) = (nr, nc) and continue the loop.
8.  Output the resulting grid.
```python
import numpy as np
from collections import Counter, defaultdict

"""
Transformation Rule Description:

1.  Find all non-background pixels in the input grid. If none exist, return the input grid.
2.  **Identify the Agent:**
    *   a. Check if there's a largest group of same-colored pixels (minimum 2) forming a single horizontal or vertical line.
    *   b. If such a line structure exists and there is *exactly one* other non-background pixel remaining, designate that single pixel as the **agent**.
    *   c. If step (b) did not identify an agent, check if there is *exactly one* pixel whose color is unique across the entire grid. If so, designate that pixel as the **agent**.
    *   d. If steps (b) and (c) did not identify an agent, check if there is *exactly one* pixel that has no neighbors (including diagonals) of the same color. If so, designate that pixel as the **agent**.
    *   e. If no agent was identified, return the input grid unchanged.
3.  Designate all non-background pixels that are *not* the agent as **obstacles**. Note the agent's color (C) and position (r0, c0).
4.  Analyze the obstacle positions: Determine if they occupy only a single row OR a single column (structure is 'solid_line'), or if they occupy multiple rows AND columns (structure is 'scattered'). Record the set of rows (R_O) and columns (C_O) occupied by any obstacle.
5.  Determine the drawing direction vector (dr, dc) based on the agent's position (r0, c0). The direction moves away from the nearest grid edge or corner (ties favor Up and/or Left components).
6.  Initialize the current drawing position (r, c) to the agent's position (r0, c0).
7.  **Draw the Line:**
    *   Repeatedly calculate the next potential position (nr, nc) = (r + dr, c + dc).
    *   Stop drawing if (nr, nc) is outside the grid boundaries.
    *   **Check Stopping Conditions:**
        *   If the obstacle structure is 'solid_line':
            *   If moving vertically (`dc == 0`) and the next row `nr` is in R_O, stop drawing *before* coloring (nr, nc).
            *   If moving horizontally (`dr == 0`) and the next column `nc` is in C_O, stop drawing *before* coloring (nr, nc).
            *   If moving diagonally (`dr != 0` and `dc != 0`) and the next row `nr` is in R_O OR the next column `nc` is in C_O, stop drawing *before* coloring (nr, nc).
        *   If the obstacle structure is 'scattered':
            *   If the next row `nr` is in R_O OR the next column `nc` is in C_O, plan to stop drawing *after* coloring this pixel (nr, nc).
    *   If the decision was made to stop *before* coloring, exit the drawing loop now.
    *   Color the pixel at (nr, nc) with the agent's color C.
    *   If the decision was made to stop *after* coloring (in the 'scattered' case), exit the drawing loop now.
    *   Update the current position (r, c) = (nr, nc) and continue the loop.
8.  Output the resulting grid.
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

def find_largest_line_structure(non_bg_pixels: list[tuple[int, int, int]]) -> list[tuple[int, int, int]]:
    """Finds the largest group of same-colored pixels in a single row or column.

    Args:
        non_bg_pixels: List of (r, c, color) tuples for all non-background pixels.

    Returns:
        A list of (r, c, color) tuples representing the pixels in the largest line found,
        or an empty list if no line structure (at least 2 pixels) is found or multiple
        lines have the same maximum size. Returns the first encountered max line in case of tie.
    """
    if not non_bg_pixels:
        return []

    pixels_by_color = defaultdict(list)
    for r, c, color in non_bg_pixels:
        pixels_by_color[color].append((r, c, color))

    largest_line = []
    max_len = 0

    # Iterate consistently (e.g., by color value) to handle ties predictably
    sorted_colors = sorted(pixels_by_color.keys())

    for color in sorted_colors:
        pixels = pixels_by_color[color]
        if len(pixels) < 2: # A line needs at least 2 points
            continue

        rows = set(r for r, c, _ in pixels)
        cols = set(c for r, c, _ in pixels)

        # Check for horizontal line
        if len(rows) == 1:
            if len(pixels) > max_len:
                max_len = len(pixels)
                largest_line = pixels
            # Tie breaking: first encountered (implicit by loop order and > condition)

        # Check for vertical line
        elif len(cols) == 1: # Use elif to avoid counting grids of single points as both
            if len(pixels) > max_len:
                max_len = len(pixels)
                largest_line = pixels
            # Tie breaking: first encountered (implicit by loop order and > condition)

    # Return only if a line structure was found (max_len >= 2)
    return largest_line if max_len >= 2 else []


def identify_agent_and_obstacles_refined(grid: np.ndarray) -> tuple[tuple[int, int, int] | None, list[tuple[int, int, int]]]:
    """
    Identifies the agent pixel and obstacle pixels using refined, prioritized rules.

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

    agent_pixel_info = None
    obstacle_pixels = []
    non_bg_pixel_set = set((p[0], p[1]) for p in non_bg_pixels) # For quick lookup

    # Rule 1: Structural Separation
    line_pixels = find_largest_line_structure(non_bg_pixels)
    if line_pixels:
        line_pixel_coords = set((p[0], p[1]) for p in line_pixels)
        potential_agent_coords = non_bg_pixel_set - line_pixel_coords
        if len(potential_agent_coords) == 1:
            agent_coord = potential_agent_coords.pop()
            # Find the full agent info (r, c, color)
            for r, c, color in non_bg_pixels:
                if (r, c) == agent_coord:
                    agent_pixel_info = (r, c, color)
                    break
            obstacle_pixels = line_pixels # Obstacles are the line pixels
            return agent_pixel_info, obstacle_pixels

    # Rule 2: Unique Color
    if not agent_pixel_info:
        color_counts = Counter(p[2] for p in non_bg_pixels)
        unique_colors = [color for color, count in color_counts.items() if count == 1]
        if len(unique_colors) == 1:
            agent_color = unique_colors[0]
            temp_obstacles = []
            for r, c, color in non_bg_pixels:
                if color == agent_color:
                    agent_pixel_info = (r, c, color)
                else:
                    temp_obstacles.append((r, c, color))
            obstacle_pixels = temp_obstacles
            return agent_pixel_info, obstacle_pixels

    # Rule 3: Unique Spatial Isolation
    if not agent_pixel_info:
        isolated_pixels = []
        pixel_map = {(p[0], p[1]): p[2] for p in non_bg_pixels}
        # Iterate consistently (e.g., row-major) to handle ties predictably
        sorted_non_bg_pixels = sorted(non_bg_pixels)
        for r, c, color in sorted_non_bg_pixels:
            is_isolated = True
            neighbors = get_neighbors(r, c, grid.shape)
            for nr, nc in neighbors:
                if pixel_map.get((nr, nc)) == color:
                    is_isolated = False
                    break
            if is_isolated:
                isolated_pixels.append((r, c, color))

        if len(isolated_pixels) == 1:
            agent_pixel_info = isolated_pixels[0]
            # Rebuild obstacle list excluding the found agent
            obstacle_pixels = [p for p in non_bg_pixels if (p[0], p[1]) != (agent_pixel_info[0], agent_pixel_info[1])]
            return agent_pixel_info, obstacle_pixels

    # If no agent identified by any rule
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
    # Note: len <= 1 allows single-pixel obstacles to be treated as 'solid_line'
    if len(occupied_rows) <= 1 or len(occupied_cols) <= 1:
        return 'solid_line'
    else:
        return 'scattered'


def determine_direction(agent_pos: tuple[int, int], grid_shape: tuple[int, int]) -> tuple[int, int]:
    """Determines the drawing direction (dr, dc) away from the nearest grid edge/corner.
       Ties favor Up and/or Left.

    Args:
        agent_pos: A tuple (row, col) of the agent's position.
        grid_shape: A tuple (height, width) of the grid dimensions.

    Returns:
        A tuple (dr, dc) representing the change in row and column for the next step.
        Example: (-1, 0) is Up, (1, 1) is Down-Right.
    """
    r, c = agent_pos
    h, w = grid_shape

    # Handle 1x1 grid case
    if h == 1 and w == 1:
        return (0, 0)

    # Calculate distances to edges
    dist_top = r
    dist_bottom = h - 1 - r
    dist_left = c
    dist_right = w - 1 - c

    # Find the minimum distance to any edge
    min_dist = min(dist_top, dist_bottom, dist_left, dist_right)

    # Determine potential directions (away from closest edges), prioritizing Up/Left in ties
    dr, dc = 0, 0
    # Vertical component: Prioritize Up (-1) if bottom is equidistant or closer than top
    if dist_bottom <= dist_top and dist_bottom == min_dist:
        dr = -1 # Move Up
    elif dist_top == min_dist:
        dr = 1  # Move Down

    # Horizontal component: Prioritize Left (-1) if right is equidistant or closer than left
    if dist_right <= dist_left and dist_right == min_dist:
        dc = -1 # Move Left
    elif dist_left == min_dist:
        dc = 1  # Move Right

    # Ensure direction is non-zero if grid > 1x1 and initial dr/dc are 0
    # This can happen if perfectly centered
    if dr == 0 and dc == 0 and (h > 1 or w > 1):
         # Default: away from top-left -> down-right
         dr, dc = 1, 1
         # Apply tie-breaking priorities if applicable
         if dist_bottom <= dist_top: dr = -1
         if dist_right <= dist_left: dc = -1


    return dr, dc


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the described transformation to the input grid.
    """
    # Initialize grid using numpy for easier manipulation
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy()
    h, w = grid.shape

    # --- Step 1-3: Identify agent and obstacles using refined rules ---
    agent_info, obstacles = identify_agent_and_obstacles_refined(grid)

    # If no agent identified, return the original grid
    if agent_info is None:
        return input_grid # Return as list of lists

    agent_r, agent_c, agent_color = agent_info

    # --- Step 4: Get obstacle information and classify structure ---
    obstacle_rows, obstacle_cols = get_obstacle_info(obstacles)
    structure = classify_obstacle_structure(obstacles)

    # --- Step 5: Determine drawing direction ---
    dr, dc = determine_direction((agent_r, agent_c), (h, w))

    # If direction is (0,0) (e.g., 1x1 grid), no drawing needed
    if dr == 0 and dc == 0:
        return output_grid.tolist() # Return current grid as list of lists

    # --- Step 6 & 7: Draw line with appropriate stopping condition ---
    curr_r, curr_c = agent_r, agent_c

    while True:
        # Calculate the *next* potential position
        next_r, next_c = curr_r + dr, curr_c + dc

        # Check if next position is within grid bounds
        if not (0 <= next_r < h and 0 <= next_c < w):
            break # Stop drawing if out of bounds

        # Initialize stop flags for this iteration
        stop_before_coloring = False
        stop_after_coloring = False

        # Check stopping conditions based on obstacle structure
        if structure == 'solid_line':
            # Check if the next step enters the obstacle line's row/column
            if dr != 0 and dc == 0: # Pure vertical move
                if next_r in obstacle_rows: stop_before_coloring = True
            elif dr == 0 and dc != 0: # Pure horizontal move
                if next_c in obstacle_cols: stop_before_coloring = True
            elif dr != 0 and dc != 0: # Diagonal move
                if next_r in obstacle_rows or next_c in obstacle_cols: stop_before_coloring = True

        elif structure == 'scattered':
            # Check if the next step enters any row or column occupied by obstacles
            if next_r in obstacle_rows or next_c in obstacle_cols:
                stop_after_coloring = True # Stop after coloring this pixel

        # --- Apply Stop Conditions ---
        # If stopping before coloring, break the loop now
        if stop_before_coloring:
            break

        # --- Color the Pixel ---
        output_grid[next_r, next_c] = agent_color

        # If stopping after coloring, break the loop now
        if stop_after_coloring:
            break

        # --- Update Position ---
        # Update current position for the next iteration
        curr_r, curr_c = next_r, next_c

    # --- Step 8: Return the modified grid ---
    return output_grid.tolist()
```
