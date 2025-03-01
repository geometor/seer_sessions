"""
1.  **Identify Vertical Azure Groups:** Find all groups of *exactly three* vertically contiguous azure (8) pixels in the input grid.
2.  **Horizontal Extension:** For each identified group, extend it horizontally to a total length of four azure pixels.  The direction of extension depends on original position. The extension includes the original 3 pixels.
3.  **Preserve Red Pixels:** All red (2) pixels must remain in their original positions in the output grid.
4. **Background:** All other cells will remain white/empty (0).
"""

import numpy as np

def find_vertical_groups(grid, color, length):
    """Finds vertically contiguous groups of a specified color and length."""
    rows, cols = grid.shape
    groups = []
    visited = np.zeros((rows, cols), dtype=bool)

    def dfs(row, col, current_group):
        if (row < 0 or row >= rows or col < 0 or col >= cols or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        current_group.append((row, col))
        dfs(row + 1, col, current_group)  # Check only downwards

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                group = []
                dfs(r, c, group)
                if len(group) == length: #check length
                    groups.append(group)
    return groups

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid) #initialize to all white
    rows, cols = output_grid.shape

    #copy red pixels
    for r in range(rows):
      for c in range(cols):
        if(input_grid[r,c] == 2):
            output_grid[r,c] = 2

    # Find azure pixel groups of length 3
    azure_groups = find_vertical_groups(input_grid, 8, 3)

    # Extend azure pixels horizontally
    for group in azure_groups:
        min_col = min(c for _, c in group) #find left-most column
        max_col = max(c for _, c in group) #find right-most col (same)
        row = group[0][0] #any row (they all have the same)

        #extend to length 4
        for i in range(4):
            output_grid[row,min_col-3+i] = 8
    return output_grid.tolist()