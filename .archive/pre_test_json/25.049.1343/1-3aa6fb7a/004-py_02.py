"""
Transformation Rule:
1. Identify azure (color 8) objects in the input grid, classifying them as "L" or "reverse-L" shapes.
2. For each "reverse-L" shaped object, change the color of the cell immediately to the left of its top-left corner to blue (color 1), if the cell exists and contains a 0.
3. For each "L" shaped object, change the color of the cell immediately to the right of its top-left corner to blue (color 1), if the cell exists and contains a 0.
"""

import numpy as np

def find_objects(grid, color):
    """
    Finds objects of a specific color in the grid and classifies them as "L" or "reverse-L".
    Returns a list of (shape, top_left_corner_row, top_left_corner_col) tuples.
    """
    objects = []
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, shape_coords):
        visited[r, c] = True
        shape_coords.append((r, c))
        neighbors = [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
        for nr, nc in neighbors:
            if is_valid(nr, nc) and grid[nr, nc] == color and not visited[nr, nc]:
                dfs(nr, nc, shape_coords)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                shape_coords = []
                dfs(r, c, shape_coords)
                
                # Classify the shape based on relative coordinates
                if len(shape_coords) == 3:
                    # Determine if it's an L or reverse-L
                    coords = sorted(shape_coords) #sort by row, then by column
                    
                    if (coords[1][0] == coords[0][0]  # two in the same row
                        and coords[2][0] == coords[1][0] + 1):
                        objects.append(("L", coords[0][0], coords[0][1])) # L shape, store the top-left
                        
                    elif (coords[1][0] == coords[0][0] +1 # two in the same column
                        and coords[2][0] == coords[1][0]):
                         objects.append(("reverse-L", coords[0][0], coords[0][1]))  # Reverse-L, store top-left
    return objects

def transform(input_grid):
    """
    Transforms the input grid according to the specified rule.
    """
    output_grid = np.copy(input_grid)
    objects = find_objects(input_grid, 8)

    for shape, r, c in objects:
        if shape == "L":
            # Change cell to the right to blue (1), if the cell is 0
            if c + 2 < output_grid.shape[1] and output_grid[r, c + 2] == 0:  # Check bounds and color
                output_grid[r, c + 2] = 1
        elif shape == "reverse-L":
            # Change cell to the left to blue (1), if the cell is 0
            if c - 1 >= 0 and output_grid[r, c - 1] == 0:  # Check bounds and color
                output_grid[r, c - 1] = 1

    return output_grid