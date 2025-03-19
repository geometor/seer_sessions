"""
1.  **Identify Objects:** Find all rectangular blocks of non-black (non-zero) pixels within the input grid.
2.  **Color Change:** For each identified object, change its color to blue (1).
3.  **Output:** Create an output grid identical in dimensions to the input grid.  Place the recolored blue objects in the same positions in the output grid as they were in the input grid. All other pixels in the output grid should be black (0).
"""

import numpy as np

def find_objects(grid):
    # Find all rectangular, non-black objects in a grid.
    objects = []
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    visited = set()

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, object_coords):
        # Depth-first search to find contiguous regions.
        stack = [(r, c)]
        while stack:
            row, col = stack.pop()
            if (row, col) in visited or not is_valid(row, col) or grid[row][col] != color:
                continue

            visited.add((row, col))
            object_coords.append((row, col))

            # Add neighbors (up, down, left, right)
            neighbors = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
            for nr, nc in neighbors:
                stack.append((nr, nc))


    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != 0 and (r, c) not in visited:
                object_coords = []
                dfs(r, c, grid[r][c], object_coords)
                # Determine if it's rectangular
                if object_coords:
                    min_row = min(object_coords, key=lambda x: x[0])[0]
                    max_row = max(object_coords, key=lambda x: x[0])[0]
                    min_col = min(object_coords, key=lambda x: x[1])[1]
                    max_col = max(object_coords, key=lambda x: x[1])[1]

                    # Check for rectangular shape
                    is_rectangular = True
                    for row in range(min_row, max_row + 1):
                        for col in range(min_col, max_col+1):
                            if (row,col) not in object_coords:
                                is_rectangular = False
                                break
                        if not is_rectangular:
                            break
                    
                    if is_rectangular:
                        objects.append({
                            "color": grid[r][c],
                            "top_left": (min_row, min_col),
                            "bottom_right": (max_row, max_col)
                        })
    return objects

def transform(input_grid):
    # initialize output_grid as all black
    output_grid = np.zeros_like(input_grid).tolist()

    # Find objects
    objects = find_objects(input_grid)

    # change output pixels, set to blue
    for obj in objects:
        for r in range(obj["top_left"][0], obj["bottom_right"][0] + 1):
            for c in range(obj["top_left"][1], obj["bottom_right"][1] + 1):
                output_grid[r][c] = 1

    return output_grid