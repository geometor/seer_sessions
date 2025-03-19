import numpy as np

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

def object_metrics(objects):
  metrics = {}
  for color, obj_list in objects.items():
    metrics[color] = []
    for obj in obj_list:
      min_row = min(r for r, c in obj)
      max_row = max(r for r, c in obj)
      min_col = min(c for r, c in obj)
      max_col = max(c for r, c in obj)
      width = max_col - min_col + 1
      height = max_row - min_col + 1
      metrics[color].append({
          "min_row": min_row,
          "max_row": max_row,
          "min_col": min_col,
          "max_col": max_col,
          "width": width,
          "height": height,
          "count": len(obj)
      })
  return metrics

for task_name, task_data in task_data.items():
    input_objects = find_objects(task_data['input'])
    output_objects = find_objects(task_data['output'])

    input_metrics = object_metrics(input_objects)
    output_metrics = object_metrics(output_objects)
    print(f"---- {task_name} ----")
    print(f"Input Objects: {input_metrics}")
    print(f"Output Objects: {output_metrics}")
