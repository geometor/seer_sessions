import numpy as np

input_grid = np.array([[5, 5, 5], [5, 0, 5], [5, 5, 5]])
output_grid = np.array([[8, 8, 8], [8, 0, 8], [8, 8, 8]])

def find_contiguous_regions(grid, color):
    visited = np.zeros_like(grid, dtype=bool)
    regions = []

    def dfs(row, col, current_region):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        current_region.append((row, col))
        dfs(row + 1, col, current_region)
        dfs(row - 1, col, current_region)
        dfs(row, col + 1, current_region)
        dfs(row, col - 1, current_region)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and not visited[row, col]:
                current_region = []
                dfs(row, col, current_region)
                regions.append(current_region)
    return regions

def calculate_centroid(region):
    rows, cols = zip(*region)
    return sum(rows) / len(rows), sum(cols) / len(cols)

gray_regions = find_contiguous_regions(input_grid, 5)
print(f"Gray Regions: {gray_regions}")
centroids = [calculate_centroid(region) for region in gray_regions]
print(f"Centroids: {centroids}")
grid_center = (input_grid.shape[0] / 2, input_grid.shape[1] / 2)
print(f"Grid Center: {grid_center}")

