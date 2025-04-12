
Previous Code:
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
