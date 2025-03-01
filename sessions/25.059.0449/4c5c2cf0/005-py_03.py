import numpy as np

def find_objects(grid):
    """
    Identifies distinct objects in the grid.
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    def dfs(r, c, color, obj):
        if (r < 0 or r >= rows or c < 0 or c >= cols or
                visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        obj.append((r, c))
        dfs(r + 1, c, color, obj)
        dfs(r - 1, c, color, obj)
        dfs(r, c + 1, color, obj)
        dfs(r, c - 1, c, obj)

    for r in range(rows):
        for c in range(cols):
            if not visited[r, c] and grid[r, c] != 0:
                obj = []
                dfs(r, c, grid[r, c], obj)
                objects.append((grid[r,c], obj))
    return objects
def calculate_object_metrics(grid):
    """Calculates metrics for each object in the grid."""
    objects = find_objects(grid)
    metrics = []
    for color, obj_pixels in objects:
        min_row = min(p[0] for p in obj_pixels)
        max_row = max(p[0] for p in obj_pixels)
        min_col = min(p[1] for p in obj_pixels)
        max_col = max(p[1] for p in obj_pixels)
        width = max_col - min_col + 1
        height = max_row - min_row + 1
        metrics.append({
            "color": color,
            "min_row": min_row,
            "max_row": max_row,
            "min_col": min_col,
            "max_col": max_col,
            "width": width,
            "height": height,
            "pixels": obj_pixels
        })
    return metrics

def calculate_transformation_metrics(input_grid, output_grid, predicted_output_grid):

    input_metrics = calculate_object_metrics(input_grid)
    output_metrics = calculate_object_metrics(output_grid)
    predicted_output_metrics = calculate_object_metrics(predicted_output_grid)

    return {
      "input": input_metrics,
      "output": output_metrics,
      "predicted": predicted_output_metrics
    }
def compare_grids(grid1, grid2):
    """Compares two grids and returns a grid showing the differences."""
    if grid1.shape != grid2.shape:
        return "Grids have different shapes"
    diff_grid = np.where(grid1 != grid2, 1, 0)
    return diff_grid

def test_transform(examples, transform_function):
    results = []
    for i, (input_grid, output_grid) in enumerate(examples):
        predicted_output_grid = transform_function(input_grid)
        diff_grid = compare_grids(np.array(output_grid), np.array(predicted_output_grid))
        metrics = calculate_transformation_metrics(input_grid, output_grid, predicted_output_grid)
        results.append({
          "example_index": i,
          "diff_grid": diff_grid.tolist(),
          "metrics": metrics
        })
    return results