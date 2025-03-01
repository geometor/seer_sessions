import numpy as np

input_grid = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8]
])

output_grid = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [0, 3, 0, 0, 0, 0, 0, 0, 3, 0],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8]
])

def get_objects(grid):
    """Identifies distinct objects in a grid."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if not visited[i, j] and grid[i, j] != 0:
                color = grid[i, j]
                object_coords = []
                queue = [(i, j)]
                visited[i, j] = True

                while queue:
                    x, y = queue.pop(0)
                    object_coords.append((x, y))

                    # Check adjacent cells (up, down, left, right)
                    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < grid.shape[0] and 0 <= ny < grid.shape[1] and \
                           not visited[nx, ny] and grid[nx, ny] == color:
                            queue.append((nx, ny))
                            visited[nx, ny] = True

                objects.append({
                    "color": color,
                    "coordinates": object_coords,
                    "min_row": min(y for x,y in object_coords),
                    "max_row": max(y for x,y in object_coords),
                    "min_col": min(x for x,y in object_coords),
                    "max_col": max(x for x,y in object_coords),
                })
                
    return objects

input_objects = get_objects(input_grid)
output_objects = get_objects(output_grid)

print("Input Objects:")
for obj in input_objects:
    print(obj)

print("\nOutput Objects:")
for obj in output_objects:
    print(obj)
