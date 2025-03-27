"""
Find the shortest Manhattan path from the top-left corner (0, 0) to the 
bottom-right corner (H-1, W-1) of the input grid, avoiding a single 
non-background colored pixel (the obstacle). Then, color the cells of this 
path blue (1), except for the obstacle cell itself, which retains its original 
color. All other cells retain their original colors.
"""

import numpy as np
from collections import deque

def find_obstacle(grid):
    """
    Finds the coordinates and color of the single non-background pixel.
    Assumes the background color is the most frequent one.
    """
    unique, counts = np.unique(grid, return_counts=True)
    background_color = unique[np.argmax(counts)]
    
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != background_color:
                return (r, c), grid[r, c]
    return None, None # Should not happen based on task description

def find_shortest_path_bfs(grid, start, end, obstacle_pos):
    """
    Finds the shortest path using Breadth-First Search (BFS) avoiding the obstacle.
    Returns the path as a list of coordinates, or None if no path exists.
    """
    rows, cols = grid.shape
    queue = deque([(start, [start])]) # Store (current_pos, path_so_far)
    visited = {start}
    
    while queue:
        (r, c), path = queue.popleft()
        
        if (r, c) == end:
            return path
            
        # Explore neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            
            # Check bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbor_pos = (nr, nc)
                # Check if obstacle or already visited
                if neighbor_pos != obstacle_pos and neighbor_pos not in visited:
                    visited.add(neighbor_pos)
                    new_path = path + [neighbor_pos]
                    queue.append((neighbor_pos, new_path))
                    
    return None # No path found

def transform(input_grid):
    """
    Applies the pathfinding transformation to the input grid.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    grid_np = np.array(input_grid, dtype=int)
    rows, cols = grid_np.shape
    
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(grid_np)
    
    # Identify the obstacle's position and color
    obstacle_pos, obstacle_color = find_obstacle(grid_np)
    
    # Define start and end points for the path
    start_pos = (0, 0)
    end_pos = (rows - 1, cols - 1)
    
    # Find the shortest path using BFS, avoiding the obstacle
    shortest_path = find_shortest_path_bfs(grid_np, start_pos, end_pos, obstacle_pos)
    
    # If a path is found, color the path cells blue (1) in the output grid,
    # except for the obstacle cell itself.
    if shortest_path:
        for r, c in shortest_path:
            # Check if the current cell in the path is not the obstacle
            if (r, c) != obstacle_pos:
                output_grid[r, c] = 1 # Set to blue
            # If it is the obstacle, it retains its original color (already copied)
                
    # Convert the final numpy array back to a list of lists
    return output_grid.tolist()
