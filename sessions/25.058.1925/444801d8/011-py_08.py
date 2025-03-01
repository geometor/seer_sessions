import numpy as np

# Provided get_objects function (copied here for completeness)
def get_objects(grid, color):
    """
    Find connected regions of a specific color.
    """
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    def dfs(row, col):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return []

        visited[row, col] = True
        region = [(row, col)]

        region.extend(dfs(row + 1, col))
        region.extend(dfs(row - 1, col))
        region.extend(dfs(row, col + 1))
        region.extend(dfs(row, col - 1))

        return region

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and not visited[row, col]:
                objects.append(dfs(row, col))
    return objects

# Example data (replace with actual input grids)
example_inputs = [
    np.array([[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,1,1,1,0],[0,0,1,1,1,0],[0,0,0,0,0,0],[0,0,1,1,1,0],[0,0,1,1,1,0]]),
    np.array([[0,0,0,0,0,0,0],[0,1,1,1,1,1,0],[0,1,1,1,1,1,0],[0,1,1,1,1,1,0],[0,0,0,0,0,0,0],[0,1,1,1,1,1,0],[0,1,1,1,1,1,0]]),
    np.array([[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,1,1,1,0,0,0],[0,0,1,1,1,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,1,1,1,0,0],[0,0,0,1,1,1,0,0],[0,0,0,0,0,0,0,0]]),
    np.array([[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,1,1,1,0,0],[0,0,0,0,1,1,1,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,1,1,1,0,0],[0,0,0,0,1,1,1,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]]),
    np.array([[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,1,1,1,1,0,0],[0,0,0,0,1,1,1,1,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,1,1,1,1,0,0],[0,0,0,0,1,1,1,1,0,0],[0,0,0,0,0,0,0,0,0,0]]),
]


for i, input_grid in enumerate(example_inputs):
    blue_objects = get_objects(input_grid, 1)
    print(f"Example {i+1} Blue Objects:")
    for j, obj in enumerate(blue_objects):
        print(f"  Object {j+1}: {obj}")
    print("-" * 20)

