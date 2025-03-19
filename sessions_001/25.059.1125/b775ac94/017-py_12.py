import numpy as np

def find_objects(grid):
    """Finds distinct colored regions (objects) in the grid."""
    objects = {}
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, obj_coords):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        obj_coords.append((row, col))
        dfs(row + 1, col, color, obj_coords)
        dfs(row - 1, col, color, obj_coords)
        dfs(row, col + 1, color, obj_coords)
        dfs(row, col - 1, color, obj_coords)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] != 0 and not visited[row, col]:
                color = grid[row, col]
                obj_coords = []
                dfs(row, col, color, obj_coords)
                if color not in objects:
                    objects[color] = []
                objects[color].append(obj_coords)
    return objects

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    objects = find_objects(input_grid)

    # Expand blue object (color 1)
    if 1 in objects:
        for obj in objects[1]:
          #find "center" of object
            min_row = min(r for r, c in obj)
            min_col = min(c for r, c in obj)

            for r in range(min_row -1, min_row + 2):
                for c in range(min_col, min_col + 3):
                    if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
                      output_grid[r,c] = 1

    #Mirror azure
    if 8 in objects:
      for obj in objects[8]:
          min_row = min(r for r,c in obj)
          max_row = max(r for r, c in obj)
          min_col = min(c for r,c in obj)
          max_col = max(c for r, c in obj)

          width = max_col - min_col + 1
          height = max_row - min_row + 1

          for r in range(min_row, max_row +1):
            for c in range(output_grid.shape[1] - width, output_grid.shape[1]):
              output_grid[r,c] = 8

    #Expand yellow
    if 4 in objects:
        for obj in objects[4]:
            min_row = min(r for r,c in obj)
            max_row = max(r for r,c in obj)
            min_col = min(c for r,c in obj)

            for r in range(min_row, max_row+1):
                for c in range(min_col, output_grid.shape[1]):
                    output_grid[r,c] = 4

    #Expand magenta
    if 6 in objects:
      for obj in objects[6]:
        for r,c in obj:
          if c+1 < output_grid.shape[1]:
            output_grid[r, c+1] = 6
    return output_grid

def calculate_difference_metrics(predicted_grid, expected_grid):
    """Calculates the difference between the predicted and expected grids."""
    diff = predicted_grid.astype(int) - expected_grid.astype(int)
    num_different_pixels = np.sum(diff != 0)
    return num_different_pixels

task_data = {
    "train_000": {
        "input": np.array([[0,8,0,0,0,0,0,0,0],[0,8,0,0,0,1,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,2,4,4,0,0],[0,0,0,0,2,0,0,0,0],[0,0,0,0,6,0,0,0,0]]),
        "output": np.array([[0,8,0,0,0,1,1,1,8],[0,8,0,0,0,1,1,1,8],[0,0,0,0,0,1,1,1,0],[0,0,0,0,2,4,4,4,4],[0,0,0,0,2,0,0,0,0],[0,0,0,0,6,6,0,0,0]])
    },
    "train_001": {
        "input": np.array([[0,0,0,0,0,0,0,0,0],[8,0,0,0,0,0,0,0,0],[0,0,0,0,4,0,0,0,0],[0,0,0,0,4,0,0,0,0],[0,0,0,0,4,0,6,0,0],[0,0,0,0,4,0,0,0,0]]),
        "output": np.array([[0,0,0,0,0,0,0,0,8],[8,0,0,0,4,4,4,4,8],[0,0,0,0,4,4,4,4,0],[0,0,0,0,4,4,4,4,0],[0,0,0,0,4,4,4,4,6],[0,0,0,0,4,4,4,4,0]])
    },
    "train_002": {
        "input": np.array([[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,4,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,1,0,0,0,0,0,0]]),
        "output": np.array([[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,4,4,4,0],[0,0,0,0,0,4,4,4,0],[0,0,1,1,1,4,4,4,0]])
    },
     "train_003": {
        "input": np.array([[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,2,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,4,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,1]]),
        "output": np.array([[0,0,0,0,0,0,2,2,2],[0,0,0,0,0,0,2,2,2],[0,0,0,0,0,0,2,2,2],[0,0,0,0,0,0,0,0,0],[0,4,4,4,0,0,0,0,0],[1,1,1,0,0,0,0,0,0]])
    }
}

results = {}
for task_name, task in task_data.items():
  predicted = transform(task["input"])
  diff_pixels = calculate_difference_metrics(predicted, task["output"])
  results[task_name] = {"diff_pixels": diff_pixels, "predicted": predicted.tolist(), "expected": task["output"].tolist()}

print(results)