import numpy as np

def find_objects(grid):
    """Finds distinct objects in the grid."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(r, c, color, obj_coords):
        """Depth-first search to find contiguous regions."""
        if (r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1] or
                visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        obj_coords.append((r, c))
        dfs(r + 1, c, color, obj_coords)
        dfs(r - 1, c, color, obj_coords)
        dfs(r, c + 1, color, obj_coords)
        dfs(r, c - 1, color, obj_coords)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if not visited[r, c] and grid[r, c] != 0:
                obj_coords = []
                dfs(r, c, grid[r, c], obj_coords)
                objects.append({
                    "color": grid[r, c],
                    "coords": obj_coords,
                    "min_r":min(obj_coords)[0],
                    "max_r":max(obj_coords)[0],
                    "min_c":min(obj_coords, key=lambda x: x[1])[1],
                    "max_c":max(obj_coords, key=lambda x: x[1])[1],

                })
    return objects

def analyze_example(input_grid, output_grid):
    """Analyzes a single input-output pair."""
    input_objects = find_objects(input_grid)
    output_objects = find_objects(output_grid)

    print("Input Objects:")
    for obj in input_objects:
        obj['width'] = obj['max_c'] - obj['min_c'] + 1
        print(f"  Color: {obj['color']}, Min Row: {obj['min_r']}, Max Row: {obj['max_r']}, Min Col: {obj['min_c']}, Max Col: {obj['max_c']}, Width: {obj['width']}")

    print("\nOutput Objects:")
    for obj in output_objects:
        obj['width'] = obj['max_c'] - obj['min_c'] + 1
        print(f"  Color: {obj['color']}, Min Row: {obj['min_r']}, Max Row: {obj['max_r']},  Min Col: {obj['min_c']}, Max Col: {obj['max_c']}, Width: {obj['width']}")
    print("-" * 20)
    return input_objects, output_objects

def test_transform(transform_func, input_grid, output_grid):
    """Tests a transform function and compares with expected output.  Returns object details"""
    transformed_grid = transform_func(input_grid)
    print("\nTransformed Grid:")
    print(transformed_grid)

    print("\nExpected Output:")
    print(output_grid)

    comparison = np.array_equal(transformed_grid, output_grid)
    print(f"\nMatch: {comparison}")

    return transformed_grid

def get_in_out_grids(task, train_or_test, example_num):
    return np.array(task[train_or_test][example_num]['input']), np.array(task[train_or_test][example_num]['output'])


task = {
  "train": [
    {
      "input": [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 8, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 8, 8, 8, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0]
      ]
    },
    {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 3, 3, 3, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 3, 3, 3, 3, 3],
        [0, 0, 0, 0, 0, 0, 0, 0]
      ]
    },
    {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 8, 8, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 8, 8, 8, 8, 8],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
      ]
    },
    {
      "input": [
        [0, 2, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 3, 0, 0],
        [0, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
        [0, 2, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 3, 3, 3],
        [0, 0, 0, 0, 0, 0, 0]
      ]
    }
  ],
    "test": [
        {
            "input": [
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 3, 0, 0],
                [0, 0, 0, 0, 0, 0],
            ],
            "output": [
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 3, 3, 3],
                [0, 0, 0, 0, 0, 0],
            ]
        }
    ]
}
from previous_code import transform

for i in range(len(task["train"])):
    input_grid, output_grid = get_in_out_grids(task, 'train', i)
    print(f"Example {i + 1}:")
    analyze_example(input_grid, output_grid)
    test_transform(transform, input_grid, output_grid)