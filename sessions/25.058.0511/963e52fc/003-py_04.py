import numpy as np
input_grid = np.array([
    [0, 0, 0, 0, 0],
    [0, 2, 0, 0, 0],
    [0, 0, 1, 1, 1],
    [0, 0, 1, 1, 1],
    [0, 0, 1, 1, 1]
])

output_grid = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 2, 2, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 1, 1, 1, 1, 1, 1]
])
print(f"Input shape: {input_grid.shape}")
print(f"Output shape: {output_grid.shape}")

#Check for objects
def get_objects(grid):
    objects = []
    visited = set()

    def dfs(row, col, color, obj):
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != color:
            return
        visited.add((row, col))
        obj.append((row, col))
        dfs(row + 1, col, color, obj)
        dfs(row - 1, col, color, obj)
        dfs(row, col + 1, color, obj)
        dfs(row, col - 1, color, obj)
    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if (row,col) not in visited:
                obj=[]
                dfs(row, col, grid[row,col],obj)
                if len(obj) > 0:
                    objects.append(obj)

    return objects
input_objects=get_objects(input_grid)
output_objects=get_objects(output_grid)

print(f"input objects count: {len(input_objects)}")
print(f"output objects count: {len(output_objects)}")
