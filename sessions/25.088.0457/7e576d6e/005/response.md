```python
import numpy as np
from collections import Counter, deque

"""
Transforms an input grid by:
1. Identifying the background color (most frequent color).
2. Identifying two 'endpoint' pixels which share the same color, where that color appears exactly twice in the grid (excluding the background color).
3. Identifying all other colors as 'obstacles'.
4. Finding the shortest path between the two endpoints using Breadth-First Search (BFS). The path can only move horizontally or vertically and must only traverse cells that originally contained the background color.
5. Constructing an output grid by copying the input grid and then drawing the found path (excluding the start and end points themselves) onto the copy using the endpoint color. If no unique endpoints are found or no path exists, the original grid is returned.
"""

def find_endpoints_and_obstacles(grid):
    """
    Identifies the background color, endpoint color and coordinates, 
    and obstacle colors from the input grid.

    Args:
        grid (np.array): The input grid.

    Returns:
        tuple: (background_color, endpoint_color, endpoints, obstacle_colors)
               Returns (None, None, None, None) if identification fails 
               (e.g., no color appears exactly twice besides background, or multiple colors appear twice).
    """
    unique_colors, counts = np.unique(grid, return_counts=True)
    
    # Handle empty or single-color grids gracefully
    if not unique_colors.size:
        return None, None, None, None
    if unique_colors.size == 1:
         return unique_colors[0], None, None, set() # Only background exists

    # Assume background color is the most frequent
    background_color_index = np.argmax(counts)
    background_color = unique_colors[background_color_index]

    endpoint_color = None
    endpoints = []
    obstacle_colors = set()
    potential_endpoint_colors_found = 0
    
    # Iterate through colors to find endpoints and obstacles
    for i, color in enumerate(unique_colors):
        if color == background_color:
            continue # Skip background

        count = counts[i]
        if count == 2:
            potential_endpoint_colors_found += 1
            if potential_endpoint_colors_found > 1:
                # Ambiguity: More than one color appears exactly twice
                return None, None, None, None 
            
            endpoint_color = color
            # Find coordinates efficiently using np.where
            rows, cols = np.where(grid == color)
            endpoints = list(zip(rows, cols))

        else:
            # Any other non-background color is an obstacle
            obstacle_colors.add(color)
            
    # Check if exactly one endpoint color was found
    if potential_endpoint_colors_found != 1 or not endpoints:
        return None, None, None, None

    return background_color, endpoint_color, endpoints, obstacle_colors


def solve_bfs_optimized(grid, start_pos, end_pos, background_color):
    """
    Finds the shortest path between start_pos and end_pos using BFS, 
    moving only on the background color. Optimized to avoid storing full paths in the queue.

    Args:
        grid (np.array): The input grid.
        start_pos (tuple): The (row, col) of the starting point.
        end_pos (tuple): The (row, col) of the ending point.
        background_color (int): The color of valid path cells.

    Returns:
        list: A list of (row, col) tuples representing the path, or None if no path exists.
    """
    rows, cols = grid.shape
    queue = deque([start_pos])  # Store just the current position
    visited = {start_pos} # Keep track of visited cells
    parents = {start_pos: None} # Store {child_pos: parent_pos} to reconstruct path

    while queue:
        r, c = queue.popleft()

        # Check if we reached the end point
        if (r, c) == end_pos:
            # Reconstruct path
            path = []
            curr = end_pos
            while curr is not None:
                path.append(curr)
                curr = parents[curr]
            return path[::-1] # Return reversed path (start -> end)

        # Explore neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            neighbor_pos = (nr, nc)

            # Check if the neighbor is within grid bounds and not visited
            if 0 <= nr < rows and 0 <= nc < cols and neighbor_pos not in visited:
                neighbor_color = grid[nr, nc]

                # Determine if the neighbor cell is valid for traversal
                # It's valid if it's the end position OR if it's a background cell
                is_end_cell = (neighbor_pos == end_pos)
                is_background_cell = (neighbor_color == background_color)

                if is_end_cell or is_background_cell:
                    # Mark as visited, store parent, and add to the queue
                    visited.add(neighbor_pos)
                    parents[neighbor_pos] = (r, c)
                    queue.append(neighbor_pos)
                    
    # If the queue becomes empty and we haven't returned, no path exists
    return None 


def transform(input_grid_list):
    """
    Transforms the input grid by finding two endpoint pixels and drawing the shortest 
    path between them using the background color cells.

    Args:
        input_grid_list (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The output grid with the path drawn, or the original grid if 
                       identification fails or no path is found.
    """
    # Convert input list of lists to numpy array for processing
    input_grid = np.array(input_grid_list, dtype=int)
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    
    # --- 1. Identify Key Components ---
    # Find background color, endpoints, and obstacles based on color frequencies
    background_color, endpoint_color, endpoints, obstacle_colors = find_endpoints_and_obstacles(input_grid)

    # --- Check if Identification was Successful ---
    # If we couldn't find a unique background or exactly two endpoints of the same color,
    # return the original grid unmodified.
    if background_color is None or endpoint_color is None or not endpoints or len(endpoints) != 2:
        return output_grid.tolist() 

    # Extract start and end positions
    start_pos, end_pos = endpoints[0], endpoints[1]

    # --- 2. Find the Shortest Path using Optimized BFS ---
    # Search for the shortest path from start to end, only moving on background cells
    # Note: obstacle_colors aren't strictly needed by BFS if it only checks for background_color or end_pos
    path = solve_bfs_optimized(input_grid, start_pos, end_pos, background_color)

    # --- 3. Draw the Path on the Output Grid ---
    # If a path was found by BFS:
    if path:
        # Iterate through the coordinates in the found path
        for r, c in path:
            # Do not recolor the original start and end points
            # Only color the intermediate cells that were originally background
            if (r, c) != start_pos and (r, c) != end_pos:
                 output_grid[r, c] = endpoint_color
    # else: # No path found or identification failed earlier
        # If no path is found, we implicitly return the unmodified output_grid copy

    # --- 4. Return Result ---
    # Convert the final numpy array back to a list of lists for the expected output format
    return output_grid.tolist()
```