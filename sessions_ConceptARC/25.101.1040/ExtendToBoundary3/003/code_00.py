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