"""
Finds the largest contiguous block of red pixels (value 2) in the input grid,
conceptualizes a bounding box around it, and creates a 3x3 output grid where
blue pixels (value 1) represent the presence of the red shape's outline, and
white pixels (value 0) indicate the absence of red.
"""

import numpy as np

def find_largest_red_object(grid):
    # Find the largest connected component of red (2) pixels.
    rows, cols = len(grid), len(grid[0])
    visited = set()
    max_size = 0
    largest_object_coords = []

    def dfs(row, col, current_object_coords):
        if (
            row < 0
            or row >= rows
            or col < 0
            or col >= cols
            or grid[row][col] != 2
            or (row, col) in visited
        ):
            return 0
        visited.add((row, col))
        current_object_coords.append((row, col))
        size = 1
        size += dfs(row + 1, col, current_object_coords)
        size += dfs(row - 1, col, current_object_coords)
        size += dfs(row, col + 1, current_object_coords)
        size += dfs(row, col - 1, current_object_coords)
        return size

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2 and (r, c) not in visited:
                current_object_coords = []
                size = dfs(r, c, current_object_coords)
                if size > max_size:
                    max_size = size
                    largest_object_coords = current_object_coords
    return largest_object_coords

def transform(input_grid):
    # Find the largest connected red object.
    largest_red_object_coords = find_largest_red_object(input_grid)

    # If no red object is found, return a 3x3 grid of all zeros.
    if not largest_red_object_coords:
        return [[0] * 3 for _ in range(3)]

    # Determine the bounding box.
    min_row = min(r for r, _ in largest_red_object_coords)
    max_row = max(r for r, _ in largest_red_object_coords)
    min_col = min(c for _, c in largest_red_object_coords)
    max_col = max(c for _, c in largest_red_object_coords)

    # conceptualize shrinking the rectangle
    # top
    top_edge_present = any(input_grid[min_row][c] == 2 for c in range(min_col, max_col + 1))
    # bottom
    bottom_edge_present = any(input_grid[max_row][c] == 2 for c in range(min_col, max_col + 1))    
    # left
    left_edge_present = any(input_grid[r][min_col] == 2 for r in range(min_row, max_row + 1))
    # right
    right_edge_present = any(input_grid[r][max_col] == 2 for r in range(min_row, max_row + 1))    
    
    # Initialize output grid.
    output_grid = [[0] * 3 for _ in range(3)]
    
    # Set output based on presence of edges
    if top_edge_present:
        output_grid[0] = [1]*3
    if bottom_edge_present:
        output_grid[2] = [1]*3
    if left_edge_present:
        for i in range(3):
            output_grid[i][0]=1
    if right_edge_present:
        for i in range(3):
            output_grid[i][2]=1        

    # check if object exists in the center
    center_row = (min_row + max_row) // 2
    center_col = (min_col + max_col) // 2
    
    if (center_row >= 0 and center_row < len(input_grid) and
          center_col >= 0 and center_col < len(input_grid[0]) and
          input_grid[center_row][center_col] == 2):
          
          output_grid[1][1] = 1 # mark the core as present
    
    return output_grid