import numpy as np

def compare_grids(predicted, expected):
    """Checks if two grids are identical and returns a diff and comments if not."""
    if predicted.shape != expected.shape:
        return False, f"Shapes differ: Predicted {predicted.shape}, Expected {expected.shape}", predicted - expected

    if not np.array_equal(predicted, expected):
        diff = predicted - expected
        return False, "Values differ", diff

    return True, "Grids are identical", None

def find_objects(grid):
    # Find contiguous blocks of non-zero pixels
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(r, c, color, obj):
        if (r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1] or
                visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        obj.append([r, c])
        dfs(r + 1, c, color, obj)
        dfs(r - 1, c, color, obj)
        dfs(r, c + 1, color, obj)
        dfs(r, c - 1, color, obj)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != 0 and not visited[r, c]:
                obj = []
                dfs(r, c, grid[r, c], obj)
                objects.append((grid[r, c], obj))  # Store color and object
    return objects
    
def get_reports(task):
    reports = []
    for i, example in enumerate(task['train']):
      input_grid = np.array(example['input'])
      expected_output = np.array(example['output'])
      predicted_output = transform(input_grid)  # Use the provided transform function
      is_equal, comment, diff = compare_grids(predicted_output, expected_output)

      input_objects = find_objects(input_grid)
      expected_objects = find_objects(expected_output)
      predicted_objects = find_objects(predicted_output)

      report = {
            "example_index": i,
            "input_shape": input_grid.shape,
            "output_shape": expected_output.shape,
            "predicted_shape": predicted_output.shape,
            "grids_equal": is_equal,
            "comparison_comment": comment,
            "input_objects": input_objects,
            "expected_objects": expected_objects,
            "predicted_objects": predicted_objects,
            "diff": diff.tolist() if diff is not None else None,  # Convert diff to list for easy viewing
        }
      reports.append(report)
    return reports

# The task data, replace this with your task
task = {
  "train": [
    {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 8, 8, 0, 0, 0, 0, 4, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [8, 8, 8, 0, 0, 0, 0, 0, 4, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      ]
    },
    {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 8, 8, 8, 0, 0, 0, 4],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 8, 8, 8, 0, 0, 0, 0, 4],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      ]
    },
    {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [4, 0, 0, 0, 0, 8, 8, 8, 0, 0]
      ],
      "output": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [4, 0, 0, 8, 8, 8, 0, 0, 0, 0]
      ]
    },
        {
      "input": [
        [0, 4, 0, 0, 8, 8, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
        [0, 4, 8, 8, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      ]
    }
  ]
}
reports = get_reports(task)

for report in reports:
    print(report)