```python
"""
1.  **Identify Key Pixels:** Locate all yellow (4) and red (2) pixels within the input grid.
2.  **Pathfinding:** Determine the continuous paths formed by adjacent red (2) pixels. Adjacency includes horizontal and vertical neighbors (not diagonal).
3.  **Connectivity Check:** A path is considered *valid* if:
     a. It connects two distinct yellow pixels.
     b. It connects one yellow pixel to the edge of the grid.
     c. It connects two edges of the grid (this seems implied by example 2).
4.  **Transformation:**
    *   Replace all red (2) pixels that are part of a *valid* path with azure (8).
    *   Replace all red (2) pixels *not* part of a valid path with black (0).
5. **Preservation:** Yellow (4) pixels remain unchanged. Black (0) pixels that aren't replacements for the described '2' pixels should also remain unchanged.
"""

import numpy as np

def get_positions(grid, color):
    """Finds all positions of a specific color in the grid."""
    positions = []
    for r_idx, row in enumerate(grid):
        for c_idx, pixel in enumerate(row):
            if pixel == color:
                positions.append((r_idx, c_idx))
    return positions

def is_adjacent(pos1, pos2):
    """Checks if two positions are adjacent (horizontally or vertically)."""
    return (abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])) == 1

def find_paths(grid, start_pos):
    """Finds all paths starting from a given position, consisting of red pixels."""
    red = 2
    paths = [[start_pos]]
    final_paths = []

    while paths:
        current_path = paths.pop()
        last_pos = current_path[-1]
        
        is_complete = False
        #check it this completes:
        if len(current_path) > 1: # needs at least 2
           #if connects to another yellow
           for y_pos in get_positions(grid, 4):
              if is_adjacent(last_pos, y_pos):
                 final_paths.append(current_path)
                 is_complete = True
                 break
           #if it is at the edge
           if not is_complete:
             if last_pos[0] == 0 or last_pos[0] == grid.shape[0]-1 or last_pos[1] == 0 or last_pos[1] == grid.shape[1] -1:
                final_paths.append(current_path)
                is_complete = True
        
        if not is_complete:
            neighbors = [(last_pos[0] - 1, last_pos[1]), (last_pos[0] + 1, last_pos[1]),
                         (last_pos[0], last_pos[1] - 1), (last_pos[0], last_pos[1] + 1)]
            for neighbor in neighbors:
                if (0 <= neighbor[0] < grid.shape[0] and 0 <= neighbor[1] < grid.shape[1] and
                        grid[neighbor] == red and neighbor not in current_path):
                    new_path = current_path + [neighbor]
                    paths.append(new_path)

    return final_paths

def transform(input_grid):
    """Transforms the input grid according to the described rules."""
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid).astype(int)
    yellow_positions = get_positions(input_grid, 4)
    red_positions = get_positions(input_grid, 2)

    # Find all valid paths
    valid_path_pixels = set()
    for r_pos in red_positions:
        #only check paths if start next to yellow:
        start_path = False
        for y_pos in yellow_positions:
          if is_adjacent(r_pos, y_pos):
            start_path = True
            break
        if not start_path:  # or already in valid path
            if r_pos[0] == 0 or r_pos[0] == input_grid.shape[0] - 1 or r_pos[1] == 0 or r_pos[1] == input_grid.shape[1] - 1:
                start_path = True
        if start_path:  # or already in valid path
            paths = find_paths(input_grid, r_pos)
            for path in paths:
                 for pos in path:
                    valid_path_pixels.add(pos)

    # Apply transformations
    for r_idx, c_idx in red_positions:
        if (r_idx, c_idx) in valid_path_pixels:
            output_grid[r_idx, c_idx] = 8  # Change to azure
        else:
            output_grid[r_idx, c_idx] = 0  # Change to black

    return output_grid
```