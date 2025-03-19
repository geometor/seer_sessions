import numpy as np

def analyze_example(input_grid, output_grid, predicted_grid):
    """Analyzes an example and provides metrics."""

    report = {
        'input_shape': input_grid.shape,
        'output_shape': output_grid.shape,
        'predicted_shape': predicted_grid.shape if predicted_grid is not None else None,
        'success': np.array_equal(output_grid, predicted_grid) if predicted_grid is not None else False,
    }

    # Find gray objects in the input
    def find_objects(grid):
        objects = []
        visited = np.zeros_like(grid, dtype=bool)

        def dfs(row, col, color, obj_pixels):
            if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                    visited[row, col] or grid[row, col] != color):
                return
            visited[row, col] = True
            obj_pixels.append((row, col))
            dfs(row + 1, col, color, obj_pixels)
            dfs(row - 1, col, color, obj_pixels)
            dfs(row, col + 1, color, obj_pixels)
            dfs(row, col - 1, color, obj_pixels)
        for row in range(grid.shape[0]):
            for col in range(grid.shape[1]):
                if not visited[row, col] and grid[row, col] != 0:
                    obj_pixels = []
                    dfs(row, col, grid[row, col], obj_pixels)
                    objects.append({'color': grid[row, col], 'pixels': obj_pixels})
        return objects

    input_objects = find_objects(input_grid)
    gray_objects = [obj for obj in input_objects if obj['color'] == 5]
    report['gray_objects'] = []

    for obj in gray_objects:
      min_row = min(pixel[0] for pixel in obj['pixels'])
      max_row = max(pixel[0] for pixel in obj['pixels'])
      min_col = min(pixel[1] for pixel in obj['pixels'])
      max_col = max(pixel[1] for pixel in obj['pixels'])
      width = max_col - min_col + 1
      height = max_row - min_row + 1
      report['gray_objects'].append({
          'bounding_box': (min_row, min_col, max_row, max_col),
          'width': width,
          'height': height,
          'shape': 'square' if width==height else 'rectangle'
      })

    return report

# Provided examples (assuming these are defined elsewhere)
examples = [
    # Example 1 data
    (np.array([[5, 5, 5, 0, 0, 0, 0, 0],
               [5, 5, 5, 0, 0, 0, 0, 0],
               [5, 5, 5, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 5, 5],
               [0, 0, 0, 0, 0, 0, 5, 5]]),
     np.array([[2, 2, 2, 0, 0, 0, 0, 0],
               [2, 4, 4, 0, 0, 0, 0, 0],
               [4, 4, 4, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 5, 5],
               [0, 0, 0, 0, 0, 0, 5, 5]])),

    # Example 2 data
    (np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 5, 5, 0, 0, 0, 0, 5, 5],
               [0, 5, 5, 0, 0, 0, 0, 5, 5],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 5, 5, 5, 5, 0, 0, 0, 0],
               [0, 5, 5, 5, 5, 0, 0, 0, 0]]),
     np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 2, 2, 0, 0, 0, 0, 2, 2],
               [0, 4, 4, 0, 0, 0, 0, 4, 4],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 2, 2, 2, 2, 0, 0, 0, 0],
               [0, 2, 4, 4, 4, 0, 0, 0, 0]])),

    # Example 3 data
    (np.array([[5, 5, 0, 0, 0, 0, 0, 0, 0],
               [5, 5, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 5, 5, 5],
               [0, 0, 0, 0, 0, 0, 5, 5, 5]]),
     np.array([[2, 2, 0, 0, 0, 0, 0, 0, 0],
               [4, 4, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 2, 2, 2],
               [0, 0, 0, 0, 0, 0, 2, 4, 4]])),

    # Example 4 data
        (np.array([[0, 0, 0, 0, 0, 5, 5, 0, 0],
               [0, 0, 0, 0, 0, 5, 5, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 5, 5, 0, 0, 0, 0, 0, 0],
               [0, 5, 5, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 5],
               [0, 0, 0, 0, 0, 0, 0, 0, 5],
               [0, 0, 0, 0, 0, 0, 0, 0, 5]]),
     np.array([[0, 0, 0, 0, 0, 2, 2, 0, 0],
               [0, 0, 0, 0, 0, 4, 4, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 2, 2, 0, 0, 0, 0, 0, 0],
               [0, 4, 4, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 5],
               [0, 0, 0, 0, 0, 0, 0, 0, 5],
               [0, 0, 0, 0, 0, 0, 0, 0, 5]]))
]


reports = []
for i, (input_grid, output_grid) in enumerate(examples):
    predicted_grid = transform(input_grid.copy())  # Use the provided transform function
    report = analyze_example(input_grid, output_grid, predicted_grid)
    reports.append((i + 1, report))

for example_num, report in reports:
    print(f"Example {example_num}:")
    print(f"  Input shape: {report['input_shape']}")
    print(f"  Output shape: {report['output_shape']}")
    print(f"  Predicted shape: {report.get('predicted_shape')}")
    print(f"  Success: {report.get('success', False)}")  # Default to False if no prediction
    print(f"  Gray Objects:")
    for obj in report['gray_objects']:
      print(f"\t Bounding Box: {obj['bounding_box']}")
      print(f"\t Width: {obj['width']}")
      print(f"\t Height: {obj['height']}")
      print(f"\t Shape: {obj['shape']}")
