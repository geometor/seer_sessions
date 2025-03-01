import numpy as np

def get_adjacent_pixels(grid, pixel, include_diagonal=False):
    """Returns a list of adjacent pixel coordinates to the given pixel."""
    row, col = pixel
    adjacent = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if (dr == 0 and dc == 0) or (include_diagonal is False and (dr != 0 and dc != 0)):
                continue
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < grid.shape[0] and 0 <= new_col < grid.shape[1]:
                adjacent.append((new_row, new_col))
    return adjacent

def find_clusters(grid, color):
    """Finds clusters of a specific color in a grid."""
    visited = np.zeros_like(grid, dtype=bool)
    clusters = []

    def dfs(row, col, current_cluster):
        """Depth-first search to explore a cluster."""
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or visited[row, col]
            or grid[row, col] != color
        ):
            return
        visited[row, col] = True
        current_cluster.append((row, col))
        dfs(row + 1, col, current_cluster)
        dfs(row - 1, col, current_cluster)
        dfs(row, col + 1, current_cluster)
        dfs(row, col - 1, current_cluster)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and not visited[row, col]:
                current_cluster = []
                dfs(row, col, current_cluster)
                clusters.append(current_cluster)
    return clusters

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Locate Red Clusters
    red_clusters = find_clusters(output_grid, 2)

    # Check for Red/Gray Adjacency and Conditional Gray Modification
    for cluster in red_clusters:
        for red_pixel in cluster:
            adjacent_pixels = get_adjacent_pixels(output_grid, red_pixel, include_diagonal=False)
            for adj_row, adj_col in adjacent_pixels:
                if output_grid[adj_row, adj_col] == 5:  #If the adjacent pixel is gray
                    #Check if gray pixel is part of the checkerboard
                    neighbors = get_adjacent_pixels(output_grid, (adj_row, adj_col), include_diagonal=False)
                    is_checkerboard = False
                    for nr, nc in neighbors:
                        if output_grid[nr, nc] == 0: #Check for at least one white neighbor
                            is_checkerboard = True
                            break

                    if is_checkerboard:
                        output_grid[adj_row, adj_col] = 8 #Change gray to azure

    return output_grid

def compare_grids(grid1, grid2):
    """Compares two grids and returns a dictionary of differences."""
    if grid1.shape != grid2.shape:
        return "Different shapes"
    diff = (grid1 != grid2)
    num_diffs = np.sum(diff)
    diff_indices = np.where(diff)
    diff_details = []
    for i in range(num_diffs):
        row = diff_indices[0][i]
        col = diff_indices[1][i]
        diff_details.append(
            {
                "location": (row, col),
                "grid1_value": grid1[row, col],
                "grid2_value": grid2[row, col],
            }
        )

    return {"num_differences": num_diffs, "differences": diff_details}

def count_colors(grid):
   color_counts = {}
   for color in range(10):
      color_counts[color] = np.count_nonzero(grid == color)
   return color_counts


# Task examples - including example 2 and 3
task_examples = [
    {
        "input": np.array([[5, 0, 5, 0, 5], [0, 5, 2, 5, 0], [5, 0, 5, 0, 5]]),
        "output": np.array([[5, 0, 5, 0, 5], [0, 8, 2, 8, 0], [5, 0, 5, 0, 5]]),
    },
    {
        "input": np.array([[5, 0, 5, 0, 5, 0, 5, 0], [0, 5, 0, 5, 2, 5, 0, 5], [5, 0, 5, 0, 5, 0, 5, 0], [0, 5, 0, 5, 0, 5, 0, 5]]),
        "output": np.array([[5, 0, 5, 0, 5, 0, 5, 0], [0, 5, 0, 8, 2, 8, 0, 5], [5, 0, 5, 0, 5, 0, 5, 0], [0, 5, 0, 5, 0, 5, 0, 5]]),
    },
    {
        "input": np.array([[0, 5, 0, 5, 0], [5, 0, 5, 2, 5], [0, 5, 0, 5, 0], [5, 0, 5, 0, 5]]),
        "output": np.array([[0, 5, 0, 5, 0], [5, 0, 8, 2, 8], [0, 5, 0, 5, 0], [5, 0, 5, 0, 5]]),
    }
]

for i, example in enumerate(task_examples):
  input_grid = example["input"]
  expected_output_grid = example["output"]
  predicted_output_grid = transform(input_grid)
  comparison_result = compare_grids(expected_output_grid, predicted_output_grid)

  print(f"Example {i}:")
  print("Input Color Counts:", count_colors(input_grid))
  print("Expected Color Counts:", count_colors(expected_output_grid))
  print("Predicted Color Counts:", count_colors(predicted_output_grid))
  print("Comparison Result:", comparison_result)
  print("-" * 20)
