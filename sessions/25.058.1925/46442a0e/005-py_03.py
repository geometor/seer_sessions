import numpy as np

def describe_grid(grid, grid_name):
    """Provides a description of the grid's properties."""
    height, width = grid.shape
    unique_colors = np.unique(grid)
    print(f"{grid_name}:")
    print(f"  Dimensions: {height}x{width}")
    print(f"  Unique Colors: {unique_colors}")
    # add object detection as connected components of the same color
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    
    def dfs(row, col, color, object_coords):
        if (row < 0 or row >= height or col < 0 or col >= width or
            visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        object_coords.append((row, col))
        dfs(row + 1, col, color, object_coords)
        dfs(row - 1, col, color, object_coords)
        dfs(row, col + 1, color, object_coords)
        dfs(row, col - 1, color, object_coords)
    
    for r in range(height):
        for c in range(width):
            if not visited[r, c]:
                color = grid[r, c]
                object_coords = []
                dfs(r, c, color, object_coords)
                # store the bounding box
                min_row = min(object_coords, key=lambda item:item[0])[0]
                max_row = max(object_coords, key=lambda item:item[0])[0]
                min_col = min(object_coords, key=lambda item:item[1])[1]
                max_col = max(object_coords, key=lambda item:item[1])[1]
                
                object_desc = {
                    "color": int(color),
                    "coordinates": object_coords,
                    "min_row": min_row,
                    "max_row": max_row,
                    "min_col": min_col,
                    "max_col": max_col,
                }                
                objects.append(object_desc)

    print(f"  Objects: {len(objects)}")
    for i, obj in enumerate(objects):
      print(f"    Object {i + 1}:")
      print(f"      Color: {obj['color']}")
      print(f"      Bounding Box: {obj['min_row']},{obj['min_col']} - {obj['max_row']},{obj['max_col']}")

    print("-" * 20)

def compare_grids(input_grid, output_grid):
  describe_grid(input_grid, "Input Grid")
  describe_grid(output_grid, "Output Grid")

# load the example grids from the text
task_data = {
  "train": [
    {
      "input": np.array([[1, 0], [0, 1]]),
      "output": np.array([[1, 0, 1, 0], [0, 1, 0, 1], [1, 0, 1, 0], [0, 1, 0, 1]])
    },
    {
      "input": np.array([[5, 1, 5], [1, 0, 1], [5, 1, 5]]),
      "output": np.array([[5, 1, 5, 5, 1, 5], [1, 0, 1, 1, 0, 1], [5, 1, 5, 5, 1, 5], [5, 1, 5, 5, 1, 5], [1, 0, 1, 1, 0, 1], [5, 1, 5, 5, 1, 5]])
    },
    {
      "input": np.array([[7, 0, 7, 0, 7], [0, 5, 0, 5, 0], [7, 0, 7, 0, 7], [0, 5, 0, 5, 0], [7, 0, 7, 0, 7]]),
      "output": np.array([[7, 0, 7, 0, 7, 7, 0, 7, 0, 7], [0, 5, 0, 5, 0, 0, 5, 0, 5, 0], [7, 0, 7, 0, 7, 7, 0, 7, 0, 7], [0, 5, 0, 5, 0, 0, 5, 0, 5, 0], [7, 0, 7, 0, 7, 7, 0, 7, 0, 7], [7, 0, 7, 0, 7, 7, 0, 7, 0, 7], [0, 5, 0, 5, 0, 0, 5, 0, 5, 0], [7, 0, 7, 0, 7, 7, 0, 7, 0, 7], [0, 5, 0, 5, 0, 0, 5, 0, 5, 0], [7, 0, 7, 0, 7, 7, 0, 7, 0, 7]])
    },
      {
      "input": np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8]]),
      "output": np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]])
    }
  ]
}

for example in task_data["train"]:
    compare_grids(example["input"], example["output"])