def code_execution(input_grid, predicted_output_grid, true_output_grid):
    """
    Executes code to analyze and compare the input, predicted output, and true output grids.

    Args:
        input_grid: The initial grid.
        predicted_output_grid: The grid after applying the current transformation logic.
        true_output_grid: The expected output grid.

    Returns:
        A dictionary containing analysis results, including object details and differences.
    """

    def get_objects(grid):
        objects = {}
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
                    color = grid[row, col]
                    obj_pixels = []
                    dfs(row, col, color, obj_pixels)
                    if color not in objects:
                        objects[color] = []
                    objects[color].append(obj_pixels)
        return objects

    input_objects = get_objects(input_grid)
    predicted_objects = get_objects(predicted_output_grid)
    true_objects = get_objects(true_output_grid)

    differences = []
    for row in range(input_grid.shape[0]):
      for col in range(input_grid.shape[1]):
        if predicted_output_grid[row,col] != true_output_grid[row,col]:
          differences.append(
              {
                  "location" : (row, col),
                  "predicted" : predicted_output_grid[row,col],
                  "true" : true_output_grid[row,col],
              }
          )


    analysis = {
        "input_objects": input_objects,
        "predicted_objects": predicted_objects,
        "true_objects": true_objects,
        "differences": differences
    }
    return analysis

# Example Usage (replace with actual grids)
#  This assumes you have defined input_grids, predicted_output_grids, and true_output_grids
#  as lists of numpy arrays for each example.
import numpy as np
task_id = "3618c87e"

train = [
  ([
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,0,0,0],
    [0,4,4,4,4,4,4,4,4,0],
    [0,0,0,0,0,0,1,0,0,0],
    [0,0,0,0,0,0,0,0,0,0]
  ],
  [
    [0,0,0,0,0,0,0,0,0,0],
    [0,4,4,4,4,4,4,4,4,0],
    [0,4,4,4,4,4,4,4,4,0],
    [0,4,4,4,4,4,4,4,4,0],
    [0,0,0,0,0,0,0,0,0,0]
  ]),
  ([
    [0,0,0,0,0,0,0,0,0,0],
    [0,4,4,4,4,4,4,4,4,0],
    [0,0,0,0,0,0,1,0,0,0],
    [0,4,4,4,4,4,4,4,4,0],
    [0,0,0,0,0,0,0,0,0,0]
  ],
  [
    [0,4,4,4,4,4,4,4,4,0],
    [0,4,4,4,4,4,4,4,4,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,4,4,4,4,4,4,4,4,0],
    [0,4,4,4,4,4,4,4,4,0]
  ]),
    ([
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,1,0,0,0,0,0],
    [0,0,0,0,1,0,0,0,0,0],
    [0,4,4,4,4,4,4,4,4,0],
    [0,0,0,0,0,0,0,0,0,0]
  ],
  [
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,4,4,4,4,4,4,4,4,0],
    [0,4,4,4,4,4,4,4,4,0]
    ]),
    ([
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,4,4,4,4,4,4,0,0],
    [0,0,4,4,4,4,4,4,0,0],
    [0,0,4,4,4,4,4,4,0,0],
    [0,0,4,4,4,4,4,4,0,0],
    [0,0,0,0,0,0,0,0,0,0]
    ],
    [
    [0,0,4,4,4,4,4,4,0,0],
    [0,0,4,4,4,4,4,4,0,0],
    [0,0,4,4,4,4,4,4,0,0],
    [0,0,4,4,4,4,4,4,0,0],
    [0,0,4,4,4,4,4,4,0,0],
    [0,0,0,0,0,0,0,0,0,0]
      ]),
    ([
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,4,4,4,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0]
    ],
    [
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,4,4,4,0,0,0,0],
    [0,0,0,4,4,4,0,0,0,0],
    [0,0,0,4,4,4,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0]
    ])
]

input_grids = [np.array(i[0]) for i in train]
true_output_grids = [np.array(i[1]) for i in train]

predicted_output_grids = []
for i in input_grids:
    predicted_output_grids.append(transform(i))

results = []
for i in range(len(input_grids)):
    results.append(code_execution(input_grids[i], predicted_output_grids[i], true_output_grids[i]))

for i in range(len(results)):
    print(f"Example {i+1}:")
    print(results[i])
    print("-" * 20)