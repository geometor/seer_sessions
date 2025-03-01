"""
1. Identify the largest connected component of gray (5) pixels. A connected component is a set of pixels where each pixel is adjacent (horizontally or vertically, not diagonally) to at least one other pixel in the set. "Largest" refers to the component with the most pixels.
2. Recolor the top row and leftmost column of the bounding box of this largest connected component to azure (8).
3. Recolor the remaining gray pixels within the largest connected component to red (2).
"""

import numpy as np
from collections import deque

def find_largest_connected_component(grid, color):
    visited = set()
    max_component = []

    def bfs(start_row, start_col):
        queue = deque([(start_row, start_col)])
        component = []
        while queue:
            row, col = queue.popleft()
            if (row, col) not in visited and 0 <= row < grid.shape[0] and 0 <= col < grid.shape[1] and grid[row, col] == color:
                visited.add((row, col))
                component.append((row, col))
                # Add adjacent cells (up, down, left, right)
                queue.extend([(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)])
        return component

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if (row, col) not in visited and grid[row, col] == color:
                current_component = bfs(row, col)
                if len(current_component) > len(max_component):
                    max_component = current_component
    return max_component

def transform(input_grid):
    # Initialize output grid
    output_grid = np.copy(input_grid)

    # Find the largest connected component of gray (5) pixels
    largest_component = find_largest_connected_component(input_grid, 5)

    if not largest_component:
        return output_grid  # Return original if no gray pixels

    # Get bounding box of the largest component
    rows, cols = zip(*largest_component)
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)
    
    # Recolor the largest component
    for r, c in largest_component:
        if r == min_row or c == min_col:
           output_grid[r,c] = 8
        else:
            output_grid[r,c] = 2

    return output_grid