"""
Transforms an input grid by propagating colors based on their original position, with the highest color filling horizontally right and the next highest filling other positions in the column.
"""

import numpy as np

def get_objects(grid):
    """
    Finds all contiguous blocks of the same color in the grid.
    """
    objects = {}
    visited = set()
    rows, cols = len(grid), len(grid[0])

    def dfs(row, col, color, obj):
        if (row, col) in visited or row < 0 or row >= rows or col < 0 or col >= cols or grid[row][col] != color:
            return
        visited.add((row, col))
        obj.append((row, col))
        dfs(row + 1, col, color, obj)
        dfs(row - 1, col, color, obj)
        dfs(row, col + 1, color, obj)
        dfs(row, col - 1, color, obj)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited and grid[r][c]!=0:
                color = grid[r][c]
                obj = []
                dfs(r, c, color, obj)
                if color not in objects:
                    objects[color] = []
                objects[color].append(obj)
    return objects
def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid).tolist()
    rows = len(input_grid)
    cols = len(input_grid[0])

    # Iterate through each row
    for r in range(rows):
        #find non-zero colors present in current row, sort desc
        colors = sorted(list(set(input_grid[r])), reverse=True)
        colors = [c for c in colors if c!=0]

        #iterate through found colors
        for color in colors:
            #find leftmost occurance of colour
            indices = [i for i, x in enumerate(input_grid[r]) if x == color]
            if len(indices)>0:
                leftmost_index = min(indices)
                #fill left
                for i in range(0,leftmost_index):
                    output_grid[r][i] = color


    return output_grid