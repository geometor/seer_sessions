import numpy as np

def report(grid, label):
    print(f"  {label}:")
    print(grid)
    # Find the single pixels (blue, red, yellow)
    blue_pixels = np.argwhere(grid == 1)
    red_pixels = np.argwhere(grid == 2)
    yellow_pixels = np.argwhere(grid == 4)
    azure_pixels = np.argwhere(grid == 8)

    print(f"    blue: {blue_pixels.tolist()}")
    print(f"    red: {red_pixels.tolist()}")
    print(f"    yellow: {yellow_pixels.tolist()}")
    print(f"    azure: {azure_pixels.tolist()}")
    # Find the azure cluster (contiguous azure pixels)

    # Function to find connected components (clusters)
    def find_cluster(grid, color):
      coords = np.argwhere(grid == color)
      if len(coords) == 0:
          return []

      cluster = []
      visited = set()
      
      def dfs(row, col):
          if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != color:
              return
          visited.add((row, col))
          cluster.append((row, col))
          dfs(row + 1, col)
          dfs(row - 1, col)
          dfs(row, col + 1)
          dfs(row, col - 1)
          
      start_row, start_col = coords[0]
      dfs(start_row, start_col)    
      return cluster
    
    azure_cluster = find_cluster(grid, 8)
    print(f"    azure cluster: {azure_cluster}")
    if len(azure_cluster) > 0:
        min_row = min([p[0] for p in azure_cluster])
        max_row = max([p[0] for p in azure_cluster])
        min_col = min([p[1] for p in azure_cluster])
        max_col = max([p[1] for p in azure_cluster])
        print(f"    cluster bounding box: min_row={min_row}, max_row={max_row}, min_col={min_col}, max_col={max_col}")

# provided examples
example_0 = {
    'input': np.array([[4, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 8, 8, 0, 0, 0, 0, 2, 0],
                       [0, 8, 8, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 1],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
    'output': np.array([[4, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 2, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 8, 8, 0, 0, 0, 0, 0, 1],
                       [0, 8, 8, 0, 0, 0, 0, 0, 0]]),
    'test_output': np.array([[4, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 2, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 8, 8, 0, 0, 0, 0, 0, 1],
                       [0, 8, 8, 0, 0, 0, 0, 0, 0]])
}

example_1 = {
 'input': np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 8, 8, 0, 0, 0, 1, 0, 0],
                    [0, 8, 8, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 2, 0, 0, 0]]),
 'output': np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 1, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 8, 8, 0, 0, 2, 0, 0, 0],
                    [0, 8, 8, 0, 0, 0, 0, 0, 0]]),
 'test_output': np.array([[0, 0, 0, 0, 0, 0, 1, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 8, 8, 0, 0, 2, 0, 0, 0],
                    [0, 8, 8, 0, 0, 0, 0, 0, 0]])
}

example_2 = {
 'input': np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 2, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 8, 8, 0, 0, 0, 0, 0, 0],
                    [0, 8, 8, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 1]]),
 'output': np.array([[0, 0, 0, 0, 0, 0, 2, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 8, 8, 0, 0, 0, 0, 0, 1],
                    [0, 8, 8, 0, 0, 0, 0, 0, 0]]),
 'test_output': np.array([[0, 0, 0, 0, 0, 0, 2, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 8, 8, 0, 0, 0, 0, 0, 1],
                    [0, 8, 8, 0, 0, 0, 0, 0, 0]])
}
report(example_0['input'], "example 0 input")
report(example_0['output'], "example 0 output")
report(example_0['test_output'], "example 0 test output")
report(example_1['input'], "example 1 input")
report(example_1['output'], "example 1 output")
report(example_1['test_output'], "example 1 test output")
report(example_2['input'], "example 2 input")
report(example_2['output'], "example 2 output")
report(example_2['test_output'], "example 2 test output")