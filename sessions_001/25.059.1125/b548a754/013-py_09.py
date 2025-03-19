import numpy as np
from typing import List, Tuple

def analyze_example(input_grid: np.ndarray, output_grid: np.ndarray, predicted_grid: np.ndarray) -> dict:
    """Analyzes a single example and returns relevant metrics."""

    def find_objects(grid, color):
        """Find contiguous regions of a specific color."""
        objects = []
        visited = np.zeros_like(grid, dtype=bool)

        def dfs(r, c, current_object):
            """Depth-first search to explore contiguous regions."""
            if (r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1] or
                    visited[r, c] or grid[r, c] != color):
                return
            visited[r, c] = True
            current_object.append((r, c))
            dfs(r + 1, c, current_object)
            dfs(r - 1, c, current_object)
            dfs(r, c + 1, current_object)
            dfs(r, c - 1, current_object)

        for r in range(grid.shape[0]):
            for c in range(grid.shape[1]):
                if grid[r, c] == color and not visited[r, c]:
                    current_object = []
                    dfs(r, c, current_object)
                    objects.append(current_object)
        return objects
    
    def get_bounding_box(obj):
      """Get the bounding box of a list of coordinates."""
      min_row = min(p[0] for p in obj)
      max_row = max(p[0] for p in obj)
      min_col = min(p[1] for p in obj)
      max_col = max(p[1] for p in obj)
      return min_row, max_row, min_col, max_col

    def is_contained(inner_obj, outer_obj):
        """Check if inner_obj is fully contained within outer_obj."""
        inner_min_row, inner_max_row, inner_min_col, inner_max_col = get_bounding_box(inner_obj)
        outer_min_row, outer_max_row, outer_min_col, outer_max_col = get_bounding_box(outer_obj)
        return (inner_min_row >= outer_min_row and inner_max_row <= outer_max_row and
                inner_min_col >= outer_min_col and inner_max_col <= outer_max_col)

    def find_outermost_object(objects):
        """Find the object that contains all others."""
        if not objects:
            return None
        if len(objects) == 1:
            return objects[0]

        outermost = objects[0]
        for obj in objects[1:]:
            if is_contained(outermost, obj):
                outermost = obj
        return outermost
    
    def rightmost_colored_edge(grid):
      """Determine rightmost edge of any non-white pixel."""
      max_col = -1
      for r in range(grid.shape[0]):
          for c in range(grid.shape[1]):
              if grid[r, c] != 0:
                  max_col = max(max_col, c)
      return max_col

    metrics = {}

    # Find objects
    metrics["input_green_objects"] = find_objects(input_grid, 3)
    metrics["input_red_objects"] = find_objects(input_grid, 2)
    metrics["output_green_objects"] = find_objects(output_grid, 3)
    metrics["output_red_objects"] = find_objects(output_grid, 2)
    metrics["predicted_green_objects"] = find_objects(predicted_grid, 3)
    metrics["predicted_red_objects"] = find_objects(predicted_grid, 2)
    
    metrics["input_outermost_green"] = find_outermost_object(metrics["input_green_objects"])
    metrics["input_rightmost_edge"] = rightmost_colored_edge(input_grid)

    metrics["output_outermost_green"] = find_outermost_object(metrics["output_green_objects"])
    metrics["output_rightmost_edge"] = rightmost_colored_edge(output_grid)    

    metrics["predicted_outermost_green"] = find_outermost_object(metrics["predicted_green_objects"])
    metrics["predicted_rightmost_edge"] = rightmost_colored_edge(predicted_grid)    
    
    metrics["input_contains_red"] = False
    if metrics["input_outermost_green"] is not None:
      for red_object in metrics["input_red_objects"]:
          if is_contained(red_object, metrics["input_outermost_green"]):
              metrics["input_contains_red"] = True
              break;

    metrics["output_contains_red"] = False
    if metrics["output_outermost_green"] is not None:
      for red_object in metrics["output_red_objects"]:
          if is_contained(red_object, metrics["output_outermost_green"]):
              metrics["output_contains_red"] = True
              break;
              
    metrics["predicted_contains_red"] = False
    if metrics["predicted_outermost_green"] is not None:      
      for red_object in metrics["predicted_red_objects"]:
          if is_contained(red_object, metrics["predicted_outermost_green"]):
              metrics["predicted_contains_red"] = True
              break;

    metrics["correct"] = np.array_equal(output_grid, predicted_grid)

    return metrics

# Example Usage (replace with your actual data)
task_id = "6b6b767a"
train_input_0 = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
train_output_0 = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3], [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3, 3], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
train_predicted_0 = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3], [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3, 3], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

train_input_1 = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 2, 3, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
train_output_1 = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 0], [0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 2, 3, 3, 0], [0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
train_predicted_1 = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3], [0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 2, 3, 3, 3], [0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

train_input_2 = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 3, 0, 0], [0, 0, 0, 0, 0, 0, 0, 3, 0, 0], [0, 0, 0, 0, 0, 0, 0, 3, 0, 0], [0, 0, 0, 0, 0, 0, 0, 3, 2, 0], [0, 0, 0, 0, 0, 0, 0, 3, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
train_output_2 = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 3, 3, 0], [0, 0, 0, 0, 0, 0, 0, 3, 3, 0], [0, 0, 0, 0, 0, 0, 0, 3, 3, 0], [0, 0, 0, 0, 0, 0, 0, 3, 2, 0], [0, 0, 0, 0, 0, 0, 0, 3, 3, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
train_predicted_2 = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 3, 3, 3], [0, 0, 0, 0, 0, 0, 0, 3, 3, 3], [0, 0, 0, 0, 0, 0, 0, 3, 3, 3], [0, 0, 0, 0, 0, 0, 0, 3, 2, 3], [0, 0, 0, 0, 0, 0, 0, 3, 3, 3], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])


metrics_0 = analyze_example(train_input_0, train_output_0, train_predicted_0)
metrics_1 = analyze_example(train_input_1, train_output_1, train_predicted_1)
metrics_2 = analyze_example(train_input_2, train_output_2, train_predicted_2)


print("Metrics for Example 0:")
print(metrics_0)
print("\nMetrics for Example 1:")
print(metrics_1)
print("\nMetrics for Example 2:")
print(metrics_2)
