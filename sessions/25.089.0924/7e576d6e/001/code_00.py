import numpy as np
from collections import deque, Counter

"""
Transformation Rule:
1. Identify the background color (most frequent color in the grid).
2. Identify the path color and the two endpoint coordinates. This color appears exactly twice and is different from the background color.
3. Identify obstacle colors (any color that is not the background or path color).
4. Find the shortest path between the two endpoints using Breadth-First Search (BFS). The path can only move horizontally or vertically onto cells containing the background color. Obstacle cells cannot be part of the path.
5. Create an output grid by copying the input grid.
6. Draw the found shortest path onto the output grid using the path color, changing the color of the background cells that form the path. The endpoints remain their original color.
"""

def find_colors_and_endpoints(grid):
    """Identifies background, path color, endpoints, and obstacles."""
    unique_colors, counts = np.unique(grid, return_counts=True)
    color_counts = dict(zip(unique_colors, counts))

    # Background color is the most frequent
    background_color = max(color_counts, key=color_counts.get)

    path_color = -1
    endpoints = []
    obstacle_colors = set()

    # Find path color (appears twice) and potential obstacles
    for color, count in color_counts.items():
        if color == background_color:
            continue
        if count == 2:
            path_color = color
        else:
            # Any other non-background color is treated as part of an obstacle structure
            obstacle_colors.add(color)

    if path_color == -1:
        raise ValueError("Path color (exactly two pixels) not found.")

    # Find endpoint coordinates
    endpoint_coords = np.argwhere(grid == path_color)
    if len(endpoint_coords) != 2:
         raise ValueError(f"Expected 2 endpoints for color {path_color}, found {len(endpoint_coords)}.")
    endpoints = [tuple(coord) for coord in endpoint_coords]

    return background_color, path_color, endpoints, obstacle_colors


def bfs_shortest_path(grid, start, end, background_color, obstacle_colors):
    """Finds the shortest path using BFS."""
    rows, cols = grid.shape
    queue = deque([(start, [start])])  # Store (current_pos, path_list)
    visited = {start}

    while queue:
        (r, c), path = queue.popleft()

        if (r, c) == end:
            return path # Found the shortest path

        # Explore neighbors (Up, Down, Left, Right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check boundaries
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbor_pos = (nr, nc)
                neighbor_color = grid[nr, nc]

                # Check if valid move (background or end point) and not visited
                if neighbor_pos not in visited and (neighbor_color == background_color or neighbor_pos == end):
                    visited.add(neighbor_pos)
                    new_path = path + [neighbor_pos]
                    queue.append((neighbor_pos, new_path))

    return None # No path found


def transform(input_grid):
    """
    Finds and draws the shortest path between two points on the grid,
    avoiding obstacles.
    """
    # Convert input list of lists to numpy array for easier processing
    grid = np.array(input_grid, dtype=int)
    rows, cols = grid.shape

    # 1. Identify colors and endpoints
    try:
        background_color, path_color, endpoints, obstacle_colors = find_colors_and_endpoints(grid)
        start_point, end_point = endpoints[0], endpoints[1]
    except ValueError as e:
        print(f"Error identifying elements: {e}")
        # Return a copy of the input if analysis fails
        # Or handle the error appropriately depending on expected behavior
        return grid.tolist()


    # 3. Find the shortest path using BFS
    # We treat obstacle colors as impassable, but the BFS logic inherently only
    # moves onto background_color cells (or the target endpoint), effectively avoiding obstacles.
    shortest_path = bfs_shortest_path(grid, start_point, end_point, background_color, obstacle_colors)

    # 4. Create the output grid
    output_grid = grid.copy()

    # 5. Draw the path if found
    if shortest_path:
        # Iterate through the path coordinates (excluding start and end points,
        # as they are already the correct color)
        for r, c in shortest_path[1:-1]:
             # Check if the cell is background before drawing (should always be true by BFS logic)
             # This check adds safety but might be redundant if BFS is correct.
             if output_grid[r, c] == background_color:
                 output_grid[r, c] = path_color
    else:
        # Handle cases where no path is found, though the problem implies one exists.
        # For now, return the grid as is or raise an error.
        print("Warning: No path found between endpoints.")
        # Depending on requirements, might return input or raise error.
        # return grid.tolist() # Return original if no path

    # Convert back to list of lists for the expected output format
    return output_grid.tolist()