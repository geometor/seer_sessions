
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
